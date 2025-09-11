import pyttsx3

class TextToSpeech:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            print("Text-to-Speech engine initialized successfully.")
        except Exception as e:
            print(f"Error initializing Text-to-Speech engine: {e}")
            self.engine = None
    
    def speak(self, text: str):
        if self.engine is None:
            print("TTS engine is not initialized, cannot speak.")
            return
        
        if not text:
            print("No text to speak.")
            return

        try:
            self.engine = pyttsx3.init()
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during TTS: {e}")



