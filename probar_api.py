"""
Script interactivo para la Evaluación de Programación II.
Demuestra la conexión con la API externa, almacenamiento en RAM,
protección de credenciales (.env) y manejo de excepciones con todos
los códigos de estatus HTTP del documento (200, 401, 403, 404, 405).

Uso:
    uv run python probar_api.py
"""
import sys
from pathlib import Path

# Asegurar importación de src
src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from pagina_cideo_juego_web.config import config
from pagina_cideo_juego_web.backend.api_service import evaluation_api_service


def ejecutar_demostracion_completa() -> None:
    print("\n" + "=" * 75)
    print("      EVALUACION DE SISTEMAS - CONEXION CON API EXTERNA REST      ")
    print("=" * 75)
    print(f"Usuario registrado en sistema : {config.username}")
    print(f"API Key protegida (en .env)   : {config.masked_key}")
    print(f"URL Base                      : {config.base_url}")
    print(f"Endpoint Asignado             : {config.endpoint}")
    print(f"Documentacion Oficial         : {config.docs_url}")
    print("=" * 75)

    # -------------------------------------------------------------
    # PRUEBA 1: Consulta exitosa (Estatus 200) y Almacenamiento en RAM
    # -------------------------------------------------------------
    print("\n>>> PRUEBA 1: Peticion Exitosa con API Key Valida (Codigo 200)")
    res_200 = evaluation_api_service.fetch_games_from_api()
    print(f" [ESTATUS HTTP] -> {res_200.status_code}")
    print(f" [EXITO]        -> {res_200.success}")
    print(f" [MENSAJE]      -> {res_200.message}")
    print(f" [MEMORIA RAM]  -> {evaluation_api_service.ram_storage.count} videojuegos almacenados")

    print("\n--- Imprimiendo Catalogo de la RAM en Pantalla ---")
    evaluation_api_service.print_to_screen(res_200)

    # -------------------------------------------------------------
    # PRUEBA 2: Omision de API Key (Estatus 401)
    # -------------------------------------------------------------
    print("\n>>> PRUEBA 2: Peticion sin cabecera X-API-Key (Codigo 401)")
    res_401 = evaluation_api_service.fetch_games_from_api(custom_key="")
    print(f" [ESTATUS HTTP] -> {res_401.status_code}")
    print(f" [MENSAJE]      -> {res_401.message}")
    print(f" [DETALLE]      -> {res_401.error_detail}")

    # -------------------------------------------------------------
    # PRUEBA 3: API Key Invalida (Estatus 403)
    # -------------------------------------------------------------
    print("\n>>> PRUEBA 3: Peticion con API Key Invalida (Codigo 403)")
    res_403 = evaluation_api_service.fetch_games_from_api(custom_key="clave_invalida_12345")
    print(f" [ESTATUS HTTP] -> {res_403.status_code}")
    print(f" [MENSAJE]      -> {res_403.message}")
    print(f" [DETALLE]      -> {res_403.error_detail}")

    # -------------------------------------------------------------
    # PRUEBA 4: Endpoint o Namespace inexistente (Estatus 404)
    # -------------------------------------------------------------
    print("\n>>> PRUEBA 4: Endpoint o Namespace Inexistente (Codigo 404)")
    url_inexistente = f"{config.base_url}/api/v1/usuario_falso_no_existe/games"
    res_404 = evaluation_api_service.fetch_games_from_api(custom_url=url_inexistente)
    print(f" [ESTATUS HTTP] -> {res_404.status_code}")
    print(f" [MENSAJE]      -> {res_404.message}")
    print(f" [DETALLE]      -> {res_404.error_detail}")

    # -------------------------------------------------------------
    # PRUEBA 5: Metodo no permitido POST en vez de GET (Estatus 405)
    # -------------------------------------------------------------
    print("\n>>> PRUEBA 5: Metodo HTTP no permitido [POST] (Codigo 405)")
    res_405 = evaluation_api_service.fetch_games_from_api(method="POST")
    print(f" [ESTATUS HTTP] -> {res_405.status_code}")
    print(f" [MENSAJE]      -> {res_405.message}")
    print(f" [DETALLE]      -> {res_405.error_detail}")

    # -------------------------------------------------------------
    # RESUMEN FINAL DE LA EVALUACION
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print("                    RESUMEN DE RESULTADOS                        ")
    print("=" * 75)
    codigos_probados = [
        ("Consulta exitosa con credenciales validas", res_200.status_code, 200),
        ("Falta de API Key requerida", res_401.status_code, 401),
        ("API Key invalida o no autorizada", res_403.status_code, 403),
        ("Ruta / Namespace no encontrado", res_404.status_code, 404),
        ("Metodo HTTP no permitido (POST en GET)", res_405.status_code, 405),
    ]

    for descripcion, obtenido, esperado in codigos_probados:
        check = "OK" if obtenido == esperado else "ERROR"
        print(f" [{check:^5}] Estatus: {obtenido:<3} (Esperado: {esperado}) | {descripcion}")

    print("-" * 75)
    ram_info = evaluation_api_service.ram_storage.summary()
    print(f" Estado de la RAM: {ram_info}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    ejecutar_demostracion_completa()
