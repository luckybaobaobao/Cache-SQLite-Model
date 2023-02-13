from flask import Flask, jsonify, request, abort
import controller
from cache import Cache
from db import create_tables


cache = Cache()
app = Flask(__name__)


@app.route("/api/jokes/", methods=["POST"])
def insert_joke():
    joke_details = request.get_json()
    category = joke_details.get("categories", [])
    icon_url = joke_details.get("icon_url", None)
    value = joke_details.get("value", None)
    if not value:
        abort(422, "The value of joke is necessary")
    result = controller.insert_joke(icon_url, value, category, cache)
    return jsonify(result)


if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', port=8000)


