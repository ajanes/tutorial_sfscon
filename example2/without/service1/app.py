import os

import requests
from flask import Flask, jsonify

SERVICE2_URL = os.environ.get("SERVICE2_URL", "http://service2:5000/")

app = Flask(__name__)


@app.get("/")
def index():
    """Call service2 and wrap its response."""
    upstream = requests.get(SERVICE2_URL, timeout=5)
    upstream.raise_for_status()
    return jsonify(service="service1", upstream=upstream.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
