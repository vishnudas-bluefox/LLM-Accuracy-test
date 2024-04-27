import json
import re
import os

from aiohttp import ClientSession

from icecream import ic
from dotenv import load_dotenv

load_dotenv()  


class LLMAnalyzer:
    
    async def create_api(self,content):
        endpoint = 'https://api.together.xyz/v1/chat/completions'
        async with ClientSession() as session:

            async with session.post(endpoint, json={
                "model": "meta-llama/Llama-3-70b-chat-hf",
                "max_tokens": 400,
                "temperature": 0.01,
                "top_p": 0.99,
                "top_k": 5,
                "repetition_penalty": 1,
                "stop": [
                    "<step>"
                ],
                "messages": [
                    {
                        "content": content,
                        "role": "user"
                    }
                ]
            }, headers={
                "Authorization": os.getenv("TOKEN"),
            }) as response:
                return await response.text()
    def clean_response_data(self,response_text):
    # Extracting the JSON string from response text
        response_text = response_text.replace('\\n', '')

        # Convert the string to a Python dictionary
        response_dict = json.loads(response_text)

        choices = response_dict['choices']

        # Access the first (and only) element of the 'choices' list, which is a dictionary
        choice_dict = choices[0]

        # Access the 'message' key, which is a dictionary
        message_dict = choice_dict['message']

        # Access the 'content' key, which is a string
        content = message_dict['content']

        if content:
            equivalent_match_true = re.search(r'"equivalent": true}', content)
            equivalent_match_true2 = re.search(r"'equivalent': true}", content)
            equivalent_match_false = re.search(r'"equivalent": false}', content)
            equivalent_match_false2 = re.search(r"'equivalent': false}", content)
            
            if equivalent_match_true or equivalent_match_true2:
                return True
            elif equivalent_match_false or equivalent_match_false2:
                return False
            else:
                ic("'equivalent' key not found in the JSON string.")
        else:
            ic("JSON string not found in the input string.")


        # Load the JSON string into a dictionary
        return content


