"""Første kig på en rigtig optagelse: tomgang ved ca. 750 omdr./min.

Forventet, hvis motoren kan høres:
    Tændingsfrekvensen f_t = 750/60 * 3/2 = 18,75 Hz og dens harmoniske
    37,5, 56,25, 75 Hz osv.

Forbehold:
    Den højeste top er ikke nødvendigvis motoren. Telefonens mikrofon
    hører dårligt under ca. 50-100 Hz, og andre kilder kan give toppe.
    Sammenlign derfor med støjoptagelsen, og brug et plot senere.

Kør fra roden:
    python scripts/check_recording.py
"""

import numpy as np

from bilscanner.loader import AudioLoader
from bilscanner.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.welchAnalyzer import WelchAnalyzer
from bilscanner.window import HanningWindow

# Indlæs optagelsen som et Signal: samples f(n) og f_s
loader = AudioLoader()
signal_750rpm = loader.load("data/02_tomgang_750rpm.ogg")

# En SpectrumAnalyzer, der bruger et Hanning-vindue mod lækage
analyzer = SpectrumAnalyzer(window=HanningWindow())

# Welch bruger analysatoren på stykker af 5 s og midler spektrene
welch = WelchAnalyzer(analyzer=analyzer, segment_duration=5)

# Fra tid til frekvens: 31 s giver 6 stykker, f0 = 0,2 Hz
spectrum_750rpm = welch.analyse(signal_750rpm)

# Første kig: den højeste top i hele spektret.
# argmax giver nummeret m for den højeste streg.
m_peak = np.argmax(spectrum_750rpm.amplitudes)

print("------------- Tomgang, Welch med 6 stykker på 5 s -------------")
print("Varighed:   ", round(signal_750rpm.duration(), 2), "s")
print("f0:         ", spectrum_750rpm.f0, "Hz")
print("Toppen:     ", spectrum_750rpm.frequencies[m_peak], "Hz")
print("Amplitude:  ", round(spectrum_750rpm.amplitudes[m_peak], 4))