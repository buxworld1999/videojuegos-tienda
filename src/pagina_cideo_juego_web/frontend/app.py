"""
Módulo principal de la interfaz gráfica Flet organizada con POO.
"""
import sys
from pathlib import Path
from typing import List

# Asegurar compatibilidad al ejecutar este archivo directamente desde VS Code
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import flet as ft
import requests

from pagina_cideo_juego_web.models.game import Game
from pagina_cideo_juego_web.frontend.components import GameCard, ApiEvaluationCard


class GameApp:
    """
    Controlador y vista principal de la aplicación GUI en Flet.
    Gestiona el estado (búsqueda, plataforma seleccionada) y consume la API Flask.
    """

    def __init__(self, page: ft.Page, api_url: str = "http://127.0.0.1:5000/api") -> None:
        self.page = page
        self.api_url = api_url
        self.selected_platform = "Todos"
        self.search_query = ""

        # Configuración general de la ventana
        self.page.title = "Python Store - Catálogo de Videojuegos (Steam & Epic Games)"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0b0f19"  # Fondo oscuro gamer
        self.page.padding = 30
        self.page.scroll = ft.ScrollMode.AUTO

        # Contenedor dinámico donde se colocarán las tarjetas de juegos
        self.games_grid = ft.Row(
            wrap=True,
            spacing=20,
            run_spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )

        # Fila de botones de filtro
        self.filter_buttons_row = ft.Row(spacing=10)

    def fetch_games(self) -> List[Game]:
        """Realiza la petición HTTP a la API de Flask y deserializa a objetos Game."""
        try:
            params = {
                "platform": self.selected_platform,
                "search": self.search_query,
            }
            response = requests.get(f"{self.api_url}/games", params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # POO: Usamos el método de clase from_dict para construir cada objeto
                return [Game.from_dict(item) for item in data]
        except requests.exceptions.RequestException as err:
            print(f"Error conectando con la API de Flask: {err}")
        return []

    def update_game_display(self) -> None:
        """Actualiza la cuadrícula de juegos según los filtros y búsqueda actuales."""
        self.games_grid.controls.clear()
        games = self.fetch_games()

        if not games:
            self.games_grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.VIDEOGAME_ASSET_OFF, size=64, color="#64748b"),
                            ft.Text("No se encontraron videojuegos", size=18, color="#94a3b8"),
                        ],
                    ),
                    padding=40,
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                )
            )
        else:
            for game in games:
                self.games_grid.controls.append(GameCard(game=game, page=self.page))

        self.page.update()

    def _on_search_change(self, e: ft.ControlEvent) -> None:
        """Manejador del evento de cambio de texto en el buscador."""
        self.search_query = e.control.value.strip()
        self.update_game_display()

    def _on_platform_select(self, platform: str) -> None:
        """Manejador del cambio de pestaña/filtro de plataforma."""
        self.selected_platform = platform
        self._build_filter_buttons()
        self.update_game_display()

    def _build_filter_buttons(self) -> None:
        """Construye los botones de filtro destacando el activo."""
        platforms = ["Todos", "Steam", "Epic Games"]
        self.filter_buttons_row.controls.clear()

        for plat in platforms:
            is_selected = self.selected_platform.lower() == plat.lower()
            btn = ft.Button(
                plat,
                bgcolor="#3b82f6" if is_selected else "#1e293b",
                color="#ffffff",
                on_click=lambda e, p=plat: self._on_platform_select(p),
            )
            self.filter_buttons_row.controls.append(btn)
        try:
            self.filter_buttons_row.update()
        except Exception:
            pass

    def build_ui(self) -> None:
        """Monta toda la interfaz gráfica en la página."""
        # 1. Encabezado principal
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SPORTS_ESPORTS, size=40, color="#38bdf8"),
                            ft.Text(
                                "Python Store",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color="#f8fafc",
                            ),
                        ]
                    ),
                    ft.Text(
                        "Explora los mejores videojuegos en Steam y Epic Games. Haz clic en cualquier portada para ir a la tienda oficial.",
                        size=14,
                        color="#94a3b8",
                    ),
                ],
                spacing=5,
            ),
            margin=ft.Margin(bottom=20),
        )

        # 1.5. Tarjeta de control y estado de la Evaluación de la API
        self.api_card = ApiEvaluationCard(
            api_url=self.api_url,
            on_refresh_callback=self.update_game_display,
        )

        # 2. Barra de búsqueda
        search_field = ft.TextField(
            hint_text="Buscar videojuego por nombre...",
            prefix_icon=ft.Icons.SEARCH,
            bgcolor="#1e293b",
            border_radius=10,
            border_color="#334155",
            color="#f8fafc",
            on_change=self._on_search_change,
            expand=True,
        )

        search_and_filter_bar = ft.Column(
            controls=[
                search_field,
                self.filter_buttons_row,
            ],
            spacing=15,
        )

        # 3. Construir botones de filtro iniciales y cargar juegos
        self._build_filter_buttons()

        # 4. Agregar todo a la página
        self.page.add(
            header,
            self.api_card,
            search_and_filter_bar,
            ft.Divider(color="#1e293b", height=30),
            self.games_grid,
        )

        # Cargar los primeros juegos
        self.update_game_display()


def main(page: ft.Page) -> None:
    """Función de entrada para la aplicación de Flet."""
    app = GameApp(page)
    app.build_ui()


if __name__ == "__main__":
    from pagina_cideo_juego_web.main import main as run_project
    run_project()

