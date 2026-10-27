# 🎮 Python Store - Catálogo Web de Videojuegos (Steam & Epic Games)

Aplicación web interactiva desarrollada con **Python**, utilizando **Flet** para la interfaz gráfica de usuario (Frontend) y **Flask** como microservicio de API REST (Backend), estructurada bajo principios de **Programación Orientada a Objetos (POO)**.

Permite explorar videojuegos disponibles en plataformas como **Steam** y **Epic Games**, filtrar por tienda o buscar por nombre, y al hacer clic en cualquier videojuego, redirige de forma automática a la página oficial de la tienda.

---

## 📋 Módulo de Evaluación - Conexión con API Externa REST

Para la evaluación académica, el sistema se conecta a la API de Render bajo las siguientes especificaciones:

* **Usuario asignado:** `buxworld`
* **API Key protegida:** Cargada de forma segura desde el archivo `.env` (`X-API-Key`). Ignorada en `.gitignore` para máxima seguridad.
* **API Base URL:** `https://progra-2-krw5.onrender.com`
* **Endpoint asignado:** `https://progra-2-krw5.onrender.com/api/v1/samuel/games`
* **Documentación oficial Swagger:** [Docs Endpoint Samuel](https://progra-2-krw5.onrender.com/docs#/Evaluación%20-%20Samuel%20(Videojuegos%20Tienda)/get_samuel_games_endpoint_api_v1_samuel_games_get)
* **Almacenamiento en RAM:** Los datos obtenidos desde el endpoint se almacenan en la memoria RAM del sistema (`RamStorage`) y se renderizan tanto en la consola/terminal como en la interfaz gráfica Flet.
* **Manejo de Excepciones y Códigos de Estatus HTTP:**
  * `200`: Éxito - Catálogo recibido y almacenado en la memoria RAM.
  * `401`: Unauthorized - Falta de cabecera `X-API-Key`.
  * `403`: Forbidden - API Key inválida o no autorizada para el namespace.
  * `404`: Not Found - Namespace o endpoint no existente.
  * `405`: Method Not Allowed - Uso de métodos HTTP no permitidos (ej. POST).
  * `500` / `503` / `504`: Manejo de errores internos y pérdida de conexión / timeouts.

### 🧪 Demostración Rápida de la Evaluación (Script de Pruebas)
Para ejecutar la prueba automática que valida la conexión, el almacenamiento en RAM, la impresión en pantalla y todos los códigos de estatus (200, 401, 403, 404, 405):

```powershell
uv run python probar_api.py
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

3. **Ejecutar la aplicación completa (Backend Flask + Frontend Web Flet):**
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

## 🔒 Configuración de Variables de Entorno (`.env`)

El archivo `.env` en la raíz contiene las credenciales protegidas:

```env
API_USERNAME=buxworld
API_KEY=sk_live_sam_5a19d08e42b74c3eb918a72c
API_BASE_URL=https://progra-2-krw5.onrender.com
API_ENDPOINT=/api/v1/samuel/games
API_DOCS_URL=https://progra-2-krw5.onrender.com/docs#/Evaluación%20-%20Samuel%20(Videojuegos%20Tienda)/get_samuel_games_endpoint_api_v1_samuel_games_get
```

---

## 🌐 Endpoints de la API REST Local (Flask)

Al iniciar el proyecto, el servidor Flask se levanta en `http://127.0.0.1:5000`:

* `GET /api/games`: Retorna la lista de todos los juegos almacenados en la RAM.
* `GET /api/games/<id>`: Retorna los datos detallados de un videojuego por su ID.
* `GET /api/platforms`: Retorna las plataformas disponibles (`["Todos", "Steam", "Epic Games"]`).
* `GET /api/evaluacion/status`: Inspecciona el estado de la conexión, código de estatus y datos en RAM.
* `POST /api/evaluacion/recargar`: Fuerza la recarga desde la API externa a la memoria RAM.
* `GET /api/evaluacion/probar/<codigo>`: Demuestra la respuesta para los códigos `200`, `401`, `403`, `404`, `405`.
