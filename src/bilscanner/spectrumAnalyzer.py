import numpy as np
from .window import Window
from .signal import Signal
from .spectrum import Spectrum

class SpectrumAnalyzer:
    def __init__(self, window: Window):
        self.window = window

    def analyse(self, signal: Signal) -> Spectrum:
        # Sæt vindue på for at undgå spectral leakage
        windowed_signal = self.window.apply_to(signal=signal)
        
        N = len(windowed_signal.samples)
        
        # Find gennemsnittet af vinduets koefficienter (w_mean) for at kompensere for dæmpningen
        ones = Signal(samples=np.ones(N), fs=windowed_signal.fs)
        w_mean = np.mean(self.window.apply_to(ones).samples)
        
        # Transformér til frekvensdomænet. rfft returnerer komplekse tal, 
        # men kun for den positive halvdel af frekvensaksen (one-sided spectrum).
        F = np.fft.rfft(windowed_signal.samples)
        
        # Beregn frekvensakse
        f0 = windowed_signal.fs / N
        frequencies = f0 * np.arange(len(F))
        
        # Find de rå amplituder via den absolutte værdi (Pythagoras på de komplekse tal)
        raw_amplitudes = np.abs(F)
        
        # 2 fordi rfft kun viser den positive halvdel.
        # / N fordi summen i formel 7.5 vokser med optagelsens længde. Svarer til c_m = F(m)/N fra Jørgens slide 2.
        # / w̄ fordi vinduet dæmper. Findes ved at lægge vinduet på 1-taller.
        # Stakit-effekten: 0,96 i stedet for 1, fordi 18,75 Hz ligger mellem to streger.
        amplitudes = (2.0 * raw_amplitudes) / (N * w_mean)
        
        # DC-komponenten (0 Hz) skal ikke ganges med 2
        amplitudes[0] = amplitudes[0] / 2.0  
        
        # Hvis N er et lige tal, skal Nyquist-frekvensen (f_s / 2) heller ikke ganges med 2
        if N % 2 == 0:
            amplitudes[-1] = amplitudes[-1] / 2.0

        return Spectrum(frequencies=frequencies, amplitudes=amplitudes, f0=f0)

    


