import requests
import json
from decouple import config
from datetime import datetime

import uuid

# Initialize Firebase configuration from .env
database_url = config('FIREBASE_DATABASE_URL')
api_key = config('FIREBASE_API_KEY')

def create_user():
    """
    Generate an anonymous user.
    """
    # Step 1: Create an anonymous user via Firebase REST API
    auth_url = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}'
    auth_data = {
        'returnSecureToken': True
    }
    response = requests.post(auth_url, data=json.dumps(auth_data))
    auth_result = response.json()

    # Check if the user was created successfully and get the user's ID token
    if 'idToken' in auth_result:
        id_token = auth_result['idToken']

        # Return the ID token as the user identifier
        return id_token
    else:
        print("Error creating anonymous user:", auth_result)
        return None

def post_prompt(prompt, id_token):
    """
    Posts the prompt to the Firebase database with a unique identifier and 'None' status initially.
    """
    # Generate a unique identifier for the prompt (e.g., using UUID)
    prompt_id = str(uuid.uuid4())

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Data to be pushed with 'None' status and a unique identifier
    data = {
        "prompt_id": prompt_id,
        "prompt": prompt,
        "status": None,  # Initially set to 'None'
        "timestamp": timestamp
    }

    # Include the ID token as an 'auth' parameter
    auth_payload = {
        "auth": id_token
    }

    # Push data to the "prompts" node in Firebase using the ID token for authentication
    response = requests.put(f'{database_url}/prompts/{prompt_id}.json', params=auth_payload, data=json.dumps(data))

    if response.status_code == 200:
        print("Prompt pushed successfully with 'None' status, prompt_id: ", prompt_id)
        return prompt_id
    else:
        print("Error pushing prompt:", response.status_code)
        return None

def update_prompt_status(prompt_id, is_success, id_token):
    """
    Updates the status of a specific prompt in the Firebase database using its unique identifier.
    """
    if prompt_id is not None:
        
        # Get the current timestamp
        timestamp = datetime.now().isoformat()

        # Determine the status based on whether it's a correct or incorrect password guess
        status = "successful" if is_success else "unsuccessful"

        # Data to update the prompt's status
        data = {
            "status": status,
            "timestamp": timestamp
        }

        # Include the ID token as an 'auth' parameter
        auth_payload = {
            "auth": id_token
        }

        # Update the specific prompt's status in the "prompts" node in Firebase using its unique identifier
        response = requests.patch(f'{database_url}/prompts/{prompt_id}.json', params=auth_payload, data=json.dumps(data))

        if response.status_code == 200:
            print(f"Prompt '{prompt_id}' status updated to '{status}' successfully.")
        else:
            print("Error updating prompt status:", response.status_code)

    else:
        print("Error updating prompt status: prompt_id is None")
