"""Build-time glyph rasteriser (NOT part of the entry).

Rasterises DejaVu glyphs to 4-bit alpha maps, base85-packed, in the
tuple format main.py consumes: (advance, bx, by, w, h, b85), where
bx/by are ink offsets from the pen origin at the ascender line.
Output: glyphs.py with one dict per font, each dict on a single line
so the generated data stays a handful of lines.
"""
import base64
import string
import zlib

from PIL import Image, ImageDraw, ImageFont

FONTS = [
    ("SERIF", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 96),
    ("SERIFR", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 96),
    ("SANS", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48),
    ("SANSB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48),
]

EXTRA = ("€·—–×−°’‘“”•…±"
         "àáâäåæçèéêëìíîïñòóôöøùúûüýÿß"
         "ÀÁÂÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÖØÙÚÛÜÝ"
         "✓✗★●○▲▼←→↑↓¡¿")
CHARS = [chr(i) for i in range(32, 127)] + list(EXTRA)


def rasterise(path, em):
    font = ImageFont.truetype(path, em)
    asc, desc = font.getmetrics()
    out = {}
    for ch in CHARS:
        adv = int(round(font.getlength(ch)))
        img = Image.new("L", (em * 3, em * 3), 0)
        d = ImageDraw.Draw(img)
        d.text((em, em), ch, font=font, fill=255, anchor="la")
        bbox = img.getbbox()
        if bbox is None:
            out[ch] = (adv, 0, 0, 0, 0, "")
            continue
        x0, y0, x1, y1 = bbox
        crop = img.crop(bbox)
        w, h = crop.size
        px = crop.load()
        nibbles = []
        for yy in range(h):
            for xx in range(w):
                nibbles.append(px[xx, yy] >> 4)
        packed = bytearray()
        for i in range(0, len(nibbles), 2):
            hi = nibbles[i]
            lo = nibbles[i + 1] if i + 1 < len(nibbles) else 0
            packed.append((hi << 4) | lo)
        b85 = base64.b85encode(zlib.compress(bytes(packed), 9)).decode("ascii")
        out[ch] = (adv, x0 - em, y0 - em, w, h, b85)
    return asc, desc, out


def main():
    lines = ['"""Glyph bitmap data rasterised from DejaVu (free licence).',
             "",
             "Generated at build time by gen_glyphs.py. Each glyph:",
             "(advance, bearing_x, bearing_y, width, height, base85 of",
             "4-bit alpha, high nibble first). Bearings are ink offsets",
             "from the pen origin on the ascender line.",
             '"""', ""]
    for name, path, em in FONTS:
        asc, desc, glyphs = rasterise(path, em)
        lines.append("%s_EM = %d" % (name, em))
        lines.append("%s_ASC = %d" % (name, asc))
        lines.append("%s_DESC = %d" % (name, desc))
        lines.append("%s = %r" % (name, glyphs))
        lines.append("")
        print(name, "asc", asc, "desc", desc, "glyphs", len(glyphs))
    with open("glyphs.py", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote glyphs.py")


if __name__ == "__main__":
    main()
