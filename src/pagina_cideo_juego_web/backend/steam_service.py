"""
Servicio para consumir la API pública y oficial de la tienda de Steam.
Permite obtener juegos destacados, más vendidos, ofertas y buscar en todo el catálogo de Steam.
"""
from typing import List, Dict, Any
import requests
from pagina_cideo_juego_web.models.game import Game


class SteamService:
    """Clase de servicio encargada de comunicarse con la API de Steam (POO)."""

    STORE_API_URL = "https://store.steampowered.com/api"
    HEADER_IMG_URL = "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg"
    STORE_PAGE_URL = "https://store.steampowered.com/app/{appid}/"

    @classmethod
    def fetch_featured_games(cls) -> List[Game]:
        """
        Consulta las categorías destacadas de Steam (Más Vendidos, Ofertas, Nuevos Lanzamientos).
        Retorna una lista de objetos Game.
        """
        games_dict: Dict[int, Game] = {}

        endpoints = [
            f"{cls.STORE_API_URL}/featuredcategories/?l=spanish&cc=US",
            f"{cls.STORE_API_URL}/featured/?l=spanish&cc=US",
        ]

        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=6)
                if response.status_code == 200:
                    data = response.json()
                    for key, val in data.items():
                        items: List[Dict[str, Any]] = []
                        if isinstance(val, dict) and "items" in val:
                            items = val["items"]
                        elif isinstance(val, list):
                            items = val

                        for it in items:
                            if isinstance(it, dict) and "id" in it and "name" in it:
                                app_id = int(it["id"])
                                if app_id not in games_dict:
                                    # El precio viene en centavos (ej: 5999 -> 59.99)
                                    raw_price = it.get("final_price", 0)
                                    price = round(raw_price / 100.0, 2) if raw_price else 0.0

                                    img_url = it.get("header_image") or cls.HEADER_IMG_URL.format(appid=app_id)

                                    genre_name = key.replace("_", " ").capitalize() if isinstance(key, str) else "Steam"

                                    games_dict[app_id] = Game(
                                        id=app_id,
                                        title=it["name"],
                                        platform="Steam",
                                        price=price,
                                        image_url=img_url,
                                        store_url=cls.STORE_PAGE_URL.format(appid=app_id),
                                        genre=genre_name,
                                    )
            except Exception as err:
                print(f"Error consultando endpoint {endpoint}: {err}")

        return list(games_dict.values())

    @classmethod
    def search_games(cls, query: str) -> List[Game]:
        """
        Busca videojuegos en todo el catálogo de Steam usando su API de búsqueda de tienda.
        """
        if not query or len(query.strip()) < 2:
            return []

        search_url = f"{cls.STORE_API_URL}/storesearch/?term={query.strip()}&l=spanish&cc=US"
        try:
            response = requests.get(search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results: List[Game] = []
                for it in data.get("items", []):
                    app_id = int(it["id"])
                    price_info = it.get("price")
                    price = 0.0
                    if isinstance(price_info, dict):
                        price = round(price_info.get("final", 0) / 100.0, 2)

                    results.append(
                        Game(
                            id=app_id,
                            title=it["name"],
                            platform="Steam",
                            price=price,
                            image_url=cls.HEADER_IMG_URL.format(appid=app_id),
                            store_url=cls.STORE_PAGE_URL.format(appid=app_id),
                            genre="Steam Store",
                        )
                    )
                return results
        except Exception as err:
            print(f"Error buscando en la API de Steam: {err}")

        return []
