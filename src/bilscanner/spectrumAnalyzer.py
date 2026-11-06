import numpy as np

from .window import Window
from .signal import Signal
from .spectrum import Spectrum



class SpectrumAnalyzer:
    # Pythons svar på konstruktor
    def __init__(self, window: Window):
        self.window = window

    def analyse(self, signal: Signal) -> Spectrum:
        # vi sætter et vindue på først for at undgå leakage
        windowed_signal = self.window.apply_to(signal=signal)
        # N skal bruges til frekvensaksen og til at skalere amplituderne
        N = len(windowed_signal.samples)
        # Benyt FFT da vi vil gå til frekvensdomænet 
        F = np.fft.rfft(windowed_signal.samples)
        # f0 er afstanden mellem stregerne i spektret, f0 = f_s/N = 1/T.
        # Frekvensen for streg nummer m er så f_m = m * f0.
        f0 = windowed_signal.fs/N
        frequencies = f0*np.arange(len(F))
        # så finder vi amplituderne det er bare pythagoras på dem alle set fra polær form
        amplitudes = np.abs(F)
        return Spectrum(frequencies = frequencies, amplitudes=amplitudes, f0 = f0)

       

    


