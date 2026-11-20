"""CarScanner: hele kæden i ét kald.

Facade-mønstret: én enkel indgang foran mange klasser. Den, der bruger
CarScanner, behøver ikke vide, at der findes en Welch-analysator,
en støjgulvsestimator osv. Indstillingerne er dem, der er fundet
til at virke på optagelserne af Hyundai i10'eren.

Kæden:
    fil -> Signal -> Welch-spektrum -> støjgulv -> toppe -> kam -> plot
"""

from matplotlib.figure import Figure

from .analysis.engineEstimator import EngineEstimator
from .analysis.noiseFloorEstimator import NoiseFloorEstimator
from .analysis.peakDetector import PeakDetector
from .analysis.spectrumAnalyzer import SpectrumAnalyzer
from .analysis.welchAnalyzer import WelchAnalyzer
from .analysis.window import HanningWindow
from .models.engineModel import EngineModel
from .models.signal import Signal
from .plotting.plotter import Plotter
from .sources.loader import AudioLoader


class CarScanner:
    """Finder motorens omdrejningstal i en lydoptagelse og tegner resultatet."""

    def __init__(self, cylinders: int = 3):
        # Alle værktøjer laves én gang med de indstillinger, der virker.
        self.loader = AudioLoader()
        # Welch med stykker på 5 s: f0 = 0,2 Hz og et jævnt støjgulv
        self.welch = WelchAnalyzer(
            analyzer=SpectrumAnalyzer(window=HanningWindow()),
            segment_duration=5,
        )
        # Medianvindue på 10 Hz: bredere end en top, smallere end gulvets ændringer
        self.floor_estimator = NoiseFloorEstimator(window_hz=10)
        # Toppe mindst 8 dB over gulvet og mindst 2 Hz fra hinanden
        self.peak_detector = PeakDetector(threshold_db=8, min_distance_hz=2)
        # Kammen. Antal cylindre bruges kun til at regne mellem f_t og rpm.
        self.engine_estimator = EngineEstimator(cylinders=cylinders)
        self.plotter = Plotter(max_hz=500)

    def scan(
        self,
        path: str,
        rpm_min: float,
        rpm_max: float,
        title: str,
        start_s: float | None = None,
        end_s: float | None = None,
    ) -> tuple[EngineModel, Figure]:
        """Kører hele kæden på én optagelse.

        Parametre:
            path:     stien til lydfilen
            rpm_min:  laveste forventede omdrejningstal
            rpm_max:  højeste forventede omdrejningstal
                      Området udelukker oktavfejl, fx at den halve orden
                      bliver regnet som tændingsfrekvensen.
            title:    titel på plottet
            start_s:  valgfri start på det stykke, der analyseres, i sekunder
            end_s:    valgfri slut på stykket, i sekunder

        Returnerer:
            motorens resultat og figuren. tuple betyder, at to ting
            returneres på én gang, ligesom (EngineModel, Figure) i C#.
        """
        # 1. Indlæs optagelsen
        signal = self.loader.load(path)

        # 2. Klip evt. et stabilt stykke ud.
        # Sekunder oversættes til pladser: n = t * f_s.
        # None betyder "fra starten" eller "til slutningen".
        if start_s is not None or end_s is not None:
            start = int(start_s * signal.fs) if start_s is not None else None
            end = int(end_s * signal.fs) if end_s is not None else None
            signal = Signal(samples=signal.samples[start:end], fs=signal.fs)

        # 3. Fra tid til frekvens, gulv, toppe og kam
        spectrum = self.welch.analyse(signal)
        floor = self.floor_estimator.estimate(spectrum)
        peaks = self.peak_detector.detect(spectrum, floor)
        engine = self.engine_estimator.estimate(peaks, rpm_min=rpm_min, rpm_max=rpm_max)

        # 4. Tegn resultatet
        fig = self.plotter.plot(spectrum, floor, engine, title=title)

        # 5. Returnér begge
        return engine, fig