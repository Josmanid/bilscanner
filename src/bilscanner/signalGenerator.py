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
        """En sum af harmoniske sinusser, ligesom en Fourierrække.

        Den m'te harmoniske ligger ved m * f_0 og har amplituden A_m:
            f(n) = sum over m af A_m * sin(2 pi m f_0 n T_s)   (afsnit 6.1)

        Generatoren ved intet om motoren. Det er den, der kalder metoden,
        der vælger grundfrekvens og amplituder.

        Parametre:
            fundamental: grundfrekvensen f_0 i Hz
            amplitudes:  liste med A_1, A_2, A_3, ... Første tal hører til
                         1 * f_0, andet til 2 * f_0 osv. 0 betyder, at den
                         harmoniske ikke er med.
            duration:    længden T i sekunder
            fs:          samplefrekvensen f_s i Hz

        Eksempel: fundamental=6.25 og amplitudes=[0, 0.5, 1.0, 0, 0, 0.3]
        giver 12,5 Hz med 0,5, 18,75 Hz med 1,0 og 37,5 Hz med 0,3.
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
        """Antal samples, N = T * f_s (formel 7.2)."""
        return int(duration * fs)

