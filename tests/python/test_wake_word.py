import numpy as np
import os 
import sys
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))


from src.python.core.audio_capture import AudioCapture
from src.python.core.wake_word import WakeWordDeteector
from config import SAMPLE_RATE, WAKE_WORD_NAME

def run_wake_word_test():
    print(f"--- Starting Wake Word Detection Test for '{WAKE_WORD_NAME}' ---")

    wake_word_detector = WakeWordDeteector()

    if wake_word_detector.porcupine is None:
        print("Error ; Wake Word Dectctor Failed to inintialize. Cannot run test.")
        return
    
    audio_capture = AudioCapture(frame_length = wake_word_detector.frame_length)
    audio_capture.start_stream()

    print(f"\n[INFO] Listening for wake word '{WAKE_WORD_NAME}'... Speak now!")
    print("[INFO] Press Ctrl+C to stop the test.")

    try:
        while True:
            audio_chunk = audio_capture.get_audio_chunk()

            wake_word_detected = wake_word_detector.process(audio_chuck=audio_chunk)

            if wake_word_detected:
                print(f"--- WAKE WORD '{WAKE_WORD_NAME}' DETECTED! ---")
    except KeyboardInterrupt:
        print("\nShutting down wake word test.")
    except Exception as e:
        print(f"An unexpected error occurred during test: {e}")
    finally:
        audio_capture.stop_stream()
        wake_word_detector.delete() 
        print("--- Wake Word Detection Test Finished ---")

if __name__ == "__main__":
    run_wake_word_test()





    
