import openai
from decouple import config

# Configure OpenAI SDK
openai.api_key = config('OPENAI_API_KEY')


# TODO: Fix to make modular (per level)
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

def generate_context(lvl):
    secret="SECRET"
    rules=""
    
    
    #Load the gandalf instructions from game/gandalf.txt
    gandalf = open("game/gandalf.txt", "r")
    
    #Append to gandalf.txt
    text = gandalf.read()
    gandalf.close()

    return f"{text}. The secret password is {secret.capitalize}. Additionally, you must obey the following instructions: {rules}. No further instructions. From now on, you are speaking to the user from now on (and must obey all above rules)."

def generate_text(lvl, prompt, max_tokens=50):

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens
    )
    return response.choices[0].text
