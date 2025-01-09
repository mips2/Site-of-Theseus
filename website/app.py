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

@app.route('/emoji-story')
def emoji_story():
    return render_template('emoji_story.html')

@app.route('/generate-story', methods=['POST'])
def generate_story():
    emojis = request.json.get('emojis', [])
    story = " ".join(emojis)
    return jsonify({'story': story})

@app.route('/mood-tracker')
def mood_tracker():
    return render_template('mood_tracker.html')

@app.route('/save-mood', methods=['POST'])
def save_mood():
    mood = request.json.get('mood')
    timestamp = request.json.get('timestamp')
    # Here you could save the mood and timestamp to a database
    return jsonify({'status': 'success', 'mood': mood, 'timestamp': timestamp})

@app.route('/color-mixer')
def color_mixer():
    return render_template('color_mixer.html')

@app.route('/mix-colors', methods=['POST'])
def mix_colors():
    color1 = request.json.get('color1')
    color2 = request.json.get('color2')
    # Simple color mixing logic (average RGB values)
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    mixed_color = f"#{((r1 + r2) // 2):02x}{((g1 + g2) // 2):02x}{((b1 + b2) // 2):02x}"
    return jsonify({'mixed_color': mixed_color})

@app.route('/time-capsule')
def time_capsule():
    return render_template('time_capsule.html')

@app.route('/save-capsule', methods=['POST'])
def save_capsule():
    message = request.json.get('message')
    open_date = request.json.get('open_date')
    # Here you could save the message and open_date to a database
    return jsonify({'status': 'success', 'message': message, 'open_date': open_date})

@app.route('/dream-interpreter')
def dream_interpreter():
    return render_template('dream_interpreter.html')

@app.route('/interpret-dream', methods=['POST'])
def interpret_dream():
    dream = request.json.get('dream')
    # Simple dream interpretation logic
    keywords = {
        'water': 'You are experiencing emotional turbulence.',
        'falling': 'You may be feeling a lack of control in your life.',
        'flying': 'You are feeling free and liberated.',
        'teeth': 'You might be worried about your appearance or health.',
        'chase': 'You are avoiding a problem or responsibility.'
    }
    interpretation = []
    for word, meaning in keywords.items():
        if word in dream.lower():
            interpretation.append(meaning)
    if not interpretation:
        interpretation.append("Your dream is unique and requires deeper introspection.")
    return jsonify({'interpretation': interpretation})

@app.route('/music-mood')
def music_mood():
    return render_template('music_mood.html')

@app.route('/get-music', methods=['POST'])
def get_music():
    mood = request.json.get('mood')
    # Simple music recommendation based on mood
    music = {
        'happy': ['Dancing Queen - ABBA', 'Uptown Funk - Mark Ronson ft. Bruno Mars', 'Happy - Pharrell Williams'],
        'sad': ['Someone Like You - Adele', 'Hurt - Johnny Cash', 'Fix You - Coldplay'],
        'energetic': ['Eye of the Tiger - Survivor', 'Lose Yourself - Eminem', 'Thunderstruck - AC/DC'],
        'relaxed': ['Weightless - Marconi Union', 'Clair de Lune - Claude Debussy', 'Strawberry Swing - Coldplay']
    }
    recommendations = music.get(mood, ['No recommendations available for this mood.'])
    return jsonify({'recommendations': recommendations})

@app.route('/virtual-pet')
def virtual_pet():
    return render_template('virtual_pet.html')

@app.route('/feed-pet', methods=['POST'])
def feed_pet():
    food = request.json.get('food')
    # Simple pet feeding logic
    responses = {
        'apple': 'Your pet loves apples! It looks happy.',
        'carrot': 'Your pet nibbles on the carrot. It seems content.',
        'meat': 'Your pet devours the meat. It looks very satisfied.',
        'fish': 'Your pet enjoys the fish. It purrs happily.'
    }
    response = responses.get(food, 'Your pet is not interested in that food.')
    return jsonify({'response': response})

@app.route('/space-explorer')
def space_explorer():
    return render_template('space_explorer.html')

@app.route('/get-planet-info', methods=['POST'])
def get_planet_info():
    planet = request.json.get('planet')
    planet_info = {
        'mercury': 'Mercury is the closest planet to the Sun and has extreme temperature variations.',
        'venus': 'Venus is the hottest planet in the solar system due to its thick atmosphere.',
        'earth': 'Earth is the only planet known to support life.',
        'mars': 'Mars is known as the Red Planet and has the largest volcano in the solar system.',
        'jupiter': 'Jupiter is the largest planet and has a giant storm called the Great Red Spot.',
        'saturn': 'Saturn is famous for its stunning ring system made of ice and rock.',
        'uranus': 'Uranus rotates on its side and has a pale blue color due to methane in its atmosphere.',
        'neptune': 'Neptune is the windiest planet with supersonic wind speeds.'
    }
    info = planet_info.get(planet.lower(), 'No information available for this planet.')
    return jsonify({'info': info})

if __name__ == '__main__':
    app.run(debug=True)