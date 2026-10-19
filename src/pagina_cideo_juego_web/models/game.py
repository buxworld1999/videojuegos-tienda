from typing import Dict, Any

class Game:

    def __init__(self,
        id: int,
        title: str,
        platform: str,
        price: float,
        image_url: str,
        store_url: str,
        genre: str = "General",
    ) -> None:

        self.id = id
        self.title = title
        self.platform = platform
        self.price = price
        self.image_url = image_url
        self.store_url = store_url
        self.genre = genre

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto Game a un diccionario serializable para la API de Flask."""
        return {
            "id": self.id,
            "title": self.title,
            "platform": self.platform,
            "price": self.price,
            "image_url": self.image_url,
            "store_url": self.store_url,
            "genre": self.genre,
        }
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Game":
        """Crea una instancia de Game a partir de un diccionario recibido desde la API."""
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            platform=data.get("platform", ""),
            price=float(data.get("price", 0.0)),
            image_url=data.get("image_url", ""),
            store_url=data.get("store_url", ""),
            genre=data.get("genre", "General"),
        )

    def __repr__(self) -> str:
        """Representación en texto para depuración."""     
        return f"<Game {self.title} ({self.platform})>"
        

