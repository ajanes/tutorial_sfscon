import random, time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hi!"

@app.route("/users")
def get_users():
    time.sleep(random.uniform(0.25, 0.75))
    return jsonify(["Alice", "Bob", "Charlie"])

if __name__ == "__main__":
    app.run(debug=True)
