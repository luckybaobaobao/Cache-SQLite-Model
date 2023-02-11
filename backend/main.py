from flask import Flask
from cache import Cache
from db import create_tables

cache = Cache()
app = Flask(__name__)

if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', port=8000)
