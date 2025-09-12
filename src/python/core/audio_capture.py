import sounddevice as sd
import numpy as np
import queue
import sys
import os 
import threading


class AudioCapture:
    """
    A class to handle capturing audio from the mic in a seprate thread and putting it into a thread-safe queue
    """
    def __init__(self,frame_length=None):
        self.audio_queue = queue.Queue()
        self.stream = None
        self.running = False
        self.frame_length=frame_length
    
    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio Stram status:{status}")
        # Add the new audio data (as a NumPy array) to the queue
        self.audio_queue.put(indata.copy())

    def start_stream(self):
        """ Starts the audio stream if it's not already running """
        if self.running:
            print("Audio Stream is already running.")
            return
        
        block_size_to_use = self.frame_length
        if block_size_to_use is None:
            print()
            block_size_to_use = 1024
        
        print("Starting audio stream...")
        self.running = True
        self.stream = sd.InputStream(
            samplerate=16000,    
            blocksize=block_size_to_use,     
            device=None,                     # Default Microphone 
            channels=1,                      # Mono or Sterio
            dtype='int16',                   # 16-bit integer (range: –32768 to 32767)
            callback=self._audio_callback    # Add this to queue
        )
        self.stream.start()
        print("Audio Stream Start and is now capturing.")

    def stop_stream(self):
        """Stop the audio stream if its running """
        if not self.running:
            print("Audio is not running ")
            return
        
        print("Stopping the audio stream...")
        self.stream.stop()
        self.stream.close()
        self.running = False
        print('Audio stream stopped.')

    def get_audio_chunk(self):
        return self.audio_queue.get(block=True)
        



