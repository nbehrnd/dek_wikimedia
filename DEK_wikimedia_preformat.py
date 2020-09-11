# name:    DEK_wikimedia_preformat.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-09-10 (YYYY-MM-DD)
# edit:    2020-09-11 (YYYY-MM-DD)
#
"""Assistant script #4: reformat Wikimedia's list of addresses of .svg.

The 21k+ .svg files by Thirunavukkarasye-Raveendran about DEK's
Verkehrsschrift, published as public domain on Wikimedia, are tagged
with "SVG" and "Deutsche Einheitskurzschrift".  Their addresses may
be collected with these tags by the service

https://tools.wmflabs.org/wikilovesdownloads/

By default, it is a single text file, 1.txt, which is provided within
a .zip archive.

This script extracts the listing from its archive, renames the file,
and adds a brief commentary within the file to share it comfortably
on GitHub while retaining a note about its origin.

Deposit this script in the same folder containing the .zip archive
provided by Wikimedia.  From the CLI of Python, call

python DEK_wikimedia_preformat.py [archive.zip]

where [archive.zip] is the sole and mandatory parameter.  This will
write a text file named [wikimedia_addresses.txt], to reflect the
origin of the data.  Internally, this new file contains a time stamp
in the format of YYYY-MM-DD about the day when this file was written.
It is the same day the Wikimedia archive was downloaded, too.

File [wikimedia_addresses.txt] is the sole - yet mandatory - parameter
to run assistant script #5, DEK_wikimedia_lists.py."""

import os
import sys
import zipfile

from datetime import date
from urllib.parse import unquote


def input_identification():
    """Identify what file should be read."""
    global SOURCE
    SOURCE = ""
    try:
        if sys.argv[1] is not None:
            SOURCE = str(sys.argv[1])
    except:
        print("\nThe expected use of this script is by\n")
        print("    python DEK_wikimedia_preformat.py [archive.zip]\n")
        print("No change of any data.  Exit.\n")
        sys.exit()

    # Preliminary check on the file name:
    if str(SOURCE).endswith(".zip") is False:
        print(
            "Based on the missing .zip extension, the input file was rejected.  Exit."
        )
        sys.exit()


def zip_extract():
    """Attempt to read the .zip file"""
    try:
        zip_archive = zipfile.ZipFile(SOURCE)
        zip_archive.extractall()
        zip_archive.close()
    except IOError:
        print("Failed to read the .zip  archive.")
        sys.exit()


def file_format():
    """Provide a prettified permanent output of the addresses."""
    today = date.today()
    register = []

    header = str("# file: wikimedia_addresses.txt\n")
    header += str("# date: {} (YYYY-MM-DD)\n".format(today))

    # File input:
    try:
        with open("1.txt", mode="r") as source:
            for line in source:

                # To provide the addresses in the order of consecution
                # as DEK_wikimedia_lists.py does for the word-list,
                # the file names (converted into UTF-8, with umlauts)
                # are injected prior to the address strings.  The use
                # of upper and lower case is irrelevant for the sort.
                address_line = str(line).strip()

                key_to_sort = address_line.split("_-_")[-1]
                key_to_sort = unquote(key_to_sort)

                sort_string = ":::".join([key_to_sort, address_line])
                register.append(sort_string)
        register.sort(key=str.lower)

        header += str("# data: {}\n#\n".format(len(register)))
    except IOError:
        print("Unable to read intermediate file '1.txt'.")
        sys.exit()

    # File output:
    try:
        with open("wikimedia_addresses.txt", mode="w") as newfile:
            newfile.write(header)
            for entry in register:
                # Remove of the "key_to_sort", the UTF-8 file name:
                retain = str(entry).split(":::")[-1]
                newfile.write("{}\n".format(retain))
        print("File 'wikimedia_addresses.txt' was written.")

    except IOError:
        print("Writing file 'wikimedia_addresses.txt' failed.  Exit.")
        sys.exit()

    # Space cleaning:
    try:
        os.remove("1.txt")
    except IOError:
        print("Remove of intermediate file '1.txt' failed.")
        sys.exit()


def main():
    """Join the functions."""
    input_identification()
    zip_extract()
    file_format()


if __name__ == "__main__":
    main()
