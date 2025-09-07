import sounddevice as sd 
import numpy as np
import time
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
from src.python.core.audio_capture import AudioCapture
from src.python.core.wake_word import WakeWordDeteector
from src.python.core.speaker_verification import SpeakerVerification
from config import *



VOICEPRINT_PATH = r"C:\Users\parth\OneDrive\Documents\Genesis\genesis_voiceprint.npy"
SAMPLE_RATE = 16000
RECORDING_SECS = 5

def select_input_device():
    """
    Lists available input devices and prompts the user to select one.
    """
    print("searching for Mic.........")
    try:
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]

        if not input_devices:
            return None

        if len(input_devices) == 1:
            print(f"Automatically selected the only available microphone: {input_devices[0]['name']}")
            return input_devices[0]['index']

        print("\n--- Please select your microphone ---")
        for i , device in enumerate(input_devices):
            print(f"[{i}] {device['name']}")
        
        while True:
            try:
                choice = int(input("Enter the number of your microphone: "))
                if 0 <= choice < len(input_devices):
                    print(f"Selected: {input_devices[choice]['name']}\n")
                    return input_devices[choice]['index']
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred while selecting a device: {e}")
        return None

def main():


    try:
        verifier = SpeakerVerification(VOICEPRINT_PATH)

        device_id = select_input_device()

        if device_id is None:
            print("\n--- ERROR ---")
            print("No audio input devices (microphones) found or selected.")
            print("Please ensure your microphone is connected and enabled.")
            return

        print(f"\nPrepare to speak for {RECORDING_SECS} seconds to test verification.")
        input("Press Enter to start recording...")
        
        for j in range(3, 0, -1):
            print(f"{j}...", end="", flush=True)
            time.sleep(1)
        print("GO! Speak now.")
        
        recorded_audio = sd.rec(
            int(RECORDING_SECS * SAMPLE_RATE), 
            samplerate=SAMPLE_RATE, 
            channels=1,
            device=device_id
        )
        sd.wait()
        print("Recording finished. Verifying...")
        
        # 4. Run the verification
        is_recognized = verifier.is_voice_recognized(recorded_audio.flatten(), SAMPLE_RATE)
        
        # 5. Print the final result
        if is_recognized:
            print("\n✅ VOICE RECOGNIZED: Access Granted.")
        else:
            print("\n❌ VOICE NOT RECOGNIZED: Access Denied.")
            
    except FileNotFoundError:
        print(f"\nError: Could not find the voiceprint file at '{VOICEPRINT_PATH}'.")
        print("Please run 'enroll_voice.py' first to create your voiceprint.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
