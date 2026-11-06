from dataclasses import dataclass

import numpy as np



@dataclass
class Spectrum:
    """
    Holds a spectrum: the result of the DFT of a Signal.
    Data in the frequency domain, like Signal is data in the time domain.
    """
    frequencies: np.ndarray # frekvensen for hver streg, f_m = m * f0, i Hz
    amplitudes: np.ndarray  # højden af hver streg
    f0: float               # afstanden mellem stregerne, f0 = 1/T, i Hz


