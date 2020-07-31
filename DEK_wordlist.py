# name:    DEK_wordlist.py
# author:  nbehrnd@yahoo.com
# license: MIT 2020
# date:    2020-07-30 (YYYY-MM-DD)
# edit:    2020-07-31 (YYYY-MM-DD)
#
"""Listung der Stenographie .svg in einer kommagetrennten Datei / Wunsch 2.

    Im Stenographiearchiv sind die .svg im Muster von

    DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Aachen v2.svg

    abgelegt.  Aus jedem Dateinamen soll das Stichwort entnommen (hier
    etwa "Aachen v2"), und alphabetisch in einer Liste abgelegt werden.

    Mit dem Aufruf von der Kommandozeile mit Python als

    python DEK_wordlist.py

    wenn sich diese Datei (DEK_wordlist.py) sich im gleichen Ordner
    wie die originalen .svg befindet wirt die Datei "DEK_wordlist.txt"
    geschrieben."""

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

    SVG_REGISTER.sort(key=str.lower)  # Sort as if all were lower case only.
    print("There are {} data identified.".format(len(SVG_REGISTER)))


def string_conversion():
    """Based on the file names, generate the table data.

    Zusammenstellung der strings aus den Dateinamen unter der Annahme,
    dass es Stichwort selbst keinen Gedankenstrich hat."""
    for entry in SVG_REGISTER:
        file_name = str(entry)

        keyword = file_name.split(" - ")[-1].strip()
        keyword = keyword[:-4]

        OUTPUT_REGISTER.append(str(keyword))
    print("There are {} output data.".format(len(OUTPUT_REGISTER)))


def report_writing():
    """Generate the permanent record."""
    with open("DEK_wordlist.txt", mode="w") as newfile:
        for entry in OUTPUT_REGISTER[:-1]:
            newfile.write("{}, ".format(entry))

        newfile.write("{}.".format(OUTPUT_REGISTER[:-1]))


def main():
    """Join the elementary functions."""
    identify_svg()
    string_conversion()
    report_writing()


if __name__ == '__main__':
    main()
