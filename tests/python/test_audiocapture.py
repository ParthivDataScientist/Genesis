import sys
import os 
import time 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))

from src.python.core.audio_capture import AudioCapture

def run_test():
    # 1. Initialize the audio capture module
    audio_capture = AudioCapture()


    # 2. start capturing audio
    audio_capture.start_stream()

    print("\n[INFO] Capturing audio for 5 seconds. You should see chunk shapes printed below.")

    start_time = time.time()
    chunks_processes = 0

    while time.time() - start_time < 5.0:
        try:
            audio_chunk = audio_capture.get_audio_chunk()
            chunks_processes += 1 

            if chunks_processes % 10 == 0 : 
                print(f" -> recevied chunk {chunks_processes}: shape={audio_chunk.shape}, dtypr = {audio_chunk.dtype}")

        except Exception as e :
            print("An error occured: {e}")
            break
    
      # 5. Stop the audio stream
    audio_capture.stop_stream()

    print(f"\n[INFO] Processed a total of {chunks_processes} audio chunks in 5 seconds.")
    print("--- Audio Capture Test Finished ---")

if __name__ == "__main__":
    run_test()

