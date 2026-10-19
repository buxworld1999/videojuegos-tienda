"""
Módulo que contiene el catálogo inicial y el repositorio en memoria de videojuegos.
Integra datos de Epic Games y consume la API oficial de Steam en tiempo real.
"""
from typing import List, Optional, Dict
from pagina_cideo_juego_web.models.game import Game
from pagina_cideo_juego_web.backend.steam_service import SteamService


class GameCatalog:
    """Clase encargada de gestionar la colección de videojuegos (POO / Repositorio)."""

    def __init__(self) -> None:
        """Inicializa el catálogo con juegos de Epic Games y descarga el catálogo en vivo de Steam."""
        # 1. Juegos de Epic Games
        self._games: List[Game] = [
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

        # 2. Descargar juegos en tiempo real desde la API de Steam
        self._load_live_steam_catalog()

    def _load_live_steam_catalog(self) -> None:
        """Consulta la API de Steam y agrega el catálogo destacado en vivo."""
        try:
            print("Consultando la API oficial de Steam...")
            steam_games = SteamService.fetch_featured_games()
            if steam_games:
                # Evitar duplicados por ID
                existing_ids = {g.id for g in self._games}
                for game in steam_games:
                    if game.id not in existing_ids:
                        self._games.append(game)
                        existing_ids.add(game.id)
                print(f"Catálogo de Steam sincronizado: {len(steam_games)} juegos cargados.")
        except Exception as err:
            print(f"No se pudo cargar el catálogo en vivo de Steam: {err}")

    def get_all(self) -> List[Game]:
        """Retorna todos los videojuegos registrados."""
        return self._games

    def filter_by_platform(self, platform: str) -> List[Game]:
        """Filtra juegos según la plataforma indicada (ignora mayúsculas/minúsculas)."""
        if not platform or platform.lower() == "todos":
            return self.get_all()
        return [g for g in self._games if g.platform.lower() == platform.lower()]

    def search_by_title(self, query: str) -> List[Game]:
        """
        Busca videojuegos por título en memoria y consulta la API de Steam en vivo si es necesario.
        """
        if not query:
            return self.get_all()

        query_lower = query.lower()
        # Coincidencias en memoria
        local_results = [g for g in self._games if query_lower in g.title.lower()]
        seen_ids = {g.id for g in local_results}

        # Búsqueda en vivo en todo el catálogo de Steam
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
