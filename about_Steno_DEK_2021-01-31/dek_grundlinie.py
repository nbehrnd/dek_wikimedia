#!/usr/bin/python3

# name:   dek_grundlinie.py
# author: nbehrnd@yahoo.com
# date:   2021-03-08 (YYYY-MM-DD)
# edit:   2021-04-03 (YYYY-MM-DD)
"""Korrektur der Grundlinie

* Hintergrund
Eine unbestimmte Anzahl DEK .svg nutzt nur eine graue Lineatur.  Um
diese besser zu erkennen, sollen die .svg einheitlich eine schwarze
Lineatur nutzen.

Teilweise erscheint die Lineatur grau, da sie als grau definiert wurde
('stroke:#969696;').  In anderen Beispielen verursacht der Eintrag
'stroke-opacity:0.83589747' im letzlich genutzten .pdf diese Anmutung.
Beide Ursachen werden mit diesem Skript korrigiert.

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
    """Tausche graue Linie durch schwarze Linie aus.

    Zahlreiche Beispiele definieren die Lineatur mit 'stroke:#969696';
    in diesen wird nun einheitlich die Farbdefinition einer schwarzen
    Linien mit 'stroke:#000000' angewandt.

    Teilweise tritt die Definition 'stroke-opacity:0.83589747', der
    diese Linien letzlich im .pdf ebenfalls grau darstellt.  Deshalb
    der zweite Austausch, der diese Anweisungen gesamthaft auf ein
    einheitliches 'stroke-opacity:1.0' umschreiben soll."""
    intermediate = str(file) + str("_intermediate")

    # Lies den bisherigen Inhalt:
    with open(file, mode="r") as source:
        content = source.read()

        # Tausche die Liniendefinition, grau gegen schwarz:
        gray_line = re.compile("stroke:#969696;")
        substituted = str(gray_line.sub("stroke:#000000;", content))

        # Tausche die Liniendefinition, keine Schattierung
        opacity = re.compile("stroke-opacity:\d\.?\d*")
        no_shadow = str(opacity.sub("stroke-opacity:1.0", substituted))

        # Lege eine korrigierte Datei an:
        with open(intermediate, mode="w") as newfile:
            # newfile.write(substituted)
            newfile.write(no_shadow)


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
