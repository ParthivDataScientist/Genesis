import numpy as np 
from faster_whisper import WhisperModel




class SpeechToText:
    def __init__(self, model_size = 'base.en'):
        self.model_size = model_size
        self.model = None

        try:
            print(f"Loading Whisper model '{self.model_size}'...")
            # This downloads the model on the first run.
            # 'device="cpu"' and 'compute_type="int8"' are for efficient CPU-based processing.
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")

    def transcribe(self , audio_data):

        if self.model is None:
            print("Whisper model not loaded. Cannot transcribe.")
            return None

        try:
            segments, _ = self.model.transcribe(audio_data, beam_size = 5)
            transcribed_text = "".join(segment.text for segment in segments).strip()
            return transcribed_text
        except Exception as e :
            print(f"Error during transcription: {e}")
            return None



