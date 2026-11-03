import numpy as np
from .signal import Signal

class SignalGenerator: 
    def sine(
        self, 
        frequency: float, 
        amplitude: float, 
        duration: float, 
        fs: float
    ) -> Signal:
        """En ren sinus med kendt frekvens og amplitude.

        Parametre:
            frequency: frekvensen f i Hz
            amplitude: højden A
            duration:  længden T i sekunder
            fs:        samplefrekvensen f_s i Hz
        """
        # Skridt 1: Hvor mange samples?
        # T = N * T_s vendt om giver N = T * f_s (formel 7.2).
        N = int(duration * fs)

        # Skridt 2: Hvornår tages hver sample?
        # np.arange(N) giver 0, 1, 2, ..., N-1, altså samplenumrene n.
        # Divideret med f_s giver det tidspunkterne t = n * T_s = n / f_s.
        t = np.arange(N) / fs

        # skridt 3: Værdien af hver samples
        # f(n) = A sin(2 pi f n T_s), samplet sinus side 209
        samples = amplitude * np.sin(2 * np.pi * frequency * t)


        return Signal(samples=samples, fs=fs)
