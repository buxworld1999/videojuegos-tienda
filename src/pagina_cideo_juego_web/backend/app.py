"""
Módulo del servidor Flask que expone la API REST de videojuegos.
"""
from flask import Flask, jsonify, request
from pagina_cideo_juego_web.backend.data import GameCatalog

# Instancia del servidor Flask
app = Flask(__name__)

# Instancia del repositorio POO
catalog = GameCatalog()


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


def run_backend(host: str = "127.0.0.1", port: int = 5000) -> None:
    """Inicia el servidor Flask en el host y puerto especificados."""
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    run_backend()

