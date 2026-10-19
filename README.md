# 🎮 Python Store - Catálogo Web de Videojuegos (Steam & Epic Games)

Aplicación web interactiva desarrollada con **Python**, utilizando **Flet** para la interfaz gráfica de usuario (Frontend) y **Flask** como microservicio de API REST (Backend), estructurada bajo principios de **Programación Orientada a Objetos (POO)**.

Permite explorar videojuegos disponibles en plataformas como **Steam** y **Epic Games**, filtrar por tienda o buscar por nombre, y al hacer clic en cualquier videojuego, redirige de forma automática a la página oficial de la tienda.


## 📁 Estructura del Proyecto

```text
pagina-cideo-juego-web/
│
├── .venv/                              # Entorno virtual aislado
├── pyproject.toml                      # Metadatos del proyecto y dependencias modernas (uv)
├── requirements.txt                    # Dependencias congeladas para pip
├── README.md                           # Documentación completa del proyecto
│
└── src/
    └── pagina_cideo_juego_web/
        ├── __init__.py                 # Exportador del paquete y script de inicio
        ├── main.py                     # Orquestador: Inicia Flask en segundo plano y lanza Flet Web
        │
        ├── models/                     # [POO] Capa de Modelos de Datos
        │   ├── __init__.py
        │   └── game.py                 # Clase Game con serialización to_dict / from_dict
        │
        ├── backend/                    # [Flask] Capa de Servicios y API REST
        │   ├── __init__.py
        │   ├── steam_service.py        # Clase SteamService (Consumo directo de la API pública de Steam)
        │   ├── data.py                 # Clase GameCatalog (Gestor híbrido Steam API + Epic Games)
        │   └── app.py                  # Servidor Flask con endpoints /api/games y /api/platforms
        │
        └── frontend/                   # [Flet] Capa de Interfaz Gráfica
            ├── __init__.py
            ├── components.py           # Clase GameCard (Componente visual interactivo)
            └── app.py                  # Clase GameApp (Vista principal, buscador y cuadrícula)
```

---

## 🛠️ Requisitos Previos

* **Python 3.11** o superior instalado en el sistema.

---

## 🚀 Instalación y Puesta en Marcha

### Opción A: Usando `uv` (Recomendado y más rápido)

1. **Clonar o abrir la carpeta del proyecto en la terminal:**
   ```powershell
   cd "c:\games\proyectos visual\pagina cideo juego web"
   ```

2. **Sincronizar el entorno virtual y dependencias:**
   ```powershell
   uv sync
   ```

3. **Ejecutar la aplicación:**
   ```powershell
   uv run pagina-cideo-juego-web
   ```
   *(o también: `uv run python -m pagina_cideo_juego_web.main`)*

---

### Opción B: Usando `venv` estándar y `pip`

1. **Crear y activar el entorno virtual:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Instalar dependencias desde `requirements.txt`:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Ejecutar el proyecto:**
   ```powershell
   python -m pagina_cideo_juego_web.main
   ```

---

## 🌐 Endpoints de la API REST (Flask)

Al iniciar el proyecto, el servidor Flask se levanta en `http://127.0.0.1:5000`:

* `GET /api/games`: Retorna la lista de todos los juegos en formato JSON.
  * *Parámetro opcional `platform`:* `/api/games?platform=Steam` o `/api/games?platform=Epic Games`.
  * *Parámetro opcional `search`:* `/api/games?search=Cyberpunk`.
* `GET /api/games/<id>`: Retorna los datos detallados de un videojuego por su identificador.
* `GET /api/platforms`: Retorna la lista de plataformas disponibles (`["Todos", "Steam", "Epic Games"]`).
