from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/puzzle-game')
def puzzle_game():
    return render_template('puzzle_game.html')

@app.route('/memory-game')
def memory_game():
    return render_template('memory_game.html')

@app.route('/emoji-story')
def emoji_story():
    return render_template('emoji_story.html')

@app.route('/color-mixer')
def color_mixer():
    return render_template('color_mixer.html')

if __name__ == '__main__':
    app.run(debug=True)