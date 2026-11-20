import matplotlib.pyplot as plt
from bilscanner.carScanner import CarScanner

scanner = CarScanner()

# Tomgang
engine, fig = scanner.scan("data/02_tomgang_900rpm.ogg", rpm_min=600, rpm_max=1200, title="Tomgang")
print(f"Tomgang: {engine.revolutions_per_minute:.0f} omdr./min.")

# 2500 omdr./min., kun den stabile del
engine, fig = scanner.scan("data/03_2500rpm.ogg", rpm_min=2000, rpm_max=4000,
                           title="Speedet op", start_s=20, end_s=55)
print(f"Speedet op: {engine.revolutions_per_minute:.0f} omdr./min.")

plt.show()