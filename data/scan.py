"""Medienbibliothek — der Anfang.

Ueber zwoelf Einheiten wird daraus ein Werkzeug, das einen Ordner mit
Filmdateien einliest, Titel und Jahr erkennt, Zusatzinformationen holt
und einen Bericht schreibt.

Einheit 1: Wir arbeiten noch mit dieser festen Liste.
Einheit 2: Statt der Liste wird ein echter Ordner eingelesen.
"""

DATEIEN = [
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


# ---------------------------------------------------------------------
# Ab hier: Uebungsblatt 1, Teil B
# ---------------------------------------------------------------------

print(len(DATEIEN), "Dateien in der Liste")
