"""Trin 7: Estimér omdrejningstallet for tomgang ud fra lyden.

Kør fra roden:
    python scripts/check_engine.py

Forventet: ca. 22,6 Hz og ca. 905 omdr./min. Tælleren viste 900.
"""

from bilscanner.sources.loader import AudioLoader
from bilscanner.analysis.window import HanningWindow
from bilscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.analysis.welchAnalyzer import WelchAnalyzer
from bilscanner.analysis.noiseFloorEstimator import NoiseFloorEstimator
from bilscanner.analysis.peakDetector import PeakDetector
from bilscanner.analysis.engineEstimator import EngineEstimator

# 1. Indlæs optagelsen
signal = AudioLoader().load("data/02_tomgang_900rpm.ogg")

# 2. Spektrum med Welch
welch = WelchAnalyzer(analyzer=SpectrumAnalyzer(window=HanningWindow()), segment_duration=5)
spectrum = welch.analyse(signal)

# 3. Støjgulvet
floor = NoiseFloorEstimator(window_hz=10).estimate(spectrum)

# 4. Toppene
peaks = PeakDetector(threshold_db=8, min_distance_hz=2).detect(spectrum, floor)

# 5. Kammen: tændingsfrekvens og omdrejningstal
engine = EngineEstimator(cylinders=3).estimate(peaks, rpm_min=600, rpm_max=1200)

print("Tændingsfrekvens:", round(engine.firing_frequency, 2), "Hz")
print("Omdrejningstal:  ", round(engine.revolutions_per_minute), "omdr./min.")
print("Motorens toppe:  ", [round(p.frequency, 1) for p in engine.matched_peaks])