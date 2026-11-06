import csv
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ORDNER = Path("data/collection")

# B1.2: Menge statt Liste
VIDEO = {".mkv", ".mp4", ".avi", ".m4v"}

# B1.4: 1080p und 2160p gehen nicht, weil keine Zahl mit 19 oder 20
# beginnt, die vierstellig weitergeht
JAHR = re.compile(r"(19\d\d|20\d\d)")


# ---------- B1.4: die eigenen Exceptions ----------

class MediathekFehler(Exception):
    """Fehler, die aus unserem Code stammen."""


class UnlesbarerName(MediathekFehler):
    """Ein Dateiname enthält kein erkennbares Jahr."""


# ---------- aus Übungsblatt 1 und 3, auf Path umgestellt ----------

def title(pfad: Path) -> str:
    return pfad.stem.replace("_", " ")


def extension(pfad: Path) -> str:
    return pfad.suffix.lower().lstrip(".")


def jahr_aus(pfad: Path) -> int:
    treffer = JAHR.search(pfad.stem)
    if treffer is None:
        raise UnlesbarerName(f"kein Jahr im Namen: {pfad.name}")
    try:
        return int(treffer.group(1))
    except ValueError as fehler:
        # kann mit diesem Muster nicht vorkommen, zeigt aber die Form
        raise UnlesbarerName(f"kein Jahr im Namen: {pfad.name}") from fehler


def titel_aus(pfad: Path) -> str:
    stamm = pfad.stem
    treffer = JAHR.search(stamm)
    roh = stamm[:treffer.start()] if treffer else stamm
    return roh.replace(".", " ").replace("_", " ").strip(" ([-")


# ---------- B1.2 bis B1.5 ----------

class Mediathek:

    def __init__(self, files: list[Path] | None = None) -> None:
        # Blatt 3, B1.3: eigene Liste statt Alias auf das Argument
        self.files = list(files) if files is not None else []

    @classmethod
    def von_ordner(cls, ordner: str | Path) -> "Mediathek":
        """B1.2: baut eine Mediathek aus einem Ordner."""
        ordner = Path(ordner)
        gefunden = [p for p in ordner.rglob("*")
                    if p.is_file() and p.suffix.lower() in VIDEO]
        return cls(sorted(gefunden))

    def __len__(self) -> int:
        return len(self.files)

    def add(self, pfad: str | Path) -> None:
        self.files.append(Path(pfad))

    def with_extension(self, wanted: str) -> list[Path]:
        wanted = wanted.lower().lstrip(".")
        return [p for p in self.files if extension(p) == wanted]

    def kopie(self) -> "Mediathek":
        return Mediathek(self.files)

    def verteilung(self) -> list[tuple[str, int]]:
        """B1.3: Endung -> Anzahl, absteigend."""
        return Counter(extension(p) for p in self.files).most_common()

    def nach_jahrzehnt(self) -> tuple[dict[int, list[str]], list[Path]]:
        """B1.4: Jahrzehnt -> Titel, dazu die unlesbaren Namen."""
        gruppen: defaultdict[int, list[str]] = defaultdict(list)
        unlesbar: list[Path] = []
        for pfad in self.files:
            try:
                jahr = jahr_aus(pfad)
            except UnlesbarerName:
                unlesbar.append(pfad)
            else:
                gruppen[jahr // 10 * 10].append(titel_aus(pfad))
        return dict(sorted(gruppen.items())), unlesbar

    def bericht_schreiben(self, pfad: str | Path) -> int:
        """B1.5: CSV nach Jahr sortiert. Kodierung ausdrücklich."""
        zeilen = []
        for datei in self.files:
            try:
                jahr = jahr_aus(datei)
            except UnlesbarerName:
                continue
            zeilen.append((titel_aus(datei), jahr, extension(datei)))
        zeilen.sort(key=lambda z: (z[1], z[0]))

        pfad = Path(pfad)
        with pfad.open("w", encoding="utf-8", newline="") as datei:
            schreiber = csv.writer(datei)
            schreiber.writerow(["titel", "jahr", "endung"])
            schreiber.writerows(zeilen)
        return len(zeilen)


# ---------- Nachweise ----------

def main() -> None:
    print("B1.1 ------------------------------------------------")
    alle = list(ORDNER.rglob("*"))
    dateien = [p for p in alle if p.is_file()]
    print("  Eintraege gesamt:", len(alle))
    print("  davon Dateien   :", len(dateien))
    print("  davon Ordner    :", len(alle) - len(dateien))

    print("B1.2 ------------------------------------------------")
    mediathek = Mediathek.von_ordner(ORDNER)
    print("  Videodateien    :", len(mediathek))
    heraus = sorted(p.name for p in dateien if p.suffix.lower() not in VIDEO)
    print("  herausgefallen  :", len(heraus))
    for name in heraus:
        print("     ", name)

    print("B1.3 ------------------------------------------------")
    verteilung = mediathek.verteilung()
    print("  alle Endungen   :", verteilung)
    print("  die drei groessten:", verteilung[:3])

    print("B1.4 ------------------------------------------------")
    gruppen, unlesbar = mediathek.nach_jahrzehnt()
    for jahrzehnt, titel in gruppen.items():
        print(f"  {jahrzehnt}er: {len(titel):>4} Titel")
    print("  Summe           :", sum(len(t) for t in gruppen.values()))
    print("  ohne Jahr       :", len(unlesbar))
    for pfad in sorted(unlesbar)[:6]:
        print("     ", pfad.relative_to(ORDNER))
    print("      ...")
    try:
        jahr_aus(Path("Urlaubsvideo.mp4"))
    except UnlesbarerName as fehler:
        print("  Ausnahme        :", type(fehler).__name__ + ":", fehler)

    print("B1.5 ------------------------------------------------")
    anzahl = mediathek.bericht_schreiben("bericht.csv")
    print("  Zeilen geschrieben:", anzahl)
    with open("bericht.csv", encoding="utf-8") as datei:
        for nummer, zeile in enumerate(datei):
            if nummer < 3:
                print("     ", zeile.rstrip())
    komma = [p for p in mediathek.files if "," in p.name]
    print("  Titel mit Komma :", len(komma))
    for pfad in komma:
        titel = titel_aus(pfad)
        selbstgebaut = f"{titel},{jahr_aus(pfad)},{extension(pfad)}"
        print("      selbst gebaut:", selbstgebaut)
        print("      Felder       :", len(selbstgebaut.split(",")),
              "statt 3")
        print("      mit csv      :", end=" ")
        import io
        puffer = io.StringIO()
        csv.writer(puffer, lineterminator="").writerow(
            [titel, jahr_aus(pfad), extension(pfad)])
        print(puffer.getvalue())

    print("B1.6 ------------------------------------------------")
    am = sorted(p for p in mediathek.files if p.name.startswith("Am"))
    titel = {p.stem.split(" (")[0] for p in am}
    print("  Dateien         :", [p.name for p in am])
    print("  Menge der Titel :", len(titel), sorted(titel))
    for t in sorted(titel):
        nfc = unicodedata.is_normalized("NFC", t)
        print(f"      {t!r:<12} len={len(t)}  NFC={nfc}")
    normalisiert = {unicodedata.normalize("NFC", t) for t in titel}
    print("  nach NFC        :", len(normalisiert), sorted(normalisiert))


if __name__ == "__main__":
    main()
