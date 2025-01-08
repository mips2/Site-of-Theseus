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

@app.route("/mood-journal")
def mood_journal():
    return render_template("mood_journal.html")

@app.route("/submit-journal", methods=["POST"])
def submit_journal():
    entry = request.form.get("journal_entry")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flash(f"Your journal entry has been saved at {timestamp}!", "success")
    return redirect(url_for("mood_journal"))

@app.route("/mood-art")
def mood_art():
    return render_template("mood_art.html")

@app.route("/generate-art", methods=["POST"])
def generate_art():
    mood = request.form.get("mood")
    colors = {
        "happy": "#FFD700",
        "sad": "#1E90FF",
        "angry": "#FF4500",
        "calm": "#32CD32",
        "excited": "#FF69B4"
    }
    color = colors.get(mood, "#000000")
    return jsonify({"color": color})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)