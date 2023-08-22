from flask import Flask
from flask import Flask, redirect, render_template, request, url_for
from openai_utils import generate_text

# Create a Flask application
app = Flask(__name__)

current_level = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        print(f"Your prompt {prompt}")
        generated_text = generate_text(lvl=current_level, prompt=prompt)
        return render_template('index.html', generated_text=generated_text)
    
    print("GET")
    return render_template('index.html')

# Entry point for the application
if __name__ == '__main__':
    app.run(debug=True)