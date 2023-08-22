from flask import Flask
from decouple import config
import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = config('OPENAI_API_KEY')

# Create a Flask application
app = Flask(__name__)

# Define a route and a view function
@app.route('/')
def hello():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt("tiger"),
        temperature=0.6,
    )

    print(response.choices[0].text)
    return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)

    return f"Hello, World! This is your {(OPEN_AI_KEY)}"


# Define a route to give a prompt to the LLM and return the response
@app.route('/prompt')
def prompt():
    #Send the prompt to the LLM


    #Return the response from the LLM
    response = "This is the response from the LLM!"

    return response


@app.route("/random", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )


# Entry point for the application
if __name__ == '__main__':
    app.run(debug=True)