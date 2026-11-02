from pathlib import Path
import soundfile as sf

dir_path = Path("data")

files = list(dir_path.glob("*.ogg"))

for file in files:
    info = sf.info(file)
    print("Navn: ",file.name)
    print("Samplerate: ",info.samplerate)
    print("Antal kanaler: ",info.channels)
    print("spilletid i sekunder: ",info.duration)
    print("--------------------------------------")
