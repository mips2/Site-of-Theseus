# website/app.py

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the AI-updated website!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
