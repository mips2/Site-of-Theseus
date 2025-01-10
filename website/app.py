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

@app.route('/interactive-story')
def interactive_story():
    return render_template('interactive_story.html')

@app.route('/quantum-leap')
def quantum_leap():
    return render_template('quantum_leap.html')

@app.route('/mystery-island')
def mystery_island():
    return render_template('mystery_island.html')

@app.route('/neon-pong')
def neon_pong():
    return render_template('neon_pong.html')

@app.route('/cyberpunk-city')
def cyberpunk_city():
    return render_template('cyberpunk_city.html')

@app.route('/retro-arcade')
def retro_arcade():
    return render_template('retro_arcade.html')

@app.route('/hologram-chat')
def hologram_chat():
    return render_template('hologram_chat.html')

@app.route('/gravity-simulator')
def gravity_simulator():
    return render_template('gravity_simulator.html')

@app.route('/neon-typer')
def neon_typer():
    return render_template('neon_typer.html')

@app.route('/maze-runner')
def maze_runner():
    return render_template('maze_runner.html')

@app.route('/soundscape-creator')
def soundscape_creator():
    return render_template('soundscape_creator.html')

@app.route('/space-invaders')
def space_invaders():
    return render_template('space_invaders.html')

@app.route('/alien-language-decoder')
def alien_language_decoder():
    return render_template('alien_language_decoder.html')

@app.route('/crystal-cavern')
def crystal_cavern():
    return render_template('crystal_cavern.html')

@app.route('/neon-dodge')
def neon_dodge():
    return render_template('neon_dodge.html')

@app.route('/quantum-paint')
def quantum_paint():
    return render_template('quantum_paint.html')

@app.route('/laser-maze')
def laser_maze():
    return render_template('laser_maze.html')

@app.route('/time-capsule')
def time_capsule():
    return render_template('time_capsule.html')

@app.route('/neon-typer-2')
def neon_typer_2():
    return render_template('neon_typer_2.html')

@app.route('/neon-typer-3')
def neon_typer_3():
    return render_template('neon_typer_3.html')

@app.route('/neon-typer-4')
def neon_typer_4():
    return render_template('neon_typer_4.html')

@app.route('/neon-typer-5')
def neon_typer_5():
    return render_template('neon_typer_5.html')

@app.route('/neon-typer-6')
def neon_typer_6():
    return render_template('neon_typer_6.html')

@app.route('/star-forger')
def star_forger():
    return render_template('star_forger.html')

@app.route('/neon-typer-7')
def neon_typer_7():
    return render_template('neon_typer_7.html')

@app.route('/neon-typer-8')
def neon_typer_8():
    return render_template('neon_typer_8.html')

if __name__ == '__main__':
    app.run(debug=True)