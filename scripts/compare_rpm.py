import numpy as np
import matplotlib.pyplot as plt

from bilscanner.sources.loader import AudioLoader
from bilscanner.models.signal import Signal
from bilscanner.analysis.spectrumAnalyzer import SpectrumAnalyzer
from bilscanner.analysis.window import HanningWindow
from bilscanner.analysis.welchAnalyzer import WelchAnalyzer

loader = AudioLoader()

analyzer = SpectrumAnalyzer(window=HanningWindow())

# signals
signal_900rpm = loader.load("data/02_tomgang_900rpm.ogg")

signal_2500rpm = loader.load("data/03_2500rpm.ogg")
start = int(20*signal_2500rpm.fs)
end = int(55*signal_2500rpm.fs)
signal_2500rpm_cut = Signal(samples=signal_2500rpm.samples[start:end],fs=signal_2500rpm.fs)

welch = WelchAnalyzer(analyzer=analyzer,segment_duration=5)

# spectrums
spectrum_900rpm = welch.analyse(signal_900rpm)
spectrum_2500rpm_cut = welch.analyse(signal_2500rpm_cut)



print("------------- plots -------------")

# Fra amplitude til decibel: L = 20 * log10(A / A_ref)
#   20 og ikke 10, fordi A er en amplitude. Effekt er A²,
#   og 10 * log10(A²) = 20 * log10(A).
#   A_ref = 1, altså fuld skala, så enheden er dBFS.
#   En faktor 10 i amplitude giver altid 20 dB.
# 1e-12 lægges til, fordi log10(0) er minus uendelig.
db_900rpm = 20 * np.log10(spectrum_900rpm.amplitudes + 1e-12)
db_2500rpm = 20 * np.log10(spectrum_2500rpm_cut.amplitudes + 1e-12)

# Ét vindue med to plot under hinanden: 2 rækker, 1 kolonne.
#   fig er hele vinduet, ax_lin og ax_db er de to plot i det.
#   sharex=True giver dem samme x-akse, så toppene står ud for hinanden.
#   figsize er vinduets størrelse i tommer, bredde og højde.
fig, (ax_lin, ax_db) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Når man har flere plot, tegner man på hvert enkelt med ax i stedet
# for plt. Navnene ændrer sig lidt: xlim bliver til set_xlim osv.

# --- Øverst: lineær amplitude ---
ax_lin.plot(spectrum_900rpm.frequencies, spectrum_900rpm.amplitudes, label="Tomgang 900 omdr./min.")
ax_lin.plot(spectrum_2500rpm_cut.frequencies, spectrum_2500rpm_cut.amplitudes, label="2500 omdr./min.")
ax_lin.set_ylabel("Amplitude")
ax_lin.set_title("Lineær skala")
ax_lin.legend()

# --- Nederst: decibel ---
ax_db.plot(spectrum_900rpm.frequencies, db_900rpm, label="Tomgang 900 omdr./min.")
ax_db.plot(spectrum_2500rpm_cut.frequencies, db_2500rpm, label="2500 omdr./min.")
ax_db.set_ylim(-100, -40)  # fra lidt under støjgulvet til lidt over den højeste top
ax_db.set_xlabel("Frekvens i Hz")
ax_db.set_ylabel("Niveau i dBFS")
ax_db.set_title("Decibel")
ax_db.legend()

# Fælles x-akse, så den sættes kun én gang
ax_db.set_xlim(0, 500)  # kun de lave frekvenser, hvor motorens ordener ligger

# Tændingsfrekvensen f_t målt fra den 4. harmoniske i hvert spektrum
f_t_900 = 90.3 / 4      # ca. 22,6 Hz, tomgang
f_t_2500 = 254.4 / 4    # 63,6 Hz, 2500 omdr./min.

# Lodrette stiplede linjer ved m * f_t, Fourierrækkens f = m * f_0.
# Kun den første linje (m = 1) får et navn, ellers ville forklaringen
# vise den samme tekst mange gange.
for f_t, color, name in [(f_t_900, "C0", "tomgang"), (f_t_2500, "C1", "2500 omdr./min.")]:
    m = 1
    while m * f_t <= 500:
        label = f"f_t = {f_t:.1f} Hz ({name})" if m == 1 else None
        for ax in (ax_lin, ax_db):
            ax.axvline(m * f_t, color=color, linestyle="--", alpha=0.4, label=label)
        m += 1

# Forklaringen skal laves EFTER alle linjer er tegnet, ellers kommer
# de stiplede linjer ikke med
ax_lin.legend()
ax_db.legend()
# Sørger for, at titler og akser ikke overlapper
plt.tight_layout()
plt.show()