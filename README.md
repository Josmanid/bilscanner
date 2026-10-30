# bilscanner

Signalbehandlingsdemo, der påviser en motors karakteristik ved forskellige omdrejningstal i stilstand. Første projekt ud af tre.

## Mål

Demoen er en **måling, ikke en diagnose**. Den skal vise, at værktøjet virker, og at fysikken passer:

- Motorens tændingsfrekvens og dens harmoniske kan findes i en optagelse i tomgang.
- Toppene flytter sig, når omdrejningstallet ændres.
- Den fundne tændingsfrekvens passer med omdrejningstælleren.

## Fysikken

For en firetaktsmotor tænder hver cylinder hver anden omdrejning:

```
krumtapfrekvens   f_k = rpm / 60
tændingsfrekvens  f_t = f_k * cylindre / 2
```

Demoens bil har en trecylindret motor, så tændingsfrekvensen er 1,5 gange krumtapfrekvensen:

| Omdrejningstal | Krumtapfrekvens f_k | Tændingsfrekvens f_t |
|---|---|---|
| 750 omdr./min. (tomgang) | 12,5 Hz | 18,75 Hz |
| 2500 omdr./min. | 41,7 Hz | 62,5 Hz |

En trecylindret rækkemotor har desuden en indbygget ubalance, der svinger med krumtapfrekvensen. Derfor forventes også en tydelig top ved f_k, ikke kun ved f_t.

## Metode

1. Indlæs optagelsen
2. Læg et Hanning-vindue på
3. FFT
4. Frekvensakse ud fra samplefrekvens og antal samples
5. Find toppe
6. Kobl toppene til motorens forventede frekvenser

## Overvejelser og valg

| Valg | Begrundelse |
|---|---|
| **Hanning-vindue** | Motorlyden har komponenter spredt over hele spektret. Hanning giver lavest lækage langt fra de kraftige toppe. Prisen er en bredere hovedtop. |
| **Optagelser på mindst 5 s** | Frekvensopløsningen er Δf = 1/T. Tændingsfrekvensen ligger lavt, så opløsningen skal være fin. 5 s giver 0,2 Hz. |
| **48 kHz samplerate** | Basebåndet går til 24 kHz, langt over motorens interessante frekvenser. Lydkortets anti-aliasing-filter klarer resten. |
| **Udendørs, fast placering** | Så tæt på frit felt som muligt, og samme opstilling i alle optagelser, så de kan sammenlignes. |
| **Python** | numpy, scipy og matplotlib har det, signalbehandlingen kræver. Skal værktøjet videre til et produkt, er C# et naturligt valg. |
| **Klasser med ét ansvar** | Hvert trin i signalbehandlingen er sin egen klasse. Vinduer, signalkilder og fejltyper ligger bag interfaces, så nye kan tilføjes uden at ændre det, der virker. |
| **Kunstige testsignaler** | Hver klasse testes på signaler med kendte frekvenser, før der bruges rigtige optagelser. |

## Data

Optagelserne ligger i `data/` og er ikke med i git. Optaget med telefon, Audio Recorder, Hyundai i10 med trecylindret motor, i tomgang (ca. 750 omdr./min.) og ved ca. 2500 omdr./min.

Demoens optagelser er gemt som **OGG**, dvs. komprimeret med tab. Kraftige toner som tændingsfrekvensen bevares, men svage detaljer og høje frekvenser kan være påvirket. Fremtidige optagelser laves i WAV eller FLAC.

## Kom i gang

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

## Videre arbejde

1. **Demo:** måling af tændingsfrekvens og harmoniske i tomgang
2. **Diagnose i tomgang:** fejlsignaturer, fx ventiltik ved knastakslens frekvens, kræver en reference og data med kendte fejl
3. **Diagnose under kørsel:** hjul, lejer og gearkasse, hvor frekvenserne ændrer sig over tid
