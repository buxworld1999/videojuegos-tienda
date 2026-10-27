"""
Módulo de servicio para conexión con la API externa de la evaluación (Render).
Implementa:
- Seguridad y protección de la API Key mediante variables de entorno (.env).
- Petición HTTP al endpoint oficial.
- Almacenamiento en memoria RAM de nuestro sistema.
- Impresión detallada en pantalla (consola/terminal).
- Manejo estricto de excepciones y códigos de estatus HTTP (200, 401, 403, 404, 405, etc.).
"""
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import requests

from pagina_cideo_juego_web.config import config
from pagina_cideo_juego_web.models.game import Game


@dataclass
class RamStorage:
    """
    Repositorio residente en la memoria RAM del sistema.
    Mantiene los videojuegos y metadatos cargados desde la API externa.
    """
    games: List[Game] = field(default_factory=list)
    raw_payload: Optional[Dict[str, Any]] = None
    last_status_code: Optional[int] = None
    last_updated: Optional[float] = None
    source: str = "RAM_MEMORY"

    def clear(self) -> None:
        """Limpia los datos almacenados en RAM."""
        self.games.clear()
        self.raw_payload = None
        self.last_status_code = None
        self.last_updated = None

    def save(self, games: List[Game], raw_payload: Dict[str, Any], status_code: int) -> None:
        """Almacena la respuesta directamente en la memoria RAM."""
        self.games = list(games)
        self.raw_payload = raw_payload
        self.last_status_code = status_code
        self.last_updated = time.time()

    @property
    def count(self) -> int:
        """Cantidad de elementos almacenados en RAM."""
        return len(self.games)

    def summary(self) -> Dict[str, Any]:
        """Resumen del estado actual de la memoria RAM."""
        return {
            "almacenado_en_ram": True,
            "total_juegos_en_ram": self.count,
            "codigo_estatus": self.last_status_code,
            "timestamp": self.last_updated,
            "origen": self.source,
        }


@dataclass
class ApiResponseResult:
    """Objeto de transferencia de datos con el resultado de la consulta a la API."""
    status_code: int
    success: bool
    message: str
    games: List[Game] = field(default_factory=list)
    raw_data: Optional[Dict[str, Any]] = None
    error_detail: Optional[str] = None


class EvaluationApiService:
    """
    Servicio de integración con la API de Evaluación (POO).
    Consume el endpoint protegido, gestiona excepciones y almacena en RAM.
    """

    # Códigos HTTP documentados y sus descripciones técnicas
    STATUS_DESCRIPTIONS = {
        200: "200 OK - Petición exitosa. Catálogo recibido y almacenado en RAM.",
        401: "401 UNAUTHORIZED - Falta la cabecera 'X-API-Key' o está vacía.",
        403: "403 FORBIDDEN - API Key inválida o no corresponde al namespace del usuario.",
        404: "404 NOT FOUND - Endpoint o namespace de usuario no encontrado.",
        405: "405 METHOD NOT ALLOWED - Método HTTP no permitido para este endpoint.",
        422: "422 UNPROCESSABLE ENTITY - Error de validación en los parámetros enviados.",
        500: "500 INTERNAL SERVER ERROR - Error interno en el servidor remoto.",
        503: "503 SERVICE UNAVAILABLE - Servicio remoto no disponible o fuera de línea.",
    }

    def __init__(self) -> None:
        # Repositorio en memoria RAM dedicado
        self.ram_storage = RamStorage()

    def fetch_games_from_api(
        self,
        custom_key: Optional[str] = None,
        custom_url: Optional[str] = None,
        method: str = "GET",
        timeout: int = 10,
    ) -> ApiResponseResult:
        """
        Realiza la consulta al endpoint de la API externa, maneja excepciones,
        almacena el resultado en la memoria RAM y retorna el resultado.

        Parámetros:
            custom_key: Permite probar claves alternativas o None para usar la del .env
            custom_url: Permite probar endpoints alternativos o None para usar el del .env
            method: Método HTTP a utilizar (por defecto "GET", o "POST" para pruebas de 405)
            timeout: Tiempo máximo de espera en segundos
        """
        target_url = custom_url or config.full_url
        api_key_to_use = custom_key if custom_key is not None else config.api_key

        headers = {
            "Accept": "application/json",
        }
        # Solo incluir cabecera si la clave no está vacía
        if api_key_to_use:
            headers["X-API-Key"] = api_key_to_use

        status_code = 0
        error_detail = None
        parsed_games: List[Game] = []
        raw_json: Optional[Dict[str, Any]] = None

        try:
            # 1. Ejecutar petición HTTP según el método solicitado
            if method.upper() == "GET":
                response = requests.get(target_url, headers=headers, timeout=timeout)
            elif method.upper() == "POST":
                response = requests.post(target_url, headers=headers, json={}, timeout=timeout)
            else:
                response = requests.request(method.upper(), target_url, headers=headers, timeout=timeout)

            # 2. Extraer el código de estatus HTTP numérico
            status_code = response.status_code

            # 3. Intentar decodificar el cuerpo JSON
            try:
                raw_json = response.json()
            except Exception:
                raw_json = {"raw_text": response.text}

            # 4. Manejo según el código de estatus
            if status_code == 200:
                # Éxito: Extraer lista de items
                items = []
                if isinstance(raw_json, dict) and "items" in raw_json:
                    items = raw_json.get("items", [])
                elif isinstance(raw_json, list):
                    items = raw_json

                # Convertir cada item a objeto Game (POO)
                for item in items:
                    if isinstance(item, dict):
                        game_obj = Game.from_dict(item)
                        parsed_games.append(game_obj)

                # ALMACENAR EN LA MEMORIA RAM DE NUESTRO SISTEMA
                self.ram_storage.save(
                    games=parsed_games,
                    raw_payload=raw_json,
                    status_code=status_code,
                )

                result = ApiResponseResult(
                    status_code=status_code,
                    success=True,
                    message=f"Catálogo obtenido exitosamente ({len(parsed_games)} juegos guardados en RAM)",
                    games=parsed_games,
                    raw_data=raw_json,
                )

            elif status_code in (401, 403, 404, 405, 422, 500):
                # Extraer detalle de error si el servidor lo proporcionó
                if isinstance(raw_json, dict) and "detail" in raw_json:
                    error_detail = str(raw_json["detail"])
                else:
                    error_detail = self.STATUS_DESCRIPTIONS.get(status_code, f"Error HTTP {status_code}")

                # Actualizar estatus en RAM
                self.ram_storage.last_status_code = status_code

                result = ApiResponseResult(
                    status_code=status_code,
                    success=False,
                    message=f"Error HTTP {status_code}: {error_detail}",
                    games=[],
                    raw_data=raw_json,
                    error_detail=error_detail,
                )

            else:
                # Otros códigos HTTP no previstos
                error_detail = f"Código HTTP no esperado: {status_code}"
                self.ram_storage.last_status_code = status_code
                result = ApiResponseResult(
                    status_code=status_code,
                    success=False,
                    message=error_detail,
                    games=[],
                    raw_data=raw_json,
                    error_detail=error_detail,
                )

        # =================================================================
        # MANEJO DE EXCEPCIONES DE RED Y CONECTIVIDAD
        # =================================================================
        except requests.exceptions.Timeout as err:
            status_code = 504
            error_detail = f"Tiempo de espera agotado al conectar con {target_url} (Timeout > {timeout}s)"
            self.ram_storage.last_status_code = status_code
            result = ApiResponseResult(
                status_code=status_code,
                success=False,
                message=error_detail,
                error_detail=str(err),
            )

        except requests.exceptions.ConnectionError as err:
            status_code = 503
            error_detail = f"No fue posible establecer conexión con el host: {target_url}"
            self.ram_storage.last_status_code = status_code
            result = ApiResponseResult(
                status_code=status_code,
                success=False,
                message=error_detail,
                error_detail=str(err),
            )

        except requests.exceptions.RequestException as err:
            status_code = 500
            error_detail = f"Error en la petición HTTP: {err}"
            self.ram_storage.last_status_code = status_code
            result = ApiResponseResult(
                status_code=status_code,
                success=False,
                message=error_detail,
                error_detail=str(err),
            )

        except Exception as err:
            status_code = 500
            error_detail = f"Error inesperado al procesar la respuesta: {err}"
            self.ram_storage.last_status_code = status_code
            result = ApiResponseResult(
                status_code=status_code,
                success=False,
                message=error_detail,
                error_detail=str(err),
            )

        return result

    def print_to_screen(self, result: Optional[ApiResponseResult] = None) -> None:
        """
        Imprime en pantalla (consola/terminal) la información detallada
        requerida para la evaluación, con el estatus en código y protección de credenciales.
        """
        # Si no se pasó un resultado previo, consultar ahora
        if result is None:
            result = self.fetch_games_from_api()

        code = result.status_code
        status_meaning = self.STATUS_DESCRIPTIONS.get(code, f"HTTP {code}")

        print("\n" + "=" * 65)
        print("          CONEXIÓN CON API EXTERNA          ")
        print("=" * 65)
        print(f" * Usuario Asignado    : {config.username}")
        print(f" * URL del Endpoint    : {config.full_url}")
        print(f" * API Key (Protegida) : {config.masked_key}")
        print(f" * CÓDIGO DE ESTATUS   : {code}")
        print(f" * Descripción Código  : {status_meaning}")
        print(f" * Estado en RAM       : {self.ram_storage.count} juegos cargados en memoria RAM")
        print("-" * 65)

        if result.success and result.games:
            print(" VIDEOJUEGOS ALMACENADOS EN LA MEMORIA RAM:")
            print("-" * 65)
            for idx, game in enumerate(result.games, start=1):
                price_str = "GRATIS" if game.price == 0.0 else f"${game.price:.2f}"
                print(f" [{idx}] ID: {game.id:<4} | {game.title:<30} | {game.platform:<11} | {price_str}")
        elif not result.success:
            print(f" [AVISO] Falló la consulta con el código: {code}")
            if result.error_detail:
                print(f" Detalle: {result.error_detail}")

        print("=" * 65 + "\n")


# Instancia global del servicio para acceso singleton
evaluation_api_service = EvaluationApiService()
