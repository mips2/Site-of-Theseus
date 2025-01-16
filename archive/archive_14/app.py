from flask import Flask, render_template
import requests

app = Flask(__name__)

def fetch_random_quote():
    """Fetch a random quote from a public API."""
    try:
        response = requests.get("https://api.quotable.io/random")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return None

@app.route('/')
def home():
    quote_data = fetch_random_quote()
    quote = quote_data.get("content", "No quote available") if quote_data else "No quote available"
    author = quote_data.get("author", "Unknown") if quote_data else "Unknown"
    return render_template('index.html', quote=quote, author=author)

if __name__ == '__main__':
    app.run(debug=True)


###