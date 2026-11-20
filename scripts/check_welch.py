"""Compares one 5 s spectrum with Welch averaging over 6 pieces of a noisy 18.75 Hz sine.

Expected: same peak (18.8 Hz, about 0.96), noise floor about sqrt(6) = 2.4 times smoother.
Run from the project root: python scripts/check_welch.py
"""

import numpy as np

from carscanner.models.signal import Signal
from carscanner.sources.signalGenerator import SignalGenerator
from carscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from carscanner.analysis.welchAnalyzer import WelchAnalyzer
from carscanner.analysis.window import HanningWindow

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
    """Sine at F_TEST Hz plus white noise, duration seconds in total."""
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

# .std() er spredningen: hvor meget gulvet hopper op og ned i frekvenserne 
std_single = spectrum_single.amplitudes[band].std()
std_welch = spectrum_welch.amplitudes[band].std()


# ------------------------------------------------------------------
# 4. Resultat
# ------------------------------------------------------------------
print("---------------- Without Welch, one 5 s piece ----------------")
print("Peak:            ", spectrum_single.frequencies[m_single], "Hz")
print("Amplitude:       ", round(spectrum_single.amplitudes[m_single], 3))
print("Floor spread:    ", std_single)

print("---------------- With Welch, 6 pieces of 5 s -----------------")
print("Peak:            ", spectrum_welch.frequencies[m_welch], "Hz")
print("Amplitude:       ", round(spectrum_welch.amplitudes[m_welch], 3))
print("Floor spread:    ", std_welch)

print("---------------- Comparison ----------------------------------")
print("The floor is", round(std_single / std_welch, 2), "times smoother with Welch")
print("Expected about", round(np.sqrt(6), 2), "= sqrt(6)")