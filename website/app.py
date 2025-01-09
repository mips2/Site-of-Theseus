from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/space')
def space():
    return render_template('space.html')

@app.route('/ocean')
def ocean():
    return render_template('ocean.html')

@app.route('/forest')
def forest():
    return render_template('forest.html')

@app.route('/interactive-galaxy')
def interactive_galaxy():
    return render_template('interactive_galaxy.html')

if __name__ == '__main__':
    app.run(debug=True)