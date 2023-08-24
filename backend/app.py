import os
from flask import Flask, render_template, request, url_for, redirect, session

from utils.openai import generate_text, generate_text_v2
from game.config import get_characters, get_character, get_bot_prompt
from game.character import Character  # Import the Character class

# Create a Flask application
app = Flask(__name__)

# Replace 'your_secret_key_here' with a strong, random secret key
app.secret_key = 'd14cb1844d85e6d3fd8b0d583482c08519ee8ec40bf88cfb'

# Define the route for the home page with character selections
@app.route('/')
def index():
    characters = get_characters()
    return render_template('index.html', characters=characters)

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Initialize session variables if they don't exist
    if 'selected_character' not in session:
        session['selected_character'] = None
    if 'prompt' not in session:
        session['prompt'] = ""

    # Page is loaded for the first time
    if request.method == 'GET':
        character_id = request.args.get('character')

        if character_id is not None:
            character = get_character(character_id)
            session['selected_character'] = character.to_dict()  # Store Character as a dictionary in the session
            session['prompt'] = ""
            return render_template('game.html', character=character)
        else:
            return render_template('index.html')

    # Prompt is entered by the user
    if request.method == 'POST' and request.form.get('prompt') is not None:
        session['prompt'] = request.form.get('prompt')
        bot = get_bot_prompt(Character.from_dict(session['selected_character']))  # Convert session data back to Character object
        generated_text = generate_text_v2(bot, prompt=session['prompt'])
        return render_template('game.html', character=Character.from_dict(session['selected_character']), config=bot, prompt=session['prompt'], generated_text=generated_text)

    # Password is entered by the user
    elif request.method == 'POST' and request.form.get('password') is not None:
        guess = request.form.get('password')
        selected_character = Character.from_dict(session['selected_character'])  # Convert session data back to Character object

        if guess == selected_character.secret[str(selected_character.current_level)]:
            # Update the current level of the selected character
            selected_character.current_level += 1


            #Update the session data
            session['selected_character'] = selected_character.to_dict()

            if selected_character.current_level > selected_character.total_levels:
                session['prompt'] = ""
                # TODO: Handle winning the game

                return redirect(url_for('index', characters=selected_character))
            else:
                return render_template('game.html', character=selected_character, prompt=session['prompt'])
        # Password guessed incorrectly
        else:
            return render_template('game.html', character=selected_character, prompt=session['prompt'])

# Define the route for the statistics page
@app.route('/statistics')
def statistics():
    # You can render the statistics.html template or return any response you need.
    return render_template('statistics.html')

@app.route('/custom')
def custom():
    # You can render the statistics.html template or return any response you need.
    return render_template('custom.html')

# Entry point for the application
if __name__ == '__main__':
    # Retrieve the port from the $PORT environment variable or use 5000 as a default
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
