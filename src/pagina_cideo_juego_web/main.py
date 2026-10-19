"""
Punto de entrada principal del proyecto.
Inicia el microservicio de backend (Flask) en segundo plano y luego lanza la interfaz gráfica (Flet).
"""
import sys
import threading
import time
from pathlib import Path
import flet as ft

# Asegurar que la ruta 'src' esté en el path de Python para ejecución directa o desde VS Code
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from pagina_cideo_juego_web.backend.app import run_backend
from pagina_cideo_juego_web.frontend.app import main as flet_main


def start_flask_service() -> None:
    """Inicia el servidor Flask en un hilo independiente (daemon) para no bloquear la GUI."""
    flask_thread = threading.Thread(
        target=run_backend,
        kwargs={"host": "127.0.0.1", "port": 5000},
        daemon=True,
    )
    flask_thread.start()
    # Pausa de cortesía para que Flask inicialice el socket
    time.sleep(1)


def launch_browser() -> None:
    """Abre automáticamente el navegador predeterminado una vez levantado el servidor."""
    time.sleep(2)
    import webbrowser
    webbrowser.open("http://localhost:8550")


def main() -> None:
    """Función principal que orquesta el backend y levanta la interfaz en el navegador web."""
    print("====================================================")
    print("Iniciando Servidor Flask (API REST) en http://127.0.0.1:5000")
    print("====================================================")
    start_flask_service()

    print("====================================================")
    print("Iniciando Python Store en el navegador web...")
    print("Enlace directo: http://localhost:8550")
    print("====================================================")
    # Hilo para abrir la ventana del navegador automáticamente
    threading.Thread(target=launch_browser, daemon=True).start()

    # En Flet 1.0+ se usa ft.run() con view=ft.AppView.WEB_BROWSER y puerto fijo
    ft.run(flet_main, view=ft.AppView.WEB_BROWSER, port=8550)


if __name__ == "__main__":
    main()

