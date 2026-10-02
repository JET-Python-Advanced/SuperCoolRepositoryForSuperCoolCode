# Übungsblatt 1 — Grundlagen

**Python Advanced · Einheit 1 · Freitag, 02.10.2026**

Arbeiten Sie in Ihrem eigenen Projektordner, nicht im Unterlagen-Repository.

---

## Einrichtung

Die Einrichtung haben wir schon gemeinsam im Unterricht gemacht. Sollte bei Ihnen alles funktioniert haben, können Sie gleich mit Teil A.1 beginnen. Falls etwas nicht funktioniert hat, finden Sie untenstehend nochmals alle Schritte. 

1. Auf GitHub das Template `erarbeitung` öffnen, **„Use this template"** anklicken. Sichtbarkeit **privat**, wählen Sie einen sinnvollen (und nicht peinlichen) Namen.
2. Das neue Repo klonen, indem Sie in Ihrer IDE ein Projekt aus der VSC erstellen. 

3. In der IDE mittels Token anmelden, falls noch nicht geschehen.

4. Eine Datei `worksheet01.py` im Directory `exercises` anlegen und commiten und pushen.

5. Auf GitHub im Browser nachsehen, dass die Datei dort angekommen ist.
   **Wenn sie dort steht, ist die Einrichtung fertig.**

  Verwechseln Sie nicht Ihr eigenes Repository mit dem Unterlagen-Repository. 

---

## Teil A1 — Bestimmen Sie den Output

Probieren Sie den Output zuerst ohne Computer zu bestimmen. Arbeiten Sie für den gesamten Teil A in `worksheet01.py`.

**A1.1**
```python
print(7 / 2, 7 // 2, 2 ** 3)
```

**A1.2**
```python
print(2 + 3 * 2 ** 2)
```

**A1.3**
```python
print("ab" * 3, "a" + "b")
```

**A1.4**
```python
print("Blade " "Runner")
```

**A1.5**
```python
print(0 <= 5 <= 10)
print(1 < 2 < 3 < 2)
```

**A1.6**
```python
zahlen = [1, 2, 3, 4, 5]
print(zahlen[-1], zahlen[-2])
```

**A1.7**
```python
print([1, 2] + [3])
print([1, 2] * 2)
print(3 in [1, 2])
```

**A1.8**
```python
a = ["Tor", "Haus", "Fenster"]
b = a.sort()
print(a)
print(b)
```

**A1.9**
```python
print(sorted(["Tor", "Fenster", "Haus"], key=len))
print(sorted(["Tor", "Fenster", "Haus"], key=len, reverse=True))
```

**A1.10**
```python
def double(x):
    print(x * 2)

result = double(4)
print(result)
```

**A1.11**
```python
count = 0

def count_up():
    count = 5

count_up()
print(count)
```

**A1.12**
```python
def movie(title, year=0, extension="mkv"):
    return f"{title} ({year}).{extension}"

print(movie("Alien", extension="mp4"))
print(movie("Heat", 1995))
```

---

## Teil A2 — Schöner Code nach PEP 8

Der Code funktioniert, verstößt aber an sechs Stellen gegen die PEP 8 Richtlinien. Finden Sie diese Stellen und schreiben Sie den Code um. 

```python
width=0
isLargeFormat = False
count      = 0
totalSize = 0

if isLargeFormat == True:
    print( "large format" )

result = calculate(file, minWidth, height, depth, extension, quality, language, subtitles)
```

**Selbstkontrolle:** Lassen Sie pycodestyle prüfen, ob Ihr korrigierter Code nun PEP  8 konform ist. Führen Sie dazu folgenden Code aus:

```
pip install pycodestyle
pycodestyle exercises/worksheet01.py
```

Sollten Sie keine Ausgabe sehen, entspricht Ihr Code allen Richtlinien. 

Achtung: `pycodestyle` prüft keine Namen. Eine der sechs Stellen findet es also nicht. Hier sind Sie gefragt!

---

## Teil A3 — Programmieren

**A3.1** Schreiben Sie eine Funktion `longer_than(words, min_length=4)`, die zählt, wie viele Wörter mindestens so lang sind wie angegeben. Der zweite Parameter soll weggelassen werden können.

```python
longer_than(["Haus", "Tor", "Fenster"])        # Output: 2
longer_than(["Haus", "Tor", "Fenster"], 6)     # Output: 1
```

**A3.2** Schreiben Sie eine Funktion `initials(name)`, die aus einem Namen die Initialen ausgibt.

```python
initials("Max Mustermann")        # Output: 'M.M.'
initials("Anna Maria Huber")      # Output: 'A.M.H.'
```

**A3.3** Schreiben Sie eine Funktion `countdown(start)`, die mit einer `while`-Schleife von `start` bis 1 herunterzählt und dann `los` ausgibt.

---

## Teil B1 — Medienbibliothek

Das Ziel über zwölf Wochen: Ein Kommandozeilenwerkzeug für eine unordentliche Mediensammlung. Es liest einen Ordner mit Film- und Seriendaten ein, erkennt aus den Dateinamen Titel, Jahr, Staffel/Folge, Auflösung und Sprache, gleicht das gegen einen lokalen Filmdatenbestand ab, meldet Auffälligkeiten (Duplikate, nicht erkannte Namen, etc.), reichert die Treffer über eine Web-API an und erzeugt am Ende einen Bericht. 

Heute: Arbeiten mit einer festen Liste. 
Nächste Woche: Einlesen eines echten Ordners statt der festen Liste.

Zwei String-Methoden aus der Dokumentation, auf die Folie 29 verweist, brauchen Sie dafür:

```python
"Alien_1979.mkv".split(".")      # ['Alien_1979', 'mkv']   zerlegt an einem Zeichen
"Das_Boot".replace("_", " ")     # 'Das Boot'              ersetzt alle Vorkommen
```

In `scan.py` finden Sie die Liste mit den Filmtiteln. Schreiben Sie Ihre Lösungen für Teil B auch in `scan.py`!

```python
FILES = [
    "Alien_1979_1080p.mkv",
    "Heat_1995_720p.mkv",
    "Fargo_1996.mp4",
    "Das_Boot_1981_1080p.mkv",
    "Blade_Runner_1982_2160p.mkv",
    "Der_dritte_Mann_1949.avi",
    "Memento_2000_1080p.mkv",
    "Die_Faelscher_2007_720p.mp4",
    "Arrival_2016_2160p.mkv",
    "Nosferatu_1922.avi",
    "Das_weisse_Band_2009_1080p.mkv",
    "Toni_Erdmann_2016_1080p.mkv",
    "Winterschlaefer_1997.mp4",
    "Lola_rennt_1998_720p.mkv",
    "Die_Blechtrommel_1979_1080p.mkv",
]
```

**B1.1** Geben Sie aus, wie viele Dateien die Liste enthält.

**B1.2** Schreiben Sie eine Funktion `title(filename)`, die den lesbaren Titel liefert, d.h. alles vor dem Punkt und Unterstriche durch Leerzeichen ersetzen.

```python
title("Alien_1979_1080p.mkv")      # Output: 'Alien 1979 1080p'
title("Der_dritte_Mann_1949.avi")  # Output: 'Der dritte Mann 1949'
```

**B1.3** Schreiben Sie eine Funktion `extension(filename)`, die die Dateiendung ohne Punkt liefert. **Hinweis:** Arbeiten Sie mit negativen Indizes.

```python
extension("Alien_1979_1080p.mkv")  # Output: 'mkv'
```

**B1.4** Schreiben Sie eine Funktion `count_extension(files, wanted="mkv")`, die zählt, wie viele Dateien eine bestimmte Endung haben. Die Endung (Parameter) soll weggelassen werden können.

**B1.5** Schreiben Sie eine Funktion `longest(files)`, die den längsten Dateinamen liefert — **mit einer Schleife**, ohne `max`.

**B1.6** Schreiben Sie eine Funktion `report(files)`, die alle Informationen gesammelt ausgibt:

```
15 files found
  mkv: 10
  mp4: 3
  avi: 2
  longest name: Die Blechtrommel 1979 1080p
```

**B1.7** Lösen Sie Aufgabe B1.5 noch einmal in einer Zeile, mit `sorted` und `key`.

**B1.8** Das Jahr steht in jedem Dateinamen als vierstellige Zahl. Schreiben Sie eine Funktion
`year(filename)`, die es als `int` liefert — ohne regular Expressions. 
**Beispiel:** Für `"Nosferatu_1922.avi"` soll `1922` herauskommen.

Geben Sie dann aus, wie viele Filme vor 1990 erschienen sind.

**B1.9** Lassen Sie `pycodestyle` über `scan.py` laufen und beheben Sie, was es meldet.
