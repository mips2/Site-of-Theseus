# website/app.py

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory storage for feedback (for demonstration purposes)
feedback_storage = []

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

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        user_feedback = request.json.get("feedback")
        if user_feedback:
            feedback_storage.append({
                "feedback": user_feedback,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return jsonify({"status": "success", "message": "Feedback received!"})
        else:
            return jsonify({"status": "error", "message": "No feedback provided"}), 400
    else:
        return jsonify({"status": "info", "message": "Submit your feedback using POST with JSON data: {'feedback': 'your feedback here'}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)