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

@app.route('/music-mixer')
def music_mixer():
    return render_template('music_mixer.html')

@app.route('/virtual-pet')
def virtual_pet():
    return render_template('virtual_pet.html')

@app.route('/time-traveler')
def time_traveler():
    return render_template('time_traveler.html')

@app.route('/dreamscape-builder')
def dreamscape_builder():
    return render_template('dreamscape_builder.html')

@app.route('/cosmic-race')
def cosmic_race():
    return render_template('cosmic_race.html')

@app.route('/word-weaver')
def word_weaver():
    return render_template('word_weaver.html')

if __name__ == '__main__':
    app.run(debug=True)