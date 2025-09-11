import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from src.python.core.text_to_speech import TextToSpeech

def run_tts_test():
    print("--- Starting Text-to-Speech Test ---")
    tts = TextToSpeech()

    if tts.engine is None:
        print("TSS engine failed to initialize. Aborting test")
        return
    
    print("\n[INFO] Testing a simple sentence...")
    test_sentence_1 = "Hello, world. This is Genesis speaking."
    print(f"Genesis should say: '{test_sentence_1}'")
    tts.speak(test_sentence_1)
    
    print("\n[INFO] Testing a second sentence to ensure it works multiple times...")
    test_sentence_2 = "Text-to-Speech module test successful."
    print(f"Genesis should say: '{test_sentence_2}'")
    tts.speak(test_sentence_2)

    print("\n--- Text-to-Speech Test Finished ---")

if __name__ == "__main__":
    run_tts_test()
    
