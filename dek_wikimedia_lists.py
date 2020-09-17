#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_wikimedia_lists.py
# author:  nbehrnd@yahoo.com
# license: MIT 2020
# date:    2020-09-10 (YYYY-MM-DD)
# edit:    2020-09-17 (YYYY-MM-DD)
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
    Skript, dek_wikimedia_lists.py, den dazu alternativen Ansatz,
    Wikimedia abzufragen, welche Dateien simultan mit "SVG" und
    "Deutsche Einheitskurzschrift" verschlagwortet sind (tagged), um
    nur aus dieser Liste die drei hilfreichen Listen zu bilden.  Das
    spart Bandbreite und Zeit, da nun nur noch eine Datei (etwa 3 MB,
    komprimiert etwa 200 kB), statt 21k+ Dateien zu transferieren sind.

    Skript DEK_wikimedia_preformat.py schreibt die hier benutzte Datei
    [wikimedia_addresses.txt] (siehe dort).  Von Pythons Eingabezeile
    wird dieses Skript mit

    python dek_wikimedia_lists.py [wikimedia_addresses.txt]

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

    + Option -v listet die mehrfache Symbolisierungen von gleichen
      langschriftlichen Formen (_v1, _v2, -_v3, -_v4) mit ihrer
      Stammform.  Die Sortierung ist alphabetisch (a-z, ä, ö, ü) ohne
      Berücksichtigung von Gross- oder Kleinschreibung.

    + Option -a listed in alphabetischer Ordnung (a-z, ä, ö, ü; ohne
      Berücksichtigung von Gross- oder Kleinschreibung) Abkürzungen
      darstellende .svg.  Gegenwärtig sind das langschriftliche Formen
      mit mehr als einem Punkt (wie 'd. h.'); oder Formen mit mehr als
      einem Grossbuchstaben bei simultaner Abwesenheit von entweder
      Bindestrich, Unterstrich, Leerzeichen, oder dem kontrastierenden
      String 'ABER'.

    + Option -c listed die Dateien, die die Pronomina ich, du, er, sie
      es, wir, ihr enthalten.  Die Gross- und Kleinschreibung spielt
      weder bei der Identifizierung eine Rolle (auch 'Sie' gilt als
      'sie', 'Ihr´ als 'ihr'), noch bei der Sortierung der Dateinamen
      (a-z, ä, ö, ü).

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


def variant_symbolizations():
    """List the raw_data files drawn in multiple variants.

    Considered are variants explicitly labeled by _v1, _v2, _v3, and
    _v4.  In addition, for a variant .svg named like 'example_v2.svg',
    the script equally suggests the complement file 'example.svg'."""
    variant_register = []
    today = date.today()

    # learn from the past:
    for entry in register:
        # skip plausible commentary lines:
        if str(entry).startswith("#"):
            continue

        if str(entry)[-7:] in ["_v1.svg", "_v2.svg", "_v3.svg", "_v4.svg"]:
            variant = str(entry).split("DEK")[1]
            variant = ''.join(["DEK", variant])

            # Recreate accents and umlauts from the internet notation:
            variant = unquote(str(variant))

            variant_register.append(str(variant))

        # .svg are marked by "_v2.svg", but "_v1.svg" marks may be incomplete:
        if str("_v2.svg") in str(entry):
            complement_file = str(entry).split("DEK")[1]
            complement_file = ''.join(["DEK", complement_file])

            # replace "_v2.svg" by ".svg"
            complement_file = complement_file.split("_v2.svg")[0]
            complement_file = ''.join([complement_file, ".svg"])

            # Recreate accents and umlauts from the internet notation:
            complement_file = unquote(str(complement_file))

            variant_register.append(str(complement_file))
    variant_register.sort(key=str.lower)

    # document findings:
    try:
        with open("wikimedia_variants.txt", mode="w") as newfile:
            # header commentaries
            newfile.write("# name: wikimedia_variants.txt\n")
            newfile.write("# date: {}\n".format(today))
            newfile.write("# data: {}\n#\n".format(len(variant_register)))

            # and the entries:
            for variant in variant_register:
                output = ""
                for char in str(variant):
                    if str(char) == str("_"):
                        output += str(" ")
                    else:
                        output += str(char)
                newfile.write("{}\n".format(str(output)))

        print("File 'wikimedia_variants.txt' was written.")

    except IOError:
        print("Error writing file 'wikimedia_variants.txt'.  Exit.")
        sys.exit()


def check_abbreviations():
    """Identify and report symbolizations about abbreviations.

    Entries are considered to be about an abbreviations if either a)
    the stem contains more than one period, like in 'e.g.', 'd. M.'.
    In addition b), if the stem does not contain a blank ' ' while
    more than one character is upper case, like in 'UNESCO'.  Again,
    the list will be sorted a-z, ä, ö, ü without discern for upper /
    lower case spelling."""

    abbreviation_register = []
    today = date.today()

    # learn from the past:
    for entry in register:
        # skip plausible commentary lines:
        if str(entry).startswith("#"):
            continue

        file = str(entry).split("DEK")[1]
        file = ''.join(["DEK", file])

        # Recreate accents and umlauts from the internet notation:
        file = unquote(str(file))

        # identify the stem:
        stem = str(file).split("_-_")[-1]
        stem = str(stem).split(".svg")[0]

        # test for periods:
        count_periods = 0
        for char in str(stem):
            if str(char) is str("."):
                count_periods += 1
        if count_periods > 1:
            abbreviation_register.append(file)

        # check for upper case characters:
        if (str("ABER") in str(stem)) or (str("_") in str(stem)) or (
                str("-") in str(stem)) or (str(" ") in str(stem)):
            pass
        else:
            count_upper_case = 0
            for char in str(stem):
                if str(char).isupper():
                    count_upper_case += 1
            if count_upper_case > 1:
                abbreviation_register.append(file)
    abbreviation_register.sort(key=str.lower)

    # report the findings:
    try:
        with open("wikimedia_abbreviations.txt", mode="w") as newfile:
            # header comments
            newfile.write("# name: wikimedia_abbreviations.txt\n")
            newfile.write("# date: {}\n".format(today))
            newfile.write("# data: {}\n#\n".format(len(abbreviation_register)))

            for abbreviation in abbreviation_register:
                output = ""
                for char in str(abbreviation):
                    if str(char) == str("_"):
                        output += str(" ")
                    else:
                        output += str(char)
                newfile.write("{}\n".format(str(output)))

        print("File 'wikimedia_abbreviations.txt' was written.")

    except IOError:
        print("Error writing 'wikimedia_abbreviations.txt'.  Exit.")
        sys.exit()


def check_conjugations():
    """Identify symbolizations likely about conjugations.

    A symbolization about conjugation consist of two or more words,
    separated in the file name by an underscore.  In addition, it must
    contain one of the following strings:  'ich_', 'du_', 'er_',
    'sie_', 'es_', 'wir_' or 'ihr_'."""

    conjugation_register = []
    today = date.today()

    # learn from the past:
    for entry in register:
        # skip plausible commentary lines:
        if str(entry).startswith("#"):
            continue

        file = str(entry).split("DEK")[1]
        file = ''.join(["DEK", file])

        # Recreate accents and umlauts from the internet notation:
        file = unquote(str(file))

        # identify the stem:
        stem = str(file).split("_-_")[-1]
        stem = str(stem).split(".svg")[0]

        # exclude explicit variant symbolizations
        if str(stem)[-3:] in ("_v1", "_v2", "_v3", "_v4"):
            continue
        # exclude contrasting symbolizations:
        if str("ABER") in str(stem):
            continue
        # exclude symbolizations with only one word:
        if str("_") not in str(stem):
            continue

        # conjugation test
        test_list = str(stem).split("_")
        example_identified = False
        for word in test_list:
            if (example_identified is False) and (str(word).lower() in [
                    'ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr'
            ]):
                conjugation_register.append(file)
                example_identified = True
    conjugation_register.sort(key=str.lower)

    # report the results:
    try:
        with open("wikimedia_conjugation.txt", mode="w") as newfile:
            # commenting headers:
            newfile.write("# name: wikimedia_conjugation.txt\n")
            newfile.write("# date: {}\n".format(today))
            newfile.write("# data: {}\n#\n".format(len(conjugation_register)))

            for example in conjugation_register:
                output = ""
                for char in str(example):
                    if str(char) == str("_"):
                        output += str(" ")
                    else:
                        output += str(char)
                newfile.write("{}\n".format(str(output)))

        print("File 'wikimedia_conjugation.txt' was written.")

    except IOError:
        print("Error writing file 'wikimedia_conjugation.txt'.  Exit.")
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

group.add_argument('-v',
                   '--variants',
                   action='store_true',
                   help='print a list of .svg drawn in variants')

group.add_argument('-a',
                   '--abbreviations',
                   action='store_true',
                   help='list .svg about abbreviations')

group.add_argument('-c',
                   '--conjugations',
                   action='store_true',
                   help='list .svg about conjugations')

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

    elif args.variants:
        print("Print a list of symbolizations drawn in variants.")
        variant_symbolizations()

    elif args.abbreviations:
        check_abbreviations()

    elif args.conjugations:
        check_conjugations()
