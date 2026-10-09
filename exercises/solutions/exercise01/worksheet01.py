# ---------------------------------------------------------------------
# A1 — Output bestimmen
# ---------------------------------------------------------------------

#A1.1
print(7 / 2, 7 // 2, 2 ** 3)                      # 3.5 3 8

#A1.2
print(2 + 3 * 2 ** 2)                             # 14

#A1.3
print("ab" * 3, "a" + "b")                        # ababab ab

#A1.4
print("Blade " "Runner")                          # Blade Runner

#A1.5
print(0 <= 5 <= 10)                               # True
print(1 < 2 < 3 < 2)                              # False

#A1.6
numbers = [1, 2, 3, 4, 5]
print(numbers[-1], numbers[-2])                   # 5 4

#A1.7
print([1, 2] + [3])                               # [1, 2, 3]
print([1, 2] * 2)                                 # [1, 2, 1, 2]
print(3 in [1, 2])                                # False

#A1.8
a = ["Tor", "Haus", "Fenster"]
b = a.sort()
print(a)                                          # ['Fenster', 'Haus', 'Tor']
print(b)                                          # None

#A1.9
print(sorted(["Tor", "Fenster", "Haus"], key=len))
# ['Tor', 'Haus', 'Fenster']
print(sorted(["Tor", "Fenster", "Haus"], key=len, reverse=True))
# ['Fenster', 'Haus', 'Tor']


#A1.10
def double(x):
    print(x * 2)

result = double(4)                                # 8
print(result)                                     # None

#A1.11
count = 0

def count_up():
    count = 5

count_up()
print(count)                                      # 0

#A1.12
def movie(title, year=0, extension="mkv"):
    return f"{title} ({year}).{extension}"

print(movie("Alien", extension="mp4"))            # Alien (0).mp4
print(movie("Heat", 1995))                   # Heat (1995).mkv


# ---------------------------------------------------------------------
# A2 — PEP 8
# ---------------------------------------------------------------------

width = 0 # Leerzechen um den Zuweisungsoperator
is_large_format = False #snake_case statt camelCase
count = 0 # keine Ausrichtung nach den Operatoren
total_size = 0

if is_large_format: # ohne == True
    print("large format") # keine Leerzeichen nach der öffnenden Klammer

#Muss in der Aufgabe nicht definiert werden, wird hier nur gemacht, damit das File durchläuft
#*args steht für beliebig viele positionelle Argumente
def calculate(*args):
    return len(args)


file = "x"
min_width = 1080
height = 0
depth = 0
extension = "mkv"
quality = 0
language = "de"
subtitles = None

result = calculate(
    file, min_width, height, depth,
    extension, quality, language, subtitles,
) # Zeilenumbruch, da empfohlene Charakterlänge pro Zeile überschritten wurde

# ---------------------------------------------------------------------
# A3 — Programmieren
# ---------------------------------------------------------------------

#A3.1
def longer_than(words, min_length=4):
    count = 0
    for word in words:
        if len(word) >= min_length:
            count = count + 1
    return count

#A3.2
def initials(name):
    result = ""
    for part in name.split(" "):
        result = result + part[0] + "."
    return result

#A3.3
def countdown(start):
    while start > 0:
        print(start, end=" ")
        start = start - 1
    print("los")


print(longer_than(["Haus", "Tor", "Fenster"]))     # 2
print(longer_than(["Haus", "Tor", "Fenster"], 6))  # 1
print(initials("Max Mustermann"))                  # M.M.
print(initials("Anna Maria Huber"))                # A.M.H.
countdown(5)                                       # 5 4 3 2 1 los
