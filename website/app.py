from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# List of fun facts to display dynamically
FUN_FACTS = [
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible!",
    "Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
    "Bananas are berries, but strawberries aren't.",
    "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
    "A day on Venus is longer than a year on Venus."
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fun-fact')
def fun_fact():
    return jsonify({'fact': random.choice(FUN_FACTS)})

@app.route('/interactive-quiz')
def interactive_quiz():
    return render_template('quiz.html')

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    answers = request.json
    score = 0
    correct_answers = {
        'q1': 'Paris',
        'q2': 'Mars',
        'q3': 'Blue Whale'
    }
    for q, a in answers.items():
        if correct_answers.get(q) == a:
            score += 1
    return jsonify({'score': score, 'total': len(correct_answers)})

if __name__ == '__main__':
    app.run(debug=True)