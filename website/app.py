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

@app.route('/music-mixer')
def music_mixer():
    return render_template('music_mixer.html')

@app.route('/ai-art-generator')
def ai_art_generator():
    return render_template('ai_art_generator.html')

@app.route('/virtual-pet')
def virtual_pet():
    return render_template('virtual_pet.html')

@app.route('/time-traveler')
def time_traveler():
    return render_template('time_traveler.html')

@app.route('/dreamscape-creator')
def dreamscape_creator():
    return render_template('dreamscape_creator.html')

@app.route('/cosmic-race')
def cosmic_race():
    return render_template('cosmic_race.html')

@app.route('/word-scramble')
def word_scramble():
    return render_template('word_scramble.html')

@app.route('/interactive-story')
def interactive_story():
    return render_template('interactive_story.html')

@app.route('/maze-runner')
def maze_runner():
    return render_template('maze_runner.html')

@app.route('/space-invaders')
def space_invaders():
    return render_template('space_invaders.html')

if __name__ == '__main__':
    app.run(debug=True)