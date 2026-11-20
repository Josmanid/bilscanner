"""Generates a 5 s sine at 18.75 Hz and checks its basic properties.

Expected: 240 000 samples, 48 000 Hz, 5.0 s and max value 1.0 (N = T * f_s).
Run from the project root: python scripts/check_generator.py
"""

from carscanner.sources.signalGenerator import SignalGenerator

generator = SignalGenerator()

# 18,75 Hz er tændingsfrekvensen for en trecylindret motor i tomgang
# ved 750 omdr./min.: f_t = 750/60 * 3/2
signal = generator.sine(18.75, 1, 5, 48000)

print("Antal samples N:    ", len(signal.samples))
print("Samplefrekvens f_s: ", signal.fs, "Hz")
print("Varighed T:         ", signal.duration(), "s")
print("Max-værdi:          ", signal.samples.max())

