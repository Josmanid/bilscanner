import numpy as np
from bilscanner.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.window import HanningWindow
from bilscanner.welchAnalyzer import WelchAnalyzer
from bilscanner.signalGenerator import SignalGenerator

generator = SignalGenerator()

# 18,75 Hz er tændingsfrekvensen for en trecylindret motor i tomgang
# ved 750 omdr./min.: f_t = 750/60 * 3/2
test_signal = generator.sine(18.75, 1, 30, 48000)
analyzer = SpectrumAnalyzer(HanningWindow())

welch = WelchAnalyzer(analyzer=analyzer,segment_duration=5)

spectrum = welch.analyse(test_signal)

m_peak = np.argmax(spectrum.amplitudes)   # nummeret m for den højeste streg

# Brug pladsen m til at slå op i begge lister
print("Frekvens ved toppen:  ", spectrum.frequencies[m_peak], "Hz")
print("Amplitude ved toppen: ", spectrum.amplitudes[m_peak])
print("f0:                   ", spectrum.f0, "Hz")
print("Antal værdier:        ", len(spectrum.frequencies))