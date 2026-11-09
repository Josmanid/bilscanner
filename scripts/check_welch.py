"""Test af Welch-midling.

Spørgsmålet:
    Gør Welch-midling støjgulvet jævnere, uden at ændre motorens toppe?

Opsætning:
    En sinus på 18,75 Hz med amplituden 1 (det deterministiske, det vi
    vil finde) plus hvid støj med spredningen 0,5 (det tilfældige).

To analyser med samme f0 = 0,2 Hz og samme vindue:
    Uden Welch: ét stykke på 5 s
    Med Welch:  30 s delt i 6 stykker á 5 s, midlet til ét spektrum
    Den eneste forskel er midlingen, så vi måler effekten af den alene.

Forventet:
    Toppen ved 18,8 Hz med ca. 0,96 i begge.
    Støjgulvet ca. 2,4 gange jævnere med Welch, fordi takkerne falder
    med 1/sqrt(K) = 1/sqrt(6).

Kør fra roden:
    python scripts/check_welch.py
"""

import numpy as np

from bilscanner.signal import Signal
from bilscanner.signalGenerator import SignalGenerator
from bilscanner.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.welchAnalyzer import WelchAnalyzer
from bilscanner.window import HanningWindow

FS = 48000          # samplefrekvens i Hz, samme som optagelserne
F_TEST = 18.75      # tændingsfrekvens: 750/60 * 3/2
SEGMENT = 5         # længden af ét Welch-stykke i sekunder

generator = SignalGenerator()


# ------------------------------------------------------------------
# 1. Testsignaler: sinus plus støj
# ------------------------------------------------------------------
# Samme seed giver samme støj. De første 5 s af den lange støj er
# derfor identiske med den korte, så de to analyser får samme data
# i det første stykke.

def noisy_sine(duration: float) -> Signal:
    """Sinus på F_TEST Hz plus hvid støj, i alt duration sekunder."""
    sine = generator.sine(frequency=F_TEST, amplitude=1, duration=duration, fs=FS)
    noise = generator.white_noise(std=0.5, duration=duration, fs=FS, seed=0)
    # Læg de to signaler sammen sample for sample
    return Signal(samples=sine.samples + noise.samples, fs=FS)

signal_short = noisy_sine(SEGMENT)   # 5 s, til analysen uden Welch
signal_long = noisy_sine(30)         # 30 s, til Welch


# ------------------------------------------------------------------
# 2. De to analyser
# ------------------------------------------------------------------
analyzer = SpectrumAnalyzer(HanningWindow())
welch = WelchAnalyzer(analyzer=analyzer, segment_duration=SEGMENT)

spectrum_single = analyzer.analyse(signal_short)   # ét spektrum
spectrum_welch = welch.analyse(signal_long)        # 6 spektre midlet


# ------------------------------------------------------------------
# 3. Målinger
# ------------------------------------------------------------------
# Toppen: argmax giver nummeret m for den højeste streg i hele spektret
m_single = np.argmax(spectrum_single.amplitudes)
m_welch = np.argmax(spectrum_welch.amplitudes)

# Støjgulvet: et boolsk filter, et array af sand og falsk, der vælger
# stregerne mellem 100 og 200 Hz, hvor der kun er støj. Begge spektre
# har f0 = 0,2 Hz, så det samme filter passer til begge.
band = (spectrum_welch.frequencies >= 100) & (spectrum_welch.frequencies <= 200)

# .std() er spredningen: hvor meget gulvet hopper op og ned
std_single = spectrum_single.amplitudes[band].std()
std_welch = spectrum_welch.amplitudes[band].std()


# ------------------------------------------------------------------
# 4. Resultat
# ------------------------------------------------------------------
print("---------------- Uden Welch, ét stykke på 5 s ----------------")
print("Toppen:             ", spectrum_single.frequencies[m_single], "Hz")
print("Amplitude:          ", round(spectrum_single.amplitudes[m_single], 3))
print("Spredning i gulvet: ", std_single)

print("---------------- Med Welch, 6 stykker på 5 s -----------------")
print("Toppen:             ", spectrum_welch.frequencies[m_welch], "Hz")
print("Amplitude:          ", round(spectrum_welch.amplitudes[m_welch], 3))
print("Spredning i gulvet: ", std_welch)

print("---------------- Sammenligning -------------------------------")
print("Gulvet er", round(std_single / std_welch, 2), "gange jævnere med Welch")
print("Forventet ca.", round(np.sqrt(6), 2), "= sqrt(6)")