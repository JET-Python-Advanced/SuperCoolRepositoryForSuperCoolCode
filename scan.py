"""Media library — the beginning.

Over twelve units this grows into a tool that reads a folder of movie
files, recognises title and year, fetches additional information and
writes a report.

Unit 1: we still work with this fixed list.
Unit 2: the list is replaced by a real folder.
"""

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


# ---------------------------------------------------------------------
# From here on: worksheet 1, part B
# ---------------------------------------------------------------------

print(len(FILES), "files in the list")
