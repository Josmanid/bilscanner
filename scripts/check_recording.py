"""Compares the idle spectrum with the background noise recording.

Peaks found in both come from the surroundings, peaks only at idle come from the car.
Run from the project root: python scripts/check_recording.py
"""

import numpy as np
import matplotlib.pyplot as plt

from carscanner.sources.loader import AudioLoader
from carscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from carscanner.analysis.welchAnalyzer import WelchAnalyzer
from carscanner.analysis.window import HanningWindow

# Indlæs optagelsen som et Signal: samples f(n) og f_s
loader = AudioLoader()
signal_900rpm = loader.load("data/02_idle_900rpm.ogg")
signal_noise = loader.load("data/01_noise.ogg")
# En SpectrumAnalyzer, der bruger et Hanning-vindue mod lækage
analyzer = SpectrumAnalyzer(window=HanningWindow())

# Welch bruger analysatoren på stykker af 5 s og midler spektrene
welch = WelchAnalyzer(analyzer=analyzer, segment_duration=5)

# Fra tid til frekvens: 31 s giver 6 stykker, f0 = 0,2 Hz
spectrum_900rpm = welch.analyse(signal_900rpm)
spectrum_noise = welch.analyse(signal_noise)

# Første kig: den højeste top i hele spektret.
# argmax giver nummeret m for den højeste streg.
m_peak = np.argmax(spectrum_900rpm.amplitudes)

print("------------- Idle, Welch with 6 segments of 5 s -------------")
print("Duration:   ", round(signal_900rpm.duration(), 2), "s")
print("f0:         ", spectrum_900rpm.f0, "Hz")
print("Peak:       ", spectrum_900rpm.frequencies[m_peak], "Hz")
print("Amplitude:  ", round(spectrum_900rpm.amplitudes[m_peak], 4))

print("------------- plots -------------")
plt.plot(spectrum_900rpm.frequencies, spectrum_900rpm.amplitudes, label="Idle 900 rpm")
plt.plot(spectrum_noise.frequencies, spectrum_noise.amplitudes, label="Background noise")
plt.xlim(0, 500)  # kun de lave frekvenser, hvor motorens ordener ligger
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()