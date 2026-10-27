"""
Módulo de configuración centralizada y protección de secretos.
Carga variables de entorno desde el archivo .env de forma segura.
"""
import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Localizar la raíz del proyecto para asegurar la carga del archivo .env
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()


@dataclass(frozen=True)
class ApiConfig:
    """Clase inmutable para la configuración de la API externa (POO)."""
    username: str = os.getenv("API_USERNAME", "buxworld")
    api_key: str = os.getenv("API_KEY", "")
    base_url: str = os.getenv("API_BASE_URL", "https://progra-2-krw5.onrender.com").rstrip("/")
    endpoint: str = os.getenv("API_ENDPOINT", "/api/v1/samuel/games")
    docs_url: str = os.getenv(
        "API_DOCS_URL",
        "https://progra-2-krw5.onrender.com/docs#/Evaluación%20-%20Samuel%20(Videojuegos%20Tienda)/get_samuel_games_endpoint_api_v1_samuel_games_get",
    )

    @property
    def full_url(self) -> str:
        """Retorna la URL completa al endpoint asignado."""
        clean_endpoint = self.endpoint if self.endpoint.startswith("/") else f"/{self.endpoint}"
        return f"{self.base_url}{clean_endpoint}"

    @property
    def masked_key(self) -> str:
        """Retorna la API key ofuscada para protegerla al imprimirla en pantalla o logs."""
        if not self.api_key:
            return "[NO CONFIGURADA]"
        if len(self.api_key) <= 8:
            return "******"
        return f"{self.api_key[:12]}...{self.api_key[-4:]}"


# Instancia singleton para uso en todo el proyecto
config = ApiConfig()
