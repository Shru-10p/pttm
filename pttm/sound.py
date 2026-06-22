import math
import os
import struct
import subprocess
import threading
import wave

from pttm.config import CONFIG_FILE

_CONFIG_DIR = os.path.dirname(os.path.abspath(CONFIG_FILE))
DING_WAV_PATH = os.path.join(_CONFIG_DIR, "ding.wav")

def _write_ding_wav(
    path: str,
    freq: float = 880.0,
    duration: float = 0.6,
    sample_rate: int = 44100,
    volume: float = 0.45,
) -> None:
    """Synthesise a bell-like ding and write it to *path*."""
    n_samples = int(sample_rate * duration)

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)          # 16-bit
        wf.setframerate(sample_rate)

        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate

            # Exponential decay envelope (quick attack, smooth tail-off)
            envelope = math.exp(-5.0 * t / duration)

            # Two harmonics for a warmer, bell-like timbre
            sample = (
                math.sin(2 * math.pi * freq * t)                    # fundamental
                + 0.35 * math.sin(2 * math.pi * freq * 2 * t)      # octave
            )
            value = int(sample * envelope * volume * 32767)
            value = max(-32768, min(32767, value))
            frames += struct.pack("<h", value)

        wf.writeframes(bytes(frames))


def _ensure_ding_wav() -> None:
    """Generate ding.wav if it doesn't already exist on disk."""
    if not os.path.exists(DING_WAV_PATH):
        _write_ding_wav(DING_WAV_PATH)


# Generate once on import (fast — only runs if the file is missing).
_ensure_ding_wav()


def play_ding() -> None:
    """Play the cached ding.wav in a background daemon thread (non-blocking)."""
    threading.Thread(target=_play, daemon=True).start()


def _play() -> None:
    """Internal: hand the WAV file path to aplay."""
    try:
        subprocess.run(
            ["aplay", "--quiet", DING_WAV_PATH],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass # Ignore any errors (e.g., aplay not installed, no audio device, etc.)
