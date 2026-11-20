"""Plots the revved recording in time to find the stable part at about 2500 rpm.

Ramp-up ends at about 18 s and ramp-down starts at about 55 s, so 20 to 55 s is used (35 s).
Run from the project root: python scripts/inspect_2500rpm.py
"""

import numpy as np
import matplotlib.pyplot as plt

from carscanner.sources.loader import AudioLoader
from carscanner.models.signal import Signal

loader = AudioLoader()

signal_2500rpm = loader.load("data/03_revved_2500rpm.ogg")
samples = signal_2500rpm.samples
N = len(signal_2500rpm.samples)
fs = signal_2500rpm.fs
xAxis = np.arange(N) / fs  # appendix 2: t = n*T_s omskrevet da T_s = 1/f_s, hvor t er det givne tidspunkt for hver sample

plt.plot(xAxis, samples)

plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

plt.show()

print("---------------- cut signal ----------------")

start = int(20 * fs)
end = int(55 * fs)

signal_2500rpm_cut = Signal(samples=samples[start:end], fs=fs)

print("Duration of the cut signal:", signal_2500rpm_cut.duration(), "s")

