from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Global variable to store user's streak
user_streak = 0

@app.route('/')
def home():
    # Initialize session for daily streak tracking
    if 'last_played' not in session:
        session['last_played'] = datetime.now().strftime('%Y-%m-%d')
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
        
        # Update last played date and check for daily streak bonus
        last_played = datetime.strptime(session['last_played'], '%Y-%m-%d')
        today = datetime.now()
        if today.date() > last_played.date():
            if (today - last_played).days == 1:  # Played consecutively
                user_streak += 1  # Bonus streak point for daily play
            session['last_played'] = today.strftime('%Y-%m-%d')
        
        return render_template('game_result.html', user_choice=user_choice, computer_choice=computer_choice, result=result, streak=user_streak)
    
    return render_template('start_game.html')

@app.route('/streak_rewards')
def streak_rewards():
    rewards = {
        3: "Unlock a secret emoji! 🎉",
        5: "Get a special badge! 🏅",
        10: "Exclusive access to a new game mode! 🚀"
    }
    return render_template('streak_rewards.html', rewards=rewards, streak=user_streak)

@app.route('/secret_game_mode')
def secret_game_mode():
    if user_streak >= 10:
        return render_template('secret_game_mode.html')
    else:
        return redirect(url_for('streak_rewards'))

@app.route('/emoji_roulette')
def emoji_roulette():
    if user_streak >= 3:
        emojis = ["🎉", "🎲", "🍀", "🌟", "💎", "🔥", "🌈", "🍕", "🚀", "🎁"]
        selected_emoji = random.choice(emojis)
        return render_template('emoji_roulette.html', selected_emoji=selected_emoji)
    else:
        return redirect(url_for('streak_rewards'))

if __name__ == '__main__':
    app.run(debug=True)