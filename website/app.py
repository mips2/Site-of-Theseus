from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memory-game')
def memory_game():
    return render_template('memory_game.html')

@app.route('/puzzle-escape')
def puzzle_escape():
    return render_template('puzzle_escape.html')

@app.route('/color-mixer')
def color_mixer():
    return render_template('color_mixer.html')

if __name__ == '__main__':
    app.run(debug=True)