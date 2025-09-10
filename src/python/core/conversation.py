# modules/conversation.py

import requests
import json
from config import OLLAMA_API_BASE_URL, OLLAMA_MODEL_NAME, CONVERSATION_SYSTEM_PROMPT

class ConversationManager:
    def __init__(self):
        self.api_url = OLLAMA_API_BASE_URL
        self.model_name = OLLAMA_MODEL_NAME
        print(f"ConversationManager initialized with Ollama model: {self.model_name}")

    def get_response(self, user_command: str) -> str | None:
        # This is our original, non-streaming method. We'll keep it for now.
        # ... (code from before) ...
        pass # The previous code for this method is fine, no changes needed here.

    def get_response_stream(self, user_command: str):
        """
        Communicates with the Ollama LLM and yields response chunks as they arrive.
        This is a generator function.

        :param user_command: The transcribed text of the user's command.
        :yield: A string chunk of the AI's response.
        """
        full_prompt = CONVERSATION_SYSTEM_PROMPT.format(user_command=user_command)

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": True, # <-- IMPORTANT: This tells Ollama to stream the response
            "options": {
                "temperature": 0.7,
                "num_predict": 150,
            }
        }

        try:
            # The 'stream=True' argument in requests is crucial for handling streaming responses
            with requests.post(self.api_url, json=payload, stream=True) as response:
                response.raise_for_status()
                
                # Iterate over the response line by line as it comes in
                for line in response.iter_lines():
                    if line:
                        # Each line is a JSON object. We parse it to get the content.
                        chunk = json.loads(line)
                        content = chunk.get('response', '')
                        yield content # 'yield' turns this function into a generator

                        # The final chunk contains 'done: true'. We can stop then.
                        if chunk.get('done', False):
                            break
        
        except requests.exceptions.ConnectionError:
            yield "I'm having trouble connecting to my brain right now."
        except Exception as e:
            yield f"I seem to be experiencing a technical difficulty: {e}"