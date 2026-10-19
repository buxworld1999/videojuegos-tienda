"""
Paquete principal de la aplicación web de catálogo de videojuegos.
"""
def main() -> None:
    """Función de arranque del script de paquete."""
    from pagina_cideo_juego_web.main import main as run_app
    run_app()

__all__ = ["main"]
