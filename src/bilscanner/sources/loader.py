import soundfile as sf

from ..models.signal import Signal


class AudioLoader:

    def load(self, path: str) -> Signal:
        samples, fs = sf.read(path)
        return Signal(samples = samples, fs = fs)

    