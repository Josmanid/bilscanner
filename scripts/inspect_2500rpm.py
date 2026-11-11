import numpy as np
import matplotlib.pyplot as plt

from bilscanner.sources.loader import AudioLoader

loader = AudioLoader()

signal_2500rpm = loader.load("data/03_2500rpm.ogg")
samples = signal_2500rpm.samples
N = len(signal_2500rpm.samples)
fs = signal_2500rpm.fs
xAxis = np.arange(N)/fs # appendix 2: t = n*T_s omskrevet da T_s = 1/f_s, hvor t er det givne tidspunkt for hver sample

plt.plot(xAxis,samples)

plt.xlabel("Tid i sekunder")
plt.ylabel("Amplitude")

plt.show()



