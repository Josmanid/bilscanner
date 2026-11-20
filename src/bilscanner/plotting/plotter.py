"""Trin 8: Tegn resultatet.

Ét dB-plot med alt, der skal til for at forstå resultatet:
    spektret, støjgulvet, motorens toppe og kammens tænder m * f_t.

Plotter regner ikke noget nyt. Den tegner kun det, de andre klasser
har fundet, så tegning og beregning holdes adskilt.
"""

import matplotlib.pyplot as plt
import numpy as np

from ..models.engineModel import EngineModel
from ..models.spectrum import Spectrum


class Plotter:
    """Tegner spektrum, støjgulv, motorens toppe og kammens tænder."""

    def __init__(self, max_hz: float = 500):
        # Hvor langt op x-aksen går. Motorens toppe ses kun op til
        # ca. 500 Hz med telefonens mikrofon.
        self.max_hz = max_hz

    def _to_db(self, amplitudes: np.ndarray) -> np.ndarray:
        """Fra amplitude til dBFS: L = 20 * log10(A / A_ref), A_ref = 1.

        1e-12 beskytter mod log10(0), som er minus uendelig.
        Understregen foran navnet betyder: kun til brug inde i klassen.
        """
        return 20 * np.log10(amplitudes + 1e-12)

    def plot(self, spectrum: Spectrum, floor: Spectrum, engine: EngineModel, title: str):
        """Tegner ét dB-plot og returnerer figuren.

        Figuren returneres i stedet for at blive vist med det samme,
        så den, der kalder, selv vælger at vise den eller gemme den.
        """
        db_spectrum = self._to_db(spectrum.amplitudes)
        db_floor = self._to_db(floor.amplitudes)

        # fig er vinduet, ax er selve plottet
        fig, ax = plt.subplots(figsize=(10, 5))

        # 1. Spektret og støjgulvet
        ax.plot(spectrum.frequencies, db_spectrum, label="Spektrum (Welch)")
        ax.plot(floor.frequencies, db_floor, linestyle="--", label="Støjgulv (median)")

        # 2. Kammens tænder ved m * f_t, Fourierrækkens f = m * f0.
        # Kun den første får et navn, så forklaringen ikke gentager sig.
        f_t = engine.firing_frequency
        m = 1
        while m * f_t <= self.max_hz:
            label = f"m · f_t, f_t = {f_t:.2f} Hz" if m == 1 else None
            ax.axvline(m * f_t, color="gray", linestyle=":", alpha=0.5, label=label)
            m += 1

        # 3. Motorens toppe som prikker oven på spektret
        peak_freqs = [p.frequency for p in engine.matched_peaks]
        peak_db = self._to_db(np.array([p.amplitude for p in engine.matched_peaks]))
        ax.plot(peak_freqs, peak_db, "o", color="red", label="Motorens toppe")

        # 4. Akser. y-aksen sættes ud fra data inden for det viste område,
        # så meget lave værdier ved høje frekvenser (OGG) ikke trækker den ned.
        visible = spectrum.frequencies <= self.max_hz
        ax.set_xlim(0, self.max_hz)
        ax.set_ylim(db_floor[visible].min() - 10, db_spectrum[visible].max() + 5)
        ax.set_xlabel("Frekvens i Hz")
        ax.set_ylabel("Niveau i dBFS")

        # 5. Titel med resultatet
        ax.set_title(f"{title}: {engine.revolutions_per_minute:.0f} omdr./min.")
        ax.legend()

        # Sørger for, at titel og akser ikke overlapper
        fig.tight_layout()
        return fig