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

@app.route('/galaxy-explorer')
def galaxy_explorer():
    return render_template('galaxy_explorer.html')

@app.route('/emoji-story')
def emoji_story():
    return render_template('emoji_story.html')

@app.route('/ai-art-generator')
def ai_art_generator():
    return render_template('ai_art_generator.html')

if __name__ == '__main__':
    app.run(debug=True)