"""Tjekker vinduerne på en kendt sinus.

Kør fra roden:
    python scripts/check_window.py

Facit:
    Hanning:     første og sidste sample er 0, max tæt på 1
    Rektangulær: samme værdier som den oprindelige sinus
"""

from bilscanner.signalGenerator import SignalGenerator
from bilscanner.window import HanningWindow, RectangularWindow


generator = SignalGenerator()
signal = generator.sine(18.75, 1, 5, 48000)

hanning = HanningWindow().apply_to(signal)
rectangular = RectangularWindow().apply_to(signal)

print("--- Hanning ---")
print("Første sample:", hanning.samples[0])
print("Sidste sample:", hanning.samples[-1])
print("Max-værdi:    ", hanning.samples.max())

print("--- Rektangulær ---")
print("Første sample:", rectangular.samples[0])
print("Sidste sample:", rectangular.samples[-1])
print("Max-værdi:    ", rectangular.samples.max())