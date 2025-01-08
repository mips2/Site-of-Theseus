from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mood-tracker")
def mood_tracker():
    return render_template("mood_tracker.html")

@app.route("/save-mood", methods=["POST"])
def save_mood():
    mood = request.form.get("mood")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flash(f"Your mood ({mood}) has been recorded at {timestamp}!", "success")
    return redirect(url_for("mood_tracker"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)