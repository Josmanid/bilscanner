"""Step 8: Draw the result.

One dB plot with everything needed to understand the result:
    the spectrum, the noise floor, the engine's peaks and the comb teeth m * f_t.

Plotter does not calculate anything new. It only draws what the other
classes have found, keeping drawing and calculation separate.
"""

import matplotlib.pyplot as plt
import numpy as np

from ..models.engineModel import EngineModel
from ..models.spectrum import Spectrum


class Plotter:
    """Draws the spectrum, noise floor, engine peaks and comb teeth."""

    def __init__(self, max_hz: float = 500):
        # How far the x-axis goes. With the phone's microphone the engine's
        # peaks are only visible up to about 500 Hz.
        self.max_hz = max_hz

    def _to_db(self, amplitudes: np.ndarray) -> np.ndarray:
        """From amplitude to dBFS: L = 20 * log10(A / A_ref), A_ref = 1.

        1e-12 protects against log10(0), which is minus infinity.
        The leading underscore means: for use inside the class only.
        """
        return 20 * np.log10(amplitudes + 1e-12)

    def plot(self, spectrum: Spectrum, floor: Spectrum, engine: EngineModel, title: str):
        """Draws one dB plot and returns the figure.

        The figure is returned instead of shown right away, so the caller
        decides whether to show it or save it.
        """
        db_spectrum = self._to_db(spectrum.amplitudes)
        db_floor = self._to_db(floor.amplitudes)

        # fig is the window, ax is the plot itself
        fig, ax = plt.subplots(figsize=(10, 5))

        # 1. Spectrum and noise floor
        ax.plot(spectrum.frequencies, db_spectrum, label="Spectrum (Welch)")
        ax.plot(floor.frequencies, db_floor, linestyle="--", label="Noise floor (median)")

        # 2. Comb teeth at m * f_t, the Fourier series f = m * f0.
        # Only the first line gets a label, so the legend does not repeat itself.
        f_t = engine.firing_frequency
        m = 1
        while m * f_t <= self.max_hz:
            label = f"m · f_t, f_t = {f_t:.2f} Hz" if m == 1 else None
            ax.axvline(m * f_t, color="gray", linestyle=":", alpha=0.5, label=label)
            m += 1

        # 3. The engine's peaks as dots on top of the spectrum
        peak_freqs = [p.frequency for p in engine.matched_peaks]
        peak_db = self._to_db(np.array([p.amplitude for p in engine.matched_peaks]))
        ax.plot(peak_freqs, peak_db, "o", color="red", label="Engine peaks")

        # 4. Axes. The y-axis is set from the data inside the visible range,
        # so very low values at high frequencies (OGG) do not pull it down.
        visible = spectrum.frequencies <= self.max_hz
        ax.set_xlim(0, self.max_hz)
        ax.set_ylim(db_floor[visible].min() - 10, db_spectrum[visible].max() + 5)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Level (dBFS)")

        # 5. Title with the result
        ax.set_title(f"{title}: {engine.revolutions_per_minute:.0f} rpm")
        ax.legend()

        # Keeps the title and axes from overlapping
        fig.tight_layout()
        return fig