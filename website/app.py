from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# In-memory storage for a simple game state
game_state = {
    "score": 0,
    "current_question": None,
    "questions": [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
        {"question": "What is the smallest prime number?", "answer": "2"},
        {"question": "What is the chemical symbol for gold?", "answer": "Au"},
        {"question": "What is the square root of 64?", "answer": "8"}
    ]
}

# Memory game state
memory_game_state = {
    "cards": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "flipped": [],
    "matched": []
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-quiz', methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'POST':
        game_state["score"] = 0
        game_state["current_question"] = random.choice(game_state["questions"])
        return redirect(url_for('quiz'))
    return render_template('start_quiz.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer.lower() == game_state["current_question"]["answer"].lower():
            game_state["score"] += 1
            message = "Correct! 🎉"
        else:
            message = f"Wrong! The correct answer was {game_state['current_question']['answer']}."
        game_state["current_question"] = random.choice(game_state["questions"])
        return render_template('quiz.html', question=game_state["current_question"], score=game_state["score"], message=message)
    return render_template('quiz.html', question=game_state["current_question"], score=game_state["score"])

@app.route('/end-quiz')
def end_quiz():
    final_score = game_state["score"]
    game_state["score"] = 0
    game_state["current_question"] = None
    return render_template('end_quiz.html', final_score=final_score)

@app.route('/memory-game')
def memory_game():
    memory_game_state["flipped"] = []
    memory_game_state["matched"] = []
    random.shuffle(memory_game_state["cards"])
    return render_template('memory_game.html', cards=memory_game_state["cards"])

@app.route('/flip-card/')
def flip_card(index):
    if index not in memory_game_state["flipped"] and index not in memory_game_state["matched"]:
        memory_game_state["flipped"].append(index)
        if len(memory_game_state["flipped"]) == 2:
            if memory_game_state["cards"][memory_game_state["flipped"][0]] == memory_game_state["cards"][memory_game_state["flipped"][1]]:
                memory_game_state["matched"].extend(memory_game_state["flipped"])
                memory_game_state["flipped"] = []
            else:
                memory_game_state["flipped"] = []
    return render_template('memory_game.html', cards=memory_game_state["cards"], flipped=memory_game_state["flipped"], matched=memory_game_state["matched"])

if __name__ == '__main__':
    app.run(debug=True)