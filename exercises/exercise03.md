# Übungsblatt 3 — Typisierung, Kopieren, Referenzparameter

**Python Advanced · Einheit 3 · Freitag, 23.10.2026**

Teil A in `exercises/worksheet03.py`, Teil B in `scan.py`.

---

## Teil A1 — Verstehen

**A1.1** Füllen Sie die vier Felder. Wohin gehören **Python**, **Java**, **C#** und
**JavaScript**?

|  | statisch geprüft | dynamisch geprüft |
|---|---|---|
| **stark typisiert** | | |
| **schwach typisiert** | | |

**A1.2** *Mechanical* oder *semantic representation*? Ordnen Sie zu.

- Der Prozessor muss wissen, wie viele Bytes er lesen soll.
- Ein Kollege sieht am Typ, dass er dieses Objekt nicht runden kann.
- Python weiß zur Laufzeit, welche Operationen auf einem Objekt erlaubt sind.
- Ein Parameter heißt `point_in_time` und ist als `datetime` annotiert.

**A1.3** Ein Parameter ist als `str` annotiert, aufgerufen wird die Funktion mit einer
Zahl. Was macht Python?

**A1.4** Warum heißt es `len(x)` und nicht `x.len()`?

---

## Teil A2 — Was ist der Output?

**A2.1**
```python
a = ["Alien", "Heat"]
b = a
b.append("Fargo")
print(a)
print(a is b)
```

**A2.2**
```python
a = ["Alien", "Heat"]
b = ["Alien", "Heat"]
print(a == b)
print(a is b)
```

**A2.3**
```python
t = ("Alien", [1979, "SciFi"])
t[1].append("Horror")
print(t)
```

Was passiert bei `t[1] = []`?

**A2.4**
```python
import copy

original = [["Alien", 1979], ["Heat", 1995]]
flach = list(original)
tief = copy.deepcopy(original)

original[0].append("mkv")
print(flach[0])
print(tief[0])
print(flach is original, flach[0] is original[0])
```

**A2.5**
```python
def hinzufuegen(titel, sammlung=[]):
    sammlung.append(titel)
    return sammlung

print(hinzufuegen("Alien"))
print(hinzufuegen("Heat"))
```

**A2.6**
```python
def leeren(liste):
    liste = []

def wirklich_leeren(liste):
    liste.clear()

a = ["Alien"]
leeren(a)
print(a)
wirklich_leeren(a)
print(a)
```

**A2.7**
```python
def zaehle(filme=None):
    if filme is None:
        filme = []
    filme.append("x")
    return filme

print(zaehle(), zaehle())
```

**A2.8**
```python
class Mediathek:
    def __init__(self, filme):
        self.filme = filme

    def __len__(self):
        return len(self.filme)

print(len(Mediathek(["Alien", "Heat"])))
print(bool(Mediathek(["Alien"])))
print(bool(Mediathek([])))
```

**A2.9**
```python
def verdoppeln(x):
    return x + x

print(verdoppeln(3), verdoppeln("ab"), verdoppeln([1]))
```

Was passiert bei `verdoppeln({"a": 1})`?

---

## Teil A3 — Duck Typing

**A3.1** Schreiben Sie eine Funktion `zeige_alle(quelle)`, die jedes Element ihres
Arguments in einer eigenen Zeile ausgibt. Es darf **keine** Typprüfung darin vorkommen.

**A3.2** Rufen Sie sie der Reihe nach auf mit:

```python
["Alien", "Heat"]           # Liste
("Alien", "Heat")           # Tupel
{"Alien", "Heat"}           # Menge
{"Alien": 1979}             # Dictionary
"Alien"                     # Zeichenkette
range(3)                    # range
42                          # eine Zahl
```

Welche funktionieren, welche nicht? Bei den funktionierenden: Was wird jeweils
ausgegeben?

---

## Teil A4 — Fehler finden

**A4.1** Dieser Code läuft, ist aber falsch. Erklären Sie, was passiert, und reparieren Sie ihn.

```python
class Warteschlange:
    def __init__(self, eintraege=[]):
        self.eintraege = eintraege

    def hinzufuegen(self, eintrag):
        self.eintraege.append(eintrag)


a = Warteschlange()
a.hinzufuegen("Alien")

b = Warteschlange()
print(b.eintraege)
```

**A4.2** Finden Sie den Fehler und beheben Sie ihn. 

```python
class Playlist:
    def __init__(self, titel):
        self.titel = titel


meine_liste = ["Alien", "Heat"]
p = Playlist(meine_liste)
p.titel.append("Fargo")

print(meine_liste)
```

---

## Teil B1 — Medienbibliothek

Achtung: Ab hier wieder weiter in `scan.py`. 

**B1.1** Versehen Sie Ihre Funktionen aus Blatt 1 mit Typannotationen: `title`,
`extension` und `count_extension`. 
**Hinweis:** Für eine Liste von Zeichenketten schreibt man `list[str]`.

**B1.2** Schreiben Sie eine Klasse `Mediathek`, die eine Liste von Dateinamen hält.

- Der Konstruktor nimmt die Liste **optional** entgegen — ohne Argument soll die
  Mediathek leer sein.
- `__len__` liefert die Anzahl der Dateien.
- `add(filename)` fügt eine Datei hinzu.

Prüfen Sie danach, dass `len(mediathek)` funktioniert und eine leere Mediathek in einem
`if` als falsch gilt.

**B1.3** Achtung: Dieser Code soll **nicht** funktionieren:

```python
aussen = ["Alien_1979_1080p.mkv"]
m = Mediathek(aussen)
m.add("Heat_1995_720p.mkv")
print(aussen)        # soll weiterhin nur einen Eintrag haben
```

Achten Sie darauf, dass die übergebene Liste von außen unberührt bleibt.

**B1.4** Schreiben Sie eine Methode `with_extension(wanted)`, die alle Dateien mit einer
bestimmten Endung liefert. Die Rückgabe muss eine **neue** Liste sein.

**B1.5** Schreiben Sie eine Methode `kopie()`, die eine zweite Mediathek
mit demselben Inhalt liefert. Reicht hier eine shallow Kopie, oder braucht es
`deepcopy`? Begründen Sie Ihre Antwort mit dem, was in `self.files` steht.

