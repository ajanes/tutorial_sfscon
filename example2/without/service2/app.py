from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    """Return a basic payload consumed by service1."""
    return jsonify(service="service2", message="Hello from service2")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
