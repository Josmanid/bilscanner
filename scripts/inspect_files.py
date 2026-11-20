"""Lists every OGG recording in data/ with its sample rate, channels and duration.

Checks that all recordings share the same format (48 000 Hz, mono) before analysis.
Run from the project root: python scripts/inspect_files.py
"""

from pathlib import Path
import soundfile as sf

dir_path = Path("data")

files = list(dir_path.glob("*.ogg"))

for file in files:
    info = sf.info(file)
    print("Name:        ", file.name)
    print("Sample rate: ", info.samplerate)
    print("Channels:    ", info.channels)
    print("Duration (s):", info.duration)
    print("--------------------------------------")