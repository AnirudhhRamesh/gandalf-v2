import os
from decouple import config
from flask import Flask, redirect, render_template, request, session, url_for
from utils.openai import generate_text
from utils.firebase import create_user, post_prompt, update_prompt_status
from game.gamestate import GameState

app = Flask(__name__)

# Set the secret key for the session
app.secret_key = config('FLASK_SECRET_KEY')

@app.route('/')
def index():
    # Check if the user has a session token, create one if not
    user_token = session.get('user_token')
    if user_token is None:
        user_token = create_user()
        if user_token is not None:
            session['user_token'] = user_token

    # Create or deserialize the game object
    game = GameState()
    if 'game' in session:
        game = GameState.deserialize(session['game'])

    # Store the game object in the session
    session['game'] = game.serialize()

    #Clear the session values
    session.pop('prompt', None)
    session.pop('prompt_id', None)
    session.pop('generated_text', None)

    # Get the characters for display
    characters = game.get_characters()

    return render_template('index.html', characters=characters)

@app.route('/game', methods=['GET', 'POST'])
def game():
    # Create or deserialize the game object
    game = GameState()
    if 'game' in session:
        game = GameState.deserialize(session['game'])

    if request.method == 'GET':
        character = request.args.get('character')

        if character is not None:
            # Set the active character
            game.set_active_character(character)
            selected_character = game.get_active_character()

            # Store the game object in the session
            session['game'] = game.serialize()

            return render_template('game.html', character=selected_character)
        else:
            return render_template('index.html')

    if request.method == 'POST' and request.form.get('prompt') is not None:
        prompt = request.form.get('prompt')

        # Store the prompt and its ID in the session
        session["prompt"] = prompt
        session["prompt_id"] = post_prompt(prompt, session['user_token'])

        active_character = game.get_active_character()
        bot = game.get_bot_prompt(active_character.id)

        generated_text = generate_text(bot, prompt=prompt)
        session["generated_text"] = generated_text

        return render_template('game.html', character=active_character, config=bot, prompt=prompt, generated_text=generated_text)

    elif request.method == 'POST' and request.form.get('password') is not None:
        # Retrieve prompt, prompt_id and generated_text from the session
        prompt = session.get("prompt", "")
        prompt_id = session.get("prompt_id")
        generated_text = session.get("generated_text", "")

        guess = request.form.get('password')
        active_character = game.get_active_character()

        # Correct password guess
        if guess == active_character.secret[active_character.current_level]:
            print("You guessed the password correctly!!")
            update_prompt_status(prompt_id, True, session['user_token'])

            game.increment_character_level(active_character.id)
            
            # Store the game object in the session
            session['game'] = game.serialize()
            
            if active_character.current_level >= active_character.total_levels:
                game.reset_character_level(active_character.id)
                session['game'] = game.serialize()

                #Clear the session values
                session.pop('prompt', None)
                session.pop('prompt_id', None)
                session.pop('generated_text', None)

                return redirect(url_for('index'))
            else:
                generated_text = "You got the secret correct! 😱"
                session["generated_text"] = generated_text

                return render_template('game.html', character=active_character, prompt=prompt, generated_text=generated_text)

        # Incorrect password guess
        else:
            print("Your guess was incorrect :/")
            update_prompt_status(prompt_id, False, session['user_token'])
            
            generated_text = "That's the wrong secret, try again! 😋"
            session["generated_text"] = generated_text

            return render_template('game.html', character=active_character, prompt=prompt, generated_text=generated_text)

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/custom')
def custom():
    return render_template('custom.html')

if __name__ == '__main__':
    # Retrieve the port from the environment variable or use 5000 as the default
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
