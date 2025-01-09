from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Store user progress in a simple in-memory dictionary
user_progress = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-adventure', methods=['GET', 'POST'])
def start_adventure():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user_progress[username] = {'level': 1, 'score': 0}
            session['username'] = username  # Store username in session
            return redirect(url_for('adventure', username=username))
    return render_template('start_adventure.html')

@app.route('/adventure/')
def adventure(username):
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    level = user_progress[username]['level']
    score = user_progress[username]['score']
    
    # Generate a random challenge for the user
    challenges = [
        "Solve the riddle: I speak without a mouth and hear without ears. What am I?",
        "Find the hidden treasure in the maze!",
        "Defeat the dragon by choosing the right weapon!",
        "Decipher the ancient code to unlock the next level!"
    ]
    challenge = random.choice(challenges)
    
    return render_template('adventure.html', username=username, level=level, score=score, challenge=challenge)

@app.route('/adventure//complete', methods=['POST'])
def complete_challenge(username):
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    user_progress[username]['level'] += 1
    user_progress[username]['score'] += 10
    
    return redirect(url_for('adventure', username=username))

@app.route('/leaderboard')
def leaderboard():
    # Sort users by score in descending order
    sorted_users = sorted(user_progress.items(), key=lambda x: x[1]['score'], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_users)

@app.route('/mini-game')
def mini_game():
    if 'username' not in session:
        return redirect(url_for('start_adventure'))
    
    username = session['username']
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    return render_template('mini_game.html', username=username)

@app.route('/mini-game/complete', methods=['POST'])
def complete_mini_game():
    if 'username' not in session:
        return redirect(url_for('start_adventure'))
    
    username = session['username']
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    user_progress[username]['score'] += 5  # Bonus points for completing the mini-game
    return redirect(url_for('adventure', username=username))

if __name__ == '__main__':
    app.run(debug=True)