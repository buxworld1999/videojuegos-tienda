"""
Módulo del servidor Flask que expone la API REST de videojuegos.
Incluye endpoints del catálogo y endpoints dedicados a la evaluación de la API externa.
"""
from flask import Flask, jsonify, request, redirect
from pagina_cideo_juego_web.backend.data import GameCatalog
from pagina_cideo_juego_web.backend.api_service import evaluation_api_service
from pagina_cideo_juego_web.config import config

# Instancia del servidor Flask
app = Flask(__name__)

# Instancia del repositorio POO (Carga la API y almacena en RAM al iniciar)
catalog = GameCatalog()


@app.route("/", methods=["GET"])
def index():
    """Redirige automáticamente a la interfaz web en http://localhost:8550."""
    return redirect("http://localhost:8550")


@app.route("/api/games", methods=["GET"])
def get_games():
    """
    Endpoint principal para obtener el catálogo de videojuegos.
    Permite filtrar por plataforma (?platform=Steam) y buscar (?search=texto).
    """
    platform = request.args.get("platform")
    search_query = request.args.get("search")

    if search_query:
        games = catalog.search_by_title(search_query)
        if platform and platform.lower() != "todos":
            games = [g for g in games if g.platform.lower() == platform.lower()]
    elif platform and platform.lower() != "todos":
        games = catalog.filter_by_platform(platform)
    else:
        games = catalog.get_all()

    # Serializamos los objetos Game usando su método to_dict()
    return jsonify([game.to_dict() for game in games]), 200


@app.route("/api/games/<int:game_id>", methods=["GET"])
def get_game_detail(game_id: int):
    """Endpoint para obtener los detalles de un videojuego por su ID."""
    game = catalog.get_by_id(game_id)
    if game:
        return jsonify(game.to_dict()), 200
    return jsonify({"error": "Videojuego no encontrado"}), 404


@app.route("/api/platforms", methods=["GET"])
def get_platforms():
    """Endpoint que retorna las plataformas disponibles para la interfaz de usuario."""
    return jsonify(["Todos", "Steam", "Epic Games"]), 200


# =========================================================================
# ENDPOINTS DEDICADOS A LA EVALUACIÓN (API EXTERNA, RAM Y CÓDIGOS DE ESTATUS)
# =========================================================================

@app.route("/api/evaluacion/status", methods=["GET"])
def get_evaluacion_status():
    """
    Retorna el estado de la conexión con la API externa, el código de estatus HTTP numérico,
    la información almacenada en RAM y los datos de autenticación protegidos.
    """
    ram_summary = evaluation_api_service.ram_storage.summary()
    return jsonify({
        "status_code": ram_summary.get("codigo_estatus", 200),
        "usuario": config.username,
        "api_key_protegida": config.masked_key,
        "endpoint": config.full_url,
        "documentacion": config.docs_url,
        "almacenado_en_ram": ram_summary.get("almacenado_en_ram", True),
        "total_en_ram": ram_summary.get("total_juegos_en_ram", 0),
        "timestamp": ram_summary.get("timestamp"),
    }), 200


@app.route("/api/evaluacion/recargar", methods=["POST", "GET"])
def recargar_api_externa():
    """
    Fuerza una nueva consulta al endpoint de la API externa,
    actualiza los datos en la memoria RAM e imprime en pantalla.
    """
    result = catalog.refresh_from_api()
    evaluation_api_service.print_to_screen(result)
    return jsonify({
        "status_code": result.status_code,
        "success": result.success,
        "message": result.message,
        "juegos_guardados_en_ram": len(result.games),
    }), (result.status_code if result.status_code in (200, 401, 403, 404, 405) else 200)


@app.route("/api/evaluacion/probar/<int:target_code>", methods=["GET"])
def probar_codigo_estatus(target_code: int):
    """
    Endpoint para probar y simular de forma demostrativa
    cualquiera de los códigos de estatus HTTP del documento (200, 401, 403, 404, 405).
    """
    if target_code == 200:
        res = evaluation_api_service.fetch_games_from_api()
    elif target_code == 401:
        res = evaluation_api_service.fetch_games_from_api(custom_key="")
    elif target_code == 403:
        res = evaluation_api_service.fetch_games_from_api(custom_key="clave_invalida_demo")
    elif target_code == 404:
        res = evaluation_api_service.fetch_games_from_api(custom_url=f"{config.base_url}/api/v1/no_existe/games")
    elif target_code == 405:
        res = evaluation_api_service.fetch_games_from_api(method="POST")
    else:
        return jsonify({"error": f"Código {target_code} no soportado para prueba"}), 400

    return jsonify({
        "status_code": res.status_code,
        "success": res.success,
        "message": res.message,
        "detalle": res.error_detail,
        "total_en_ram": evaluation_api_service.ram_storage.count,
    }), 200


def run_backend(host: str = "127.0.0.1", port: int = 5000) -> None:
    """Inicia el servidor Flask en el host y puerto especificados."""
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    run_backend()
