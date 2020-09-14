#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    DEK_wikimedia_lists.py
# author:  nbehrnd@yahoo.com
# license: MIT 2020
# date:    2020-09-10 (YYYY-MM-DD)
# edit:    2020-09-14 (YYYY-MM-DD)
#
"""Assistenzskript #5 zu Wikimedia Projekt zur DEK / Verkehrsschrift.

    Wikimediaautor Thirunavukkarasye-Raveendran, der nicht Autor dieses
    Projektes ist, publiziert 21k+ Beispiele zur Verkehrsschrift, dem
    ersten Grad der Vereinfachung der Deutschen Verkehrsschrift (DEK)
    unter public domain.  Bei der Zusammenfassung der individuellen
    .svg Vektorillustrationen haben sich drei Typen von Listen als
    hilfreich erwiesen:
    + eine einfache Wortliste; gebildet aus dem Dateinamen der .svg
    + eine Liste, die sowohl auf die Dateinamen, als auch auf die
      eigentliche Datei hinweist
    + eine Liste, die sowohl auf die Dateinamen, als auch auf die
      eigentliche Datei hinweist und die Ausgabe in Dreiergruppen
      anordnet

    Mit den drei Skripten DEK_wordlist.py, table_formatter.py sowie
    DEK_gruppen.py lassen sich diese drei Listen schreiben, wenn sich
    diese im gleichen Ordner wie die .svg befinden.  Als Nichtautor
    setzt das voraus, tatsächlich alle diese Dateien beispielsweise
    von Wikimedia auch lokal abgespeichert zu haben.

    Gemeinsam mit Skript DEK_wikimedia_preformat.py verfolgt dieses
    Skript, DEK_wikimedia_lists.py, den dazu alternativen Ansatz,
    Wikimedia abzufragen, welche Dateien simultan mit "SVG" und
    "Deutsche Einheitskurzschrift" verschlagwortet sind (tagged), um
    nur aus dieser Liste die drei hilfreichen Listen zu bilden.  Das
    spart Bandbreite und Zeit, da nun nur noch eine Datei (etwa 3 MB,
    komprimiert etwa 200 kB), statt 21k+ Dateien zu transferieren sind.

    Skript DEK_wikimedia_preformat.py schreibt die hier benutzte Datei
    [wikimedia_addresses.txt] (siehe dort).  Von Pythons Eingabezeile
    wird dieses Skript mit

    python DEK_wikimedia_lists.py [wikimedia_addresses.txt]

    gestartet; [wikimedia_addresses.txt] ist der einzige, allerdings
    obligate Parameter.  Die Anschriften in [wikimeida_addresses.txt]
    beschreiben auch Umlaute; um die originalen Dateinamen zu erhalten
    werden die relevanten strings in UTF-8 dekodiert und trennende
    Unterstriche (zur Zeit wieder) durch Leerzeichen ersetzt.  Die
    anschliessende Sortierung (a-z, sodann Umlaute) behandelt Gross-
    und Kleinschreibung ohne Unterschied.

    Bereits bei Aufruf des Skriptes muss die Auswahl eines der drei
    folgenden Ausgabeformate erfolgen:
    + Option -w die fortlaufende, alphabetisch sortierte Wortliste.
      Da einige der Dateinamen mehrere Beispiele illustrieren, die
      durch ein Komma getrennt sind, werden die einzelnen Dateien
      voneinander ist das Trennzeichen das Semikolon.  Ablage in Datei
      [wikimedia_wordlist.txt].

    + Option -p, die alphabetisch sortierte Liste von Dateinamen mit
      Hinweis auf das Vorschaubild (thumbnail) in einem Muster von

      [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Aachen.svg|thumb|Aachen]]

      Hier ist das Trennzeichen der Zeilenvorschub, \n.  Ablage in
      Datei [wikimedia_thumbnail_list.txt].

    + Option -g, die alphabetisch sortierte Liste von Dateinamen mit
      Hinweis auf das Vorschaubild (thumbnail) in Dreiergruppen nach
      dem Muster

      | [[File:Aachen v2.svg|thumb|Aachen v2]]
      || [[File:Aal.svg|thumb|Aal]]
      || [[File:Aale.svg|thumb|Aale]]
      |-
      | [[File:Aas.svg|thumb|Aas]]
      || [[File:Aasgeier.svg|thumb|Aasgeier]]
      || [[File:Aasvögel.svg|thumb|Aasvögel]]
      |-

      Ablage ist Datei [wikimedia_thumbnail_groups.txt].

    Stets beginnt die Ausgabe mit einem vierzeiligen Kopf, der den
    Namen der Datei, das Erstellungsdatum und die Anzahl der aus
    [wikimedia_addresses.txt] verarbeiteten Zeilen benennt.  Das
    Muster ist

    # name: wikimedia_thumbnail_groups.txt
    # date: 2020-09-10 (YYYY-MM-DD)
    # data: 25459
    #

    Auf diese Weise soll die Verwaltung der Listen mit git unter
    GitHub vereinfacht werden."""

import argparse
import sys

from datetime import date
from urllib.parse import unquote

register = []
RETAINER = []


def check_python():
    """Assure the script is used with Python 3, only."""
    if str(sys.version_info[0]) == str(2):
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif str(sys.version_info[0]) == str(3):
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def file_read():
    """Identify the file to read."""
    try:
        with args.inputfile as source:
            for line in source:
                register.append(str(line).strip())

    # except Exception:
    except IOError:
        print("File not accessible, exit.")
        sys.exit()
        #        print(parser.print_usage())


def input_reader():
    """Build an UTF-8 encoded register."""

    for line in register:
        if str(line).startswith("#") is False:

            retain = str(line).strip()
            retain = retain.split("_-_")[-1]

            # re-encode the keyword:
            retain = unquote(str(retain))
            retain = str(retain)[:-4]

            # substitute separating underscore chars by spaces:
            per_entry = ""
            for char in retain:
                if str(char) == str("_"):
                    per_entry += str(" ")
                else:
                    per_entry += str(char)

            RETAINER.append(per_entry)
    RETAINER.sort(key=str.lower)


def output_wordlist():
    """Provide the list of words, sorted, separated by a semicolon."""
    today = date.today()

    try:
        with open("wikimedia_wordlist.txt", mode="w") as newfile:
            newfile.write("# name: wikimedia_wordlist.txt\n")
            newfile.write("# date: {} (YYYY-MM-DD)\n".format(today))
            newfile.write("# data: {}\n#\n".format(str(len(RETAINER))))

            for entry in RETAINER[:-1]:
                newfile.write("{}; ".format(entry))
            newfile.write(RETAINER[-1])
        print("File 'wikimedia_wordlist.txt' was written.")
    except IOError:
        print("Error writing file 'wikimedia_wordlist.txt'.  Exit.")
        sys.exit()


def output_preview_list():
    """Provide the simple preview listing, separated by carriage return."""
    # "[[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Aachen v2.svg|thumb|Aachen v2]]"
    today = date.today()

    try:
        with open("wikimedia_thumbnail_list.txt", mode="w") as newfile:
            newfile.write("# name: wikimedia_thumbnail_list.txt\n")
            newfile.write("# date: {} (YYYY-MM-DD)\n".format(today))
            newfile.write("# data: {}\n#\n".format(str(len(RETAINER))))

            for entry2 in RETAINER:
                output = str(
                    "[[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - {}.svg|thumb|{}]]"
                    .format(entry2, entry2))
                newfile.write("{}\n".format(output))
        print("File 'wikimedia_thumbnail_list.txt' was written.")
    except IOError:
        print("Error writing file 'wikimedia_thumbnail_list.txt'.  Exit.")
        sys.exit()


def output_grouped_preview():
    """Similar as in function output_preview_list(), but in groups of three."""
    # "| [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Bockwürste.svg|thumb|Bockwürste]]
    # || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Bockwurst.svg|thumb|Bockwurst]]
    # || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Wurst.svg|thumb|Wurst]]
    # |-
    # | [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Xaver.svg|thumb|Bockwürste]]
    # || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Yacht.svg|thumb|Bockwurst]]
    # || [[File:DEK Deutsche Einheitskurzschrift - Verkehrsschrift - Zündkerze.svg|thumb|Wurst]]
    # |-"
    today = date.today()

    try:
        with open("wikimedia_thumbnail_groups.txt", mode="w") as newfile:
            newfile.write("# name: wikimedia_thumbnail_groups.txt\n")
            newfile.write("# date: {} (YYYY-MM-DD)\n".format(today))
            newfile.write("# data: {}\n#\n".format(str(len(RETAINER))))

            iterator = 0
            for entry in RETAINER:
                file_name = ''.join([entry, ".svg"])
                keyword = str(entry)
                iterator += 1

                if iterator == 1:
                    output = ''.join(
                        ["| [[File:", file_name, "|thumb|", keyword, "]]"])
                elif iterator == 2:
                    output = ''.join(
                        ["|| [[File:", file_name, "|thumb|", keyword, "]]"])
                elif iterator == 3:
                    output = ''.join([
                        "|| [[File:", file_name, "|thumb|", keyword, "]]",
                        "\n|-"
                    ])
                    iterator = 0
                else:
                    print("Warnung, eventuell fehlerhafte Ausgabe.")
                newfile.write("{}\n".format(output))
        print("File 'wikimedia_thumbnail_groups.txt' was written.")
    except IOError:
        print("Error writing file 'wikimedia_thumbnail_groups.txt'.  Exit.")
        sys.exit()


# clarification for argparse, start:
parser = argparse.ArgumentParser(
    description=
    'List generator for Wikimedia .svg about DEK / Deutsche Verkehrsschrift.')
parser.add_argument(
    'inputfile',
    type=argparse.FileType('r'),
    help='Input text file, typically "wikimedia_addresses.txt"')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-w',
                   '--wordlist',
                   action='store_true',
                   help='create the simple wordlist')
group.add_argument('-p',
                   '--previewlist',
                   action='store_true',
                   help='create the simple list of previews')
group.add_argument('-g',
                   '--grouppreview',
                   action='store_true',
                   help='create the grouped list of previews')

args = parser.parse_args()
# clarification for argparse, end.

if __name__ == "__main__":
    file_read()
    input_reader()
    if args.wordlist:
        print("Seek the creation of an wordlist")
        output_wordlist()
    elif args.previewlist:
        print("Seek the creation of a previewlist.")
        output_preview_list()
    elif args.grouppreview:
        print("Seek the creation of a grouped previewlist.")
        output_grouped_preview()
