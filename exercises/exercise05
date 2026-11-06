# Übungsblatt 5 — Comprehensions, Generatoren, itertools

**Python Advanced · Einheit 5 · Freitag, 06.11.2026**

Teil A in `exercises/worksheet05.py`, Teil B in `scan.py`.

----------

## Teil A1 — Was ist der Output?

**A1.1**

```python
FILME = [("Alien", 1979), ("Heat", 1995), ("Fargo", 1996)]

print([t for t, j in FILME])
print([t for t, j in FILME if j > 1990])
print([(j, t) for t, j in FILME])

```

**A1.2**

```python
zahlen = [1, 2, 3, 4, 5]

print([x for x in zahlen if x % 2])
print([x if x % 2 else 0 for x in zahlen])

```

Die beiden Zeilen unterscheiden sich nur durch die Stellung des `if`. Was macht das jeweils mit der Länge des Ergebnisses?

**A1.3**

```python
x = "aussen"
print([x for x in range(3)])
print(x)

for y in range(3):
    pass
print(y)

```

**A1.4**

```python
verschachtelt = [[1, 2], [3], [4, 5]]

print([a for teil in verschachtelt for a in teil])
print([[a * 10 for a in teil] for teil in verschachtelt])

```

**A1.5**

```python
FILME = [("Alien", "mkv"), ("Heat", "mp4"), ("Fargo", "mkv")]

print({e: t for t, e in FILME})
print({e for t, e in FILME})
print(len({e for t, e in FILME}))

```

Die erste Zeile verliert einen Film. Welchen und warum?

**A1.6**

```python
g = (x * 2 for x in [1, 2, 3])

print(type(g).__name__)
print(sum(g))
print(sum(g))
print(list(g))

```

**A1.7**

```python
def zaehle():
    print("  A")
    yield 1
    print("  B")
    yield 2
    print("  C")

g = zaehle()
print("angelegt")
print(next(g))
print(list(g))

```

Achten Sie auf die Reihenfolge der Zeilen.

**A1.8**

```python
liste = [1, 2, 3]
leser = iter(liste)

print(next(leser), next(leser))
print(list(leser))
print(list(liste))
print(iter(leser) is leser)

```

**A1.9**

```python
from itertools import groupby

daten = ["a1", "a2", "b1", "a3"]

print([(k, list(g)) for k, g in groupby(daten, key=lambda s: s[0])])
print({k: list(g) for k, g in groupby(daten, key=lambda s: s[0])})

```

Die zweite Zeile verliert Daten. Wie viele und warum?

**A1.10**

```python
from itertools import islice, count

print(list(islice(count(5), 3)))
print(list(zip("abc", [1, 2])))
print(list(enumerate("ab", start=1)))

```

**A1.11**

```python
FILME = [("Alien", 1979, 117), ("Heat", 1995, 170), ("Fargo", 1996, 98)]

print(next((f for f in FILME if f[2] > 160), None))
print(next((f for f in FILME if f[2] > 200), None))
print(sorted(FILME, key=lambda f: (f[1] % 100, -f[2]))[0])

```

**A1.12**

```python
daten = [3, 1, 2]

print(sorted(daten))
print(daten.sort())
print(daten)

```

----------

## Teil A2 — Selbst schreiben

**A2.1** Übersetzen Sie die sechs LINQ-Ausdrücke nach Python. Die Daten:

```python
FILME = [
    ("Alien",    1979, 117, "mkv"),
    ("Heat",     1995, 170, "mp4"),
    ("Fargo",    1996,  98, "mkv"),
    ("Memento",  2000, 113, "mkv"),
    ("Arrival",  2016, 116, "mkv"),
    ("Das Boot", 1981, 149, "avi"),
]

```

LINQ

a)

`filme.Where(f => f.Jahr < 1990).Select(f => f.Titel)`

b)

`filme.OrderBy(f => f.Endung).ThenByDescending(f => f.Jahr)`

c)

`filme.Sum(f => f.Laufzeit)`

d)

`filme.Any(f => f.Laufzeit > 160)`

e)

`filme.FirstOrDefault(f => f.Jahr > 2010)`

f)

`filme.GroupBy(f => f.Endung)`

Bei f) gibt es mehr als eine richtige Antwort. Schreiben Sie dazu, welche Sie gewählt haben und warum.

**A2.2** Schreiben Sie einen Generator `videodateien(ordner)`, der aus einem Ordner rekursiv nur die Videodateien liefert —  ohne vorher eine Liste zu bauen.

```python
for pfad in videodateien("data/collection"):
    ...

```

Danach: Zählen Sie die Treffer, **ohne** `list()` zu verwenden. Warum benutzt die Funktion `yield` und nicht `return`.

**A2.3** Diese Funktion liest eine Datei und liefert die langen Zeilen. Schreiben Sie sie so um, dass sie mit einer Datei beliebiger Größe zurechtkommt.

```python
def lange_zeilen(pfad, mindestens=80):
    with open(pfad, encoding="utf-8") as f:
        zeilen = f.readlines()
    return [z.rstrip() for z in zeilen if len(z) > mindestens]

```

----------

## Teil A3 — Fehler finden

**A3.1** Dieser Code läuft durch und liefert zwei falsche Werte. Erklären Sie, warum, und reparieren Sie ihn.

```python
def jahre(filme):
    return (j for _t, j in filme)


FILME = [("Alien", 1979), ("Heat", 1995)]
g = jahre(FILME)

print("Anzahl:", sum(1 for _ in g))
print("Summe :", sum(g))
print("Jüngster:", max(g, default="keiner"))

```

**A3.2** Dieser Code soll Dateien nach ihrer Endung gruppieren. Er meldet `mkv: 1`, obwohl drei `.mkv`-Dateien in der Liste stehen.

```python
from itertools import groupby

dateien = ["a.mkv", "b.mp4", "c.mkv", "d.avi", "e.mkv"]

nach_endung = {k: list(g) for k, g in
               groupby(dateien, key=lambda n: n.rsplit(".", 1)[1])}

print(nach_endung)
print("mkv:", len(nach_endung.get("mkv", [])))

```

Finden Sie beide Ursachen.

**A3.3** Hier ist nichts falsch, solange die Datei klein ist. Was passiert bei einer Datei mit zwanzig Millionen Zeilen?

```python
def erste_treffer(pfad, suchwort, wie_viele=10):
    treffer = [z for z in open(pfad, encoding="utf-8") if suchwort in z]
    return treffer[:wie_viele]

```

**Hinweis:** Zwei Probleme. Eines betrifft den Speicher, eines die Datei selbst.

----------

## Teil B1 — Medienbibliothek

Achtung: Ab hier wieder weiter in `scan.py`.

**B1.1** Die drei Auswertungen aus Blatt 1 — Anzahl je Endung, Gesamtgröße, die zehn größten Dateien — sind damals als Schleifen entstanden. Schreiben Sie jede davon als **Comprehension** oder als Aufruf einer eingebauten Funktion neu.

Lassen Sie die alten Fassungen daneben stehen und benennen Sie sie um (`anzahl_je_endung_alt` und so weiter). Sie werden in Einheit 9 gebraucht: Dann prüft ein Test, dass alte und neue Fassung dasselbe liefern.

Zählen Sie zum Schluss die Zeilen vorher und nachher.

**B1.2** Eine der Auswertungen aus Blatt 4 lässt sich **nicht** sinnvoll als Comprehension schreiben: `nach_jahrzehnt()`. Versuchen Sie es trotzdem.

**B1.3** Ersetzen Sie in `Mediathek.von_ordner()` die Liste durch Ihren Generator aus A2.2. Die Mediathek selbst soll weiterhin eine Liste halten — es geht nur darum, dass beim Einlesen keine zweite Liste entsteht.

Prüfen Sie danach, dass `len(mediathek)` unverändert dieselbe Zahl liefert.

**B1.4** Jetzt der große Datenbestand. Erzeugen Sie ihn zuerst — das Skript gehört nach `data/create_titles.py` und braucht kein Netz:

```python
import gzip
from pathlib import Path

ZIEL = Path("data/titles.tsv.gz")
ZIEL.parent.mkdir(parents=True, exist_ok=True)

with gzip.open(ZIEL, "wt", encoding="utf-8", newline="") as f:
    f.write("tconst\tprimaryTitle\tstartYear\ttitleType\n")
    for i in range(2_000_000):
        art = "movie" if i % 3 else "tvEpisode"
        f.write(f"tt{i:07d}\tTitel {i}\t{1890 + i % 140}\t{art}\n")

```

Zwei Millionen Zeilen, rund 11 MB gepackt.

**Die Datei gehört nicht ins Repository.** Ergänzen Sie `.gitignore` entsprechend — das Erzeugungsskript wird eingecheckt, die Daten nicht.

Lesen Sie die Datei nun **zweimal** und zählen Sie die Zeilen:

```python
# Variante A
with gzip.open(ZIEL, "rt", encoding="utf-8") as f:
    zeilen = f.readlines()
anzahl = len(zeilen)

# Variante B
with gzip.open(ZIEL, "rt", encoding="utf-8") as f:
    anzahl = sum(1 for _ in f)

```

Messen Sie beide: die Zeit mit `time.perf_counter()`, den Speicher mit `tracemalloc`. Tragen Sie die vier Zahlen in die README ein.

**Wichtig — in zwei getrennten Läufen messen.** `tracemalloc` verfolgt jede einzelne Speicheranforderung und kostet dabei selbst Zeit, und zwar umso mehr, je mehr angefordert wird. Wer Zeit und Speicher gleichzeitig misst, bekommt für die Listen-Variante eine Zeit, die zur Hälfte aus der Messung besteht.

Das ist nicht nur ein Detail dieser Aufgabe: Es ist der Grund, warum man Geschwindigkeit niemals mit eingeschaltetem Profiler misst (Wissen Sie natürlich schon aus Analytik ;))

**B1.5** Schreiben Sie einen Generator `titel_aus(pfad)`, der aus dieser Datei nur die Kinofilme ab 1950 liefert — als Paare `(titel, jahr)`.

-   `titleType` muss `movie` sein
-   `startYear` muss eine Zahl sein und mindestens 1950
-   Die Datei wird **einmal** gelesen, und es entsteht zu keinem Zeitpunkt eine Liste aller Zeilen

**Hinweis:** `csv.DictReader(f, delimiter="\t")` nimmt das geöffnete File entgegen und ist selbst ein Iterator. Beim Öffnen `newline=""` angeben.

Bauen Sie daraus ein Dictionary — aber nur für die Filme **eines** Jahrzehnts, etwa der 1970er. Geben Sie aus, wie viele Einträge es geworden sind, und wie viel Speicher das belegt.

**B1.6** _(Zusatz)_ Wenn der echte IMDb-Datenbestand auf Ihrem Rechner liegt: Richten Sie `titel_aus` darauf. Die Spaltennamen stimmen überein — der Code muss sich nicht ändern, nur der Pfad.
