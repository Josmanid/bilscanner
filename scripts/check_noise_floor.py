
import numpy as np
import matplotlib.pyplot as plt

from bilscanner.sources.loader import AudioLoader
from bilscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.analysis.window import HanningWindow
from bilscanner.analysis.welchAnalyzer import WelchAnalyzer
from bilscanner.analysis.noiseFloorEstimator import NoiseFloorEstimator
from bilscanner.analysis.peakDetector import PeakDetector

loader = AudioLoader()

analyze_spectrum = SpectrumAnalyzer(window=HanningWindow())

detect_peaks = PeakDetector()

# signals
signal_900rpm = loader.load("data/02_tomgang_900rpm.ogg")


welch = WelchAnalyzer(analyzer=analyze_spectrum,segment_duration=5)
noise_floor_estimator = NoiseFloorEstimator()

# spectrums
spectrum_900rpm = welch.analyse(signal_900rpm)


# finder gulvet af welch spektrummet
spectrum_900rpm_noise_floor = noise_floor_estimator.estimate(spectrum_900rpm)

#benyt detect
analysed_peaks = detect_peaks.detect(spectrum_900rpm,spectrum_900rpm_noise_floor)

# print frekvenserne
for peak in analysed_peaks:
    print(f"{peak.frequency:7.1f} Hz   {peak.above_floor_db:5.1f} dB over gulvet")

# Fra amplitude til dB, som i compare_rpm.py.
# 1e-12 lægges til, fordi log10(0) er minus uendelig.
db_spectrum = 20 * np.log10(spectrum_900rpm.amplitudes + 1e-12)
db_floor = 20 * np.log10(spectrum_900rpm_noise_floor.amplitudes + 1e-12)

plt.plot(spectrum_900rpm.frequencies, db_spectrum, label="Tomgang 900 omdr./min.")
# Gulvet stiplet ovenpå, så toppene stadig kan ses
plt.plot(spectrum_900rpm.frequencies, db_floor, linestyle="--", label="Støjgulv, median 10 Hz")
plt.xlim(0, 500)      # kun de lave frekvenser, hvor motorens ordener ligger
plt.ylim(-100, -50)   # fra under gulvet til over den højeste top
plt.xlabel("Frekvens i Hz")
plt.ylabel("Niveau i dBFS")
plt.legend()
plt.show()
