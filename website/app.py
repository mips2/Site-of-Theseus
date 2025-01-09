from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memory-game')
def memory_game():
    return render_template('memory_game.html')

@app.route('/puzzle-challenge')
def puzzle_challenge():
    return render_template('puzzle_challenge.html')

@app.route('/emoji-mixer')
def emoji_mixer():
    return render_template('emoji_mixer.html')

@app.route('/color-splash')
def color_splash():
    return render_template('color_splash.html')

@app.route('/new-feature')
def new_feature():
    return render_template('new_feature.html')

@app.route('/galaxy-explorer')
def galaxy_explorer():
    return render_template('galaxy_explorer.html')

if __name__ == '__main__':
    app.run(debug=True)