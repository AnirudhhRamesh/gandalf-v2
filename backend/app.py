import os
from decouple import config

from flask import Flask, redirect, render_template, request, url_for, session

from utils.openai import generate_text_v2
from utils.firebase import create_user, post_prompt, update_prompt_status

from game.config import Game


app = Flask(__name__)
app.secret_key = config('FLASK_SECRET_KEY')

@app.route('/')
def index():
    user_token = None
    if 'user_token' not in session:
        user_token = create_user()

        if user_token is not None:
            session['user_token'] = user_token

    game = Game()
    
    if 'game' in session:
        game = Game.deserialize(session['game'])
    
    # Store the game object in the session
    session['game'] = game.serialize()

    print(game.get_characters())
    
    return render_template('index.html', characters=game.get_characters())

@app.route('/game', methods=['GET', 'POST'])
def game():
    game = Game()
    
    if 'game' in session:
        game = Game.deserialize(session['game'])

    if request.method == 'GET':
        character = request.args.get('character')
        prompt = ""

        if character is not None:
            game.set_active_character(character)
            selected_character = game.get_active_character()

            # Store the game object in the session
            session['game'] = game.serialize()

            return render_template('game.html', character=selected_character)

        else:
            return render_template('index.html')

    if request.method == 'POST' and request.form.get('prompt') is not None:
        prompt = request.form.get('prompt')

        session["prompt"] = prompt
        session["prompt_id"] = post_prompt(prompt, session['user_token'])

        active_character = game.get_active_character()
        bot = game.get_bot_prompt(active_character.id)

        generated_text = generate_text_v2(bot, prompt=prompt)

        return render_template('game.html', character=active_character, config=bot, prompt=prompt, generated_text=generated_text)

    elif request.method == 'POST' and request.form.get('password') is not None:
        prompt=""
        if "prompt" in session:
            prompt = session["prompt"]

        prompt_id=None
        if "prompt_id" in session:
            prompt_id = session["prompt_id"]
            print(f"Prompt_ID restored from Session: {prompt_id}")

        guess = request.form.get('password')
        active_character = game.get_active_character()

        #Correct password guess
        if guess == active_character.secret[active_character.current_level]:
            print("You guessed the password correctly!!")
            update_prompt_status(prompt_id, True, session['user_token'])

            game.increment_character_level(active_character.id)
            
            # Store the game object in the session
            session['game'] = game.serialize()
            
            if active_character.current_level >= active_character.total_levels:
                game.reset_character_level(active_character.id)
                session['game'] = game.serialize()

                return redirect(url_for('index'))
            else:
                return render_template('game.html', character=active_character, prompt=prompt)

        #Incorrect password guess
        else:
            update_prompt_status(prompt_id, False, session['user_token'])
            return render_template('game.html', character=active_character, prompt=prompt)

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/custom')
def custom():
    return render_template('custom.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
