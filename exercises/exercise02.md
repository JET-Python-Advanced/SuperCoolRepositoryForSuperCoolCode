# Übungsblatt 2 — Git

**Python Advanced · Einheit 2 · Freitag, 09.10.2026**

---
## Einrichtung

  

**Arbeiten Sie nicht in Ihrem Projektrepository von letzter Woche!** Im Laufe dieses Übungsblatts werden Commits gelöscht, was wir nicht auf einem Repo üben wollen, das Sie noch brauchen. Legen Sie ein Wegwerf-Repository an:

  

1. Auf GitHub ein neues Repository `git-uebung` anlegen, **privat**, Häkchen bei *Add a README file*.

2. In der Git Bash in den Ordner wechseln, in dem es liegen soll, und klonen:

  

```

cd Desktop

git clone <URL aus dem grünen Code-Button>

cd git-uebung

```

Das Repository muss wirklich auf GitHub liegen — im Aufgabenteil A4 brauchen Sie eine Gegenstelle, sonst kommt dort die falsche Fehlermeldung.

  

---

  

## Teil A1 — Theorie

**A1.1** In welcher Stage liegt eine Datei
- direkt nach dem Anlegen?

- nach `git add`?

- nach `git commit`?

**A1.2** Eine `.gitignore`-Datei enthält:
```

temp/

*.tmp

secret.csv

!wichtig.tmp

```

Welche der folgenden Dateien landen auf GitHub?

```

analyse.py temp/cache.json notiz.tmp

secret.csv wichtig.tmp README.md

```

  

**A1.3** Ordnen Sie zu — Git oder GitHub?

- läuft lokal auf dem eigenen Rechner

- zeigt Pull Requests an

- braucht eine Internetverbindung

- speichert den Verlauf im Ordner `.git`

  

**A1.4** Zentralisierte oder verteilte Versionskontrolle? 
- Der vollständige Verlauf liegt auf jedem Rechner.

- Ohne Verbindung zum Server kann nicht committet werden.

- Es gibt zwei Stufen: lokal festschreiben, dann hochladen.

**A1.5** Sie veröffentlichen ein Repository **ohne** Lizenzdatei. Was darf ein Fremder damit tun und was nicht?

**A1.6** Was passiert, wenn Sie den Ordner `.git` löschen? 

---

  

## Teil A2 — Terminal

  

Führen Sie die folgenden Aufgaben alle in der Git Bash, im Ordner `git-uebung` durch. Verwenden Sie **nicht** den Dateiexplorer, die Git GUI oder einen anderen Editor außer Nano. 

  

**A2.1** Legen Sie den Ordner `src` an und wechseln Sie hinein.

**A2.2** Erzeugen Sie dort die leere Datei `analyse.py`. Prüfen Sie mit `ls`, dass sie da ist.

**A2.3** Öffnen Sie sie mit `nano` und schreiben Sie `print("Hallo")` hinein. Speichern Sie mit **Strg+S** und beenden Sie den Editor mit **Strg+X**. Prüfen Sie mit `cat`, dass der Inhalt stimmt.

**A2.4** Kopieren Sie die Datei nach `kopie.py`. Benennen Sie `kopie.py` in `test.py` um. Hinweis: Dafür gibt es keinen eigenen Befehl, wir haben aber mit einem kleinen Trick gearbeitet.

**A2.5** Verschieben Sie `test.py` eine Ebene nach oben und löschen Sie sie dort.

---

## Teil A3 — Der Grundzyklus

Navigieren Sie zurück in `git-uebung` (nicht in `src`).

**A3.1** Legen Sie `login.py` an und schreiben Sie die folgenden zwei Zeilen hinein:

```python

name = input("Wie ist dein Name? ")

print(f"Hallo {name}")

```

**A3.2** Führen Sie `git status` aus. Denken Sie nach, was die Ausgabe bedeutet und warum Sie diese Ausgabe bekommen. 

**A3.3**  `git add login.py`, dann wieder `git status`. Was hat sich geändert?

**A3.4**  `git commit -m "login.py angelegt"`, dann wieder `git status`. Was steht jetzt da?

**A3.5** Ändern Sie in `login.py` den Gruß auf `Guten Tag` und führen Sie `git status` aus. Die Datei taucht wieder auf — wie sieht es diesmal aus?

**A3.6** Machen Sie die Änderung rückgängig, ohne die Datei von Hand zu bearbeiten. Hinweis: Der Befehl steht in der Ausgabe von `git status`. 

---

  

## Teil A4 — Branches

  

**A4.1** Lassen Sie sich alle Branches auflisten. 

**A4.2** Legen Sie den Branch `feature/gruss` an und wechseln Sie hinein. 

**A4.3** Ändern Sie auf diesem Branch den Gruß auf `Guten Tag` und committen Sie.

**A4.4** Versuchen Sie `git push`. Das schlägt fehl. Lesen Sie die Fehlermeldung, notieren Sie den Befehl, den Git vorschlägt, und führen Sie ihn aus. Sehen Sie danach auf GitHub nach, wie viele Branches das Repository jetzt anzeigt?

**A4.5** Wechseln Sie zurück auf `main` und führen Sie `cat login.py` aus. Welcher Gruß steht jetzt da und warum?

**A4.6** Führen Sie den Branch zusammen: `git merge feature/gruss`. 

**A4.7** Löschen Sie den Branch. Was passiert mit den Commits, die darauf gemacht wurden?

### Selbstkontrolle

Am Ende von Teil A4 gilt in `git-uebung`:

-  `git branch` zeigt nur noch `main`

-  `git log --oneline` zeigt mindestens zwei Commits

-  `git status` meldet nichts Offenes

-  `cat login.py` zeigt den Gruß `Guten Tag`

  

## Teil A5 — Konflikte

Einen echten Konflikt können Sie alleine erzeugen: Sie ändern dieselbe Zeile zweimal, also einmal auf jedem Branch.

**A5.1** Stellen Sie sicher, dass Sie auf `main` sind und `login.py` den Gruß `Hallo` enthält.

**A5.2** Legen Sie den Branch `feature/gruss2` an, wechseln Sie hinein, ändern Sie den Gruß auf `Guten Tag` und committen Sie.

**A5.3** Wechseln Sie zurück auf `main`. Ändern Sie dort dieselbe Zeile auf `Guten Morgen` und committen Sie.

**A5.4**  Führen Sie `git merge feature/gruss2` aus. Notieren Sie die Meldung.

**A5.5** Sehen Sie sich `login.py` an. Erklären Sie, welche der beiden Fassungen über und welche unter dem `=======` steht.

**A5.6** Lösen Sie den Konflikt: Entscheiden Sie sich für eine Fassung, löschen Sie die Markierungen, dann `git add login.py` und `git commit`. Warum braucht `commit` hier kein `-m`?

**A5.7** Mit welchem Befehl hätten Sie den Merge abbrechen und zum Zustand davor zurückkehren können?

---

## Teil A6 — Rückgängig machen

Weiterhin im Wegwerf-Repository. **In diesem Teil wird nicht gepusht** — alles bleibt lokal, denn sonst gehen lokaler Stand und GitHub auseinander.

Legen Sie sich erst eine überschaubare Historie an:

```

echo "Zeile 1" > notizen.txt

git add . && git commit -m "erster Commit"

echo "Zeile 2" >> notizen.txt

git commit -am "zweiter Commit"

echo "Zeile 3" >> notizen.txt

git commit -am "dritter Commit"

```
**Hinweis:** `>` schreibt die Ausgabe in eine Datei und überschreibt dabei. `>>` hängt stattdessen an.  
`echo "Zeile 1" > notizen.txt` legt die Datei also mit Inhalt an, `echo "Zeile 2" >> notizen.txt` ergänzt eine Zeile.

**A6.1**  `git log --oneline`. Notieren Sie die ID des **zweiten** Commits.

**A6.2**  `git checkout <ID>`. Lesen Sie die Meldung. Wie nennt Git diesen Zustand?

**A6.3**  `cat notizen.txt` und `git log --oneline`. Was fehlt, und warum?

**A6.4** Zurück mit `git checkout main`. Ist alles wieder da?  

**A6.5**  `git revert HEAD`. Sehen Sie sich danach `notizen.txt`  **und**  `git log --oneline`

an. Die Datei ist kürzer geworden, der Verlauf **länger**. Warum?  

**A6.6** Die drei Stufen von `reset`. Führen Sie nach **jeder** Zeile `git status --short` aus und notieren Sie die Ausgabe:

```

git reset --soft HEAD~1

git reset --mixed

git reset --hard HEAD

```

`git status --short` hat zwei Spalten. Die linke steht für die Staging Area, die rechte für das Arbeitsverzeichnis. Welche Stufe räumt welche Spalte?

**A6.7** Warum ist `revert` für ein Repository, mit dem andere arbeiten, die sichere Wahl und `reset --hard` nicht?
