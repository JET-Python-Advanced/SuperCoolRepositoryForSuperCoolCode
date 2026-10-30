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


def title(filename):

    title = filename.split(".", 1)[0]
    title = str.replace(title, "_", " ")
    return title


def extension(filename):
    partitioned_title = str.partition(filename, ".")
    extension = partitioned_title[2]
    return extension


def count_extension(files, wanted=None):
    count = 0
    for file in files:
        if extension(file) == wanted:
            count += 1

    return count


# def longest(files):
#     if files == None:
#         return None

#     longest_title = title(files[0])

#     for i in range(1, len(files) - 1):
#         next_tile = title(files[i + 1])
#         if len(next_tile) > len(longest_title):
#             longest_title = next_tile
#     return longest_title

def longest(files):
    return title(sorted(files, key=len)[-1])


def report(files):
    found_extensions = {}

    for title in files:
        if extension(title) not in found_extensions:
            found_extensions[extension(title)] = 1
        else:
            found_extensions[extension(title)] += 1

    print(f"{len(files)} files found")
    print(found_extensions)
    print(f"Longest Title: {longest(files)}")


def year(filename):
    current = ""
    for char in filename:
        if str.isdigit(char):
            current += char
        elif current != "" and (char == " " or char == "_" or char == "."):
            if 1900 < int(current) < 2026:
                return int(current)


extension("Alien_1979_1080p.mkv")
print(count_extension(FILES, "mkv"))
print("--------REPORT-----------")
report(FILES)

count = 0
for file in FILES:
    if year(file) < 1990:
        count += 1
print(f"Movies released before 1990: {count}")
