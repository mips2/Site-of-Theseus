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

@app.route('/puzzle')
def puzzle():
    return render_template('puzzle.html')

@app.route('/generate_puzzle', methods=['POST'])
def generate_puzzle():
    difficulty = request.json['difficulty']
    if difficulty == 'easy':
        size = 3
    elif difficulty == 'medium':
        size = 4
    else:
        size = 5
    numbers = list(range(1, size * size))
    numbers.append(None)  # Empty tile
    random.shuffle(numbers)
    puzzle = [numbers[i:i + size] for i in range(0, len(numbers), size)]
    return jsonify(puzzle)

if __name__ == '__main__':
    app.run(debug=True)