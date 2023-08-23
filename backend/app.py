from flask import Flask
from flask import Flask, redirect, render_template, request, url_for

from utils.openai import generate_text, generate_text_v2

from game.config import get_level_config

# Create a Flask application
app = Flask(__name__)

current_level = 2

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_level

    config = get_level_config(current_level)

    if request.method == 'POST' and request.form.get('prompt') != None:
        print("POST")

        prompt = request.form.get('prompt')

        # generated_text = generate_text(prompt=full_prompt)
        generated_text = generate_text_v2(config[0], prompt=prompt)

        return render_template('index.html', lvl=current_level, config=config[0], prompt=prompt, generated_text=generated_text)
    
    elif request.method == 'POST' and request.form.get('password') != None:
        guess = request.form.get('password')

        if guess==config[1]:
            current_level += 1
            print("You guess the password correctly!!")
            return redirect(url_for('index'), prompt=prompt)

    print("GET")
    return render_template('index.html', lvl=current_level)

# Define the route for the statistics page
@app.route('/statistics')
def statistics():
    # You can render the statistics.html template or return any response you need.
    return render_template('statistics.html')

# Entry point for the application
if __name__ == '__main__':
    app.run(debug=True)