"""
Creates the practice collection for the course

The files are empty (0 bytes). Only the names and the folder structure
matter. The random seed is fixed, so the result is identical on every
machine.
"""

import argparse
import random
import sys
import unicodedata
from pathlib import Path

SEED = 20261002

TITLES = [
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

SERIES = [
    "Der Pass", "Dark", "Babylon Berlin", "Tatort", "Soko Donau",
    "Die Toten vom Bodensee", "Vorstadtweiber", "Braunschlag",
]

EXTENSIONS = ["mkv", "mp4", "avi", "m4v"]
RESOLUTIONS = ["720p", "1080p", "2160p", "480p"]
SOURCES = ["BluRay", "WEBRip", "HDTV", "DVDRip"]


def dot_scheme(rng, title, year):
    parts = [title.replace(" ", "."), str(year), rng.choice(RESOLUTIONS)]
    if rng.random() < 0.5:
        parts.append(rng.choice(SOURCES))
    return ".".join(parts) + "." + rng.choice(EXTENSIONS)


def bracket_scheme(rng, title, year):
    name = f"{title} ({year})"
    if rng.random() < 0.4:
        name = name + f" [{rng.choice(RESOLUTIONS)}]"
    return name + "." + rng.choice(EXTENSIONS)


def underscore_scheme(rng, title, year):
    parts = [title.replace(" ", "_"), str(year), rng.choice(RESOLUTIONS)]
    return "_".join(parts) + "." + rng.choice(EXTENSIONS)


def plain_scheme(rng, title, year):
    source = rng.choice(SOURCES)
    return f"{title} {year} {source}." + rng.choice(EXTENSIONS)


SCHEMES = [dot_scheme, bracket_scheme, underscore_scheme, plain_scheme]


def create_file(path, problems):
    """Creates an empty file and reports file system failures."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        return True
    except OSError as error:
        problems.append(f"{error.__class__.__name__}: {path.name[:60]}...")
        return False


def generate(target, count):
    rng = random.Random(SEED)
    target = Path(target)
    problems = []
    created = 0

    # --- 1. The bulk: four schemes, mixed --------------------------
    while created < count - 40:
        title = rng.choice(TITLES)
        year = rng.randint(1922, 2026)
        scheme = rng.choice(SCHEMES)
        subfolder = rng.choice(
            ["", "", "", "movies", "movies/archive", "new"])
        name = scheme(rng, title, year)
        if create_file(target / subfolder / name, problems):
            created += 1

    # --- 2. Same movie in two schemes (unit 7) --------------------
    create_file(target / "Der.Pate.1972.1080p.mkv", problems)
    create_file(target / "movies" / "Der Pate (1972).mkv", problems)

    # --- 3. Umlauts in two encodings (unit 2) ---------------------
    nfc = unicodedata.normalize("NFC", "Amélie")
    nfd = unicodedata.normalize("NFD", "Amélie")
    create_file(target / (nfc + " (2001).mkv"), problems)
    create_file(target / (nfd + " (2001) [1080p].mkv"), problems)
    create_file(target / "Amelie (2001).mkv", problems)

    # --- 4. No year in the name (units 4 and 9) -------------------
    for name in ["Film_ohne_Jahr.avi", "Unbekannt.mkv", "Urlaubsvideo.mp4"]:
        create_file(target / name, problems)

    # --- 5. Orphaned companion files (unit 7) ---------------------
    for name in ["Verschollen.de.srt", "Verschollen.en.srt", "Niemand.nfo"]:
        create_file(target / "movies" / name, problems)

    # --- 6. Partial downloads (unit 7) ----------------------------
    for name in ["Downloading.Film.2024.mkv.part", "Halbfertig.2023.mkv.!ut"]:
        create_file(target / "new" / name, problems)

    # --- 7. Sample folder (unit 7) --------------------------------
    for i in range(3):
        create_file(target / "movies" / "Sample" / f"sample-{i}.mkv", problems)

    # --- 8. Very long name (units 1 and 2) ------------------------
    long_name = ("Der.unglaublich.lange.Titel."
                 + "und.immer.weiter." * 12)[:236] + ".mkv"
    create_file(target / "movies" / "archive" / long_name, problems)

    # --- 9. Series in three spellings (units 4 and 5) -------------
    for series in SERIES:
        s = rng.randint(1, 5)
        e = rng.randint(1, 12)
        folder = target / "series" / series
        create_file(folder / f"{series}.s{s:02d}e{e:02d}.mkv", problems)
        create_file(folder / f"{series} {s}x{e:02d}.mkv", problems)
        create_file(folder / f"Staffel {s}" / f"Folge {e}.mkv", problems)

    # --- 10. Title containing a comma (unit 8, CSV) ---------------
    create_file(target / "Zurueck in die Zukunft, Teil II (1989).mkv",
                problems)
    create_file(target / "Alles steht Kopf, aber richtig (2015).mkv",
                problems)

    return target, problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="data/collection",
                        help="target folder (default: data/collection)")
    parser.add_argument("--count", type=int, default=5000,
                        help="approximate total number of files")
    args = parser.parse_args()

    target, problems = generate(args.target, args.count)

    files = [p for p in Path(target).rglob("*") if p.is_file()]
    print(f"{len(files)} files in {target}")

    if problems:
        print()
        print(f"{len(problems)} file(s) could not be created:")
        for line in problems[:10]:
            print("  ", line)
        print()
        print("This is not a bug. On Windows, very long names fail while")
        print("the path length limit is active. That exact case comes up")
        print("in unit 2.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
