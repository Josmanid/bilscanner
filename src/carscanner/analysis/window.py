"""Step 3: Windows.

Theory: the FFT assumes the recording repeats. Unless it contains a whole
number of periods, there is a jump where the end meets the start, which
causes leakage in the spectrum. A window tapers the recording towards both
ends, so the jump disappears.

Here the window is applied to the samples in time. In the textbook's
section 6.4 it is applied to the coefficients in frequency, the mirrored use.
"""

from abc import ABC, abstractmethod

import numpy as np

from ..models.signal import Signal


class Window(ABC):
    """Interface for all windows, like an interface in C#.

    @abstractmethod means every class inheriting from Window must have
    an apply_to. If it is missing, Python raises an error.
    """

    @abstractmethod
    def apply_to(self, signal: Signal) -> Signal:
        """Applies the window to the signal and returns a new Signal."""
        ...


class RectangularWindow(Window):
    """No window: multiplies by 1 everywhere.

    Used for comparison with Hanning, to see how much leakage the window removes.
    """

    def apply_to(self, signal: Signal) -> Signal:
        # Hver sample ganges med 1, så intet ændrer sig.
        samples = signal.samples * 1

        return Signal(samples=samples, fs=signal.fs)


class HanningWindow(Window):
    """Hanning window: rises from 0 to 1 in the middle and back to 0.

    Because it ends at 0 at both ends, there is no jump when the FFT repeats
    the recording. This gives low leakage far from strong peaks, at the cost
    of a wider main peak.
    """

    def apply_to(self, signal: Signal) -> Signal:
        # Vinduet skal have samme længde som signalet,
        # så hver sample får sin egen vægt.
        N = len(signal.samples)
        window = np.hanning(N)

        # Element for element: sample nr. n ganges med vinduets
        # værdi nr. n, ligesom .* i opgave 6.23.
        samples = signal.samples * window

        return Signal(samples=samples, fs=signal.fs)
