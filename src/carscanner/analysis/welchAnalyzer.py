"""Welch-midling: et jævnere spektrum ved at tage gennemsnittet af flere.

Idé:
    Støj er tilfældig og forskellig i hvert stykke af optagelsen.
    Motorens toppe er deterministiske og ligger samme sted i hvert stykke.
    Tager man gennemsnittet af spektrene, bliver støjgulvet jævnt,
    mens toppene står tilbage.

Afvejning:
    Kortere stykker giver større f0 = 1/T, altså grovere opløsning,
    men flere spektre at tage gennemsnittet af.
"""

import numpy as np

from ..models.signal import Signal
from ..models.spectrum import Spectrum
from .spectrumAnalyzer import SpectrumAnalyzer


class WelchAnalyzer:
    """Deler et Signal i stykker, laver et spektrum af hvert og midler dem."""

    def __init__(self, analyzer: SpectrumAnalyzer, segment_duration: float):
        # SpectrumAnalyzer bruges til hvert stykke. Den har allerede sit vindue.
        self.analyzer = analyzer
        # Varigheden af ét stykke i sekunder, fx 5. Vælges udefra.
        self.segment_duration = segment_duration

    def analyse(self, signal: Signal) -> Spectrum:
        # Skridt 1: L, antal samples i ét stykke.
        # N = T * f_s med T = stykkets varighed. Et array deles op i
        # pladser, ikke i sekunder, så sekunder oversættes til samples.
        #   5 s * 48 000 = 240 000
        L = int(self.segment_duration * signal.fs)

        # Skridt 2: K, antal hele stykker i optagelsen.
        # // er heltalsdivision, så det sidste ufuldstændige stykke droppes.
        #   1 488 480 // 240 000 = 6
        N = len(signal.samples)
        K = N // L

        # Er optagelsen kortere end ét stykke, kan der ikke midles.
        if K == 0:
            raise ValueError("Signalet er kortere end ét stykke.")

        # Skridt 3 til 5: del op, lav spektrum af hvert stykke, læg sammen.
        #
        # Vi lægger effekten sammen, amplitude i anden, ikke amplituden.
        # Det er sådan, Welch er defineret, og effekt er det rigtige mål
        # for støj (Parseval). For en sinus giver det samme top som før.
        total_power = 0.0
        for k in range(K):
            # Stykke nummer k går fra plads k*L til lige før (k+1)*L
            segment = Signal(
                samples=signal.samples[k * L:(k + 1) * L],
                fs=signal.fs,
            )

            # Spektrum af stykket med den analysator, vi fik udefra
            spectrum = self.analyzer.analyse(segment)

            # Læg stykkets effekt til summen, element for element
            total_power = total_power + spectrum.amplitudes ** 2

        # Skridt 5: gennemsnittet af effekten
        mean_power = total_power / K

        # Tilbage til amplitude, så Spectrum betyder det samme som før
        amplitudes = np.sqrt(mean_power)

        # Skridt 6: alle stykker har samme længde, så frekvensaksen og f0
        # er ens. Vi bruger dem fra det sidste stykke.
        return Spectrum(
            frequencies=spectrum.frequencies,
            amplitudes=amplitudes,
            f0=spectrum.f0,
        )