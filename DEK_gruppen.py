# name:    DEK_gruppen.py
# author:  nbehrnd@yahoo.com
# license: MIT 2020
# date:    2020-07-30 (YYYY-MM-DD)
# edit:    2020-07-31 (YYYY-MM-DD)
#
"""Listung der Stenographie .svg in Dreiergruppen / Wunsch 3.

    Im Stenographiearchiv sind die .svg im Muster von

    DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Aachen v2.svg

    abgelegt.  Jedem dieser Dateien soll ein string zugeordnet werden,
    der dem Format

    "[[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Aachen v2.svg|thumb|Aachen v2]]"

    entspricht.  Weiterhin sind diese strings in dem Muster

    | [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Bockwürste.svg|thumb|Bockwürste]]
    || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Bockwurst.svg|thumb|Bockwurst]]
    || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Wurst.svg|thumb|Wurst]]
    |-
    | [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Xaver.svg|thumb|Bockwürste]]
    || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Yacht.svg|thumb|Bockwurst]]
    || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Zündkerze.svg|thumb|Wurst]]
    |-

    in Dreiergruppen in Datei "DEK_gruppen.txt" abzulegen.

    Aufruf von der Kommandozeile mit Python 3 als

    python DEK_gruppen.py

    wenn diese Datei (DEK_gruppen.py) sich im gleichen Ordner wie
    die originalen .svg befindet."""

import os
SVG_REGISTER = []
OUTPUT_REGISTER = []


def identify_svg():
    """Identify the .svg to work with.

    Nur .svg Dateien sind von Interesse, deren Namen bereits nach dem ABC
    aufsteigend sortiert werden."""
    for file in os.listdir("."):
        if file.endswith(".svg"):
            SVG_REGISTER.append(file)

    SVG_REGISTER.sort()  # Sort as if all were lower case only.
    print("There are {} data identified.".format(len(SVG_REGISTER)))


def string_conversion():
    """Based on the file names, generate the table data.

    Zusammenstellung der strings aus den Dateinamen unter der Annahme,
    dass es Stichwort selbst keinen Gedankenstrich hat."""
    iterator = 0
    for entry in SVG_REGISTER:
        iterator += 1
        file_name = str(entry)

        keyword = file_name.split(" - ")[-1].strip()
        keyword = keyword[:-4]

        if iterator == 1:
            output = ''.join(["| [[File:", file_name, "|thumb|", keyword, "]]"])
        elif iterator == 2:
            output = ''.join(["|| [[File:", file_name, "|thumb|", keyword, "]]"])
        elif iterator == 3:
            output = ''.join(["|| [[File:", file_name, "|thumb|", keyword, "]]", "\n|-"])
            iterator = 0
        else:
            print("Warnung, Zusammenstellung der Ausgabedaten eventuell fehlerhaft.")

        OUTPUT_REGISTER.append(output)
    print("There are {} output data.".format(len(OUTPUT_REGISTER)))


def report_writing():
    """Generate the permanent record."""
    with open("DEK_gruppen.txt", mode="w") as newfile:
        for entry in OUTPUT_REGISTER:
            newfile.write("{}\n".format(entry))


def main():
    """Join the elementary functions."""
    identify_svg()
    string_conversion()
    report_writing()


if __name__ == '__main__':
    main()
