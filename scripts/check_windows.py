"""Tjekker vinduerne på en kendt sinus.

Kør fra roden:
    python scripts/check_window.py

Facit:
    Hanning:     første og sidste sample er 0, max tæt på 1
    Rektangulær: samme værdier som den oprindelige sinus

Lækage (lektion 6, side 205):
    FFT'en regner spektret af det signal, man får ved at gentage
    optagelsen. 18,75 Hz i 5 s er 93,75 svingninger, altså ikke et
    helt antal. Den rektangulære slutter ved ca. -1 og starter ved 0,
    så der er et spring, hver gang optagelsen gentages. Springet
    smører energien ud over nabofrekvenserne i sidetoppe.

Afvejningen (afsnit 6.4, figur 6.12):
    Hanning fjerner springet ved at gå ned til 0 i begge ender.
    Til gengæld bliver hovedtoppen i spektret ca. dobbelt så bred.
    Mindre lækage koster altså frekvensopløsning, ligesom mindre
    rippel i figur 6.12 kostede en blødere overgang.

Konsekvenser for trin 4:
    1. To toppe tæt på hinanden er sværere at skille ad med Hanning.
       Modvirkes med en længere optagelse, så f_0 = 1/T bliver mindre.
    2. Vinduet sænker amplituden, fordi signalet nedtones i enderne.
       Hannings gennemsnit er 0,5, så toppene bliver ca. halvt så
       høje og skal ganges med 2 for at vise den rigtige amplitude.
"""

from bilscanner.signalGenerator import SignalGenerator
from bilscanner.window import HanningWindow, RectangularWindow


generator = SignalGenerator()
signal = generator.sine(18.75, 1, 5, 48000)

hanning = HanningWindow().apply_to(signal)
rectangular = RectangularWindow().apply_to(signal)

# Forventet med Hanning:
#   første og sidste sample er 0, fordi vinduet ender i 0
#   max er lidt under 1, fordi sinussens toppe ikke ligger præcis
#   midt i vinduet, hvor det er 1
print("--- Hanning ---")
print("Første sample:", hanning.samples[0])
print("Sidste sample:", hanning.samples[-1])
print("Max-værdi:    ", hanning.samples.max())

# Forventet med rektangulær:
#   første sample er 0, fordi sin(0) = 0
#   sidste sample er ca. -1
#
# Hvorfor det giver lækage:
#   FFT'en ser optagelsens længde T = N * T_s (formel 7.2) som den
#   periode, signalet gentager sig med. 18,75 Hz i 5 s er 93,75
#   svingninger, så sinussens egen periode passer ikke et helt antal
#   gange ind i T. Når FFT'en gentager optagelsen, hopper signalet
#   fra -1 til 0 ved hver gentagelse. Det spring findes ikke i det
#   rigtige signal.
#   For at bygge springet skal FFT'en bruge ekstra frekvenser ud
#   over 18,75 Hz. Energien smøres derfor ud over nabofrekvenserne.
#   Det er lækage.
#
# Hvorfor vi bruger et vindue:
#   Med 4 s ville det være 75 svingninger, et helt antal, og intet
#   spring. Men i praksis kan man ikke optage med en længde, der
#   passer præcis til motorens periode, fordi man ikke kender den på
#   forhånd. Hanning-vinduet går ned til 0 i begge ender, så springet
#   forsvinder, uanset hvor optagelsen slutter.
#
#   max er 1, fordi intet er ændret
print("--- Rektangulær ---")
print("Første sample:", rectangular.samples[0])
print("Sidste sample:", rectangular.samples[-1])
print("Max-værdi:    ", rectangular.samples.max())