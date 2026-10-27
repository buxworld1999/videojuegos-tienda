"""
Módulo de componentes visuales en Flet utilizando Programación Orientada a Objetos.
Incluye tarjetas de videojuegos (GameCard) y el panel de control de la evaluación (ApiEvaluationCard).
"""
from typing import Callable, Optional
import flet as ft
import requests

from pagina_cideo_juego_web.models.game import Game
from pagina_cideo_juego_web.config import config


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

        # Redirección nativa oficial
        if self.game.store_url:
            self.url = ft.Url(self.game.store_url, target=ft.UrlTarget.BLANK)

        # Construcción visual de la tarjeta
        self.content = self._build_content()

    def _build_content(self) -> ft.Column:
        """Construye y organiza los elementos visuales internos de la tarjeta."""
        platform_color = "#00adee" if "steam" in self.game.platform.lower() else "#ffffff"
        platform_bg = "#171a21" if "steam" in self.game.platform.lower() else "#2b2b2b"

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


class ApiEvaluationCard(ft.Container):
    """
    Componente visual interactivo para la Evaluación de Sistemas.
    Muestra en pantalla el estatus en código (200, 401, 403, 404, 405),
    la información en RAM, la protección de la API Key (.env) y botones de prueba.
    """

    def __init__(
        self,
        api_url: str = "http://127.0.0.1:5000/api",
        on_refresh_callback: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__()
        self.api_url = api_url
        self.on_refresh_callback = on_refresh_callback

        # Estilo del contenedor principal
        self.bgcolor = "#111827"  # Gris azulado oscuro premium
        self.border = ft.Border.all(1, "#1f2937")
        self.border_radius = 16
        self.padding = 20
        self.margin = ft.Margin(bottom=20)

        # Elementos dinámicos reactivos
        self.status_code_text = ft.Text("200", size=18, weight=ft.FontWeight.BOLD, color="#ffffff")
        self.status_badge = ft.Container(
            content=ft.Row(
                tight=True,
                spacing=6,
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=18, color="#ffffff"),
                    ft.Text("ESTATUS:", size=12, weight=ft.FontWeight.BOLD, color="#ffffff"),
                    self.status_code_text,
                ],
            ),
            bgcolor="#15803d",  # Verde éxito inicial
            padding=ft.Padding(left=12, right=12, top=6, bottom=6),
            border_radius=8,
        )

        self.ram_info_text = ft.Text("6 juegos en RAM", size=12, color="#38bdf8", weight=ft.FontWeight.W_600)
        self.console_output = ft.Text(
            "Sistema conectado a la API. Datos cargados en memoria RAM listos para visualización.",
            size=12,
            font_family="Consolas, monospace",
            color="#a7f3d0",
        )

        self.content = self._build_content()

    def _build_content(self) -> ft.Column:
        """Construye la jerarquía visual del panel de evaluación."""
        return ft.Column(
            spacing=14,
            controls=[
                # Fila 1: Encabezado del panel con título y Badge de Estatus numérico
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,
                    controls=[
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.CLOUD_SYNC, color="#38bdf8", size=24),
                                    bgcolor="#0f172a",
                                    padding=8,
                                    border_radius=8,
                                ),
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            "Módulo de Evaluación: Conexión API REST Externa",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color="#f8fafc",
                                        ),
                                        ft.Text(
                                            "Consumo seguro del endpoint, almacenamiento en RAM y manejo de excepciones",
                                            size=12,
                                            color="#94a3b8",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        self.status_badge,
                    ],
                ),
                ft.Divider(color="#1f2937", height=1),
                # Fila 2: Métricas de seguridad y memoria RAM
                ft.Row(
                    wrap=True,
                    spacing=12,
                    controls=[
                        # Usuario
                        self._build_info_pill(
                            icon=ft.Icons.PERSON,
                            label="Usuario",
                            value=config.username,
                            color="#818cf8",
                        ),
                        # API Key Protegida (.env)
                        self._build_info_pill(
                            icon=ft.Icons.LOCK,
                            label="API Key (.env)",
                            value=config.masked_key,
                            color="#34d399",
                        ),
                        # Almacenamiento en RAM
                        ft.Container(
                            content=ft.Row(
                                tight=True,
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.MEMORY, size=16, color="#38bdf8"),
                                    ft.Text("Almacenado en RAM:", size=11, color="#94a3b8"),
                                    self.ram_info_text,
                                ],
                            ),
                            bgcolor="#1e293b",
                            padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                            border_radius=8,
                        ),
                        # Endpoint
                        self._build_info_pill(
                            icon=ft.Icons.HTTP,
                            label="Endpoint",
                            value=config.endpoint,
                            color="#fbbf24",
                        ),
                    ],
                ),
                # Fila 3: Botonera interactiva para el evaluador (Prueba de códigos 200, 401, 403, 404, 405)
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            "Probar Códigos de Estatus HTTP del Documento en Vivo:",
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color="#cbd5e1",
                        ),
                        ft.Row(
                            wrap=True,
                            spacing=8,
                            controls=[
                                ft.Button(
                                    "200 OK",
                                    bgcolor="#15803d",
                                    color="#ffffff",
                                    on_click=lambda e: self._test_code(200),
                                ),
                                ft.Button(
                                    "401 Sin Key",
                                    bgcolor="#b45309",
                                    color="#ffffff",
                                    on_click=lambda e: self._test_code(401),
                                ),
                                ft.Button(
                                    "403 Key Inválida",
                                    bgcolor="#b91c1c",
                                    color="#ffffff",
                                    on_click=lambda e: self._test_code(403),
                                ),
                                ft.Button(
                                    "404 No Encontrado",
                                    bgcolor="#7c2d12",
                                    color="#ffffff",
                                    on_click=lambda e: self._test_code(404),
                                ),
                                ft.Button(
                                    "405 Método POST",
                                    bgcolor="#4c1d95",
                                    color="#ffffff",
                                    on_click=lambda e: self._test_code(405),
                                ),
                                ft.Button(
                                    "Recargar y Guardar en RAM",
                                    bgcolor="#2563eb",
                                    color="#ffffff",
                                    on_click=lambda e: self._sync_now(),
                                ),
                                ft.Button(
                                    "Doc Oficial (Swagger)",
                                    bgcolor="#334155",
                                    color="#f8fafc",
                                    url=ft.Url(config.docs_url, target=ft.UrlTarget.BLANK),
                                ),
                            ],
                        ),
                    ],
                ),
                # Fila 4: Consola de salida impresa en pantalla
                ft.Container(
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.TERMINAL, size=14, color="#94a3b8"),
                                    ft.Text("SALIDA IMPRESA EN PANTALLA:", size=11, color="#94a3b8", weight=ft.FontWeight.BOLD),
                                ],
                            ),
                            self.console_output,
                        ],
                    ),
                    bgcolor="#030712",
                    border=ft.Border.all(1, "#1e293b"),
                    border_radius=8,
                    padding=10,
                ),
            ],
        )

    def _build_info_pill(self, icon, label: str, value: str, color: str) -> ft.Container:
        """Construye un chip informativo estilizado."""
        return ft.Container(
            content=ft.Row(
                tight=True,
                spacing=6,
                controls=[
                    ft.Icon(icon, size=16, color=color),
                    ft.Text(f"{label}:", size=11, color="#94a3b8"),
                    ft.Text(value, size=11, color="#f1f5f9", weight=ft.FontWeight.W_600),
                ],
            ),
            bgcolor="#1e293b",
            padding=ft.Padding(left=10, right=10, top=6, bottom=6),
            border_radius=8,
        )

    def _update_status_ui(self, code: int, message: str, ram_count: int, is_success: bool) -> None:
        """Actualiza el indicador visual de código de estatus y la consola en pantalla."""
        self.status_code_text.value = str(code)

        # Colores según el código HTTP
        if code == 200:
            self.status_badge.bgcolor = "#15803d"  # Verde
            self.console_output.color = "#a7f3d0"
        elif code in (401, 403):
            self.status_badge.bgcolor = "#b91c1c"  # Rojo
            self.console_output.color = "#fca5a5"
        elif code in (404, 405):
            self.status_badge.bgcolor = "#c2410c"  # Naranja oscuro
            self.console_output.color = "#fdba74"
        else:
            self.status_badge.bgcolor = "#4b5563"  # Gris
            self.console_output.color = "#cbd5e1"

        self.ram_info_text.value = f"{ram_count} juegos en RAM"
        self.console_output.value = f"[CÓDIGO DE ESTATUS: {code}] {message}"

        try:
            self.status_badge.update()
            self.ram_info_text.update()
            self.console_output.update()
        except Exception:
            pass

    def _test_code(self, target_code: int) -> None:
        """Invoca la prueba del código seleccionado y actualiza la pantalla."""
        try:
            res = requests.get(f"{self.api_url}/evaluacion/probar/{target_code}", timeout=6)
            if res.status_code == 200:
                data = res.json()
                code = data.get("status_code", target_code)
                msg = data.get("message") or data.get("detalle") or "Respuesta procesada"
                ram_cnt = data.get("total_en_ram", 6)
                self._update_status_ui(
                    code=code,
                    message=msg,
                    ram_count=ram_cnt,
                    is_success=(code == 200),
                )
        except Exception as err:
            self._update_status_ui(
                code=500,
                message=f"Excepción al conectar con servicio interno: {err}",
                ram_count=0,
                is_success=False,
            )

    def _sync_now(self) -> None:
        """Sincroniza la API externa con la RAM y notifica a la interfaz."""
        try:
            res = requests.post(f"{self.api_url}/evaluacion/recargar", timeout=8)
            data = res.json()
            code = data.get("status_code", 200)
            msg = data.get("message", "Sincronizado")
            ram_cnt = data.get("juegos_guardados_en_ram", 6)
            self._update_status_ui(
                code=code,
                message=f"{msg} | Guardado en la memoria RAM exitosamente.",
                ram_count=ram_cnt,
                is_success=(code == 200),
            )
            # Refrescar catálogo visual
            if self.on_refresh_callback:
                self.on_refresh_callback()
        except Exception as err:
            self._update_status_ui(
                code=503,
                message=f"Error al sincronizar con la API: {err}",
                ram_count=0,
                is_success=False,
            )
