"""Loads an audio file from disk as a Signal."""
import soundfile as sf

from ..models.signal import Signal


class AudioLoader:
    """Reads the samples f(n) and the sample rate f_s from the file.
    Assumes a mono recording. A stereo file gives two columns of samples.
    """
    def load(self, path: str) -> Signal:
        samples, fs = sf.read(path)
        return Signal(samples = samples, fs = fs)

    