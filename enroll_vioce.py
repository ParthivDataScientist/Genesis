# enroll_voice.py (Revised for explicit device selection)

import sounddevice as sd
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import time

# --- Configuration ---
SAMPLE_RATE = 16000
RECORDING_SECS = 5
NUM_SAMPLES = 4
OUTPUT_FILENAME = "genesis_voiceprint.npy"

def select_input_device():
    """
    Lists available input devices and prompts the user to select one.
    """
    print("Searching for available microphones...")
    devices = sd.query_devices()
    input_devices = [d for d in devices if d['max_input_channels'] > 0]
    
    if not input_devices:
        return None # No devices found

    if len(input_devices) == 1:
        print(f"Automatically selected the only available microphone: {input_devices[0]['name']}")
        return input_devices[0]['index']

    print("\n--- Please select your microphone ---")
    for i, device in enumerate(input_devices):
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

def record_audio(duration, sample_rate, device_id): # <-- MODIFIED: Added device_id
    """Records audio from a specific microphone for a given duration."""
    print("Recording...")
    # --- MODIFIED: Added device=device_id ---
    audio_data = sd.rec(
        int(duration * sample_rate), 
        samplerate=sample_rate, 
        channels=1, 
        dtype='float32',
        device=device_id  # Explicitly use the selected device
    )
    sd.wait()
    print("Recording finished.")
    return audio_data.flatten()

def main():
    """
    Main function to guide the user through the voice enrollment process.
    """
    # --- MODIFIED: Select device at the start ---
    device_id = select_input_device()
    if device_id is None:
        print("\n--- ERROR ---")
        print("No audio input devices (microphones) found or selected.")
        print("Please ensure your microphone is connected and enabled.")
        return
    
    print("\n--- Genesis Voice Enrollment ---")
    print(f"You will be asked to record {NUM_SAMPLES} sentences of {RECORDING_SECS} seconds each.")
    print("Please speak clearly in a quiet environment.")
    print("Speak a different sentence for each recording to create a robust voiceprint.\n")

    try:
        encoder = VoiceEncoder()
        print("Voice encoder loaded successfully.")
    except Exception as e:
        print(f"Error loading voice encoder: {e}")
        return

    embeddings = []
    for i in range(NUM_SAMPLES):
        input(f"Press Enter to start recording sample {i + 1}/{NUM_SAMPLES}...")
        
        for j in range(3, 0, -1):
            print(f"{j}...", end="", flush=True)
            time.sleep(1)
        print("GO!")

        # --- MODIFIED: Pass device_id to the function ---
        recorded_audio = record_audio(RECORDING_SECS, SAMPLE_RATE, device_id)

        processed_wav = preprocess_wav(recorded_audio, source_sr=SAMPLE_RATE)
        embedding = encoder.embed_utterance(processed_wav)
        embeddings.append(embedding)
        print(f"Sample {i + 1} processed and embedding created.\n")

    if not embeddings:
        print("No embeddings were created. Aborting.")
        return

    print("Calculating the master voiceprint...")
    master_voiceprint = np.mean(embeddings, axis=0)

    np.save(OUTPUT_FILENAME, master_voiceprint)
    print("--- Enrollment Complete! ---")
    print(f"Your master voiceprint has been saved to '{OUTPUT_FILENAME}'.")

if __name__ == "__main__":
    main()