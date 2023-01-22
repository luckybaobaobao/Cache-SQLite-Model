from flask import Flask
from db import create_tables

app = Flask(__name__)

if __name__ == "__main__":
    create_tables()
    app.run(host='0.0.0.0', port=8000)
