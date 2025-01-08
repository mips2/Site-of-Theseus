from flask import Flask, jsonify, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("website/static/feedback.txt", "a") as f:
            f.write(f"{timestamp} - {name}: {message}\n")
        return redirect(url_for("thank_you"))
    return render_template("feedback.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/view-feedback")
def view_feedback():
    try:
        with open("website/static/feedback.txt", "r") as f:
            feedback_entries = f.readlines()
    except FileNotFoundError:
        feedback_entries = []
    return render_template("view_feedback.html", feedback_entries=feedback_entries)

@app.route("/search-feedback", methods=["GET", "POST"])
def search_feedback():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        try:
            with open("website/static/feedback.txt", "r") as f:
                feedback_entries = f.readlines()
            filtered_entries = [entry for entry in feedback_entries if search_term.lower() in entry.lower()]
        except FileNotFoundError:
            filtered_entries = []
        return render_template("search_feedback.html", feedback_entries=filtered_entries, search_term=search_term)
    return render_template("search_feedback.html")

@app.route("/delete-feedback", methods=["POST"])
def delete_feedback():
    if request.method == "POST":
        entry_to_delete = request.form.get("entry_to_delete")
        try:
            with open("website/static/feedback.txt", "r") as f:
                feedback_entries = f.readlines()
            with open("website/static/feedback.txt", "w") as f:
                for entry in feedback_entries:
                    if entry.strip() != entry_to_delete.strip():
                        f.write(entry)
        except FileNotFoundError:
            pass
        return redirect(url_for("view_feedback"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)