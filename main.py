# main.py

import threading
import time
import numpy as np
import sys
import os

# Import all our custom modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from src.python.core.audio_capture import AudioCapture
from src.python.core.conversation import ConversationManager
from src.python.core.text_to_speech import TextToSpeech
from src.python.core.SpeachToText import SpeechToText
from src.python.core.wake_word import WakeWordDetector

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..','..')))
from config import SAMPLE_RATE

# --- Global State Management ---
# This dictionary will hold the state of the assistant
# 'listening' -> Waiting for wake word
# 'recording' -> Wake word detected, now recording a command
# 'processing' -> Transcribing and thinking of a response
app_state = {"status": "listening"} 

def main():
    """
    The main function that orchestrates the entire Genesis assistant.
    """
    print("Initializing Genesis...")

    # --- 1. Initialize All Modules ---
    wake_word_detector = WakeWordDetector()
    # Ensure the wake word engine is ready before proceeding
    if wake_word_detector.porcupine is None:
        print("CRITICAL: Wake Word engine failed to initialize. Exiting.")
        return
        
    audio_capture = AudioCapture(frame_length=wake_word_detector.frame_length)
    stt = SpeechToText(model_size="base.en")
    conversation_manager = ConversationManager()
    tts = TextToSpeech()
    
    # Start capturing audio in the background
    audio_capture.start_stream()
    print("\nGenesis is now listening for the wake word...")

    try:
        while True:
            # --- 2. Main Listening Loop ---
            audio_chunk = audio_capture.get_audio_chunk()
            
            if app_state["status"] == "listening":
                wake_word_detected = wake_word_detector.process(audio_chunk)
                
                if wake_word_detected:
                    print("--- WAKE WORD DETECTED ---")
                    app_state["status"] = "recording"
                    
                    # --- 3. Activation & Recording ---
                    tts.speak("Yes?") # Acknowledge wake word
                    
                    print("Recording command for 5 seconds...")
                    command_audio_frames = []
                    # Calculate how many chunks to record for 5 seconds
                    num_chunks_to_record = int(5 * SAMPLE_RATE / wake_word_detector.frame_length)
                    
                    for _ in range(num_chunks_to_record):
                        command_audio_frames.append(audio_capture.get_audio_chunk())
                    
                    # Combine the recorded chunks into a single audio clip
                    command_audio = np.concatenate(command_audio_frames, axis=0)
                    print("Recording complete.")
                    
                    app_state["status"] = "processing"

            elif app_state["status"] == "processing":
                print("Transcribing command...")
                # --- 4. Transcribe ---
                command_text = stt.transcribe(command_audio.flatten())
                print(f"You said: '{command_text}'")

                if command_text:
                    # --- 5. Think ---
                    print("Getting response from LLM...")
                    ai_response = conversation_manager.get_response(command_text)
                    print(f"Genesis says: '{ai_response}'")

                    # --- 6. Speak ---
                    tts.speak(ai_response)
                else:
                    print("Could not transcribe the command.")
                    tts.speak("I'm sorry, I didn't catch that.")
                
                # --- 7. Return to Listening ---
                print("\nReturning to listening for wake word...")
                app_state["status"] = "listening"

    except KeyboardInterrupt:
        print("\nShutting down Genesis.")
    finally:
        # --- 8. Cleanup ---
        audio_capture.stop_stream()
        wake_word_detector.delete()

if __name__ == "__main__":
    main()