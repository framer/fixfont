#!/usr/bin/env python3

import argparse
import sys
import os
from fontTools.ttx import makeOutputFileName
from fontTools.ttLib import TTFont
from unidecode import unidecode

# WOFF name table IDs
FAMILY = 1
SUBFAMILY = 2
FULL_NAME = 4
POSTSCRIPT_NAME = 6
PREFERRED_FAMILY = 16
PREFERRED_SUBFAMILY = 17
WWS_FAMILY = 21
WWS_SUBFAMILY = 22

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-f", "--family-name")
    parser.add_argument("-s", "--subfamily-name")
    parser.add_argument("--no-rename", action="store_true")
    parser.add_argument("--weight-class", type=int)
    parser.add_argument("--width-class", type=int)
    parser.add_argument("-i", "--italic", action=argparse.BooleanOptionalAction)
    parser.add_argument("--strip-extended-metadata")
    parser.add_argument("-o", "--output")
    options = parser.parse_args()

    font = TTFont(options.input)
    
    if font.flavor not in ("woff2"):
        print("Input file is not a WOFF2 font", file=sys.stderr)
        return 1

    if not options.no_rename:
        family, subfamily = extract_names(options.input, options.family_name, options.subfamily_name)
        full = "%s %s" % (family, subfamily)
        postscript = "%s-%s" % (postscriptify(family), postscriptify(subfamily))[:63]

        for rec in font["name"].names:
            if rec.nameID in [FAMILY, PREFERRED_FAMILY, WWS_FAMILY]:
                rec.string = family
            elif rec.nameID in [SUBFAMILY, PREFERRED_SUBFAMILY, WWS_SUBFAMILY]:
                rec.string = subfamily
            elif rec.nameID == FULL_NAME:
                rec.string = full
            elif rec.nameID == POSTSCRIPT_NAME:
                rec.string = postscript

    if options.weight_class:
        set_weight_class(font, options.weight_class)
    if options.width_class:
        set_width_class(font, options.width_class)
    if options.italic is not None:
        set_italic(font, options.italic)

    # Remove extended metadata and private data
    if options.strip_extended_metadata:
        font.flavorData.metaData = None
        font.flavorData.privData = None

    if options.output:
        font.save(options.output)
    else:
        filename, ext = os.path.splitext(options.input)
        outfile = makeOutputFileName(filename, None, ext)
        font.save(outfile)
        print("Output saved in “%s”" % outfile)

def set_weight_class(font, weight_class: int):
    font["OS/2"].usWeightClass = weight_class

def set_width_class(font, width_class: int):
    font["OS/2"].usWidthClass = width_class

def set_italic(font, italic: bool):
    os2_italic_flag_bitmask = 0x1
    mac_style_italic_flag_bitmask = 0x2
    if italic:
        font["OS/2"].fsSelection |= os2_italic_flag_bitmask
        font["head"].macStyle |= mac_style_italic_flag_bitmask
    else:
        font["OS/2"].fsSelection &= ~os2_italic_flag_bitmask
        font["head"].macStyle &= ~mac_style_italic_flag_bitmask

def postscriptify(name):
    return "".join(char for char in unidecode(name) if 33 <= ord(char) <= 126 and char not in " [](){}<>/%")

def extract_names(file, family_name=None, subfamily_name=None):
    filename, _ = os.path.splitext(os.path.basename(file))

    if filename.count("-") == 1:
        family, subfamily = filename.split("-")
    elif filename.count(" ") == 1:
        family, subfamily = filename.split(" ")
    elif not family_name or not subfamily_name:
        print("Could not figure out names from “%s”" % filename, file=sys.stderr)
        sys.exit(1)

    return family_name or family, subfamily_name or subfamily

if __name__ == "__main__":
    sys.exit(main())
