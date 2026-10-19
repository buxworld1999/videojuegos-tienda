"""
Módulo de componentes visuales en Flet utilizando Programación Orientada a Objetos.
"""
import flet as ft
from pagina_cideo_juego_web.models.game import Game


class GameCard(ft.Container):
    """
    Componente visual que representa la tarjeta interactiva de un videojuego.
    Hereda de ft.Container (POO) y abre el enlace de la tienda al hacer clic.
    """

    def __init__(self, game: Game, page: ft.Page = None) -> None:
        super().__init__()
        self.game = game

        # Configuración estética de la tarjeta
        self.width = 280
        self.bgcolor = "#1e293b"  # Azul oscuro elegante
        self.border_radius = 12
        self.padding = 10
        self.ink = True  # Efecto ripple al hacer clic
        self.tooltip = f"Clic para ver {game.title} en la tienda oficial"

        # Redirección nativa oficial (abre en nueva pestaña sin errores de Flet)
        if self.game.store_url:
            self.url = ft.Url(self.game.store_url, target=ft.UrlTarget.BLANK)

        # Construcción visual de la tarjeta
        self.content = self._build_content()

    def _build_content(self) -> ft.Column:
        """Construye y organiza los elementos visuales internos de la tarjeta."""
        # Color del badge según la plataforma
        platform_color = "#00adee" if "steam" in self.game.platform.lower() else "#ffffff"
        platform_bg = "#171a21" if "steam" in self.game.platform.lower() else "#2b2b2b"

        # Formato del precio
        price_text = "GRATIS" if self.game.price == 0.0 else f"${self.game.price:.2f}"
        price_color = "#4ade80" if self.game.price == 0.0 else "#facc15"

        return ft.Column(
            controls=[
                # Imagen de portada del juego
                ft.Container(
                    border_radius=8,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Image(
                        src=self.game.image_url,
                        width=260,
                        height=140,
                        fit=ft.BoxFit.COVER,
                    ),
                ),
                # Título del juego
                ft.Text(
                    self.game.title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="#f8fafc",
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                # Fila con la plataforma y el género
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        # Badge de la tienda (Steam / Epic Games)
                        ft.Container(
                            content=ft.Text(
                                self.game.platform,
                                size=11,
                                weight=ft.FontWeight.W_600,
                                color=platform_color,
                            ),
                            bgcolor=platform_bg,
                            padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                            border_radius=6,
                        ),
                        # Género
                        ft.Text(
                            self.game.genre,
                            size=12,
                            color="#94a3b8",
                        ),
                    ],
                ),
                # Fila inferior: Precio y llamado a la acción
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            price_text,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=price_color,
                        ),
                        ft.Row(
                            spacing=4,
                            controls=[
                                ft.Text("Ir a tienda", size=12, color="#38bdf8"),
                                ft.Icon(ft.Icons.OPEN_IN_NEW, size=14, color="#38bdf8"),
                            ],
                        ),
                    ],
                ),
            ],
            spacing=8,
        )

