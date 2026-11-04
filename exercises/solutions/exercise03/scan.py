FILES = [
    "Alien_1979_1080p.mkv",
    "Heat_1995_720p.mkv",
    "Fargo_1996.mp4",
    "Der_dritte_Mann_1949.avi",
    "Memento_2000_1080p.mkv",
]


# ---------- B1.1: Annotationen ----------

def title(filename: str) -> str:
    return filename.split(".")[0].replace("_", " ")


def extension(filename: str) -> str:
    return filename.split(".")[-1]


def count_extension(files: list[str], wanted: str = "mkv") -> int:
    count = 0
    for filename in files:
        if extension(filename) == wanted:
            count = count + 1
    return count


# ---------- B1.2 bis B1.5 ----------

class Mediathek:
    """Hält eine Liste von Dateinamen."""

    def __init__(self, files: list[str] | None = None) -> None:
        # B1.3: eigene Liste statt Alias auf das Argument
        self.files = list(files) if files is not None else []

    def __len__(self) -> int:
        return len(self.files)

    def add(self, filename: str) -> None:
        self.files.append(filename)

    def with_extension(self, wanted: str) -> list[str]:
        # B1.4: Comprehension liefert immer eine neue Liste
        return [f for f in self.files if extension(f) == wanted]

    def kopie(self) -> "Mediathek":
        # B1.5: der Konstruktor kopiert bereits, mehr braucht es nicht
        return Mediathek(self.files)


# ---------- Nachweise ----------

print("B1.1:", title("Der_dritte_Mann_1949.avi"), "|",
      extension("Alien_1979_1080p.mkv"), "|", count_extension(FILES))

leer = Mediathek()
voll = Mediathek(FILES)
print("B1.2:", len(voll), len(leer), "| leer ist falsch:", not leer)

aussen = ["Alien_1979_1080p.mkv"]
m = Mediathek(aussen)
m.add("Heat_1995_720p.mkv")
print("B1.3 aussen:", aussen)
print("B1.3 innen :", len(m), "| dieselbe Liste:", m.files is aussen)

treffer = voll.with_extension("mkv")
treffer.append("ERFUNDEN.mkv")
print("B1.4 Treffer:", len(treffer), "| Mediathek:", len(voll))

zweite = voll.kopie()
zweite.add("Nosferatu_1922.avi")
print("B1.5 Original:", len(voll), "| Kopie:", len(zweite))
print("B1.5 geteilte Liste:", zweite.files is voll.files)
print("B1.5 gleiche Titel :", zweite.files[0] is voll.files[0])
