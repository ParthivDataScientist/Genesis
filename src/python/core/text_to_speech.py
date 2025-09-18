import torch 
import threading
import sounddevice as sd
import soundfile as sf 
import os 
import time 
from TTS.api import TTS

MODEL_NAME = "C:\\Users\\parth\\OneDrive\\Documents\\Genesis\\models\\tts\\en_US-amy-medium.onnx"
OUTPUT_WAV_PATH ='temp_speech.wav'


class TextToSpeech:
    def __init__(self,rate = 180, volumne = 1.0):
        try:
<<<<<<< HEAD
            print("Initializing Coqui XTTSv2 engine.. This may take a moment.")
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"uning dvice {self.device}")

            self.tss = TTS(MODEL_NAME, gpu = (self.device == 'cuda'))
            self.lock = threading.Lock()
            print("✅ Coqui XTTSv2 engine initialized successfully.")
=======
            self.engine = pyttsx3.init()
            print("Text-to-Speech engine initialized successfully.")
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volumne)
>>>>>>> 5bba01104110a3814e04607be0676d9ed7a9cbfe
        except Exception as e:
            print(f"CRITICAL: Error initializing Coqui TTS engine: {e}")
            self.tts = None

    
    def _speck_thread(self, text:str):
        if self.tts is None:
            return
        
        with self.lock:
            try:
                # Synthesize speech and save to a temporary WAV file
                self.tts.tts_to_file(
                    text=text,
                    file_path=OUTPUT_WAV_PATH,
                    # You can use different speaker WAVs for voice cloning.
                    # This default is a standard male English voice.
                    speaker_wav="tts_models/en/vctk/p225.wav",
                    language="en"
                )

                data, sample_rate = sf.read(OUTPUT_WAV_PATH, dtype='float32')
                sd.play(data, sample_rate)
                sd.wait()
            except Exception as e:
                print(f"Error during Coqui TTS execution: {e}")
            finally:
                # Clean up the temporary file after playing
                if os.path.exists(OUTPUT_WAV_PATH):
                    time.sleep(0.1) # Brief pause to ensure file is not in use
                    os.remove(OUTPUT_WAV_PATH)

    def speak(self, text: str):
        """
        Speaks the given text in a non-blocking manner by starting a new thread.
        """
        if not self.tts:
            print("Cannot speak, TTS engine not initialized.")
            return

<<<<<<< HEAD
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            print("No valid text to speak.")
            return
=======
        try:
            # self.engine = pyttsx3.init()
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during TTS: {e}")


>>>>>>> 5bba01104110a3814e04607be0676d9ed7a9cbfe

        # Start the synthesis and playback in a background thread
        thread = threading.Thread(target=self._speak_thread, args=(text,))
        thread.daemon = True
        thread.start()
