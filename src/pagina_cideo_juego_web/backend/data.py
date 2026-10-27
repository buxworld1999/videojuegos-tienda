"""
Módulo que contiene el catálogo inicial y el repositorio en memoria (RAM) de videojuegos.
Integra datos desde la API externa de la evaluación (Render) y desde la API de Steam en tiempo real.
"""
from typing import List, Optional, Dict, Any
from pagina_cideo_juego_web.models.game import Game
from pagina_cideo_juego_web.backend.steam_service import SteamService
from pagina_cideo_juego_web.backend.api_service import evaluation_api_service, ApiResponseResult


class GameCatalog:
    """
    Repositorio en memoria RAM para la colección de videojuegos (POO).
    Consume la API REST externa de la evaluación protegida con API Key y almacena en RAM.
    """

    def __init__(self) -> None:
        """Inicializa el catálogo cargando los juegos desde la API en la memoria RAM."""
        self._games: List[Game] = []
        self._last_api_result: Optional[ApiResponseResult] = None

        # 1. Cargar juegos desde la API externa de la evaluación (Render) a la RAM
        self._load_from_evaluation_api()

        # 2. Descargar juegos adicionales en tiempo real desde la API de Steam
        self._load_live_steam_catalog()

    def _load_from_evaluation_api(self) -> None:
        """
        Consulta la API de la evaluación, maneja excepciones,
        almacena los juegos en RAM e imprime en pantalla.
        """
        try:
            print("\n[GameCatalog] Conectando con API externa de Evaluación...")
            result = evaluation_api_service.fetch_games_from_api()
            self._last_api_result = result

            # Imprimir en consola de acuerdo al requerimiento
            evaluation_api_service.print_to_screen(result)

            if result.success and result.games:
                self._games = list(result.games)
                print(f"[GameCatalog] Éxito: {len(self._games)} juegos cargados en RAM desde la API.")
            else:
                print(f"[GameCatalog] Aviso (Estatus {result.status_code}): Cargando catálogo base de respaldo.")
                self._load_fallback_games()

        except Exception as err:
            print(f"[GameCatalog] Excepción al inicializar catálogo desde API: {err}")
            self._load_fallback_games()

    def _load_fallback_games(self) -> None:
        """Catálogo de respaldo en caso de desconexión o fallo en la API."""
        if not self._games:
            self._games = [
                Game(
                    id=1001,
                    title="Fortnite",
                    platform="Epic Games",
                    price=0.0,
                    image_url="https://cdn2.unrealengine.com/14br-consoles-1920x1080-wlogo-1920x1080-e50f5a914378.jpg",
                    store_url="https://store.epicgames.com/es-ES/p/fortnite",
                    genre="Battle Royale",
                ),
                Game(
                    id=1002,
                    title="Rocket League",
                    platform="Epic Games",
                    price=0.0,
                    image_url="https://cdn1.epicgames.com/offer/9773aa1aa54f4f7b80e44bef049cb012/EGS_RocketLeague_PsyonixLLC_S1_2560x1440-410a0194848602b489a2e6f4770fc569",
                    store_url="https://store.epicgames.com/es-ES/p/rocket-league",
                    genre="Deportes / Acción",
                ),
                Game(
                    id=1003,
                    title="Fall Guys",
                    platform="Epic Games",
                    price=0.0,
                    image_url="https://cdn1.epicgames.com/offer/50118b7f954e450f8823df1614b24e80/EGS_FallGuys_Mediatonic_S1_2560x1440-272da7ef34327668ccae7ff3d48d08ea",
                    store_url="https://store.epicgames.com/es-ES/p/fall-guys",
                    genre="Party / Plataformas",
                ),
                Game(
                    id=1004,
                    title="Genshin Impact",
                    platform="Epic Games",
                    price=0.0,
                    image_url="https://cdn1.epicgames.com/offer/879b0d8776ab46a59dc329ff5055bc94/EGS_GenshinImpact_miHoYoLimited_S1_2560x1440-91c6cd7312cc26a471404d0f8185c62c",
                    store_url="https://store.epicgames.com/es-ES/p/genshin-impact",
                    genre="Acción / Aventura",
                ),
                Game(
                    id=1005,
                    title="Alan Wake 2",
                    platform="Epic Games",
                    price=49.99,
                    image_url="https://cdn1.epicgames.com/offer/c4763ff8d7d14d40ab7100194b61db28/EGS_AlanWake2_RemedyEntertainment_S1_2560x1440-8b1b5e282161b90382f7c0062bc4665c",
                    store_url="https://store.epicgames.com/es-ES/p/alan-wake-2",
                    genre="Survival Horror",
                ),
                Game(
                    id=1006,
                    title="Grand Theft Auto V: Premium Edition",
                    platform="Epic Games",
                    price=29.99,
                    image_url="https://cdn1.epicgames.com/0584dacc0136465db43516bbc9c50d6e/offer/GTAV_EGS_Artwork_1920x1080_Hero-1920x1080-2a8d3e098867c00c7e2b10a26ef7f938.jpg",
                    store_url="https://store.epicgames.com/es-ES/p/grand-theft-auto-v",
                    genre="Acción / Mundo Abierto",
                ),
            ]

    def _load_live_steam_catalog(self) -> None:
        """Consulta la API de Steam y agrega el catálogo destacado en vivo."""
        try:
            print("[GameCatalog] Consultando la API oficial de Steam...")
            steam_games = SteamService.fetch_featured_games()
            if steam_games:
                existing_ids = {g.id for g in self._games}
                for game in steam_games:
                    if game.id not in existing_ids:
                        self._games.append(game)
                        existing_ids.add(game.id)
                print(f"[GameCatalog] Catálogo de Steam sincronizado: {len(steam_games)} juegos cargados.")
        except Exception as err:
            print(f"[GameCatalog] No se pudo cargar el catálogo en vivo de Steam: {err}")

    def refresh_from_api(self) -> ApiResponseResult:
        """Fuerza una nueva sincronización con la API y actualiza la RAM."""
        result = evaluation_api_service.fetch_games_from_api()
        self._last_api_result = result
        if result.success and result.games:
            # Reemplazar juegos de la API en la memoria RAM manteniendo los de Steam
            steam_games = [g for g in self._games if g.platform.lower() == "steam"]
            self._games = list(result.games) + steam_games
        return result

    def get_api_status(self) -> Dict[str, Any]:
        """Retorna el estado actual de la conexión y memoria RAM."""
        ram_info = evaluation_api_service.ram_storage.summary()
        last_code = self._last_api_result.status_code if self._last_api_result else 200
        return {
            "status_code": last_code,
            "ram": ram_info,
            "last_message": self._last_api_result.message if self._last_api_result else "Inicializado",
            "total_games_in_memory": len(self._games),
        }

    def get_all(self) -> List[Game]:
        """Retorna todos los videojuegos registrados en memoria RAM."""
        return self._games

    def filter_by_platform(self, platform: str) -> List[Game]:
        """Filtra juegos según la plataforma indicada (ignora mayúsculas/minúsculas)."""
        if not platform or platform.lower() == "todos":
            return self.get_all()
        return [g for g in self._games if g.platform.lower() == platform.lower()]

    def search_by_title(self, query: str) -> List[Game]:
        """
        Busca videojuegos por título en memoria RAM y consulta Steam si es necesario.
        """
        if not query:
            return self.get_all()

        query_lower = query.lower()
        local_results = [g for g in self._games if query_lower in g.title.lower()]
        seen_ids = {g.id for g in local_results}

        try:
            online_results = SteamService.search_games(query)
            for g in online_results:
                if g.id not in seen_ids:
                    local_results.append(g)
                    seen_ids.add(g.id)
        except Exception as err:
            print(f"Error buscando en la API en vivo de Steam: {err}")

        return local_results

    def get_by_id(self, game_id: int) -> Optional[Game]:
        """Obtiene un juego por su identificador único."""
        for g in self._games:
            if g.id == game_id:
                return g
        return None
