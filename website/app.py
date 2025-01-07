# website/app.py

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the AI-updated website!"

@app.route("/status")
def status():
    return jsonify({"status": "ok", "message": "Server is running smoothly"})

@app.route("/timestamp")
def timestamp():
    now = datetime.now()
    return jsonify({
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "UTC"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)