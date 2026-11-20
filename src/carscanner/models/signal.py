from dataclasses import dataclass

import numpy as np



@dataclass
class Signal:
    """holds the data for samplingfrequency fs and the array of time """
    samples: np.ndarray  # talrækken i tid f(n) se appendix transformationer
    fs: float

    def duration(self) -> float:
        """Length of the recording in seconds, T = N / f_s (formula 7.2)."""
        N = len(self.samples) # samlede antal samples i hele optagelsen 
        T = N/self.fs
        return T


