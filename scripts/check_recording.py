"""Første kig på en rigtig optagelse: tomgang ved ca. 900 omdr./min.

Forventet, hvis motoren kan høres:
    Tændingsfrekvensen f_t = 900/60 * 3/2 = 22,5 Hz og dens harmoniske
    45, 67,5 Hz osv.

Forbehold:
    Den højeste top er ikke nødvendigvis motoren. Telefonens mikrofon
    hører dårligt under ca. 50-100 Hz, og andre kilder kan give toppe.
    Derfor sammenlignes med støjoptagelsen: toppe, der også findes
    der, kommer ikke fra motoren.

Kør fra roden:
    python scripts/check_recording.py
"""

import numpy as np
import matplotlib.pyplot as plt

from bilscanner.loader import AudioLoader
from bilscanner.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.welchAnalyzer import WelchAnalyzer
from bilscanner.window import HanningWindow

# Indlæs optagelsen som et Signal: samples f(n) og f_s
loader = AudioLoader()
signal_900rpm = loader.load("data/02_tomgang_900rpm.ogg")
signal_noise = loader.load("data/01_stoej.ogg")
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

print("------------- Tomgang, Welch med 6 stykker på 5 s -------------")
print("Varighed:   ", round(signal_900rpm.duration(), 2), "s")
print("f0:         ", spectrum_900rpm.f0, "Hz")
print("Toppen:     ", spectrum_900rpm.frequencies[m_peak], "Hz")
print("Amplitude:  ", round(spectrum_900rpm.amplitudes[m_peak], 4))

print("------------- plots-------------")
plt.plot(spectrum_900rpm.frequencies,spectrum_900rpm.amplitudes, label = "Tomgang 900 omdr./min.")
plt.plot(spectrum_noise.frequencies,spectrum_noise.amplitudes, label = "Støj uden motor")
plt.xlim(0,500) # kun de lave frekvenser, hvor motorens ordener ligger
plt.xlabel("frekvenser i Hz")
plt.ylabel("Amplitude")
plt.legend()
plt.show()