from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Global variable to store user's streak
user_streak = 0

@app.route('/')
def home():
    return render_template('index.html', streak=user_streak)

@app.route('/start_game', methods=['GET', 'POST'])
def start_game():
    global user_streak
    if request.method == 'POST':
        user_choice = request.form.get('choice')
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)
        
        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            result = "You win!"
            user_streak += 1
        else:
            result = "You lose!"
            user_streak = 0
        
        return render_template('game_result.html', user_choice=user_choice, computer_choice=computer_choice, result=result, streak=user_streak)
    
    return render_template('start_game.html')

if __name__ == '__main__':
    app.run(debug=True)