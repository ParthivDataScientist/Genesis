import sys
import os
import sounddevice as sd
import numpy as np
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',"..")))

from src.python.core.audio_capture import AudioCapture
from src.python.core.wake_word import WakeWordDeteector
from src.python.core.SpeachToText import SpeechToText
from config import SAMPLE_RATE

def run_stt_test():

    stt = SpeechToText(model_size="base.en")
    if stt.model is None:
        print("STT model failed to initialize. Aborting test.")
        return
    
    duration = 5  # seconds
    print(f"\n[INFO] Please speak a command. Recording for {duration} seconds...")
    
    # sd.rec is a simple way to record a fixed duration
    recorded_audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()

    print("Recording complete, Now transcribing...")

    transcribed_text = stt.transcribe(recorded_audio.flatten())

    # 4. Print the result
    if transcribed_text:
        print(f"\n[RESULT] Transcribed Text: '{transcribed_text}'")
    else:
        print("\n[RESULT] Transcription failed or produced no text.")
        
    print("--- Speech-to-Text Test Finished ---")

if __name__ == "__main__":
    run_stt_test()



