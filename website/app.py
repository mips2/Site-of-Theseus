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

@app.route('/time-travel')
def time_travel():
    if 'username' not in session:
        return redirect(url_for('start_adventure'))
    
    username = session['username']
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    # Generate a random historical era for the user to explore
    eras = [
        "Prehistoric Age",
        "Ancient Egypt",
        "Medieval Europe",
        "Renaissance Italy",
        "Wild West",
        "Future World"
    ]
    era = random.choice(eras)
    
    return render_template('time_travel.html', username=username, era=era)

@app.route('/time-travel/complete', methods=['POST'])
def complete_time_travel():
    if 'username' not in session:
        return redirect(url_for('start_adventure'))
    
    username = session['username']
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    user_progress[username]['score'] += 15  # Bonus points for completing the time travel
    return redirect(url_for('adventure', username=username))

@app.route('/puzzle-room')
def puzzle_room():
    if 'username' not in session:
        return redirect(url_for('start_adventure'))
    
    username = session['username']
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    # Generate a random puzzle for the user to solve
    puzzles = [
        "Arrange the numbers 1-9 in a 3x3 grid so that each row, column, and diagonal sums to 15.",
        "Find the missing number in the sequence: 2, 5, 10, 17, __, 37.",
        "Unscramble the letters to form a meaningful word: R A I N B O W.",
        "Determine the next shape in the pattern: ○, △, □, ○, △, __."
    ]
    puzzle = random.choice(puzzles)
    
    return render_template('puzzle_room.html', username=username, puzzle=puzzle)

@app.route('/puzzle-room/complete', methods=['POST'])
def complete_puzzle_room():
    if 'username' not in session:
        return redirect(url_for('start_adventure'))
    
    username = session['username']
    if username not in user_progress:
        return redirect(url_for('start_adventure'))
    
    user_progress[username]['score'] += 20  # Bonus points for completing the puzzle room
    return redirect(url_for('adventure', username=username))

if __name__ == '__main__':
    app.run(debug=True)