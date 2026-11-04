#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Code zu Einheit 4 - Collections, Exceptions

Die Datei hat zwei Teile, wobei der zweite der ist, worum es geht. Den ersten können Sie prinzipiell ignorieren.

1. Das Gerüst (bis etwa Zeile 200). Es sorgt dafür, dass sich einzelne
   Abschnitte starten lassen und dass Fehlerbeispiele die Datei nicht
   abbrechen. Darin stecken Dekoratoren, Kontextmanager und yield, also Konzepte,
   die wir im Unterricht noch nicht gemacht haben.

2. Die Abschnitte (ab Kapitel 1). Das ist der Unterrichtsstoff. Jeder Abschnitt
   ist eine Funktion, deren Name die Nummer trägt: 2.4 heisst a_2_4.
   Unter der Zeile mit def steht in Anführungszeichen, was der
   Abschnitt zeigt.

AUFRUF
    python einheit04.py              alles hintereinander
    python einheit04.py 2            nur Kapitel 2
    python einheit04.py 2.4          nur Abschnitt 2.4
    python einheit04.py 1.5 5.6      mehrere Abschnitte
    python einheit04.py --liste      Inhaltsverzeichnis

Die Datei legt nichts auf der Festplatte an: Kapitel 6 bis 8 arbeiten in
einem temporären Ordner, der danach wieder verschwindet.

    python einheit04.py 6.4 --behalten

lässt diese Ordner stehen und nennt am Ende ihre Pfade - zum Öffnen im
Explorer. Löschen muss man diesen dann selbst.
"""

import contextlib
import io
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# ======================================================================
#  GERÜST
#
#  Alles bis zum nächsten Kapitelbalken ist Maschinerie, kein
#  Lernstoff. Es löst drei Aufgaben:
#
#    1. jeden Abschnitt einzeln startbar machen   -> abschnitt, REGISTER
#    2. Fehlerbeispiele vorführen, ohne dass die
#       Datei abbricht                            -> erwarte
#    3. echte Dateien bereitstellen,
#       ohne etwas zu hinterlassen                -> arbeitsordner
#
#  Dafür werden Konzepte benutzt, die im Unterricht noch nicht behandelt wurden.
#  Sie sind unten erklärt, damit sie nicht rätselhaft bleiben -
#  verstanden haben muss man sie für die Beispiele nicht.
# ======================================================================

# Hier sammelt sich jeder Abschnitt ein, den es in dieser Datei gibt:
# eine Liste von Tripeln (Nummer, Titel, Funktion). Gefüllt wird sie
# weiter unten vom Dekorator..
REGISTER = []

# Schalter --behalten: Arbeitsordner stehen lassen statt löschen.
# GEMERKT sammelt dann die Pfade, damit sie am Ende genannt werden.
BEHALTEN = False
GEMERKT = []


def abschnitt(nummer, titel):
    """Meldet eine Funktion als vorführbaren Abschnitt an.

    Benutzt wird das als Dekorator, also so:

        @abschnitt("2.4", "Sichten")
        def a_2_4():
            ...

    Was dabei passiert: Python liest die Zeile mit def, legt die
    Funktion an - und reicht sie dann an abschnitt("2.4", ...) weiter.
    Die Funktion landet damit in REGISTER und ist auffindbar, ohne dass
    irgendwo unten eine Liste aller Abschnitte gepflegt werden müsste.
    Einen neuen Abschnitt hinzufügen heisst deshalb: Funktion
    schreiben und eine Zeile mit @abschnitt davorsetzen.

    Wichtig fürs Verständnis: Angemeldet heisst nicht ausgeführt.
    Die Funktion selbst läuft erst, wenn main() sie aufruft.
    """
    # Der Dekorator bekommt zuerst nummer und titel, dann erst die
    # Funktion. Deshalb zwei Ebenen: abschnitt(...) liefert deko
    # zurück, und deko bekommt dann die Funktion zu sehen.
    def deko(funktion):
        REGISTER.append((nummer, titel, funktion))
        return funktion          # unverändert zurück - wir sammeln hier nur
    return deko


def kopf(text):
    """Zwischenüberschrift innerhalb eines Abschnitts.

    Rein kosmetisch: Leerzeile, Text, Strich in derselben Länge.
    """
    print()
    print("  " + text)
    print("  " + "-" * len(text))


@contextlib.contextmanager
def erwarte(*typen):
    """Führt Code aus, der eine Exceptions liefert, und zeigt den Fehler.

    Benutzt wird das so:

        with erwarte(TypeError):
            hash([1, 2])

    Ohne diesen Helfer würde die Datei beim ersten Fehlerbeispiel
    abbrechen. So steht der echte Fehlertext in der Ausgabe - nicht ein
    abgeschriebener im Kommentar - und es geht danach weiter.

    Bleibt der Fehler unerwartet aus, wird auch das gemeldet.
    """
    namen = " oder ".join(t.__name__ for t in typen)
    try:
        # yield übergibt die Kontrolle an den Rumpf des with-Blocks.
        # Was dort schiefgeht, landet hier im except - so als stünde
        # der Rumpf an dieser Stelle.
        yield
    except typen as fehler:
        print(f"    -> {type(fehler).__name__}: {fehler}")
    else:
        # else am try läuft nur, wenn nichts geworfen wurde
        print(f"    -> kein Fehler, obwohl {namen} erwartet war!")


@contextlib.contextmanager
def temp_ordner(zweck):
    """Temporärer Ordner. Mit --behalten bleibt er stehen.

    Ohne den Schalter räumt TemporaryDirectory auf, sobald der Block
    endet. Mit dem Schalter legt mkdtemp denselben Ordner an
    und löscht ihn nicht.
    """
    if BEHALTEN:
        name = tempfile.mkdtemp(prefix="demo_e2_")      # räumt nicht auf
        GEMERKT.append((zweck, name))
        print(f"    [{zweck}: {name}]")
        yield name
    else:
        with tempfile.TemporaryDirectory() as name:     # räumt auf
            yield name


@contextlib.contextmanager
def arbeitsordner():
    """Temporärer Ordner mit einer kleinen Beispielsammlung.

    data/collection/Alien_1979.mkv
    data/collection/Fargo_1996.mp4
    data/collection/notizen.txt
    data/collection/serien/Fargo_S01E01.mkv

    Die Dateien sind echt, aber leer gefüllt - nur die Namen und die
    Ordnerstruktur sind wichtig. Benutzt wird das von den Abschnitten 4.3,
    5.3, 6.4 bis 6.7 und 7.2 bis 7.5.
    """
    with temp_ordner("Beispielsammlung") as name:
        wurzel = Path(name)
        sammlung = wurzel / "data" / "collection"
        # parents=True legt data und collection gleich mit an
        (sammlung / "serien").mkdir(parents=True)
        # b"x" * 1024 ergibt 1024 Bytes - die Dateien sollen
        # unterschiedlich gross sein, der Inhalt ist unwichtig
        (sammlung / "Alien_1979.mkv").write_bytes(b"x" * 1024)
        (sammlung / "Fargo_1996.mp4").write_bytes(b"x" * 2048)
        (sammlung / "notizen.txt").write_text("nur ein Hinweis\n",
                                              encoding="utf-8")
        (sammlung / "serien" / "Fargo_S01E01.mkv").write_bytes(b"x" * 512)

        # Wir wechseln in den Ordner hinein. Dadurch funktionieren in
        # den Abschnitten relative Pfade wie "data/collection/..." -
        # genau so, wie sie später im Projektordner stehen würden.
        alt = Path.cwd()
        os.chdir(wurzel)
        try:
            yield wurzel
        finally:
            # finally, damit wir auch nach einem Fehler zurückwechseln.
            # Sonst stünde das Programm danach im falschen Ordner.
            os.chdir(alt)


# ======================================================================
#  1  Sequenzen, Slicing, Unpacking
#
#  Was Listen, Tupel, Zeichenketten und range gemeinsam haben,
#  und was man damit machen kann, ohne eine Schleife zu
#  schreiben.
# ======================================================================

@abschnitt("1.1", "Was ist eine Sequenz")
def a_1_1():
    """Welche Typen Sequenzen sind und was sie gemeinsam haben.

    Sonderfall am Ende: 'abc'[0] ist eine Zeichenkette,
    b'abc'[0] dagegen eine Zahl.
    """
    from collections.abc import Sequence

    kopf("Was alle Sequenzen können")
    # vier Elemente, 'Heat' kommt doppelt vor
    s = ["Alien", "Heat", "Fargo", "Heat"]
    print("len(s)        ", len(s))   # -> 4
    # -> ('Alien', 'Heat')  erstes und letztes Element
    print("s[0], s[-1]   ", (s[0], s[-1]))
    print("s[1:3]        ", s[1:3])   # -> ['Heat', 'Fargo']
    print("'Heat' in s   ", "Heat" in s)   # -> True
    # -> 1   die erste Fundstelle, nicht alle
    print("s.index('Heat')", s.index("Heat"))
    print("s.count('Heat')", s.count("Heat"))   # -> 2
    # -> ('Alien', 'Heat')  alphabetisch, nicht nach Position
    print("min(s), max(s)", (min(s), max(s)))

    kopf("Verketten und Vervielfachen - nicht bei jedem Typ")
    # -> (1, 2)   Tupel lassen sich verketten
    print("(1,) + (2,)   ", (1,) + (2,))
    # -> 'abab'   Zeichenketten auch, durch Vervielfachen
    print("'ab' * 2      ", repr("ab" * 2))
    # range dagegen nicht - der nächsten Zeile fehlt der Operator
    with erwarte(TypeError):
        range(3) + range(2)   # -> TypeError: unsupported operand type(s) for +

    # Schneiden geht bei range sehr wohl: -> range(2, 5)
    print("range(10)[2:5] ", range(10)[2:5])   # geschnitten wird trotzdem

    kopf("Wer gehört dazu")
    # sechs Objekte: Liste, Zeichenkette, Tupel, range, Menge, dict
    for objekt in (["a"], "ab", (1,), range(2), {1}, {1: 2}):
        # True, wenn der Typ als Sequenz gilt
        ist = isinstance(objekt, Sequence)
        # -> die ersten vier True, Menge und Dictionary False:
        # sie haben keine Positionen, über die man zugreifen könnte
        print(f"    {str(objekt):<12} Sequence? {ist}")

    kopf("Der Sonderfall: Zeichenketten und Bytefolgen")
    # -> 'a'   ein Zeichen, aber wieder eine Zeichenkette
    print("'abc'[0]      ", repr("abc"[0]), "   - wieder eine Zeichenkette")
    # -> 1    deshalb hat es selbst eine Länge
    print("len('abc'[0]) ", len("abc"[0]))
    # -> 97   bei bytes kommt eine Zahl heraus, keine Bytefolge
    print("b'abc'[0]     ", b"abc"[0], "        - eine Zahl!")
    # -> b'a'  erst der Ausschnitt liefert wieder bytes
    print("b'abc'[0:1]   ", b"abc"[0:1], "   - erst das Slice ergibt bytes")


@abschnitt("1.2", "Slicing")
def a_1_2():
    """Ausschnitte: Anfang, Ende, Schrittweite, Umkehrung.
    """
    # fünf Elemente auf den Positionen 0 bis 4
    d = ["Alien", "Heat", "Fargo", "Memento", "Arrival"]
    print("d             ", d)   # -> die ganze Liste
    print("d[1:3]        ", d[1:3])   # -> ['Heat', 'Fargo']  ab 1 bis vor 3
    # -> ['Alien', 'Heat']  ohne Angabe beginnt es bei 0
    print("d[:2]         ", d[:2])
    # -> ['Memento', 'Arrival']  negativ zählt von hinten
    print("d[-2:]        ", d[-2:])
    # -> ['Alien', 'Fargo', 'Arrival']  jedes zweite
    print("d[::2]        ", d[::2])
    print("d[::-1]       ", d[::-1])   # -> die ganze Liste rückwaerts

    kopf("Zwei Eigenschaften, auf die man sich verlassen kann")
    print("Slices liegen nie daneben:")
    # -> ['Memento', 'Arrival']  obere Grenze weit daneben, trotzdem kein Fehler
    print("    d[3:99]   ", d[3:99])
    # -> []   untere Grenze daneben: leere Liste
    print("    d[99:]    ", d[99:])
    print("Die Teilungsregel d[:n] + d[n:] == d gilt für jedes n:")
    # prüft n von -2 bis 7, also auch ausserhalb der Liste
    for n in range(-2, 8):
        if d[:n] + d[n:] != d:   # schlägt die Teilungsregel irgendwo fehl?
            print(f"    n={n}: verletzt!")   # wird nie erreicht
            break   # bei einem Gegenbeispiel wäre hier Schluss
    # dieses else gehört zur Schleife, nicht zum if:
    # es läuft nur, wenn kein break kam
    else:
        # -> wird erreicht, die Regel hält
        print("    für alle geprüften n erfüllt")


@abschnitt("1.3", "Zuweisung an ein Slice")
def a_1_3():
    """Ein Slice darf auch links vom Gleichheitszeichen stehen.

    Beim erweiterten Slice muss die Anzahl genau stimmen.
    """
    kopf("Ein Slice ist auch ein Ziel")
    # Ausgangsliste mit fünf Einträgen
    e = ["Alien", "Heat", "Fargo", "Memento", "Arrival"]
    # zwei Elemente (Position 1 und 2) durch ein einziges ersetzen
    e[1:3] = ["X"]
    # -> ['Alien', 'X', 'Memento', 'Arrival']  die Liste wurde kürzer
    print("nach e[1:3] = ['X']  ", e, "  - zwei Elemente durch eines ersetzt")
    del e[1:3]   # del auf einem Slice entfernt den Ausschnitt ganz
    print("nach del e[1:3]      ", e)   # -> ['Alien', 'Arrival']

    kopf("Beim erweiterten Slice muss die Anzahl stimmen")
    # frische Liste - die von oben ist inzwischen verändert
    g = ["Alien", "Heat", "Fargo", "Memento", "Arrival"]
    # [::2] trifft die Positionen 0, 2 und 4, also genau drei Stellen
    g[::2] = ["a", "b", "c"]
    # -> ['a', 'Heat', 'b', 'Memento', 'c']
    print("g[::2] = ['a','b','c']", g)
    # drei Stellen, aber nur ein Wert - das geht nicht
    with erwarte(ValueError):
        # -> ValueError: attempt to assign sequence of size 1 to extended slice
        # of size 3
        g[::2] = ["a"]


@abschnitt("1.4", "Das Slice-Objekt")
def a_1_4():
    """slice(1, 3) als eigenes Objekt
    """
    # dieselbe Liste wie oben
    d = ["Alien", "Heat", "Fargo", "Memento", "Arrival"]
    # der Ausschnitt bekommt einen Namen, statt im Code zu stehen
    JAHR = slice(1, 3)
    # -> slice(1, 3, None)  die Schrittweite blieb offen
    print("JAHR          ", JAHR)
    # -> ['Heat', 'Fargo']  wirkt genau wie d[1:3]
    print("d[JAHR]       ", d[JAHR])
    print()
    print("  Nützlich bei Dateien mit festen Spalten: Der Name steht")
    print("  einmal oben, nicht an zwanzig Stellen im Code.")
    # eine Zeile mit festen Spaltenbreiten, wie aus einer alten Datei
    zeile = "Alien     1979 mkv"
    # drei Spalten, einmal benannt - das ist der eigentliche Gewinn
    TITEL, JAHR2, ENDUNG = slice(0, 10), slice(10, 14), slice(15, 18)
    # -> 'Alien'  strip entfernt die auffüllenden Leerzeichen
    print("    zeile[TITEL]  ", repr(zeile[TITEL].strip()))
    # -> '1979'  als Text, nicht als Zahl
    print("    zeile[JAHR2]  ", repr(zeile[JAHR2]))
    print("    zeile[ENDUNG] ", repr(zeile[ENDUNG]))   # -> 'mkv'


@abschnitt("1.5", "Entpacken")
def a_1_5():
    """Mehrere Namen auf einmal belegen, mit und ohne Stern.
    """
    d = ["Alien", "Heat", "Fargo", "Memento", "Arrival"]   # Ausgangsliste

    kopf("Die Grundregel")
    # zwei feste Namen, alles Weitere sammelt der Stern ein
    erster, zweiter, *rest = d
    print("erster        ", erster)   # -> Alien
    print("zweiter       ", zweiter)   # -> Heat
    print("rest          ", rest)   # -> ['Fargo', 'Memento', 'Arrival']

    kopf("Ohne Stern muss die Anzahl genau stimmen")
    with erwarte(ValueError):   # zwei Namen für fünf Werte
        a, b = d   # -> ValueError: too many values to unpack (expected 2)
    with erwarte(ValueError):   # sechs Namen für fünf Werte
        # -> ValueError: not enough values to unpack (expected 6, got 5)
        a, b, c, e, f, g = d

    kopf("Der Stern liefert immer eine Liste")
    # ein einziges Element, und das geht an erster
    erster, *rest = ["nur eins"]
    # -> []   eine leere Liste, nicht None
    print("rest          ", rest, "    - leere Liste, nicht None")
    x, *mitte, y = (1, 2, 3, 4)   # rechts steht ein Tupel
    # -> [2, 3]  trotzdem eine Liste - der Stern liefert immer eine
    print("mitte         ", mitte, "  - Liste, obwohl rechts ein Tupel stand")
    # Stern in der Mitte: erster und letzter stehen fest
    erster, *mitte, letzter = d
    # -> Alien ['Heat', 'Fargo', 'Memento'] Arrival
    print("erster/mitte/letzter", erster, mitte, letzter)
    print("Zwei Sterne gehen nicht - das sieht schon der Übersetzer:")
    with erwarte(SyntaxError):   # zwei Sterne sind nicht erlaubt
        # compile übersetzt nur, statt auszuführen.
        # So lässt sich ein Syntaxfehler vorführen, ohne dass die
        # Datei selbst nicht mehr startet.
        compile("a, *b, *c = d", "<vorführung>", "exec")

    kopf("Rechts darf alles stehen, was sich durchlaufen lässt")
    # eine Zeichenkette ist durchlaufbar: drei Zeichen, drei Namen
    a, b, c = "abc"
    print("aus 'abc'     ", (a, b, c))   # -> ('a', 'b', 'c')
    a, b = range(2)   # range liefert 0 und 1
    print("aus range(2)  ", (a, b))   # -> (0, 1)
    # ein Generatorausdruck - er wird beim Entpacken abgearbeitet
    a, b = (w.upper() for w in ["mkv", "mp4"])
    print("aus Generator ", (a, b))   # -> ('MKV', 'MP4')
    # popitem liefert ein Paar aus Schlüssel und Wert
    schluessel, wert = {"Alien": 1979}.popitem()
    print("aus popitem   ", (schluessel, wert))   # -> ('Alien', 1979)

    kopf("Verschachtelt")
    # die Klammern links bilden die Klammern rechts nach
    titel, (jahr, endung) = ("Alien", (1979, "mkv"))
    print("titel/jahr/endung", titel, jahr, endung)   # -> Alien 1979 mkv
    # Liste von Paaren, deren zweites Element selbst ein Paar ist
    filme = [("Alien", (1979, "mkv")), ("Heat", (1995, "mp4"))]
    # Entpacken schon in der for-Zeile: drei Namen pro Durchlauf
    for name, (jahr, endung) in filme:
        # -> zwei Zeilen, je Name, Jahr und Endung
        print("    ", name, jahr, endung)

    kopf("Wegwerfnamen")
    # _ ist ein ganz normaler Name - Verabredung für 'brauche ich nicht'
    _, jahr, _ = ("Alien", 1979, "mkv")
    print("nur das Jahr  ", jahr)   # -> 1979
    erster, *_ = d   # *_ sammelt alles Übrige ein, damit es verschwinden kann
    print("nur das erste ", erster)   # -> Alien

    kopf("Mehrfachrueckgabe")

    def groesse_und_anzahl(dateien):
        # zwei Werte nach return ergeben ein Tupel
        return sum(len(n) for n in dateien), len(dateien)

    # hier wird es sofort wieder auseinandergenommen
    gesamt, anzahl = groesse_und_anzahl(d)
    print("gesamt, anzahl", (gesamt, anzahl))   # -> (28, 5)

    kopf("Der Tausch, und warum er funktioniert")
    x, y = 1, 2   # Ausgangswerte
    x, y = y, x   # der Tausch - ohne Hilfsvariable, ohne temp
    print("nach x, y = y, x", (x, y))   # -> (2, 1)
    print("Rechts wird komplett ausgewertet, dann von links nach rechts")
    print("zugewiesen - und das in dieser Reihenfolge:")
    a = [1, 2, 3]   # Liste mit drei Zahlen
    i = 0   # i zeigt auf die erste Stelle
    # achtung: rechts wird (1, 99) gebildet, dann i = 1 gesetzt,
    # und erst danach a[i] = 99 - mit dem neuen i
    i, a[i] = 1, 99
    print("    i             ", i)   # -> 1
    # -> [1, 99, 3]  geändert wurde a[1], nicht a[0]
    print("    a             ", a)
    print("    Zuerst i = 1, danach a[i] = 99 - und i ist da schon 1.")
    print("    Geändert wird also a[1], obwohl i beim Hinschreiben 0 war.")


# Diese drei stehen auf Modulebene, damit in den Fehlermeldungen von
# Abschnitt 1.6 die schlichten Namen erscheinen. In einer verschachtelten
# Funktion schreibt Python stattdessen "a_1_6.<locals>.bericht()".
def bericht(titel, jahr, endung):
    # baut aus drei Teilen einen Dateinamen
    return f"{titel} ({jahr}).{endung}"


def oeffnen(pfad, *, encoding="utf-8"):
    """Alles nach dem nackten Stern lässt sich nur benannt übergeben."""
    # liefert beides zurück, damit man sieht, was angekommen ist
    return pfad, encoding


def laenge(objekt, /):
    """Alles vor dem Schrägstrich lässt sich nur nach Position übergeben."""
    # nichts weiter als len - es geht nur um den Schrägstrich
    return len(objekt)


@abschnitt("1.6", "Entpacken beim Aufruf")
def a_1_6():
    """Dieselben Sterne beim Aufruf: verteilen und einsammeln.

    Dazu * und / in der Signatur.
    """
    kopf("Verteilen beim Aufruf")
    # drei Werte in genau der Reihenfolge der Parameter
    werte = ["Alien", 1979, "mkv"]
    # dieselben drei Werte, aber mit Namen versehen
    paare = {"titel": "Heat", "jahr": 1995, "endung": "mp4"}
    # * verteilt die Liste auf titel, jahr und endung
    # -> Alien (1979).mkv
    print("bericht(*werte)   ", bericht(*werte))
    # ** verteilt das Dictionary über die Namen
    # -> Heat (1995).mp4
    print("bericht(**paare)  ", bericht(**paare))
    # beides gemischt: ein Wert aus der Liste, zwei aus dem Dictionary
    # -> Fargo (1996).mp4
    print("gemischt          ",
          bericht(*["Fargo"], **{"jahr": 1996, "endung": "mp4"}))
    # zwei Sternchen-Listen hintereinander werden aneinandergehängt
    # -> Alien (1979).mkv
    print("zwei Sterne-Listen",
          bericht(*["Alien"], *[1979, "mkv"]))
    print("Die Reihenfolge entscheidet, nicht die Bedeutung:")
    # dieselben drei Werte, andere Reihenfolge - und niemand merkt es:
    # -> 1979 (mkv).Alien
    print("    falsch sortiert", bericht(*[1979, "mkv"], *["Alien"]))
    print("Schlüssel müssen Zeichenketten sein:")
    # Schlüssel 1 ist eine Zahl und taugt nicht als Parametername
    with erwarte(TypeError):
        bericht(**{1: "x"})   # -> TypeError: keywords must be strings

    kopf("Einsammeln in der Definition")

    def zeig(*args, **kwargs):
        # *args sammelt die Positionswerte, **kwargs die benannten
        return args, kwargs

    # -> (('p', 'q'), {'k': 1})
    print("zeig('p','q',k=1) ", zeig("p", "q", k=1))
    # -> ((), {})   beide leer, aber vorhanden
    print("zeig()            ", zeig())
    # -> (('p',), {})  Einertupel, am Komma zu erkennen
    print("zeig('p')         ", zeig("p"), "   - Einertupel mit Komma")
    print("zeig(k=1)         ", zeig(k=1))   # -> ((), {'k': 1})

    kopf("Beides zusammen: durchreichen")

    def mit_protokoll(funktion, *args, **kwargs):
        # zeigt, was durchgereicht wird, bevor es weitergeht
        print(f"    Aufruf von {funktion.__name__} mit {args} {kwargs}")
        # und hier geht es mit denselben Sternen wieder hinaus
        return funktion(*args, **kwargs)

    # -> Alien (1979).mkv, davor die Protokollzeile
    print("liefert           ",
          mit_protokoll(bericht, "Alien", 1979, endung="mkv"))

    kopf("Die Reihenfolge in der Signatur")

    def alles(a, b=2, *rest, c, d=4, **extra):
        # alle Parameterarten in einer einzigen Signatur
        return dict(a=a, b=b, rest=rest, c=c, d=d, extra=extra)

    # der Aufruf verteilt sich auf die sechs Namen
    for name, wert in alles(1, 9, 8, 7, c=3, e=5).items():
        # -> a=1, b=9, rest=(8, 7), c=3, d=4, extra={'e': 5}
        print(f"    {name:<6} {wert!r}")

    kopf("Der nackte Stern - ab hier nur noch benannt")
    print("    def oeffnen(pfad, *, encoding='utf-8')")
    # benannt übergeben - so war es gedacht: -> ('a.txt', 'cp1252')
    print("benannt geht      ", oeffnen("a.txt", encoding="cp1252"))
    with erwarte(TypeError):   # nach Position geht es nicht mehr
        # -> TypeError: oeffnen() takes 1 positional argument but 2 were given
        oeffnen("a.txt", "cp1252")

    kopf("Der Schrägstrich - davor nur noch nach Position")
    print("    def laenge(objekt, /)")
    # nach Position übergeben - so war es gedacht: -> 3
    print("laenge('abc')     ", laenge("abc"))
    with erwarte(TypeError):   # benannt geht es nicht mehr
        # -> TypeError: laenge() got some positional-only arguments passed as
        # keyword arguments
        laenge(objekt="abc")

    kopf("Die drei Fehlermeldungen, die man kennen sollte")
    # jahr kommt zweimal: aus der Liste und aus dem Dictionary
    with erwarte(TypeError):
        # -> TypeError: bericht() got multiple values for argument 'jahr'
        bericht(*["Alien", 1979], **{"jahr": 1980, "endung": "mkv"})
    with erwarte(TypeError):   # extra passt auf keinen Parameter
        # -> TypeError: bericht() got an unexpected keyword argument
        bericht(**{"titel": "x", "jahr": 1, "endung": "y", "extra": 9})
    with erwarte(TypeError):   # endung fehlt ganz
        # -> TypeError: bericht() missing 1 required positional argument
        bericht(*["Alien", 1979])

    kopf("Zusammenbauen statt verteilen")
    a, b = [1, 2], [3]   # zwei Listen
    # -> [1, 2, 3]  die Sterne packen beide aus
    print("[*a, *b]          ", [*a, *b])
    # -> (1, 2, 3)  dieselben Werte als Tupel
    print("(*a, *b)          ", (*a, *b))
    print("{*a, *b}          ", {*a, *b})   # -> {1, 2, 3}  und als Menge
    # zwei Dictionaries mit dem gemeinsamen Schlüssel x
    d1, d2 = {"x": 1}, {"y": 2, "x": 9}
    # -> {'x': 9, 'y': 2}
    print("{**d1, **d2}      ", {**d1, **d2}, " - der rechte gewinnt")


@abschnitt("1.7", "+= ist nicht +")
def a_1_7():
    """+= verlängert die vorhandene Liste, + baut eine neue."""
    kopf("+= verlaengert das vorhandene Objekt")
    a = ["Alien"]   # eine Liste mit einem Eintrag
    b = a   # b zeigt auf dasselbe Objekt - das ist keine Kopie
    a += ["Heat"]   # += verlängert das vorhandene Objekt an Ort und Stelle
    print("a             ", a)   # -> ['Alien', 'Heat']
    # -> ['Alien', 'Heat']  b hat sich mitverändert
    print("b             ", b, "  - mitgewandert, es ist dasselbe Objekt")
    # -> True   es ist ein und dasselbe Objekt
    print("a is b        ", a is b)

    kopf("+ erzeugt ein neues Objekt")
    a2 = ["Alien"]   # wieder eine Liste mit einem Eintrag
    b2 = a2   # wieder zeigen beide Namen auf dasselbe Objekt
    # + baut eine neue Liste; a2 zeigt danach auf diese neue
    a2 = a2 + ["Heat"]
    print("a2            ", a2)   # -> ['Alien', 'Heat']
    # -> ['Alien']  b2 blieb beim alten Objekt
    print("b2            ", b2, "          - unverändert")
    print("a2 is b2      ", a2 is b2)   # -> False  zwei verschiedene Objekte

    kopf("Bei Tupeln fällt der Unterschied nicht auf")
    t = (1,)   # ein Tupel mit einem Eintrag
    u = t   # u zeigt auf dasselbe Tupel
    t += (2,)   # += auf einem Tupel kann nicht verlängern, also baut es neu
    print("t             ", t)   # -> (1, 2)
    # -> (1,)   u blieb unverändert
    print("u             ", u, "               - Tupel sind unveränderlich,")
    print("                 also muss += hier ein neues Objekt bauen")


# ======================================================================
#  2  dict, set, Hashing, Reihenfolge
#
#  Die beiden Sammlungen, die ueber Schluessel arbeiten statt
#  ueber Positionen. Die Leitfrage des Kapitels: Warum duerfen
#  nur bestimmte Objekte Schluessel sein?
# ======================================================================

@abschnitt("2.1", "dict, hashbar, set, frozenset")
def a_2_1():
    """Die vier Begriffe des Kapitels an kleinen Beispielen.
    """
    kopf("Das Dictionary")
    # ein Dictionary: Titel als Schlüssel, Minuten als Wert
    laufzeit = {"Alien": 117, "Heat": 170}
    # -> 117   Zugriff über den Schluessel, nicht über eine Position
    print("laufzeit['Alien']  ", laufzeit["Alien"])
    # ein unbekannter Schlüssel wird beim Zuweisen angelegt
    laufzeit["Fargo"] = 98
    # -> {'Alien': 117, 'Heat': 170, 'Fargo': 98}
    print("nach dem Anlegen   ", laufzeit)
    del laufzeit["Heat"]   # del entfernt den Eintrag ganz
    print("nach dem Entfernen ", laufzeit)   # -> {'Alien': 117, 'Fargo': 98}
    # -> 2   len zählt die Einträge, nicht die Werte
    print("len(laufzeit)      ", len(laufzeit))
    print("'Fargo' in laufzeit", "Fargo" in laufzeit)   # -> True
    # -> False  in sucht nur unter den Schlüsseln
    print("98 in laufzeit     ", 98 in laufzeit,
          "  - 98 ist ein Wert, kein Schlüssel")
    # aus einer Liste von Paaren -> {'a': 1, 'b': 2}
    print("dict([('a',1)])    ", dict([("a", 1), ("b", 2)]))
    # oder mit Schlüsselwortargumenten -> dasselbe Ergebnis
    print("dict(a=1, b=2)     ", dict(a=1, b=2))

    kopf("Hashbar")
    # Achtung beim zweiten Start: Diese Zahl ist jedes Mal eine andere.
    # Python würfelt den Hash von Zeichenketten je Programmlauf neu
    # (seit 3.3, als Schutz vor einem Angriff). Innerhalb eines Laufs
    # bleibt er gleich - und nur darauf kommt es an. Deshalb darf ein
    # Hash auch nie in einer Datei oder Datenbank landen.
    print("hash('Alien')      ", hash("Alien"))
    # eine Liste lässt sich nicht hashen, weil sie sich ändern kann
    with erwarte(TypeError):
        hash([1, 2])   # -> TypeError: unhashable type: 'list'
    print("Gleiche Zahlen haben denselben Hash - mit Folgen:")
    # -> True   int und float sind hier gleich
    print("    5 == 5.0       ", 5 == 5.0)
    # -> True   und darum auch im Hash
    print("    hash(5)==hash(5.0)", hash(5) == hash(5.0))
    # -> {1: 'c'}  ein einziger Eintrag statt drei!
    # 1, 1.0 und True sind für das Dictionary derselbe Schlüssel,
    # also überschreiben sich die drei Zuweisungen gegenseitig
    print("    {1:'a', 1.0:'b', True:'c'} ->", {1: "a", 1.0: "b", True: "c"})
    print("    ein einziger Eintrag: 1, 1.0 und True sind derselbe Schlüssel")

    kopf("Die Menge")
    # -> {'mkv', 'mp4'}  die Dublette fällt weg
    print("{'mkv','mp4','mkv'}", {"mkv", "mp4", "mkv"})
    # eine Menge in einer Menge geht nicht: sie ist veränderlich
    with erwarte(TypeError):
        {{"a"}}   # -> TypeError: unhashable type: 'set'

    kopf("frozenset")
    f = frozenset({"mkv", "mp4"})   # frozenset ist die unveränderliche Menge
    print("f                  ", f)   # -> frozenset({'mkv', 'mp4'})
    with erwarte(AttributeError):   # add gibt es hier gar nicht erst
        # -> AttributeError: 'frozenset' object has no attribute 'add'
        f.add("avi")
    # darum darf ein frozenset in einer Menge stehen
    print("Mengen in Mengen   ", {frozenset({"a"}), frozenset({"b"})})
    print("frozenset als Schlüssel",   # und auch als Schlüssel dienen
          {frozenset({"mkv", "mp4"}): "Videoformate"})


@abschnitt("2.2", "Warum Schlüssel hashbar sein müssen")
def a_2_2():
    """Warum nur unveränderliche Objekte Schlüssel sein dürfen.
    """
    kopf("Was geht und was nicht")
    # drei Objekte, die sich hashen lassen - samt Beschriftung
    for ausdruck, objekt in [("'Alien'", "Alien"), ("(1, 2)", (1, 2)),
                             ("frozenset({1, 2})", frozenset({1, 2}))]:
        # -> eine grosse Zahl je Objekt, die Zahl selbst ist belanglos
        print(f"    hash({ausdruck:<18}) = {hash(objekt)}")
    # vier Objekte, die sich nicht hashen lassen
    for ausdruck, objekt in [("[1, 2]", [1, 2]), ("{1}", {1}),
                             ("{'a': 1}", {"a": 1}), ("(1, [2])", (1, [2]))]:
        print(f"    hash({ausdruck})")   # zuerst die Beschriftung ausgeben,
        # dann den Fehler dazu - so stehen beide untereinander
        with erwarte(TypeError):
            # -> TypeError: unhashable type: 'list' / 'set' / 'dict' / 'list'
            hash(objekt)

    kopf("Hashbarkeit vererbt sich an den Inhalt")
    print("    Ein Tupel ist nur hashbar, wenn alles darin hashbar ist.")
    print("    Deshalb scheitert (1, [2]) - die Liste darin steckt an.")

    kopf("Hashing ist der Grund für die Geschwindigkeit")
    import timeit   # timeit misst kurze Codestücke, hier ganz lokal gebraucht
    menge = set(range(100_000))   # 100.000 Zahlen in einer Menge
    liste = list(range(100_000))   # dieselben 100.000 in einer Liste
    # Gesucht wird das letzte Element - der schlechteste Fall für die Liste.
    # gesucht wird die letzte Zahl - für die Liste der schlechteste Fall
    t_set = timeit.timeit(lambda: 99_999 in menge, number=1_000)
    # dieselbe Suche, nur in der Liste
    t_list = timeit.timeit(lambda: 99_999 in liste, number=1_000)
    # -> etwa 0,1 Mikrosekunden - unabhängig von der Grösse
    print(f"    je Suche im set    {t_set / 1_000 * 1e6:8.3f} Mikrosekunden")
    # -> einige hundert Mikrosekunden - sie muss alles durchgehen
    print(f"    je Suche in der Liste {t_list / 1_000 * 1e6:8.1f} "
          f"Mikrosekunden")
    # -> ein vierstelliger Faktor. Die Menge rechnet aus der Zahl
    # aus, in welchem Fach sie liegen müsste, und sieht nur dort
    # nach. Genau dafür braucht sie den Hash.
    print(f"    Faktor             {t_list / t_set:8.0f}")
    print("    Die Liste muss suchen, die Menge rechnet die Stelle aus.")


@abschnitt("2.3", "Einfügereihenfolge ist keine Sortierung")
def a_2_3():
    """Die Einfügereihenfolge bleibt erhalten - sortiert ist
    das Dictionary deshalb noch lange nicht.
    """
    d1 = {"b": 1, "a": 2}   # b wurde zuerst eingefügt
    d2 = {"a": 2, "b": 1}   # dieselben Paare, umgekehrt eingefügt
    print("d1                 ", d1)   # -> {'b': 1, 'a': 2}
    # -> ['b', 'a']  die Reihenfolge des Einfügens bleibt erhalten
    print("list(d1)           ", list(d1), "   - Reihenfolge des Einfügens")
    # -> {'a': 2, 'b': 1}  andere Reihenfolge
    print("d2                 ", d2)
    # -> True   für den Vergleich zählt nur, was drinsteht
    print("d1 == d2           ", d1 == d2,
          "       - Reihenfolge zählt beim Vergleich nicht")
    # sorted sortiert die Paare, dict baut daraus ein neues Dictionary
    # -> {'a': 2, 'b': 1}
    print("sortiert           ", dict(sorted(d1.items())))
    print()
    print("  Nach Wert sortieren geht über key=:")
    # drei Filme mit Laufzeit
    laufzeit = {"Alien": 117, "Heat": 170, "Fargo": 98}
    # key= bestimmt, wonach sortiert wird: paar[1] ist der Wert
    # -> {'Fargo': 98, 'Alien': 117, 'Heat': 170}
    print("    ", dict(sorted(laufzeit.items(), key=lambda paar: paar[1])))


@abschnitt("2.4", "Sichten")
def a_2_4():
    """keys(), values() und items() liefern Sichten, keine Listen.
    """
    d = {"Alien": 1979, "Heat": 1995}   # zwei Einträge
    # -> dict_keys([...])  keine Liste, sondern eine Sicht
    print("d.keys()           ", d.keys())
    print("d.values()         ", d.values())   # -> dict_values([...])
    # -> dict_items([...])  Paare aus Schlüssel und Wert
    print("d.items()          ", d.items())

    kopf("Sichten sind lebendig")
    sicht = d.keys()   # die Sicht wird jetzt geholt, vor der Änderung
    d["Fargo"] = 1996   # und jetzt kommt ein Eintrag dazu
    # -> ['Alien', 'Heat', 'Fargo']  die Sicht kennt ihn trotzdem:
    # sie zeigt auf das Dictionary, nicht auf eine Kopie
    print("nach dem Einfügen ", list(sicht),
          " - die vorher geholte Sicht kennt den neuen Schlüssel")
    # -> 3   auch die Länge ist aktuell
    print("len(sicht)         ", len(sicht))
    # -> True  und in funktioniert wie bei einer Sammlung
    print("'Alien' in sicht   ", "Alien" in sicht)

    kopf("Verändern während des Durchlaufens geht schief")
    # weil die Sicht mitwächst, merkt Python die Änderung
    with erwarte(RuntimeError):
        # diese Schleife läuft über das Dictionary selbst,
        for schluessel in d:
            # und hier kommen Einträge dazu - das geht nicht zusammen
            # -> RuntimeError: dictionary changed size during iteration
            d["neu_" + schluessel] = 0
    print("    Abhilfe: über eine echte Kopie der Schlüssel laufen")
    # zweiter Versuch mit einem frischen Dictionary
    e = {"Alien": 1979, "Heat": 1995}
    # list() kopiert die Schlüssel in eine eigene Liste;
    # über diese Kopie lässt sich gefahrlos laufen
    for schluessel in list(e.keys()):
        # jetzt stört das Einfügen niemanden mehr
        e["neu_" + schluessel] = 0
    print("    ", sorted(e))   # -> ['Alien', 'Heat', 'neu_Alien', 'neu_Heat']

    kopf("Sichten auf Schlüsseln sind mengenartig")
    # -> {'Alien'}  Schnittmenge: was in beiden vorkommt
    print("d.keys() & {...}   ", d.keys() & {"Alien", "Gandhi"})
    # -> alle Schluessel plus Gandhi
    print("d.keys() | {...}   ", sorted(d.keys() | {"Gandhi"}))
    # -> alle ausser Alien
    print("d.keys() - {...}   ", sorted(d.keys() - {"Alien"}))
    print("Mit values() geht das nicht:")
    # Werte dürfen mehrfach vorkommen und müssen nicht hashbar sein
    with erwarte(TypeError):
        d.values() & {1979}   # -> TypeError: unsupported operand type(s) for &

    kopf("Wozu das taugt: zwei Dictionaries vergleichen")
    alt = {"Alien": 1979, "Heat": 1995}   # der alte Stand
    # der neue Stand: Heat geändert, Fargo neu
    neu = {"Alien": 1979, "Heat": 1996, "Fargo": 1996}
    # -> ['Fargo']  was im neuen steht und im alten nicht
    print("neu hinzugekommen  ", sorted(neu.keys() - alt.keys()))
    # -> []   nichts weggefallen
    print("weggefallen        ", sorted(alt.keys() - neu.keys()))
    # gemeinsame Schlüssel durchgehen und die Werte vergleichen
    # -> ['Heat']
    print("geändert          ", sorted(k for k in alt.keys() & neu.keys()
                                        if alt[k] != neu[k]))


@abschnitt("2.5", "Mengen")
def a_2_5():
    """Die vier Mengenoperatoren, und warum {} keine leere
    Menge ist.
    """
    A, B = {1, 2, 3}, {3, 4}   # zwei Mengen mit der gemeinsamen 3
    print("A, B               ", A, B)   # -> {1, 2, 3} {3, 4}
    print("A & B  Schnitt     ", A & B)   # -> {3}   nur das Gemeinsame
    # -> {1, 2, 3, 4}  alles aus beiden, jedes einmal
    print("A | B  Vereinigung ", A | B)
    # -> {1, 2}  was in A steht und nicht in B
    print("A - B  Differenz   ", A - B)
    # -> {1, 2, 4}  was in genau einer von beiden steht
    print("A ^ B  symmetrisch ", A ^ B)

    kopf("Die Stolperstelle beim Anlegen")
    # -> <class 'dict'>  geschweifte Klammern allein ergeben ein Dictionary
    print("type({})           ", type({}), "   - nicht die leere Menge!")
    # -> <class 'set'>  die leere Menge braucht set()
    print("type(set())        ", type(set()), "    - so schreibt man sie")

    kopf("Ein typischer Einsatz")
    vorhanden = {"Alien_1979.mkv", "Heat_1995.mp4"}   # was tatsächlich da ist
    erwartet = {"Alien_1979.mkv", "Fargo_1996.mp4"}   # was da sein sollte
    # -> {'Fargo_1996.mp4'}  erwartet, aber nicht vorhanden
    print("fehlt              ", erwartet - vorhanden)
    # -> {'Heat_1995.mp4'}  vorhanden, aber nicht erwartet
    print("ueberzaehlig       ", vorhanden - erwartet)


@abschnitt("2.6", "Comprehensions")
def a_2_6():
    """Dictionary und Menge lassen sich genauso kurz aufbauen

    wie eine Liste.
    """
    # Schlüssel aus der Liste, Wert aus len()
    # -> {'Alien': 5, 'Heat': 4}
    print("dict-Comprehension ",
          {k: len(k) for k in ["Alien", "Heat"]})
    # ohne Doppelpunkt wird es eine Menge - 5 und 4, je einmal
    # -> {4, 5}
    print("set-Comprehension  ",
          {len(k) for k in ["Alien", "Heat"]})
    print()
    print("  Beides zusammen mit einer Bedingung:")
    laufzeit = {"Alien": 117, "Heat": 170, "Fargo": 98}   # Ausgangsdictionary
    # if am Ende filtert: nur Werte über 100
    # -> {'Alien': 117, 'Heat': 170}
    print("    lang           ",
          {k: v for k, v in laufzeit.items() if v > 100})
    # Schlüssel und Wert tauschen die Plätze
    # -> {117: 'Alien', 170: 'Heat', 98: 'Fargo'}
    print("    umgedreht      ",
          {v: k for k, v in laufzeit.items()})


@abschnitt("2.7", "Zusammenführen und Entfernen")
def a_2_7():
    """Zusammenführen mit | und |=, entfernen mit pop und
    popitem.
    """
    kopf("Die Merge-Operatoren, seit Python 3.9")
    # beide haben den Schlüssel a, mit verschiedenen Werten
    d1, d2 = {"a": 1}, {"b": 2, "a": 9}
    # -> {'a': 9, 'b': 2}  bei a gewinnt der rechte Operand
    print("d1 | d2            ", d1 | d2, " - der rechte gewinnt")
    # -> {'a': 1}  d1 selbst blieb unberührt, es entstand ein neues
    print("d1                 ", d1, "        - unverändert")
    d3 = {"a": 1}   # ein drittes Dictionary zum Vergleich
    d3 |= d2   # |= verändert das linke an Ort und Stelle, statt neu zu bauen
    # -> {'a': 9, 'b': 2}  derselbe Inhalt, aber dasselbe Objekt
    print("nach d3 |= d2      ", d3, " - an Ort und Stelle verändert")
    # -> {'a': 9, 'b': 2}  die Schreibweise von vor Python 3.9
    print("die aeltere Form   ", {**d1, **d2})

    kopf("Entfernen")
    e = {"a": 1, "b": 2}   # zwei Einträge
    # -> None  pop mit Ersatzwert meldet den fehlenden Schlüssel nicht
    print("e.pop('z', None)   ", e.pop("z", None), "       - Ersatzwert")
    with erwarte(KeyError):   # ohne Ersatzwert sieht es anders aus
        e.pop("z")   # -> KeyError: 'z'
    # -> ('b', 2)  popitem nimmt das zuletzt eingefügte Paar
    print("e.popitem()        ", e.popitem(),
          "  - das zuletzt eingefügte Paar")
    print("e                  ", e)   # -> {'a': 1}  b ist jetzt heraus
    print("Auf dem leeren Dictionary:")
    # auf einem leeren Dictionary gibt es nichts zu nehmen
    with erwarte(KeyError):
        {}.popitem()   # -> KeyError: 'popitem(): dictionary is empty'


# ======================================================================
#  3  Counter, defaultdict, setdefault, get
#
#  Vier Werkzeuge für denselben Fall: Der Schlüssel ist
#  vielleicht noch nicht da. Sie unterscheiden sich darin, was
#  dabei mit dem Dictionary passiert.
# ======================================================================

@abschnitt("3.1", "Die vier Werkzeuge im Vergleich")
def a_3_1():
    """get, setdefault, defaultdict und Counter nebeneinander.

    Die Frage bei allen vieren: wird dabei etwas angelegt?
    """
    # beide kommen aus collections, beide erben von dict
    from collections import Counter, defaultdict

    print("  Alle lösen dasselbe Problem: ein Schlüssel, der vielleicht")
    print("  noch nicht existiert. Sie unterscheiden sich darin, was dabei")
    print("  mit dem Dictionary passiert.")
    print()
    d = {"Alien": 117}   # ein Eintrag
    print("Ausgangslage       ", d)   # -> {'Alien': 117}
    # -> 0 und das Dictionary danach unverändert
    print("d.get('Heat', 0)   ", d.get("Heat", 0), "  ->", d)
    # -> 0, aber jetzt steht Heat drin - das ist der Unterschied
    print("d.setdefault(...)  ", d.setdefault("Heat", 0), "  ->", d)
    dd = defaultdict(int)   # ein defaultdict mit int als Fabrik
    dd["Fargo"]   # nur gelesen, nichts zugewiesen
    # -> {'Fargo': 0}  und trotzdem angelegt
    print("defaultdict-Zugriff", "        ->", dict(dd))
    c = Counter()   # ein Counter, auch mit 0 als Ersatzwert
    c["Fargo"]   # wieder nur gelesen
    # -> {}  hier wurde nichts angelegt. Counter und defaultdict
    # verhalten sich an genau dieser Stelle verschieden.
    print("Counter-Zugriff    ", "        ->", dict(c),
          " - liest, ohne anzulegen")


@abschnitt("3.2", "get gegen setdefault")
def a_3_2():
    """Der Unterschied in zwei Zeilen: get liest nur,
    setdefault schreibt auch.
    """
    m = {"Alien": 117}   # ein Eintrag
    print("m                  ", m)   # -> {'Alien': 117}
    print("m.get('Heat', 0)   ", m.get("Heat", 0))   # -> 0   der Ersatzwert
    # -> {'Alien': 117}  nichts dazugekommen
    print("m danach           ", m, "      - unberührt")
    # -> 0   derselbe Rückgabewert wie oben
    print("m.setdefault('Heat', 0)", m.setdefault("Heat", 0))
    # -> {'Alien': 117, 'Heat': 0}  aber der Schlüssel steht jetzt drin
    print("m danach           ", m, " - der Schlüssel steht jetzt drin")

    kopf("Wo setdefault wirklich hilft")
    nach_endung = {}   # leeres Dictionary zum Einsortieren
    for name in ["Alien.mkv", "Heat.mp4", "Fargo.mkv"]:   # drei Dateinamen
        # rsplit teilt von hinten, [1] ist der Teil nach dem letzten Punkt
        endung = name.rsplit(".", 1)[1]
        # setdefault liefert die vorhandene Liste oder legt eine an -
        # und append hängt gleich daran. Eine Zeile statt dreier.
        nach_endung.setdefault(endung, []).append(name)
    # -> {'mkv': ['Alien.mkv', 'Fargo.mkv'], 'mp4': ['Heat.mp4']}
    print("    ", nach_endung)
    print("    Eine Zeile statt Prüfung, Anlegen und Anhängen.")


@abschnitt("3.3", "defaultdict")
def a_3_3():
    """Die Fabrik erzeugt fehlende Werte - und legt sie dabei an.
    """
    from collections import defaultdict   # defaultdict kommt aus collections

    kopf("Die Fabrik erzeugt fehlende Werte")
    # list ist die Fabrik: fehlende Werte werden zu einer Liste
    nach_endung = defaultdict(list)
    # kein Anlegen, kein Prüfen - direkt anhängen
    nach_endung["mkv"].append("Alien")
    print("    ", dict(nach_endung))   # -> {'mkv': ['Alien']}

    kopf("Als Fabrik eignet sich jeder Typ und jede Funktion ohne Argumente")
    # -> []   list() als Fabrik
    print("defaultdict(list)['x'] ", defaultdict(list)["x"])
    # -> 0    int() liefert 0 - praktisch zum Zaehlen
    print("defaultdict(int)['x']  ", defaultdict(int)["x"], "  - zum Zählen")
    print("defaultdict(set)['x']  ", defaultdict(set)["x"])   # -> set()
    print("defaultdict(dict)['x'] ", defaultdict(dict)["x"])   # -> {}
    # ein lambda liefert jeden beliebigen festen Startwert
    # -> unbekannt
    print("lambda: 'unbekannt'    ",
          defaultdict(lambda: "unbekannt")["x"])
    # ein zweites Argument füllt das Dictionary vor
    # -> {'a': [1]}
    print("vorgefuellt            ",
          dict(defaultdict(list, {"a": [1]})))
    print()
    print("  Wichtig: die Fabrik erzeugt die Werte NEU. Deshalb bekommt")
    print("  jeder Schlüssel seine eigene Liste - und nicht alle dieselbe.")
    g = defaultdict(list)   # neues defaultdict
    g["a"].append(1)   # a bekommt seine eigene Liste
    g["b"].append(2)   # b bekommt eine zweite, eigene Liste
    # -> {'a': [1], 'b': [2]}  nicht etwa beide dieselbe Liste
    print("    ", dict(g))

    kopf("Der Fallstrick: schon das Lesen legt an")
    leer = defaultdict(int)   # ein frisches defaultdict, noch leer
    # nur lesen, nichts zuweisen - und genau das legt den Schlüssel an
    leer["unbekannt"]
    # -> {'unbekannt': 0} und len = 1
    print("nach dem reinen Lesen  ", dict(leer), "  len =", len(leer))
    print("    Besonders unangenehm in Prüfungen wie 'if leer[\"x\"]:' -")
    print("    die Bedingung ist falsch, der Schlüssel steht danach drin.")
    # get und in lesen wirklich nur: -> None und False
    print("    Nachsehen ohne Anlegen:", leer.get("noch_unbekannt"),
          "/", "noch_unbekannt" in leer)

    kopf("Zurueck zum normalen Dictionary")
    # -> {'mkv': ['Alien']}  dict() baut ein gewöhnliches daraus
    print("dict(nach_endung)      ", dict(nach_endung))
    # die Fabrik abschalten geht auch nachträglich
    nach_endung.default_factory = None
    # ab jetzt verhält es sich wie ein normales Dictionary
    with erwarte(KeyError):
        nach_endung["gibtsnicht"]   # -> KeyError: 'gibtsnicht'
    print("    Die erste Form ist sinnvoll, bevor man das Ergebnis")
    print("    weitergibt - dann kann niemand versehentlich anlegen.")


@abschnitt("3.4", "Counter")
def a_3_4():
    """Zählen mit Counter, samt Rechnen mit Zählern."""
    from collections import Counter   # Counter kommt ebenfalls aus collections

    # zählt beim Anlegen durch, was in der Liste steht
    c = Counter(["mkv", "mkv", "mp4"])
    print("c                  ", c)   # -> Counter({'mkv': 2, 'mp4': 1})
    # -> 0   ein fehlender Schlüssel zählt als null
    print("c['avi']           ", c["avi"], "       - fehlende sind 0")
    # -> False  er wurde dabei aber nicht angelegt
    print("'avi' in c         ", "avi" in c,
          "   - und wurden nicht angelegt")
    # -> [('mkv', 2)]  die häufigsten, hier nur der erste
    print("c.most_common(1)   ", c.most_common(1))
    # -> 3   die Summe aller Zähler
    print("c.total()          ", c.total(), "       - ab Python 3.10")

    kopf("Rechnen mit Counters")
    # -> Counter({'a': 2, 'b': 2, 'c': 1})  Zähler werden addiert
    print("Counter('aab') + Counter('bc')", Counter("aab") + Counter("bc"))
    # -> Counter({'a': 1})  b fällt auf 0 und verschwindet dabei ganz
    print("Counter('aab') - Counter('ab')", Counter("aab") - Counter("ab"))
    print("    Minus lässt nur positive Zähler stehen.")

    kopf("Der häufigste Einsatz")
    # fünf Dateinamen, darunter eine Textdatei
    dateien = ["Alien_1979.mkv", "Heat_1995.mp4", "Fargo_1996.mkv",
               "Gandhi_1982.mkv", "notizen.txt"]
    # Path(n).suffix liefert '.mkv' samt Punkt;
    # der Generatorausdruck spart die Zwischenliste
    verteilung = Counter(Path(n).suffix for n in dateien)
    print("    ", verteilung)   # -> Counter({'.mkv': 3, '.mp4': 1, '.txt': 1})
    # most_common() ohne Zahl liefert alles, absteigend sortiert
    for endung, anzahl in verteilung.most_common():
        # ein Balken je Vorkommen - '#' * 3 ergibt '###'
        print(f"    {endung:<6} {'#' * anzahl} {anzahl}")


@abschnitt("3.5", "Was wann")
def a_3_5():
    """Entscheidungshilfe:"""
    print("  nur lesen, nichts anlegen        -> d.get(k, ersatz)")
    print("  einmal anlegen und weiterarbeiten -> d.setdefault(k, wert)")
    print("  durchgehend gruppieren oder sammeln -> defaultdict(fabrik)")
    print("  zählen                          -> Counter")
    print()
    print("  Die Faustregel: defaultdict beim Aufbauen einer Struktur,")
    print("  get beim Nachsehen in einer fertigen.")

# ======================================================================
#  ABLAUFSTEUERUNG
#
#  Der Teil, der entscheidet, welche Abschnitte laufen.
# ======================================================================

def liste():
    """Gibt das Inhaltsverzeichnis aus (Aufruf mit --liste).

    Zwischen zwei Kapiteln kommt eine Leerzeile. Erkannt wird der
    Kapitelwechsel daran, dass sich der Teil vor dem Punkt ändert.
    """
    print("Code Einheit 4 - Abschnitte")
    print()
    kapitel = None
    for nummer, titel, _f in REGISTER:
        if nummer.split(".")[0] != kapitel:
            kapitel = nummer.split(".")[0]
            print()
        print(f"  {nummer:<6} {titel}")
    print()
    print("Aufruf: python einheit04.py [Nummer ...]")


def ausgewaehlt(wuensche):
    """Sucht die gewünschten Abschnitte aus REGISTER heraus.

    Ohne Wunsch kommt alles. "2" trifft das ganze Kapitel 2, "2.4"
    nur diesen einen Abschnitt. Die Reihenfolge ist immer die der
    Datei, nicht die der Eingabe.
    """
    if not wuensche:
        return list(REGISTER)
    treffer = []
    for nummer, titel, funktion in REGISTER:
        for wunsch in wuensche:
            # "2" soll 2.1 bis 2.7 treffen, aber nicht 12.1 -
            # darum der Punkt in der zweiten Bedingung
            if nummer == wunsch or nummer.startswith(wunsch + "."):
                treffer.append((nummer, titel, funktion))
                break        # dieser Abschnitt ist drin, nächster
    return treffer


def main(argumente):
    """Wertet die Kommandozeile aus und führt die Abschnitte vor.

    Liefert den Rückgabewert des Programms: 0 heisst in Ordnung,
    alles andere heisst Fehler. Das wertet die Kommandozeile aus,
    nicht Python.
    """
    global BEHALTEN      # nur hier wird der Schalter gesetzt

    if "--liste" in argumente or "-l" in argumente:
        liste()
        return 0

    BEHALTEN = "--behalten" in argumente or "-b" in argumente
    # Alles, was mit - beginnt, ist ein Schalter und keine Nummer
    treffer = ausgewaehlt([a for a in argumente if not a.startswith("-")])
    if not treffer:
        print("Kein Abschnitt passt. Übersicht mit --liste.")
        return 1

    for nummer, titel, funktion in treffer:
        print()
        print("=" * 70)
        print(f" {nummer}  {titel}")
        print("=" * 70)
        funktion()       # hier erst läuft der Abschnitt wirklich
    print()
    print("=" * 70)
    print(f" {len(treffer)} Abschnitt(e) vorgeführt.")

    if GEMERKT:
        print()
        print(f" {len(GEMERKT)} Ordner stehen geblieben - bitte selbst")
        print(" löschen, wenn sie nicht mehr gebraucht werden:")
        for zweck, name in GEMERKT:
            print(f"   {name}      ({zweck})")
    return 0


# Dieser Block ist der Schalter zwischen "gestartet" und "importiert".
# Beim Start steht in __name__ der Text "__main__", und main() läuft.
# Wer die Datei dagegen importiert, bekommt nur die Funktionen - es
# geht nichts von selbst los. Abschnitt 8.5 führt genau das vor.
#
# Ohne diesen Block passiert beim Start gar nichts: Alle Funktionen
# wären angelegt, aber keine aufgerufen.
#
# sys.argv ist die Kommandozeile als Liste. An Stelle 0 steht der
# Dateiname selbst, deshalb [1:] - uns interessiert nur der Rest.
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))