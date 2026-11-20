"""Estimates the noise floor of the idle recording and detects the peaks above it.

Checks that the running median follows the floor without being pulled up by the peaks.
Run from the project root: python scripts/check_noise_floor.py
"""
import numpy as np
import matplotlib.pyplot as plt

from carscanner.sources.loader import AudioLoader
from carscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from carscanner.analysis.window import HanningWindow
from carscanner.analysis.welchAnalyzer import WelchAnalyzer
from carscanner.analysis.noiseFloorEstimator import NoiseFloorEstimator
from carscanner.analysis.peakDetector import PeakDetector

loader = AudioLoader()

analyze_spectrum = SpectrumAnalyzer(window=HanningWindow())

detect_peaks = PeakDetector()

# signals
signal_900rpm = loader.load("data/02_idle_900rpm.ogg")


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
    print(f"{peak.frequency:7.1f} Hz   {peak.above_floor_db:5.1f} dB over noisefloor")

# Fra amplitude til dB, som i compare_rpm.py.
# 1e-12 lægges til, fordi log10(0) er minus uendelig.
db_spectrum = 20 * np.log10(spectrum_900rpm.amplitudes + 1e-12)
db_floor = 20 * np.log10(spectrum_900rpm_noise_floor.amplitudes + 1e-12)

plt.plot(spectrum_900rpm.frequencies, db_spectrum, label="idle 900 rpm.")
# Gulvet stiplet ovenpå, så toppene stadig kan ses
plt.plot(spectrum_900rpm.frequencies, db_floor, linestyle="--", label="noise floor, median 10 Hz")
plt.xlim(0, 500)      # kun de lave frekvenser, hvor motorens ordener ligger
plt.ylim(-100, -50)   # fra under gulvet til over den højeste top
plt.xlabel("Freq. in Hz")
plt.ylabel("Niveau in dBFS")
plt.legend()
plt.show()
