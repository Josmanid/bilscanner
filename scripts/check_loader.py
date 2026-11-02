from bilscanner.loader import AudioLoader

loader = AudioLoader() # laver et nyt objekt på heapen ligesom C#

# indlæs filen
signal = loader.load("data/02_tomgang_750rpm.ogg")

# len() tæller elementerne i arrayet, altså N, antallet af samples
print("Antal samples N: ", len(signal.samples))
print("Samplefrekvens f_s: ", signal.fs)



