#!/usr/bin/python3

# name:   grundlinie.py
# author: nbehrnd@yahoo.com
# date:   2021-03-08 (YYYY-MM-DD)
# edit:
"""Korrektur der Grundlinie

* Hintergrund
Eine unbestimmte Anzahl DEK .svg nutzt nur eine graue Grundlinie.  Um
diese besser zu erkennen, sollen die .svg einheitlich eine schwarze
Grundlinie nutzen.

Die Grundlinie ist das erste in der Wiedergabe sichtbare Element, alle
anderen Linien und das Stenogramm werden erst danach beschrieben.  In
Inkscape .svg wird ein schwarzer Linienzug mit

stroke:#000000;

definiert (momentan zu sehen bei Untergrenze, Oberlinie, Obergrenze).

Die Grundlinie ist zur Zeit definiert als ein Grau mit

stroke:#969696;

Zur Korrektur muss auch diese Definition auf

stroke:#000000;

angepasst werden.

* Nutzung

+ Kopie dieses Skriptes in den Ordner mit den zu korrierenden .svg
+ Aufruf per

  python3 grundlinie.py

  ohne weitere Parameter, um den Austausch zu starten.  Dabei werden
  die bisherigen Dateien durch neue Dateien gleichen Namens ersetzt --
  ohne Sicherung der Originale."""

import os
import re


def identificator():
    """Bearbeite letzlich nur die .svg Dateien."""
    register = []
    for file in os.listdir("."):
        if file.endswith(".svg"):
            register.append(file)

    register.sort()
    return register


def corrector(file=""):
    """Tausche graue Linie durch schwarze Linie aus."""
    input_file = str(file)
    intermediate = str(file) + str("_intermediate")

    # Lies den bisherigen Inhalt:
    with open(file, mode="r") as source:
        content = source.read()

        # Tausche die Liniendefinition:
        gray_line = re.compile("stroke:#969696;")
        substituted = str(gray_line.sub("stroke:#000000;", content))

        # Lege eine korrigierte Datei an:
        with open(intermediate, mode="w") as newfile:
            newfile.write(substituted)


def space_cleaning(file=""):
    """Ersetze die originale Datei durch die korrigierte."""
    intermediate = str(file) + str("_intermediate")
    output_file = str(file)

    os.rename(intermediate, output_file)


if __name__ == "__main__":
    # Nutze die einzelnen Operationen:
    register = []
    register = identificator()

    # Arbeite an den .svg Dateien:
    error = []

    for file in register:
        print(file)  # Fortschrittssanzeige

        try:
            corrector(file)
            space_cleaning(file)
        except OSError:
            error.append(file)

    # Bennenne Bearbeitungen, die bereits jetzt als fehlerhaft erkannt sind:
    if len(error) > 0:
        print(
            "Die Bearbeitung einiger Dateien ist fehlerhaft.  Siehe 'error_log.txt'."
        )
        error.sort()

        with open("error_log.txt", mode="w") as newfile:
            newfile.write(
                "Die Bearbeitung folgender Dateien ist fehlerhaft:\n")
            for entry in error:
                newfile.write(f"{entry}\n")
            newfile.write("\nEND")

    # Coda:
    print("\nProcessing complete.")
