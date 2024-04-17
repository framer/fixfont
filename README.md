# fixfont.py

WOFF2 fonts intended for use as web fonts are sometimes distributed with
mangled metadata to “protect” them from being used as desktop fonts. Some tools
however, like Framer, rely on having the metadata available to show something
sensible in the UI.

This script can be used to fix the metadata of those fonts files.

## Usage

```
fixfont.py <font.woff2> [-f "family name"] [-s "subfamily name"] [-o output.woff2]
```

- `font.woff2`: the path to the input font, has to be in woff2 format
- `-f family name`: the name of the font, make sure to use quotes if this contains spaces, e.g `-f "My Font"`. If not provided, it will try to figure out the name from the input file.
- `-s subfamily name`: also called the style or variant of the font, usually this is something like `-s Regular`, `-s Bold`, `-s Thin`, etc. If not provided, it will try to figure out the name from the input file.
- `-o output.woff2`: the path to where to write the result, if not specified, the script will put it next to the input file and will output where it has written the result.

## Requirements

The requirements are provided in `requirements.txt`. Install them with `pip install -r requirements.txt`.

Running in a Python virtual environment is recommended.
