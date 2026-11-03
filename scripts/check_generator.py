"""Tjekker SignalGenerator.sine med motorens forventede tændingsfrekvens.

Kør fra roden af projektet:
    python scripts/check_generator.py

Facit: 240 000 samples, 48 000 Hz, 5,0 s og max-værdi 1,0.
"""

from bilscanner.signalGenerator import SignalGenerator

generator = SignalGenerator()

# 18,75 Hz er tændingsfrekvensen for en trecylindret motor i tomgang
# ved 750 omdr./min.: f_t = 750/60 * 3/2
signal = generator.sine(18.75, 1, 5, 48000)

print("Antal samples N:    ", len(signal.samples))
print("Samplefrekvens f_s: ", signal.fs, "Hz")
print("Varighed T:         ", signal.duration(), "s")
print("Max-værdi:          ", signal.samples.max())

