from flask import Flask, redirect, render_template, request, url_for
from utils.openai import generate_text, generate_text_v2
from game.config import get_characters, get_character, get_bot_prompt
import os  # Import the os module to access environment variables

# Create a Flask application
app = Flask(__name__)

current_level = 1

# Define the route for the home page with character selections
@app.route('/')
def index():
    characters = get_characters()
    return render_template('index.html', characters=characters)

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Retrieve the current level of the game. Starts at 0
    global selected_character, prompt

    # Page is loaded for the first time
    if request.method == 'GET':
        character = request.args.get('character')
        prompt=""

        if character is not None:
            selected_character = get_character(character)
            return render_template('game.html', character=selected_character)
        
        else:
            return render_template('index.html')

    # Prompt is entered by the user
    if request.method == 'POST' and request.form.get('prompt') != None:
        prompt = request.form.get('prompt')

        bot= get_bot_prompt(selected_character)

        generated_text = generate_text_v2(bot, prompt=prompt)

        return render_template('game.html', character=selected_character, config=bot, prompt=prompt, generated_text=generated_text)

    # Password is entered by the user
    elif request.method == 'POST' and request.form.get('password') != None:
        guess = request.form.get('password')

        if guess == selected_character.secret[selected_character.current_level]:
            #TODO: Make an alert that says "You guessed the password correctly!"
            print("You guessed the password correctly!!")
            selected_character.current_level += 1

            if selected_character.current_level > selected_character.total_levels:
                selected_character.current_level = 1
                prompt = ""
                #TODO: Make an alert that says "You won the game!"

                characters = get_character(selected_character.id).current_level = selected_character.total_levels + 1

                #Redirect to the index page
                return redirect(url_for('index', characters=characters))

            else:
                return render_template('game.html', character=selected_character, prompt=prompt)
        
        else:

            #Password is guessed incorrectly
            return render_template('game.html', character=selected_character, prompt=prompt)

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
