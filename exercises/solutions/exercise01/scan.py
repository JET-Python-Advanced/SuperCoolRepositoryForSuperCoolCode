"""Media library — the beginning.

Over twelve units this grows into a tool that reads a folder of movie
files, recognises title and year, fetches additional information and
writes a report.

Unit 1: we still work with this fixed list.
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

#B1.2
def title(filename):
    return filename.split(".")[0].replace("_", " ")

#B1.3
def extension(filename):
    return filename.split(".")[-1]

#B1.4
def count_extension(files, wanted="mkv"):
    count = 0
    for filename in files:
        if extension(filename) == wanted:
            count = count + 1
    return count

#B1.5
def longest(files):
    best = files[0]
    for filename in files:
        if len(filename) > len(best):
            best = filename
    return best

#B1.7
def longest_short(files):
    return sorted(files, key=len)[-1]

#B1.8
def year(filename):
    for part in filename.split(".")[0].split("_"):
        if len(part) == 4 and part.isdigit():
            return int(part)
    return 0

#B1.6
def report(files):
    print(f"{len(files)} files found")
    print(f"  mkv: {count_extension(files)}")
    print(f"  mp4: {count_extension(files, 'mp4')}")
    print(f"  avi: {count_extension(files, 'avi')}")
    print(f"  longest name: {title(longest(files))}")


#B1.1
print(len(FILES))                                  # 15
report(FILES)
print(longest_short(FILES))

before_1990 = 0
for movie_file in FILES:
    if year(movie_file) < 1990:
        before_1990 = before_1990 + 1
print(before_1990)                                 # 6
