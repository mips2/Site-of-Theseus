# website/app.py

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the AI-updated website!"

@app.route("/time")
def get_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"current_time": current_time})

@app.route("/weather")
def get_weather():
    weather_report = {
        "location": "San Francisco",
        "temperature": "72°F",
        "conditions": "Sunny"
    }
    return jsonify(weather_report)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)