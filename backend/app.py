from flask import Flask
from flask import Flask, redirect, render_template, request, url_for
from openai_utils import generate_text
from game import get_level_config

# Create a Flask application
app = Flask(__name__)

current_level = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    config = get_level_config(current_level)

    if request.method == 'POST':
        print("POST")

        prompt = request.form.get('prompt')
        print(f"Your prompt {prompt}")

        full_prompt = f"{config}. The following is the user's prompt: {prompt}."

        generated_text = generate_text(prompt=full_prompt)

        return render_template('index.html', lvl=current_level, generated_text=generated_text)
    
    print("GET")
    return render_template('index.html', lvl=current_level)

# Entry point for the application
if __name__ == '__main__':
    app.run(debug=True)