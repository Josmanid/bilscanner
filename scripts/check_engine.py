"""Trin 7: Estimér omdrejningstallet for tomgang ud fra lyden.

Kør fra roden:
    python scripts/check_engine.py

Forventet: ca. 22,6 Hz og ca. 905 omdr./min. Tælleren viste 900.
"""
import matplotlib.pyplot as plt

from carscanner.sources.loader import AudioLoader
from carscanner.analysis.window import HanningWindow
from carscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from carscanner.analysis.welchAnalyzer import WelchAnalyzer
from carscanner.analysis.noiseFloorEstimator import NoiseFloorEstimator
from carscanner.analysis.peakDetector import PeakDetector
from carscanner.analysis.engineEstimator import EngineEstimator
from carscanner.plotting.plotter import Plotter
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

# 6. plot
Plotter().plot(spectrum, floor, engine, title="Tomgang")
plt.show()