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
| 900 omdr./min. (tomgang) | 15 Hz | 22,5 Hz |
| 2500 omdr./min. | 41,7 Hz | 62,5 Hz |

Tændingerne er korte stød med jævne mellemrum, altså et periodisk signal. Ifølge Fourierrækken består det af toppe ved f = m · f_t, dvs. tændingsfrekvensen og dens harmoniske.

En trecylindret rækkemotor har desuden en indbygget ubalance ved f_k. Den ligger dog så lavt, at telefonens mikrofon næppe kan høre den.

## Første resultat
<img width="777" height="587" alt="image" src="https://github.com/user-attachments/assets/32771243-70b4-4e73-ad58-9c8532847cf4" />

Tomgangsoptagelsen viser en række toppe med ca. 22,5 Hz imellem, fra 67,5 Hz op til 450 Hz. Fx ligger den 4. harmoniske ved 90,3 Hz, hvilket svarer til ca. 903 omdr./min. Havde i første omgang aflæst omdrejningstallet forkert til 750 med varm motor.

Analysen forudsagde dog en tomgang på ca. 900 omdr./min. ud fra lyden alene. Omdrejningstælleren bekræftede efterfølgende 900 omdr./min. med varm motor.

Sammenligning med støjoptagelsen viser, at alle de skarpe toppe kommer fra bilen, og motorens støjgulv ligger omkring 300 Hz+. Toppene ved ca. 19,4 og 39,5 Hz passer ikke ind i rækken og ser ud til at have en anden kilde i bilen. Optagelsen ved 2500 omdr./min. skal vise, om de følger motoren.

## Metode

1. Indlæs optagelsen
2. Del den i stykker på 5 s (Welch)
3. Læg et Hanning-vindue på hvert stykke
4. FFT af hvert stykke
5. Frekvensakse ud fra samplefrekvens og antal samples
6. Skalér, så toppene viser den rigtige amplitude
7. Tag gennemsnittet af effekten over stykkerne
8. Find toppe og kobl dem til motorens forventede frekvenser

## Overvejelser og valg

| Valg | Begrundelse |
|---|---|
| **Hanning-vindue** | Motorlyden har komponenter spredt over hele spektret. Hanning giver lav lækage langt fra de kraftige toppe. Prisen er en bredere hovedtop. |
| **Welch med stykker på 5 s** | Midling over flere stykker gør støjgulvet jævnt, så motorens toppe står tydeligt frem. 5 s giver f₀ = 1/T = 0,2 Hz, som er rigeligt, fordi motorens toppe selv er ca. 0,5 Hz brede. |
| **48 kHz samplerate** | Basebåndet går til 24 kHz, langt over motorens interessante frekvenser. Lydkortets anti-aliasing-filter klarer resten. |
| **Telefonmikrofon** | Bygget til tale og hører dårligt under ca. 50 til 100 Hz. Derfor ses motoren mest i de harmoniske, ikke i selve grundtonen. |
| **Støjoptagelse som reference** | Toppe, der også findes uden motor, kommer ikke fra bilen. |
| **Udendørs, fast placering** | Så tæt på frit felt som muligt, og samme opstilling i alle optagelser, så de kan sammenlignes. |
| **Python** | numpy, scipy og matplotlib har det, signalbehandlingen kræver. Skal værktøjet videre til et produkt, er C# et naturligt valg. |
| **Klasser med ét ansvar** | Hvert trin i signalbehandlingen er sin egen klasse. Vinduer, signalkilder og fejltyper ligger bag interfaces, så nye kan tilføjes uden at ændre det, der virker. |
| **Kunstige testsignaler** | Hver klasse testes på signaler med kendte frekvenser, før der bruges rigtige optagelser. |

## Data

Optagelserne ligger i `data/` og er ikke med i git. Optaget med telefon, Audio Recorder, Hyundai i10 med trecylindret motor:

| Fil | Indhold |
|---|---|
| `01_stoej.ogg` | Omgivelserne uden motor, reference |
| `02_tomgang_900rpm.ogg` | Tomgang, ca. 900 omdr./min. |
| `03_2500rpm.ogg` | Ca. 2500 omdr./min., med op- og nedgang i enderne |
| `04_svingende_1000_2000rpm.ogg` | Varierende mellem 1000 og 2000 omdr./min. |

Demoens optagelser er gemt som **OGG**, dvs. komprimeret med tab. Kraftige toner som tændingsfrekvensen bevares, men svage detaljer og høje frekvenser kan være påvirket. Fremtidige optagelser laves i WAV eller FLAC.

## Kom i gang

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
pytest
```

Tjek-scripts køres fra roden, fx `python scripts/check_recording.py`.

## Videre arbejde

1. **Demo:** måling af tændingsfrekvens og harmoniske i tomgang
2. **Diagnose i tomgang:** fejlsignaturer, fx ventiltik ved knastakslens frekvens, kræver en reference og data med kendte fejl
3. **Diagnose under kørsel:** hjul, lejer og gearkasse, hvor frekvenserne ændrer sig over tid
