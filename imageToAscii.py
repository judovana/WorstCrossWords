import sys
import os
from PIL import Image
from PIL import ImageEnhance
from ascii_magic import AsciiArt

ASCII_MONOCHROME="ASCII_MONOCHROME"
ASCII_WIDTH="ASCII_WIDTH"

def imgToAscii(filename, width=80):
    my_art = AsciiArt.from_image(filename)
    monochrome=False
    if os.getenv(ASCII_MONOCHROME) and not os.getenv(ASCII_MONOCHROME) == "False":
        monochrome=True
    if os.getenv(ASCII_WIDTH):
        width=int(os.getenv(ASCII_WIDTH))
    my_art.to_terminal(columns=width, monochrome=monochrome)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("one parameter expected - path to file")
        sys.exit(1)
    if len(sys.argv) >= 2:
        imgToAscii(sys.argv[1])
