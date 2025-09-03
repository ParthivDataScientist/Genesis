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
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stream = None
        self.running = False
    
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
        
        print("Starting audio stream...")
        self.running = True
        self.stream = sd.InputStream(
            samplerate=16000,
            device=None,
            channels=1,
            dtype='int16',
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
        



