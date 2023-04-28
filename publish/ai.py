import os
from pathlib import Path

import dotenv
import openai

if Path('config/.env').exists():
    dotenv.read_dotenv('config/.env')

    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")

def transform_prompt(text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo", 
        prompt=text, 
        temperature=0, 
        max_tokens=7)
    print(response['choices'][0]['text'])
