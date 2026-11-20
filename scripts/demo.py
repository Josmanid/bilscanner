import matplotlib.pyplot as plt
from bilscanner.carScanner import CarScanner

scanner = CarScanner()

# Idle
engine, fig = scanner.scan("data/02_tomgang_900rpm.ogg", rpm_min=600, rpm_max=1200, title="Idle")
print(f"Idle: {engine.revolutions_per_minute:.0f} rpm")
fig.savefig("docs/idle.png", dpi=150)

# Revved to about 2500 rpm, stable part only (20 to 55 s)
engine, fig = scanner.scan("data/03_2500rpm.ogg", rpm_min=2000, rpm_max=3000,
                           title="Revved", start_s=20, end_s=55)
print(f"Revved: {engine.revolutions_per_minute:.0f} rpm")
fig.savefig("docs/revved.png", dpi=150)

plt.show()