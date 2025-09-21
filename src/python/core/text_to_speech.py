import numpy as np
import sounddevice as sd
import threading
from typing import Any

def _chunk_to_numpy(chunk: Any, target_channels: int = 1) -> np.ndarray:
    """
    Try many ways to convert `chunk` (whatever Piper yields) into a numpy int16 array
    with shape (frames, target_channels).
    Raises TypeError with diagnostics if conversion fails.
    """
    arr = None  # Ensure arr is always defined
    # 1) If already a numpy array
    if isinstance(chunk, np.ndarray):
        arr = chunk
    else:
        # 2) bytes-like -> frombuffer
        if isinstance(chunk, (bytes, bytearray, memoryview)):
            arr = np.frombuffer(bytes(chunk), dtype=np.int16)
        else:
            # 3) Try common attribute names that might hold bytes/arrays
            for attr in ("audio", "samples", "pcm", "data", "buffer", "raw", "frames"):
                if hasattr(chunk, attr):
                    val = getattr(chunk, attr)
                    if callable(val):
                        try:
                            val = val()
                        except Exception:
                            pass
                    # recurse to process the val
                    return _chunk_to_numpy(val, target_channels)

            # 4) Try .tobytes() / .to_bytes() / .numpy()
            if hasattr(chunk, "tobytes"):
                try:
                    b = chunk.tobytes()
                    arr = np.frombuffer(b, dtype=np.int16)
                except Exception:
                    pass
            elif hasattr(chunk, "to_bytes"):
                try:
                    b = chunk.to_bytes()
                    arr = np.frombuffer(b, dtype=np.int16)
                except Exception:
                    pass
            elif hasattr(chunk, "numpy"):
                try:
                    maybe = chunk.numpy()
                    return _chunk_to_numpy(maybe, target_channels)
                except Exception:
                    pass
            else:
                # 5) Try memoryview (buffer protocol)
                try:
                    mv = memoryview(chunk)
                except Exception:
                    mv = None

                if mv is not None:
                    try:
                        arr = np.frombuffer(mv, dtype=np.int16)
                    except Exception:
                        # try converting memoryview to bytes
                        try:
                            arr = np.frombuffer(bytes(mv), dtype=np.int16)
                        except Exception:
                            arr = None
                else:
                    arr = None

    # After attempts, ensure we have a numpy array
    if not isinstance(arr, np.ndarray):
        raise TypeError(
            f"Cannot convert AudioChunk of type {type(chunk)} into numpy array.\n"
            f"Available attributes: {dir(chunk)}"
        )

    # If arr is float type (common if audio in [-1,1]), convert to int16
    if np.issubdtype(arr.dtype, np.floating):
        # assume float in -1..1 -> convert
        arr = (arr * 32767.0).round().astype(np.int16)
    elif arr.dtype != np.int16:
        # convert other integer types to int16
        arr = arr.astype(np.int16)

    # Normalize shape: make it (frames, channels)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)  # mono
    elif arr.ndim == 2:
        # keep as is, but ensure columns match target_channels
        if arr.shape[1] != target_channels:
            if target_channels == 1:
                # drop/choose first channel
                arr = arr[:, 0].reshape(-1, 1)
            else:
                # expand/truncate to target channels
                if arr.shape[1] < target_channels:
                    # pad with zeros
                    pad = np.zeros((arr.shape[0], target_channels - arr.shape[1]), dtype=np.int16)
                    arr = np.concatenate([arr, pad], axis=1)
                else:
                    arr = arr[:, :target_channels]

    return arr


def _speak_thread(self, text: str, debug: bool = False):
    if self.voice is None:
        return

    with self.lock:
        try:
            with sd.OutputStream(
                samplerate=self.voice.config.sample_rate,
                channels=1,
                dtype="int16"
            ) as stream:
                for chunk in self.voice.synthesize(text):
                    try:
                        arr = _chunk_to_numpy(chunk, target_channels=1)  # returns (frames,1)
                        # sounddevice accepts (frames, channels). If you prefer 1D for mono:
                        # arr_to_write = arr[:, 0]  # but keeping 2D is safe
                        stream.write(arr)
                    except Exception as conv_err:
                        # helpful diagnostic for unknown chunk types
                        print("DEBUG: Failed converting chunk ->", conv_err)
                        print("DEBUG: chunk type:", type(chunk))
                        try:
                            # show small preview of dir to help debugging
                            print("DEBUG: chunk dir:", dir(chunk)[:40])
                        except Exception:
                            pass
                        # continue to next chunk (don't crash whole synth)
                        continue
        except Exception as e:
            print(f"Error during Piper TTS execution: {e}")
