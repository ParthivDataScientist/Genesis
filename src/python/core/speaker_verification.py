import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path

class SpeakerVerification:
    def __init__(self, voiceprint_path, threshold=0.8):
        self.voiceprint_path = Path(voiceprint_path)
        self.encoder = None
        self.threshold = threshold
        self.master_voiceprint = None
        self._load_model_and_voiceprint()

    def _load_model_and_voiceprint(self):
        try:
            print("Leading Spaker verficiation model")
            self.encoder = VoiceEncoder()
            print("Model loaded sucessfully")
        except Exception as e:
            print(f"Error loading voice encoder: {e}")
            raise
        
        if not self.voiceprint_path.is_file():
            print(f"Error: Voiceprint file not found at '{self.voiceprint_path}'")
            print("Please run the enroll_voice.py script first.")
            raise FileNotFoundError(f"Voiceprint file not found: {self.voiceprint_path}")
        
        print(f"Loading master voiceprint from '{self.voiceprint_path}'...")
        self.master_voiceprint = np.load(self.voiceprint_path)
        print("Master voiceprint loaded.")

    def is_voice_recognized(self, audio_clip, sample_rate):
        if self.master_voiceprint is None or self.encoder is None:
            print("Verifier is not properly initialized.")
            return False
        
        try:
            processed_wav = preprocess_wav(audio_clip, source_sr=sample_rate)
            
            # Generate the embedding for the new clip
            test_embedding = self.encoder.embed_utterance(processed_wav)

            # Similarity score
            similarity = np.dot(self.master_voiceprint, test_embedding)

            print(f"Similarity Score: {similarity:.2f} (Threshold: {self.threshold})")

            return similarity > self.threshold
        
        except Exception as e:
            print(f"Error during voice recognition: {e}")
            return False