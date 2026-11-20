"""Runs a known 18.75 Hz sine through the spectrum analyzer with a Hanning window.

Expected: peak at 18.8 Hz, amplitude about 0.96 (between two lines), f0 = 0.2 Hz, 120 001 lines.
Run from the project root: python scripts/check_spectrum.py
"""
import numpy as np
from carscanner.sources.signalGenerator import SignalGenerator
from carscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from carscanner.analysis.window import HanningWindow, RectangularWindow


generator = SignalGenerator()

signal = generator.sine(18.75, 1, 5, 48000)

analyzer = SpectrumAnalyzer(HanningWindow())

spectrum = analyzer.analyse(signal = signal)

m_peak = np.argmax(spectrum.amplitudes)   # nummeret m for den højeste streg

# Brug pladsen m til at slå op i begge lister
print("Peak frequency:   ", spectrum.frequencies[m_peak], "Hz")
print("Peak amplitude:   ", spectrum.amplitudes[m_peak])
print("f0:               ", spectrum.f0, "Hz")
print("Number of lines:  ", len(spectrum.frequencies))


