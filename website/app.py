from flask import Flask, jsonify, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)