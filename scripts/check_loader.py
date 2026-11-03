from bilscanner.loader import AudioLoader

loader = AudioLoader() # laver et nyt objekt på heapen ligesom C#

# indlæs filen
signal = loader.load("data/04_svingende_1000_2000rpm.ogg")

# len() tæller elementerne i arrayet, altså N, antallet af samples
print("Antal samples N: ", len(signal.samples))
print("Samplefrekvens f_s: ", signal.fs)

# duration() regner T = N / f_s (formel 7.2)
print("Varighed T:", signal.duration(), "s")

