"""Step 7: Estimate firing frequency and engine speed from the peaks.

Harmonic comb:
    The engine's peaks lie at m * f_t (Fourier series, f = m * f0).
    Candidate values of f_t are tried, and for each one the code counts
    how many measured peaks lie close to a tooth m * f_t. The candidate
    with the most hits is the firing frequency.

Why an expected range:
    A comb at half or a third of f_t also hits every peak (octave error).
    Searching only within an expected range, for example 600-1200 rpm
    at idle, rules those out. For three cylinders: rpm_max / rpm_min < 1.5.
"""

import numpy as np

from ..models.engineModel import EngineModel
from ..models.peak import Peak


class EngineEstimator:
    """Estimates firing frequency and engine speed from the spectrum's peaks."""

    def __init__(
        self,
        cylinders: int = 3,
        tolerance_hz: float = 0.5,
        max_frequency_hz: float = 500,
    ):
        # Antal cylindre. Bruges kun til at regne mellem rpm og f_t.
        self.cylinders = cylinders
        # Hvor langt en top må ligge fra en tand og stadig tælle som ramt.
        # Toppene ligger ikke præcist, fordi stregerne har 0,2 Hz imellem,
        # og fordi motoren svinger lidt i omdrejningstal.
        self.tolerance_hz = tolerance_hz
        # Kun toppe under denne grænse bruges. Motorens toppe ses kun op
        # til ca. 500 Hz, og ved høje m kan fremmede toppe ramme en tand
        # ved et tilfælde, som 4000 Hz med buddet 22,6 Hz.
        self.max_frequency_hz = max_frequency_hz

    def estimate(self, peaks: list[Peak], rpm_min: float, rpm_max: float) -> EngineModel:
        # Skridt 0: Brug kun toppe under grænsen.
        # [... for ... if ...] laver en ny liste med de toppe, der opfylder
        # betingelsen, ligesom .Where(...).ToList() i C#.
        usable = [peak for peak in peaks if peak.frequency <= self.max_frequency_hz]

        # Skridt 1: Fra rpm til Hz, f_t = rpm/60 * cylindre/2
        f_min = rpm_min / 60 * self.cylinders / 2
        f_max = rpm_max / 60 * self.cylinders / 2

        # Skridt 2: Buddene på f_t fra f_min til f_max i skridt af 0,01 Hz
        candidates = np.arange(f_min, f_max, 0.01)

        # Skridt 3: Find det bud, der rammer flest toppe
        best_hits = 0           # højeste antal ramte toppe indtil videre
        best_candidate = None   # det bud, der gav det

        for candidate in candidates:
            hits = 0  # tælles forfra for hvert bud
            for peak in usable:
                # Nærmeste tand: m = rund(f_top / bud)
                m = round(peak.frequency / candidate)
                # Afstanden fra den målte top til den teoretiske tand m * bud
                distance = abs(peak.frequency - m * candidate)
                # m skal være mindst 1, ellers er der ingen tand
                if m >= 1 and distance <= self.tolerance_hz:
                    hits += 1

            # Rammer dette bud flere end det hidtil bedste?
            if hits > best_hits:
                best_hits = hits
                best_candidate = candidate

        # Ramte intet bud en eneste top, kan motoren ikke findes
        if best_candidate is None:
                raise ValueError("No peaks match a firing frequency in the expected range.")

        # Skridt 4: Finjustér f_t ud fra de toppe, der ramte.
        # Nabobud som 22,55 og 22,65 Hz rammer ofte de samme toppe, så det
        # bedste bud er kun præcist til ca. tolerancen. Hver ramt top giver
        # sit eget bud f_top / m, og gennemsnittet af dem er mere præcist:
        #   67,8/3, 90,6/4, 158,2/7, 203,8/9  ->  ca. 22,62 Hz
        matched_peaks = []
        estimates = []
        for peak in usable:
            m = round(peak.frequency / best_candidate)
            distance = abs(peak.frequency - m * best_candidate)
            if m >= 1 and distance <= self.tolerance_hz:
                matched_peaks.append(peak)
                estimates.append(peak.frequency / m)

        firing_frequency = float(np.mean(estimates))

        # Skridt 5: Fra f_t tilbage til rpm, rpm = f_t * 60 * 2 / cylindre.
        # For tre cylindre er det f_t * 40.
        revolutions_per_minute = firing_frequency * 60 * 2 / self.cylinders

        return EngineModel(
            firing_frequency=firing_frequency,
            revolutions_per_minute=revolutions_per_minute,
            matched_peaks=matched_peaks,
        )




        