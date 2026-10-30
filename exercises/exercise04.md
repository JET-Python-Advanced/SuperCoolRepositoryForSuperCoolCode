# Übungsblatt 4 — Sammlungen, Fehlerkultur, Ressourcen

**Python Advanced · Einheit 4 · Freitag, 30.10.2026**

Teil A in `exercises/worksheet04.py`, Teil B in `scan.py`.

----------

## Teil A1 — Was ist der Output?

**A1.1**

```python
d = ["Alien", "Heat", "Fargo", "Memento", "Arrival"]
print(d[1:3])
print(d[-2:])
print(d[::-1])
print(d[3:99])
print(d[:2] + d[2:] == d)

```

**A1.2**

```python
g = ["a", "b", "c", "d", "e"]
g[1:3] = ["X"]
print(g)

h = ["a", "b", "c", "d", "e"]
h[::2] = [1, 2, 3]
print(h)

```

Was passiert bei `h[::2] = [1]`?

**A1.3**

```python
erster, *rest = ["nur eins"]
print(erster, rest)

x, *mitte, y = (1, 2, 3, 4)
print(mitte)

```

Von welchem Typ ist `mitte`?

**A1.4**

```python
a = [1, 2, 3]
i = 0
i, a[i] = 1, 99
print(i, a)

```

**A1.5**

```python
def bericht(titel, jahr, endung):
    return f"{titel} ({jahr}).{endung}"

print(bericht(*["Alien"], *[1979, "mkv"]))
print(bericht(*[1979, "mkv"], *["Alien"]))

```

Die zweite Zeile läuft fehlerfrei. Ist das gut?

**A1.6**

```python
print({1: "a", 1.0: "b", True: "c"})
print(len({"mkv", "mp4", "mkv"}))
print({1, 2} ^ {2, 3})

```

**A1.7**

```python
a = ["Alien"]
b = a
a += ["Heat"]
print(a, b)

c = ["Alien"]
d = c
c = c + ["Heat"]
print(c, d)

```

**A1.8**

```python
from collections import defaultdict

leer = defaultdict(int)
print(leer["unbekannt"])
print(dict(leer))
print(len(leer))
print(leer.get("noch_was"), "noch_was" in leer)

```

**A1.9**

```python
from collections import Counter

c = Counter(["mkv", "mkv", "mp4"])
print(c["avi"], "avi" in c)
print(Counter("aab") - Counter("ab"))
print(c.most_common(1))

```

**A1.10**

```python
def schluckt():
    try:
        raise ValueError("geht verloren")
    finally:
        return "fertig"

print(schluckt())

```

**A1.11**

```python
def versuch(x):
    try:
        return 10 / x
    except Exception:
        return "allgemein"
    except ZeroDivisionError:
        return "Null"

print(versuch(0))

```
Warum ist das kein Syntaxfehler?


**A1.12**

```python
from pathlib import Path

p = Path("data") / "collection" / "Film.Teil2_2019.mkv"
print(p.name)
print(p.stem)
print(p.suffix)
print(p.suffixes)
print(p.parent)

```

**A1.13**

```python
d = {"Alien": 1979, "Heat": 1995}
sicht = d.keys()
d["Fargo"] = 1996
print(list(sicht))
print(d.keys() & {"Alien", "Gandhi"})

```

----------

## Teil A2

**A2.1** Schreiben Sie `nach_endung(namen)`. Die Funktion bekommt eine Liste von Dateinamen und liefert ein Dictionary: Endung → Liste der Namen mit dieser Endung.

```python
nach_endung(["Alien.mkv", "Heat.mp4", "Fargo.mkv"])
# {'mkv': ['Alien.mkv', 'Fargo.mkv'], 'mp4': ['Heat.mp4']}

```

Schreiben Sie sie **zweimal**: einmal mit `setdefault`, einmal mit `defaultdict`. Welche Version würden Sie im Projekt behalten?

**A2.2** Schreiben Sie `haeufigste_endung(namen)`, die die häufigste Endung und ihre Anzahl als Paar liefert. Einmal ohne `Counter`, dann mit.

```python
haeufigste_endung(["a.mkv", "b.mkv", "c.mp4"])
# ('mkv', 2)

```

**A2.3** Diese Funktion ist in der LBYL-Form geschrieben. Schreiben Sie sie in der EAFP-Form um.

```python
def laufzeit(tabelle, titel):
    if titel in tabelle:
        if isinstance(tabelle[titel], int):
            return tabelle[titel]
    return 0

```

----------

## Teil A3 — Fehler finden

**A3.1** Dieser Code funktioniert nicht. Erklären Sie, warum, und reparieren Sie ihn.

```python
laufzeit = {"Alien": 117, "Heat": 170}

for titel in laufzeit:
    laufzeit[titel.lower()] = laufzeit[titel]

print(laufzeit)

```

**A3.2** Dieser Code läuft und liefert für beide Aufrufe ein Ergebnis. Er ist trotzdem in drei Punkten falsch. Finden Sie alle drei.

```python
def jahr_lesen(name):
    try:
        teil = name.split("_")[1]
        return int(teil)
    except:
        return 0


print(jahr_lesen("Alien_1979_1080p.mkv"))
print(jahr_lesen("Urlaubsvideo.mkv"))

```

**Hinweis:** Zwei der drei Punkte betreffen den `except`-Zweig, einer den `try`-Block.

**A3.3** Zwei Fehler, beide fallen auf dem eigenen Rechner nicht auf, beim Kollegen eventuell schon.

```python
def zeilen_zaehlen(pfad):
    datei = open(pfad)
    anzahl = len(datei.readlines())
    datei.close()
    return anzahl

```

----------

## Teil B1 — Medienbibliothek

Achtung: Ab hier wieder weiter in `scan.py`.

Ab diesem Blatt arbeiten wir nicht mehr mit der festen Liste `FILES`, sondern mit einem echten Ordner. Die Liste darf verschwinden.

**B1.1** Legen Sie die Übungssammlung an:

```
python data/create_collection.py

```

Das Skript meldet am Ende, wie viele Dateien es angelegt hat. Möglicherweise meldet es zusätzlich, dass eine Datei **nicht** angelegt werden konnte — das ist kein Fehler im Skript!

Zählen Sie danach mit `pathlib`, wie viele Dateien in `data/collection` liegen.

**Hinweis:** `rglob("*")` liefert Ordner mit. Sie brauchen `is_file()`.

**B1.2** Geben Sie der Klasse `Mediathek` eine zweite Art, entstanden zu sein:

```python
mediathek = Mediathek.von_ordner("data/collection")

```

-   `von_ordner` ist eine Klassenmethode (`@classmethod`) und liefert eine fertige Mediathek.
-   Aufgenommen werden nur Videodateien. Legen Sie die erlaubten Endungen als **Menge** an und vergleichen Sie kleingeschrieben.
-   `self.files` hält ab jetzt `Path`-Objekte statt Zeichenketten. Passen Sie `with_extension` entsprechend an.

Wie viele Dateien sind es, und welche fallen heraus?

**B1.3** Schreiben Sie eine Methode `verteilung()`, die zählt, wie oft jede Endung vorkommt, und das Ergebnis absteigend sortiert liefert. Geben Sie die drei häufigsten aus.

**B1.4** Jetzt das Jahr. Legen Sie zuerst zwei Exceptions an:

```python
class MediathekFehler(Exception):
    """Fehler, die aus unserem Code stammen."""


class UnlesbarerName(MediathekFehler):
    """Ein Dateiname enthält kein erkennbares Jahr."""

```

Dann:

-   `jahr_aus(pfad)` liefert das Jahr als `int`. Findet sich keines, wird `UnlesbarerName` ausgelöst — mit `raise ... from ...`, wenn eine andere Ausnahme die Ursache war.
-   `nach_jahrzehnt()` liefert ein Dictionary: Jahrzehnt → Liste der Titel. Namen ohne Jahr dürfen den Durchlauf **nicht** abbrechen. Sammeln Sie sie in einer zweiten Liste und geben Sie am Ende aus, wie viele es waren.

**Hinweis:** In den Namen stehen Jahre in vier Schreibweisen: `Alien_1979_1080p.mkv`, `Alien.1979.1080p.mkv`, `Alien (1979).mkv` und `Alien 1979 BluRay.mkv`. Ein regulärer Ausdruck wie `r"(19\d\d|20\d\d)"` deckt alle vier ab. Achten Sie darauf, dass `1080p` und `2160p` nicht als Jahr durchgehen.

**B1.5** Schreiben Sie `bericht_schreiben(pfad)`. Die Methode schreibt eine CSV-Datei mit den Spalten `titel`, `jahr`, `endung` — nach Jahr sortiert.

-   Die Kodierung wird angegeben.
-   In der Sammlung gibt es zwei Titel mit einem Komma im Namen. Suchen Sie sie und erklären Sie, was sie in einer selbst zusammengebauten CSV-Zeile anrichten.

**B1.6** In der Sammlung liegen drei Dateien, deren Name mit `Am` beginnt. Schneiden Sie aus jedem Namen den Titel heraus (alles vor dem `" ("`) und legen Sie die drei Titel in eine **Menge**.

Die Menge hat drei Einträge, aber nur zwei sehen verschieden aus. Finden Sie heraus, woran das liegt — `len()` auf den einzelnen Titeln hilft weiter — und sorgen Sie dafür, dass die Menge zwei Einträge hat.

**Hinweis:** Das Modul heißt `unicodedata`.
