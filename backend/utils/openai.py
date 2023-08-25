import openai
from decouple import config

# Configure OpenAI SDK
openai.api_key = config('OPENAI_API_KEY')

def generate_text(bot, prompt, max_tokens=50):
    """
    Generate text in a conversation format using OpenAI's Chat Completion API.

    Args:
        bot (str): The role of the bot in the conversation.
        prompt (str): The user's input prompt.
        max_tokens (int, optional): The maximum number of tokens in the generated text.

    Returns:
        str: The generated text.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{bot}"},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    return response['choices'][0]['message']['content']
