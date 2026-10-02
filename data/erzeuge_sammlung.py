"""Erzeugt die Uebungssammlung fuer den Kurs: rund 5000 leere Dateien.

Aufruf:

    python daten/erzeuge_sammlung.py
    python daten/erzeuge_sammlung.py --ziel daten/sammlung --anzahl 5000

Die Dateien sind leer (0 Byte). Es geht ausschliesslich um die Namen und
die Ordnerstruktur. Der Startwert ist fest, das Ergebnis also auf jedem
Rechner gleich.

Absichtlich eingebaut sind die Faelle, an denen die Uebungen der folgenden
Einheiten haengen: verschiedene Benennungsschemata, eine Dublette, Umlaute
in zwei Kodierungen, fehlende Jahreszahlen, verwaiste Begleitdateien,
Bruchstuecke, ein Sample-Ordner, ein sehr langer Name, Serienfolgen und
ein Titel mit Komma.
"""

import argparse
import random
import sys
import unicodedata
from pathlib import Path

STARTWERT = 20261002

TITEL = [
    "Alien", "Heat", "Fargo", "Das Boot", "Blade Runner", "Der dritte Mann",
    "Memento", "Die Faelscher", "Arrival", "Nosferatu", "Das weisse Band",
    "Toni Erdmann", "Winterschlaefer", "Lola rennt",
    "Die Blechtrommel", "Der Himmel ueber Berlin", "Good Bye Lenin",
    "Sophie Scholl", "Die Welle", "Das Leben der Anderen",
    "Lauf Lola lauf", "Knockin on Heavens Door", "Der Untergang",
    "Rossini", "Bang Boom Bang", "Lammbock", "Absolute Giganten",
    "Jenseits der Stille", "Nirgendwo in Afrika",
    "Der Baader Meinhof Komplex", "Hundstage", "Import Export",
    "Die Fetten Jahre sind vorbei", "Revanche", "Der Knochenmann",
    "Indien", "Hinterholz 8", "Muttertag", "Komm suesser Tod",
    "Silentium", "Der Taucher", "Nordrand", "Antares", "Struggle",
    "Ein halbes Leben",
]

SERIEN = [
    "Der Pass", "Dark", "Babylon Berlin", "Tatort", "Soko Donau",
    "Die Toten vom Bodensee", "Vorstadtweiber", "Braunschlag",
]

ENDUNGEN = ["mkv", "mp4", "avi", "m4v"]
AUFLOESUNGEN = ["720p", "1080p", "2160p", "480p"]
QUELLEN = ["BluRay", "WEBRip", "HDTV", "DVDRip"]


def punkt_schema(zufall, titel, jahr):
    teile = [titel.replace(" ", "."), str(jahr), zufall.choice(AUFLOESUNGEN)]
    if zufall.random() < 0.5:
        teile.append(zufall.choice(QUELLEN))
    return ".".join(teile) + "." + zufall.choice(ENDUNGEN)


def klammer_schema(zufall, titel, jahr):
    name = f"{titel} ({jahr})"
    if zufall.random() < 0.4:
        name = name + f" [{zufall.choice(AUFLOESUNGEN)}]"
    return name + "." + zufall.choice(ENDUNGEN)


def strich_schema(zufall, titel, jahr):
    teile = [titel.replace(" ", "_"), str(jahr), zufall.choice(AUFLOESUNGEN)]
    return "_".join(teile) + "." + zufall.choice(ENDUNGEN)


def freitext_schema(zufall, titel, jahr):
    quelle = zufall.choice(QUELLEN)
    return f"{titel} {jahr} {quelle}." + zufall.choice(ENDUNGEN)


SCHEMATA = [punkt_schema, klammer_schema, strich_schema, freitext_schema]


def anlegen(pfad, berichte):
    """Legt eine leere Datei an und meldet Fehler des Dateisystems."""
    try:
        pfad.parent.mkdir(parents=True, exist_ok=True)
        pfad.touch()
        return True
    except OSError as fehler:
        berichte.append(f"{fehler.__class__.__name__}: {pfad.name[:60]}...")
        return False


def erzeuge(ziel, anzahl):
    zufall = random.Random(STARTWERT)
    ziel = Path(ziel)
    berichte = []
    gezaehlt = 0

    # --- 1. Der grosse Rest: vier Schemata, gemischt --------------------
    while gezaehlt < anzahl - 40:
        titel = zufall.choice(TITEL)
        jahr = zufall.randint(1922, 2026)
        schema = zufall.choice(SCHEMATA)
        unterordner = zufall.choice(
            ["", "", "", "Filme", "Filme/Archiv", "Neu"])
        name = schema(zufall, titel, jahr)
        if anlegen(ziel / unterordner / name, berichte):
            gezaehlt += 1

    # --- 2. Dieselbe Datei in zwei Schemata (Einheit 7) ---------------
    anlegen(ziel / "Der.Pate.1972.1080p.mkv", berichte)
    anlegen(ziel / "Filme" / "Der Pate (1972).mkv", berichte)

    # --- 3. Umlaute in zwei Kodierungen (Einheit 2) ---------------------
    nfc = unicodedata.normalize("NFC", "Amélie")
    nfd = unicodedata.normalize("NFD", "Amélie")
    anlegen(ziel / (nfc + " (2001).mkv"), berichte)
    anlegen(ziel / (nfd + " (2001) [1080p].mkv"), berichte)
    anlegen(ziel / "Amelie (2001).mkv", berichte)

    # --- 4. Ohne Jahreszahl (Einheit 4 und 9) --------------------------
    for name in ["Film_ohne_Jahr.avi", "Unbekannt.mkv", "Urlaubsvideo.mp4"]:
        anlegen(ziel / name, berichte)

    # --- 5. Verwaiste Begleitdateien (Einheit 7) -----------------------
    for name in ["Verschollen.de.srt", "Verschollen.en.srt", "Niemand.nfo"]:
        anlegen(ziel / "Filme" / name, berichte)

    # --- 6. Bruchstuecke (Einheit 7) -----------------------------------
    for name in ["Downloading.Film.2024.mkv.part", "Halbfertig.2023.mkv.!ut"]:
        anlegen(ziel / "Neu" / name, berichte)

    # --- 7. Sample-Ordner (Einheit 7) ----------------------------------
    for i in range(3):
        anlegen(ziel / "Filme" / "Sample" / f"sample-{i}.mkv", berichte)

    # --- 8. Sehr langer Name (Einheit 1 und 2) -------------------------
    langer = ("Der.unglaublich.lange.Titel."
              + "und.immer.weiter." * 12)[:236] + ".mkv"
    anlegen(ziel / "Filme" / "Archiv" / langer, berichte)

    # --- 9. Serien in drei Schreibweisen (Einheit 4 und 5) -------------
    for serie in SERIEN:
        s = zufall.randint(1, 5)
        f = zufall.randint(1, 12)
        ordner = ziel / "Serien" / serie
        anlegen(ordner / f"{serie}.s{s:02d}e{f:02d}.mkv", berichte)
        anlegen(ordner / f"{serie} {s}x{f:02d}.mkv", berichte)
        anlegen(ordner / f"Staffel {s}" / f"Folge {f}.mkv", berichte)

    # --- 10. Titel mit Komma (Einheit 8, CSV) --------------------------
    anlegen(ziel / "Zurueck in die Zukunft, Teil II (1989).mkv", berichte)
    anlegen(ziel / "Alles steht Kopf, aber richtig (2015).mkv", berichte)

    return ziel, berichte


def main():
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--ziel", default="daten/sammlung",
                          help="Zielordner (Vorgabe: daten/sammlung)")
    zerleger.add_argument("--anzahl", type=int, default=5000,
                          help="ungefaehre Gesamtzahl der Dateien")
    argumente = zerleger.parse_args()

    ziel, berichte = erzeuge(argumente.ziel, argumente.anzahl)

    dateien = [p for p in Path(ziel).rglob("*") if p.is_file()]
    print(f"{len(dateien)} Dateien in {ziel}")

    if berichte:
        print()
        print(f"{len(berichte)} Datei(en) konnten nicht angelegt werden:")
        for zeile in berichte[:10]:
            print("  ", zeile)
        print()
        print("Das ist kein Fehler im Skript. Unter Windows scheitern")
        print("sehr lange Namen, solange die Pfadlaengenbegrenzung aktiv")
        print("ist. Genau dieser Fall kommt in Einheit 2 vor.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
