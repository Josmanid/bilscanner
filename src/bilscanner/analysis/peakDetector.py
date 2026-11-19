"""Trin 6: Find toppene i et spektrum.

En streg er en top, hvis den:
    1. ligger mindst threshold_db over støjgulvet, og
    2. er højere end sine naboer, altså en lokal top.
Regel 2 sikrer, at én top kun tælles én gang, selv om Hanning gør
hovedtoppen ca. 4 streger bred.
"""

import numpy as np
from scipy.signal import find_peaks

from ..models.peak import Peak
from ..models.spectrum import Spectrum


class PeakDetector:
    """Finder toppe, der stikker tydeligt op over støjgulvet."""

    def __init__(self, threshold_db: float = 8, min_distance_hz: float = 2.0):
        # Hvor mange dB over gulvet en top mindst skal ligge
        self.threshold_db = threshold_db
        # Mindste afstand mellem to toppe, så én top kun tælles én gang
        self.min_distance_hz = min_distance_hz

    def detect(self, spectrum: Spectrum, floor: Spectrum) -> list[Peak]:
        # Skridt 1: Hver streg målt i dB over gulvet.
        # Division i amplitude er minus i dB. 1e-12 beskytter mod log10(0).
        amp_spectrum = spectrum.amplitudes + 1e-12
        amp_floor = floor.amplitudes + 1e-12
        above_floor_db = 20 * np.log10(amp_spectrum / amp_floor)

        # Skridt 2: Mindste afstand i streger.
        # Fra f = m * f0 fås m = f / f0, så 2 Hz / 0,2 Hz = 10 streger.
        # Mindst 1, som find_peaks kræver. Sikre at en top kun findes en gang.
        distance = max(1, int(self.min_distance_hz / spectrum.f0))

        # Skridt 3: Find de lokale toppe over tærsklen.
        # indices er pladserne m for toppene. _ er ekstra oplysninger,
        # vi ikke bruger.
        indices, _ = find_peaks(above_floor_db, height=self.threshold_db, distance=distance)

        # Skridt 4: Lav en Peak for hver plads m.
        # Alle tre værdier slås op på samme plads m i hver sin liste.
        # Er der ingen toppe, er indices tom, og listen bliver tom.
        peaks = []
        for m in indices:
            peaks.append(Peak(
                frequency=float(spectrum.frequencies[m]),
                amplitude=float(spectrum.amplitudes[m]),
                above_floor_db=float(above_floor_db[m]),
            ))

        # Skridt 5: Returnér listen af toppe
        return peaks

        




