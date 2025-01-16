from flask import Flask, render_template
import requests

app = Flask(__name__)

def fetch_weather(city="London"):
    """Fetch weather data for a given city using OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

@app.route('/')
def home():
    weather_data = fetch_weather()
    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)


###