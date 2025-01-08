from flask import Flask, jsonify, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory storage for user feedback
feedback_data = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback_data.append({"name": name, "message": message, "timestamp": timestamp})
        return redirect(url_for("view_feedback"))
    return render_template("feedback.html")

@app.route("/view_feedback")
def view_feedback():
    return render_template("view_feedback.html", feedback=feedback_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


