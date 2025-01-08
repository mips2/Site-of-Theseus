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

@app.route("/mood-music")
def mood_music():
    return render_template("mood_music.html")

@app.route("/generate-playlist", methods=["POST"])
def generate_playlist():
    mood = request.form.get("mood")
    playlists = {
        "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
        "sad": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
        "angry": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
        "calm": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
        "excited": "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd"
    }
    playlist_url = playlists.get(mood, "https://open.spotify.com/")
    return jsonify({"playlist_url": playlist_url})

@app.route("/mood-quiz")
def mood_quiz():
    return render_template("mood_quiz.html")

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    answers = request.form.getlist("answer")
    mood_score = sum(int(answer) for answer in answers)
    if mood_score <= 5:
        mood = "sad"
    elif mood_score <= 10:
        mood = "calm"
    elif mood_score <= 15:
        mood = "happy"
    else:
        mood = "excited"
    return jsonify({"mood": mood})

@app.route("/mood-maze")
def mood_maze():
    return render_template("mood_maze.html")

@app.route("/maze-complete", methods=["POST"])
def maze_complete():
    time_taken = request.form.get("time_taken")
    flash(f"Congratulations! You completed the maze in {time_taken} seconds!", "success")
    return redirect(url_for("mood_maze"))

@app.route("/mood-pet")
def mood_pet():
    return render_template("mood_pet.html")

@app.route("/feed-pet", methods=["POST"])
def feed_pet():
    food = request.form.get("food")
    happiness_level = {
        "apple": 10,
        "carrot": 15,
        "cake": 20,
        "broccoli": 5
    }.get(food, 0)
    return jsonify({"happiness_level": happiness_level})

@app.route("/mood-stories")
def mood_stories():
    return render_template("mood_stories.html")

@app.route("/generate-story", methods=["POST"])
def generate_story():
    mood = request.form.get("mood")
    stories = {
        "happy": "Once upon a time, in a land filled with sunshine and laughter, a group of friends embarked on an adventure to find the legendary treasure of joy.",
        "sad": "In a quiet village, a young artist painted their sorrows away, creating masterpieces that spoke of loss and longing, yet held a glimmer of hope.",
        "angry": "A fierce warrior, fueled by rage, sought to right the wrongs of the world, battling injustice with every ounce of strength.",
        "calm": "Under the serene moonlight, a lone traveler found peace in the gentle whispers of the forest, where time seemed to stand still.",
        "excited": "The carnival was alive with energy, as children and adults alike reveled in the thrill of the rides, the music, and the endless possibilities of the night."
    }
    story = stories.get(mood, "Once upon a time, in a world full of emotions, a story began to unfold.")
    return jsonify({"story": story})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)