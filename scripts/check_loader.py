"""Loads a recording and checks that samples, sample rate and duration agree.

Expected for the varying recording: 5 113 920 samples, 48 000 Hz, 106.54 s (T = N / f_s).
Run from the project root: python scripts/check_loader.py
"""

from carscanner.sources.loader import AudioLoader

loader = AudioLoader() # laver et nyt objekt på heapen ligesom C#

# indlæs filen
signal = loader.load("data/04_varying_1000_2000rpm.ogg")

# len() tæller elementerne i arrayet, altså N, antallet af samples
print("Antal samples N: ", len(signal.samples))
print("Samplefrekvens f_s: ", signal.fs)

# duration() regner T = N / f_s (formel 7.2)
print("Varighed T:", signal.duration(), "s")

