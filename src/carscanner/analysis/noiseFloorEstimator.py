"""Trin 5: Støjgulvet.

Input:  et Spectrum, typisk fra WelchAnalyzer
Output: støjgulvet som et nyt Spectrum med samme frekvenser

Idé:
    Gulvet er den brede baggrund, som motorens toppe står på. Det er
    ikke fladt: under ca. 150 Hz stiger det, fordi telefonmikrofonen
    hører dårligt de laveste frekvenser. Derfor skal gulvet findes
    frekvens for frekvens, ikke som ét fast niveau.

Metode, glidende median:
    For hver streg tages medianen af nabostregerne i et vindue.
    Medianen er den midterste værdi, når de sorteres. Toppene er høje
    og smalle og havner i den ene ende af sorteringen, så medianen
    ser gennem dem og finder gulvet. Et glidende gennemsnit ville
    derimod blive trukket op af toppene.

Brug:
    Bagefter måles hver streg som dB over gulvet. Så ligger gulvet
    omkring 0 dB ved alle frekvenser, ligesom normal hørelse i et
    audiogram i dB HL, og trin 6 kan bruge én regel for toppene.
"""

from scipy.ndimage import median_filter

from ..models.spectrum import Spectrum


class NoiseFloorEstimator:
    """Finder støjgulvet i et spektrum med en glidende median."""

    def __init__(self, window_hz: float = 10):
        # Medianvinduets bredde i Hz.
        #   For smalt: en top fylder hele vinduet, og gulvet følger toppene.
        #   For bredt: vinduet blander lavt og højt gulv og kan ikke følge
        #   stigningen under ca. 150 Hz.
        #   10 Hz er 50 streger, så en top på ca. 1 Hz fylder kun 1/10.
        # Tommelfingerregel: en top skal fylde under halvdelen af vinduet.
        self.window_hz = window_hz

    def estimate(self, spectrum: Spectrum) -> Spectrum:
        # Skridt 1: Fra Hz til antal streger.
        # Stregerne ligger med afstanden f0, så 10 Hz / 0,2 Hz = 50 streger.
        width = int(self.window_hz / spectrum.f0)

        # Skridt 2: Gør antallet ulige.
        # Med et ulige antal har vinduet en midterste streg, så det står
        # centreret om den frekvens, gulvet beregnes for.
        # % 2 giver resten ved division med 2: 0 for lige, 1 for ulige.
        if width % 2 == 0:
            width += 1

        # Skridt 3: Den glidende median hen over frekvenserne.
        # Filtret glider over spektrets amplituder, ikke over lyden i tid.
        # mode="nearest": i enderne, hvor vinduet stikker ud over spektret,
        # gentages den yderste værdi i stedet for at fylde op med nuller.
        floor = median_filter(spectrum.amplitudes, size=width, mode="nearest")

        # Skridt 4: Gulvet som et Spectrum med samme frekvensakse,
        # så det kan plottes og sammenlignes direkte med spektret.
        return Spectrum(
            frequencies=spectrum.frequencies,
            amplitudes=floor,
            f0=spectrum.f0,
        )
    

        