# name:    table_formatter.py
# author:  nbehrnd@yahoo.com
# license: MIT 2020
# date:    2020-07-27 (YYYY-MM-DD)
# edit:    2020-07-30 (YYYY-MM-DD)
#
"""Tabellenausgabe der Stenographie .svg in einer kommagetrennten Datei.

    Im Stenographiearchiv sind die .svg im Muster von

    DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Aachen v2.svg

    abgelegt.  Jedem dieser Dateien soll ein string zugeordnet werden,
    der dem Format

    "[[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Aachen v2.svg|thumb|Aachen v2]]"

    entspricht.  Aufgerufen von der Kommandozeile soll Python diese
    Zuordnungen, bereits in alphabetischer Ordnung, in eine Textdatei
    "DEK_Tabelle.txt" schreiben:

    python table_formatter.py

    wenn diese Datei (table_formatter.py) sich im gleichen Ordner wie
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

    SVG_REGISTER.sort()
    print("There are {} data identified.".format(len(SVG_REGISTER)))


def string_conversion():
    """Based on the file names, generate the table data.

    Zusammenstellung der strings aus den Dateinamen unter der Annahme,
    dass es Stichwort selbst keinen Gedankenstrich hat."""
    for entry in SVG_REGISTER:
        file_name = str(entry)

        keyword = file_name.split(" - ")[-1].strip()
        keyword = keyword[:-4]

        output = ''.join(["[[File:", file_name, "|thumb|", keyword, "]]"])
        OUTPUT_REGISTER.append(output)
    print("There are {} output data.".format(len(OUTPUT_REGISTER)))


def report_writing():
    """Generate the permanent record."""
    with open("DEK_Tabelle.txt", mode="w") as newfile:
        for entry in OUTPUT_REGISTER:
            newfile.write("{}\n".format(entry))


def main():
    """Join the elementary functions."""
    identify_svg()
    string_conversion()
    report_writing()


if __name__ == '__main__':
    main()
