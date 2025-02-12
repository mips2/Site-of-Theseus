from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Static user data for initial development
users = {
    'user1': {'username': 'user1', 'password': generate_password_hash('password1')},
    'user2': {'username': 'user2', 'password': generate_password_hash('password2')}
}

# Static post data for initial development
posts = [
    {'id': 1, 'username': 'user1', 'content': 'Hello, this is my first post!', 'likes': 0},
    {'id': 2, 'username': 'user2', 'content': 'Just joined this platform!', 'likes': 0}
]

# Static follow data for initial development
follows = {
    'user1': ['user2'],
    'user2': []
}

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('home'))

@app.route('/profile/')
@login_required
def profile(username):
    if username in users:
        user_posts = [post for post in posts if post['username'] == username]
        followers = [user for user, following in follows.items() if username in following]
        following = follows.get(username, [])
        return render_template('profile.html', username=username, posts=user_posts, followers=followers, following=following)
    flash('User not found')
    return redirect(url_for('home'))

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    content = request.form['content']
    if content:
        new_post = {'id': len(posts) + 1, 'username': current_user.id, 'content': content, 'likes': 0}
        posts.append(new_post)
        flash('Post created successfully!')
    else:
        flash('Post content cannot be empty')
    return redirect(url_for('home'))

@app.route('/like/', methods=['POST'])
@login_required
def like_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        post['likes'] += 1
        flash('Post liked!')
    else:
        flash('Post not found')
    return redirect(url_for('home'))

@app.route('/follow/', methods=['POST'])
@login_required
def follow_user(username):
    if username in users and username != current_user.id:
        if username not in follows[current_user.id]:
            follows[current_user.id].append(username)
            flash(f'You are now following {username}!')
        else:
            flash(f'You are already following {username}')
    else:
        flash('User not found or cannot follow yourself')
    return redirect(url_for('profile', username=username))

@app.route('/unfollow/', methods=['POST'])
@login_required
def unfollow_user(username):
    if username in users and username != current_user.id:
        if username in follows[current_user.id]:
            follows[current_user.id].remove(username)
            flash(f'You have unfollowed {username}!')
        else:
            flash(f'You are not following {username}')
    else:
        flash('User not found or cannot unfollow yourself')
    return redirect(url_for('profile', username=username))

if __name__ == '__main__':
    app.run(debug=True)