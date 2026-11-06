import numpy as np
from bilscanner.signalGenerator import SignalGenerator
from bilscanner.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.window import HanningWindow, RectangularWindow


generator = SignalGenerator()

signal = generator.sine(18.75, 1, 5, 48000)

analyzer = SpectrumAnalyzer(HanningWindow())

spectrum = analyzer.analyse(signal = signal)

m_peak = np.argmax(spectrum.amplitudes)   # nummeret m for den højeste streg

# Brug pladsen m til at slå op i begge lister
print("Frekvens ved toppen:  ", spectrum.frequencies[m_peak], "Hz")
print("Amplitude ved toppen: ", spectrum.amplitudes[m_peak])
print("f0:                   ", spectrum.f0, "Hz")
print("Antal værdier:        ", len(spectrum.frequencies))


