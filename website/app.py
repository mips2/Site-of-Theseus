from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/maze')
def maze():
    return render_template('maze.html')

@app.route('/generate_maze', methods=['POST'])
def generate_maze():
    size = int(request.json['size'])
    maze = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]
    maze[0][0] = 0  # Start point
    maze[-1][-1] = 0  # End point
    return jsonify(maze)

if __name__ == '__main__':
    app.run(debug=True)