from flask import Flask
from decouple import config

SECRET_KEY = config('SECRET_KEY')
API_KEY = config('API_KEY')

# Create a Flask application
app = Flask(__name__)

# Define a route and a view function
@app.route('/')
def hello():
    return f"Hello, World! This is your {(SECRET_KEY)} and {(API_KEY)}"

# Entry point for the application
if __name__ == '__main__':
    app.run(debug=True)