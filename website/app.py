from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# List of fun facts to display in the interactive trivia game
FUN_FACTS = [
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible!",
    "Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
    "Bananas are berries, but strawberries aren't.",
    "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
    "A day on Venus is longer than a year on Venus.",
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trivia')
def trivia():
    return render_template('trivia.html')

@app.route('/trivia/play', methods=['GET', 'POST'])
def trivia_play():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = request.form.get('correct_answer')
        if user_answer == correct_answer:
            result = "Correct! 🎉"
        else:
            result = f"Wrong! The correct answer was: {correct_answer}"
        return render_template('trivia_result.html', result=result)
    
    # Randomly select a fun fact and generate a question
    fact = random.choice(FUN_FACTS)
    question = f"True or False: {fact}"
    correct_answer = "True"  # All facts are true in this example
    return render_template('trivia_play.html', question=question, correct_answer=correct_answer)

if __name__ == '__main__':
    app.run(debug=True)