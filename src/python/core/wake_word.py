import numpy as np 
import pvporcupine
import struct
from config import *


class WakeWordDeteector:
    
    def __init__(self):
        try:
            self.porcupine = pvporcupine.create(
                access_key=PICOVOICE_ACCESS_KEY,
                keyword_paths=KEYWORD_PATHS
            )
            self.frame_length = self.porcupine.frame_length
            print("Wake Word Engine (Porcupine) initialized successfully.")
        except Exception as e:
            print(f"Error initializing Porcupine: {e}")
            self.porcupine = None


    def process(self, audio_chuck):
        if self.porcupine is None:
            return False
        
    
        try:
            pcm = audio_chuck.flatten()
            Keyword_index = self.porcupine.process(pcm)

            return Keyword_index >= 0
        except Exception as e :
            return False
        

    def delete(self):
        if self.porcupine is not None:
            self.porcupine.delete()
            print("Porcupine resources released.")
