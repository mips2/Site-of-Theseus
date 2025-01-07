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

@app.route("/greet/<name>")
def greet(name):
    return jsonify({
        "message": f"Hello, {name}! Welcome to our website.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/weather")
def weather():
    # Simulate a weather API response
    return jsonify({
        "location": "Global",
        "temperature": "22°C",
        "condition": "Sunny",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/quote")
def quote():
    # Add a daily inspirational quote feature
    quotes = [
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
        "Do what you can, with what you have, where you are. - Theodore Roosevelt",
        "The best way to predict the future is to invent it. - Alan Kay",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "It always seems impossible until it's done. - Nelson Mandela"
    ]
    import random
    selected_quote = random.choice(quotes)
    return jsonify({
        "quote": selected_quote,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    # Add a feedback feature to collect user feedback
    data = request.get_json()
    if not data or "feedback" not in data:
        return jsonify({"error": "Feedback is required"}), 400
    
    feedback_message = data["feedback"]
    # Here you could log the feedback or store it in a database
    return jsonify({
        "message": "Thank you for your feedback!",
        "feedback_received": feedback_message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/health")
def health_check():
    # Add a health check endpoint to monitor the application's health
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)