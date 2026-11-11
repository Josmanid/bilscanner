"""Trin 3: Vinduer.

Teori (afsnit 6.4 og lektion 6): FFT'en antager, at optagelsen
gentager sig. Passer den ikke til et helt antal perioder, opstår et
spring, hvor slutningen møder begyndelsen, og det giver lækage i
spektret. Et vindue nedtoner optagelsen mod begge ender, så springet
forsvinder.

Her lægges vinduet på samplene i tid. I bogens afsnit 6.4 lægges det
på koefficienterne i frekvens. Det er den spejlvendte brug.
"""

from abc import ABC, abstractmethod

import numpy as np

from ..models.signal import Signal


class Window(ABC):
    """Interface for alle vinduer, svarende til et interface i C#.

    @abstractmethod betyder, at alle klasser, der arver fra Window,
    skal have en apply_to. Glemmer de den, giver Python en fejl.
    """

    @abstractmethod
    def apply_to(self, signal: Signal) -> Signal:
        """Applies the window to the signal and returns a new Signal."""
        ...


class RectangularWindow(Window):
    """Intet vindue: ganger med 1 overalt.

    Bruges til at sammenligne med Hanning, så man kan se,
    hvor meget lækage vinduet fjerner.
    """

    def apply_to(self, signal: Signal) -> Signal:
        # Hver sample ganges med 1, så intet ændrer sig.
        samples = signal.samples * 1

        return Signal(samples=samples, fs=signal.fs)


class HanningWindow(Window):
    """Hanning-vindue: går fra 0 op til 1 i midten og ned til 0 igen.

    Fordi det ender i 0 i begge ender, er der intet spring tilbage,
    når FFT'en gentager optagelsen. Det giver lav lækage langt fra
    de kraftige toppe. Prisen er en bredere hovedtop.
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
