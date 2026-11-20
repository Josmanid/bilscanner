"""Creates synthetic test signals with known frequencies, amplitudes and noise."""

import numpy as np
from ..models.signal import Signal

class SignalGenerator: 
    def sine(
        self, 
        frequency: float, 
        amplitude: float, 
        duration: float, 
        fs: float
    ) -> Signal:
        """A pure sine with known frequency and amplitude.

        Parameters:
            frequency: frequency f in Hz
            amplitude: amplitude A
            duration:  length T in seconds
            fs:        sample rate f_s in Hz
        """
        # Skridt 1: Hvor mange samples?
        # T = N * T_s vendt om giver N = T * f_s (formel 7.2).
        N = self._num_samples(duration,fs)

        # Skridt 2: Hvornår tages hver sample?
        # np.arange(N) giver 0, 1, 2, ..., N-1, altså samplenumrene n.
        # Divideret med f_s giver det tidspunkterne t = n * T_s = n / f_s.
        t = np.arange(N) / fs

        # skridt 3: Værdien af hver samples
        # f(n) = A sin(2 pi f n T_s), samplet sinus side 209
        samples = amplitude * np.sin(2 * np.pi * frequency * t)


        return Signal(samples=samples, fs=fs)
    def harmonics(
        self,
        fundamental: float,
        amplitudes: list[float],
        duration: float,
        fs: float,
    ) -> Signal:
        """A sum of harmonic sines, like a Fourier series.

        The m-th harmonic lies at m * f_0 with amplitude A_m:
            f(n) = sum over m of A_m * sin(2 pi m f_0 n T_s)   (section 6.1)

        The generator knows nothing about the engine. The caller chooses
        the fundamental and the amplitudes.

        Parameters:
            fundamental: fundamental frequency f_0 in Hz
            amplitudes:  list of A_1, A_2, A_3, ... The first value belongs
                         to 1 * f_0, the second to 2 * f_0, and so on.
                         0 means the harmonic is left out.
            duration:    length T in seconds
            fs:          sample rate f_s in Hz

        Example: fundamental=6.25 and amplitudes=[0, 0.5, 1.0, 0, 0, 0.3]
        gives 12.5 Hz at 0.5, 18.75 Hz at 1.0 and 37.5 Hz at 0.3.
        """
        # Skridt 1: Antal samples, N = T * f_s (formel 7.2)
        N = self._num_samples(duration,fs)

        # Skridt 2: En liste med N nuller. Her lægges sinusserne sammen.
        # np.zeros(N) laver et array med N gange 0.0.
        total = np.zeros(N)

        # Skridt 3: Gå de harmoniske igennem.
        # enumerate giver både plads og værdi. start=1 gør, at første
        # plads får nummeret m = 1 i stedet for 0.
        for m, A in enumerate(amplitudes, start=1):
            # Den m'te harmoniske ligger ved m * f_0.
            # Genbrug sine(), som allerede er testet.
            harmonic = self.sine(m * fundamental, A, duration, fs)

            # Læg dens samples til summen. += lægger element for element
            # sammen, fordi begge er numpy-arrays af samme længde.
            total += harmonic.samples

        # Skridt 4: Returnér summen som et Signal
        return Signal(samples=total, fs=fs)
    
    def _num_samples(self, duration: float, fs: float) -> int:
        """Number of samples, N = T * f_s (formula 7.2)."""
        return int(duration * fs)

    def white_noise(
        self,
        std: float,
        duration: float,
        fs: float,
        seed: int | None = None,
    ) -> Signal:
        """White noise: random samples with a flat spectrum.

        Parameters:
            std:      standard deviation, how strong the noise is
            duration: length T in seconds
            fs:       sample rate f_s in Hz
            seed:     start value for the random generator. The same seed
                      gives the same noise every time, so a test can be
                      repeated. None gives new noise every time.
        """
        # Skridt 1: Antal samples, N = T * f_s (formel 7.2)
        N = self._num_samples(duration, fs)

        # Skridt 2: En tilfældighedsgenerator.
        # Med et seed starter den samme sted hver gang.
        rng = np.random.default_rng(seed)

        # Skridt 3: N tilfældige tal fra en normalfordeling,
        # middelværdi 0 og spredning std
        samples = rng.normal(0.0, std, N)

        return Signal(samples=samples, fs=fs)
    

