"""Demo: estimates the engine speed at idle and revved from sound alone.

Saves the result plots used in the README to docs/ (rev counter: 900 and about 2500 rpm).
Run from the project root: python scripts/demo.py
"""

import matplotlib.pyplot as plt
from carscanner.carScanner import CarScanner

scanner = CarScanner()

# Idle
engine, fig = scanner.scan("data/02_idle_900rpm.ogg", rpm_min=600, rpm_max=1200, title="Idle")
print(f"Idle: {engine.revolutions_per_minute:.0f} rpm")
fig.savefig("docs/idle.png", dpi=150)

# Revved to about 2500 rpm, stable part only (20 to 55 s)
engine, fig = scanner.scan("data/03_revved_2500rpm.ogg", rpm_min=2000, rpm_max=3000,
                           title="Revved", start_s=20, end_s=55)
print(f"Revved: {engine.revolutions_per_minute:.0f} rpm")
fig.savefig("docs/revved.png", dpi=150)

plt.show()