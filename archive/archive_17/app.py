from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_bcrypt import Bcrypt
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

# Static user data (for initial development)
USERS = {
    "user1": {
        "username": "user1",
        "password": bcrypt.generate_password_hash("password1").decode('utf-8'),
        "bio": "Hello, I'm user1!",
        "posts": []
    },
    "user2": {
        "username": "user2",
        "password": bcrypt.generate_password_hash("password2").decode('utf-8'),
        "bio": "Hi, I'm user2!",
        "posts": []
    }
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('profile', username=session['username']))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = USERS.get(username)
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('profile', username=username))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/profile/')
def profile(username):
    user = USERS.get(username)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('home'))
    return render_template('profile.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS:
            flash('Username already exists', 'error')
        else:
            USERS[username] = {
                "username": username,
                "password": bcrypt.generate_password_hash(password).decode('utf-8'),
                "bio": "",
                "posts": []
            }
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)


###