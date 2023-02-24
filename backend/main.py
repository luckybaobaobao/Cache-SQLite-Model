from flask import Flask, jsonify, request, abort
import controller
from cache import Cache
from query_remote import get_joke_from_remote
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


@app.route("/api/joke/<id>", methods=["PUT"])
def update_joke(id):
    if id not in cache.local_ids:
        abort(404, "This joke does not exist in local database, you can not update")

    joke_details = request.get_json()
    icon_url = joke_details.get("icon_url", None)
    value = joke_details.get("value", None)
    category = joke_details.get("categories", None)

    result = controller.update_joke(id, icon_url, value, category)
    return jsonify(result)


@app.route("/api/joke/<id>", methods=["GET"])
def get_joke_by_id(id):
    if id in cache.local_ids:
        joke = controller.get_joke_from_local(id)
        return jsonify(joke)
    elif id in cache.deleted_remote_ids:
        abort(404, "This joke has already be deleted by user")
    else:
        return get_joke_from_remote(id)


@app.route("/api/joke/<id>", methods=["DELETE"])
def delete_joke(id):
    if id in cache.deleted_remote_ids:
        abort(404, "This joke has already be deleted by user")
    result = controller.delete_joke(id, cache)
    return jsonify(result)


if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', port=8000)


