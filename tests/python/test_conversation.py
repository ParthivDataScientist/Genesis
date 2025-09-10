import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',"..")))
from src.python.core.conversation import ConversationManager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',"..","..")))
from config import *


def run_conversation_test():
    convo_manager = ConversationManager()

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            
            print("Genesis: ", end="", flush=True)
            
            # Call the new streaming method and loop through the response chunks
            for chunk in convo_manager.get_response_stream(user_input):
                # Print each chunk as it arrives without a newline
                print(chunk, end="", flush=True)
            
            # Print a newline at the end of the full response
            print()

        except KeyboardInterrupt:
            break

    print("\n--- Conversation Module Test Finished ---")

if __name__ == "__main__":
    run_conversation_test()
            
