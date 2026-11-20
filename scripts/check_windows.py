"""Applies the Hanning and rectangular windows to an 18.75 Hz sine with 93.75 periods in 5 s.

Expected: Hanning starts and ends at 0, rectangular ends near -1, the jump that causes leakage.
Run from the project root: python scripts/check_windows.py
"""

from carscanner.sources.signalGenerator import SignalGenerator
from carscanner.analysis.window import HanningWindow, RectangularWindow


generator = SignalGenerator()
signal = generator.sine(18.75, 1, 5, 48000)

hanning = HanningWindow().apply_to(signal)
rectangular = RectangularWindow().apply_to(signal)

# Forventet med Hanning:
#   første og sidste sample er 0, fordi vinduet ender i 0
#   max er lidt under 1, fordi sinussens toppe ikke ligger præcis
#   midt i vinduet, hvor det er 1
print("--- Hanning ---")
print("First sample:", hanning.samples[0])
print("Last sample: ", hanning.samples[-1])
print("Max value:   ", hanning.samples.max())

print("--- Rectangular ---")
print("First sample:", rectangular.samples[0])
print("Last sample: ", rectangular.samples[-1])
print("Max value:   ", rectangular.samples.max())