from dataclasses import dataclass

import numpy as np



@dataclass
class Signal:
    """holds the data for samplingfrequency fs and the array of time """
    samples: np.ndarray  # talrækken i tid f(n) se appendix transformationer
    fs: float

    def duration(self) -> float:
        """optagelsens længde i sekunder se formel (7.2) T = N / f_s"""
        N = len(self.samples) # samlede antal samples i hele optagelsen 
        T = N/self.fs
        return T


