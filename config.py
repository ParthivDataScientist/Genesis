# config.py

# --- Audio Stream Configuration ---
SAMPLE_RATE = 16000     # Samples per second. Standard for most speech recognition.
CHANNELS = 1            # Mono audio.
DEVICE_ID = None        # `None` uses the default microphone.
DTYPE = 'int16'         # Data type for the audio samples.