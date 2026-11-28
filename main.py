"""THE WORLD IN ONE DAY - Friday 27 November 2026.

A program that draws one 1024x1024 newspaper front page summing up
the world's news of Friday 27 November 2026, for the make.fun
bounty news-image-20261127, entered by @badd-airdrop2.

Pure Python 3 standard library only: no network, no fonts on disk,
no randomness, no clock. Type is set from glyph bitmaps rasterised
from DejaVu (free licence) and carried in glyphs.py beside this
file; the page is drawn on a 2x supersampled canvas with a
hand-written PNG encoder and written to /output/entry.png.
Running it twice writes the same bytes.

Every story on the page happened or was first reported on Friday
27 November 2026 in some time zone, as the named outlets reported
it. Stories that look like 27 November news but are not are listed
in the DATE CHECK panel with their real dates. All times are UTC.
The design leads with drawn pictorial scenes in every hero and
grid card; statistics and badges stay secondary.
"""

import base64
import math
import os
import struct
import sys
import zlib

# The grader runs `python3 -P -s main.py`, which keeps this file's
# directory off sys.path; put it back so the sibling modules
# (glyphs, stories) import in every environment.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from glyphs import (SERIF, SERIF_ASC, SERIF_DESC, SERIF_EM,
                    SERIFR, SERIFR_ASC, SERIFR_DESC, SERIFR_EM,
                    SANS, SANS_ASC, SANS_DESC, SANS_EM,
                    SANSB, SANSB_ASC, SANSB_DESC, SANSB_EM)
from stories import STORIES, TIMELINE, DATECHECK, NUMBERS

W = 1024
H = 1024
SS = 2                      # supersampling factor (canvas is W*SS)
MX = 24                     # page margin
CW = W - 2 * MX             # content width

PAPER = (247, 243, 234)
INK = (26, 30, 44)
NAVY = (31, 49, 85)
GOLD = (176, 132, 46)
RED = (168, 44, 38)
GREY = (96, 100, 112)
RULE = (196, 190, 174)
CREAM = (255, 253, 247)

# Region colours, slots 0..12 (see stories.py).
REGIONS = [
    ("NORTH AMERICA", (178, 84, 52)),
    ("SOUTH AMERICA", (120, 150, 70)),
    ("NORTH EUROPE", (80, 120, 180)),
    ("WEST EUROPE", (62, 96, 150)),
    ("EAST EUROPE", (110, 130, 170)),
    ("MIDDLE EAST", (196, 150, 60)),
    ("AFRICA", (150, 96, 48)),
    ("SOUTH ASIA", (196, 110, 60)),
    ("SOUTHEAST ASIA", (70, 150, 120)),
    ("EAST ASIA", (170, 60, 70)),
    ("OCEANIA", (60, 140, 170)),
    ("GLOBAL", (90, 90, 120)),
    ("SPACE", (52, 58, 96)),
]

REGION_SHORT = ["N.AMERICA", "S.AMERICA", "N.EUROPE", "W.EUROPE", "E.EUROPE",
                "MID EAST", "AFRICA", "S.ASIA", "SE.ASIA", "E.ASIA",
                "OCEANIA", "GLOBAL", "SPACE"]

# ---------------------------------------------------------------- glyphs
_GCACHE = {}


def glyph_alpha(font, ch):
    """Decode a glyph's 4-bit alpha map to bytes (cached)."""
    key = (id(font), ch)
    got = _GCACHE.get(key)
    if got is not None:
        return got
    _adv, _bx, _by, w, h, b85 = font.get(ch) or font["?"]
    if not b85:
        _GCACHE[key] = b""
        return b""
    packed = zlib.decompress(base64.b85decode(b85))
    out = bytearray(w * h)
    for i in range(w * h):
        byte = packed[i // 2]
        out[i] = ((byte >> 4) if i % 2 == 0 else (byte & 15)) * 17
    _GCACHE[key] = bytes(out)
    return _GCACHE[key]


def text_width(s, font, em, size, tracking=0.0):
    """Width in logical px of s set at `size` (logical px em)."""
    scale = size * SS / em
    total = 0.0
    for ch in s:
        g = font.get(ch) or font["?"]
        total += g[0] * scale / SS + tracking
    return total - (tracking if s else 0.0)


def wrap_text(s, font, em, size, max_width, tracking=0.0):
    words = s.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, font, em, size, tracking) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    """Logical W x H canvas stored at SS supersampling."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.dw = w * SS
        self.dh = h * SS
        self.px = bytearray(bg * self.dw * self.dh)
        self.clip = None          # (x0, y0, x1, y1) in device px

    def set_clip(self, x, y, w, h):
        self.clip = (int(x * SS), int(y * SS),
                     int((x + w) * SS), int((y + h) * SS))

    def clear_clip(self):
        self.clip = None

    def _inside(self, x, y):
        if self.clip is None:
            return True
        x0, y0, x1, y1 = self.clip
        return x0 <= x < x1 and y0 <= y < y1

    def set(self, x, y, color):
        if 0 <= x < self.dw and 0 <= y < self.dh and self._inside(x, y):
            i = (y * self.dw + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def blend(self, x, y, color, a):
        if a <= 0 or not (0 <= x < self.dw and 0 <= y < self.dh) \
                or not self._inside(x, y):
            return
        if a >= 255:
            self.set(x, y, color)
            return
        i = (y * self.dw + x) * 3
        inv = 255 - a
        self.px[i] = (color[0] * a + self.px[i] * inv) // 255
        self.px[i + 1] = (color[1] * a + self.px[i + 1] * inv) // 255
        self.px[i + 2] = (color[2] * a + self.px[i + 2] * inv) // 255

    def rect(self, x, y, w, h, color):
        x, y, w, h = int(x * SS), int(y * SS), int(w * SS), int(h * SS)
        if w <= 0 or h <= 0:
            return
        if self.clip is not None:
            cx0, cy0, cx1, cy1 = self.clip
            x = max(x, cx0)
            y = max(y, cy0)
            w = min(x + w, cx1) - x
            h = min(y + h, cy1) - y
            if w <= 0 or h <= 0:
                return
        row = bytes(color) * w
        for yy in range(y, y + h):
            if 0 <= yy < self.dh:
                i = (yy * self.dw + x) * 3
                self.px[i:i + len(row)] = row

    def frame(self, x, y, w, h, color, t=1):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def vgrad(self, x, y, w, h, top, bottom):
        x, y, w, h = int(x * SS), int(y * SS), int(w * SS), int(h * SS)
        if w <= 0 or h <= 0:
            return
        if self.clip is not None:
            cx0, cy0, cx1, cy1 = self.clip
            x = max(x, cx0)
            y = max(y, cy0)
            w = min(x + w, cx1) - x
            h = min(y + h, cy1) - y
            if w <= 0 or h <= 0:
                return
        for yy in range(y, y + h):
            t = (yy - y) / max(1, h - 1)
            c = (int(top[0] + (bottom[0] - top[0]) * t),
                 int(top[1] + (bottom[1] - top[1]) * t),
                 int(top[2] + (bottom[2] - top[2]) * t))
            row = bytes(c) * w
            i = (yy * self.dw + x) * 3
            self.px[i:i + len(row)] = row

    def line(self, x0, y0, x1, y1, color, t=1):
        x0, y0, x1, y1 = int(x0 * SS), int(y0 * SS), int(x1 * SS), int(y1 * SS)
        t = max(1, int(round(t * SS)))
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for oy in range(t):
                for ox in range(t):
                    self.set(x + ox, y + oy, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color):
        cx, cy, r = int(cx * SS), int(cy * SS), int(r * SS)
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def ring(self, cx, cy, r, color, t=2):
        cx, cy, r, t = int(cx * SS), int(cy * SS), int(r * SS), int(t * SS)
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 <= d <= r * r:
                    self.set(xx, yy, color)

    def polygon(self, pts, color):
        pts = [(x * SS, y * SS) for (x, y) in pts]
        miny = int(min(p[1] for p in pts))
        maxy = int(max(p[1] for p in pts))
        n = len(pts)
        for yy in range(miny, maxy + 1):
            nodes = []
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if y0 == y1:
                    continue
                if (yy >= min(y0, y1)) and (yy < max(y0, y1)):
                    nodes.append(x0 + (yy - y0) * (x1 - x0) / (y1 - y0))
            nodes.sort()
            for i in range(0, len(nodes) - 1, 2):
                xa = int(nodes[i])
                xb = int(nodes[i + 1])
                for xx in range(xa, xb + 1):
                    self.set(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        self.polygon([(x0, y0), (x1, y1), (x2, y2)], color)

    # ---- text ----
    def text(self, x, y, s, font, em, asc, size, color, tracking=0.0):
        """Draw text with baseline at logical y; returns x after it."""
        scale = size * SS / em
        cx = x * SS
        baseline = y * SS
        for ch in s:
            g = font.get(ch) or font["?"]
            adv, bx, by, w, h, _b85 = g
            if w and h:
                alpha = glyph_alpha(font, ch)
                gx = cx + bx * scale
                gy = baseline - asc * scale + by * scale
                dw = max(1, int(round(w * scale)))
                dh = max(1, int(round(h * scale)))
                for dy in range(dh):
                    sy = dy / scale
                    iy = int(sy)
                    fy = sy - iy
                    for dx in range(dw):
                        sx = dx / scale
                        ix = int(sx)
                        fx = sx - ix
                        a00 = alpha[iy * w + ix] if iy < h and ix < w else 0
                        a10 = alpha[iy * w + ix + 1] if iy < h and ix + 1 < w else 0
                        a01 = alpha[(iy + 1) * w + ix] if iy + 1 < h and ix < w else 0
                        a11 = alpha[(iy + 1) * w + ix + 1] if iy + 1 < h and ix + 1 < w else 0
                        a = int(a00 * (1 - fx) * (1 - fy) + a10 * fx * (1 - fy)
                                + a01 * (1 - fx) * fy + a11 * fx * fy)
                        if a:
                            self.blend(int(gx) + dx, int(gy) + dy, color, a)
            cx += adv * scale + tracking * SS
        return cx / SS

    def text_center(self, cx, y, s, font, em, asc, size, color,
                    tracking=0.0):
        w = text_width(s, font, em, size, tracking)
        return self.text(cx - w / 2, y, s, font, em, asc, size, color,
                         tracking)

    def text_right(self, right, y, s, font, em, asc, size, color,
                   tracking=0.0):
        w = text_width(s, font, em, size, tracking)
        return self.text(right - w, y, s, font, em, asc, size, color,
                         tracking)

    def para(self, x, y, s, font, em, asc, size, color, max_width,
             leading=None, tracking=0.0):
        """Wrapped paragraph; y is the first baseline; returns y after."""
        if leading is None:
            leading = size * 1.35
        for line in wrap_text(s, font, em, size, max_width, tracking):
            self.text(x, y, line, font, em, asc, size, color, tracking)
            y += leading
        return y

    def downsample(self):
        out = bytearray(W * H * 3)
        for y in range(H):
            for x in range(W):
                r = g = b = 0
                for oy in range(SS):
                    base = ((y * SS + oy) * self.dw + x * SS) * 3
                    for ox in range(SS):
                        i = base + ox * 3
                        r += self.px[i]
                        g += self.px[i + 1]
                        b += self.px[i + 2]
                n = SS * SS
                j = (y * W + x) * 3
                out[j] = r // n
                out[j + 1] = g // n
                out[j + 2] = b // n
        return out


# ---------------------------------------------------------------- PNG encoder
def png_bytes(raw):
    rows = bytearray()
    stride = W * 3
    for y in range(H):
        rows.append(0)
        start = y * stride
        rows.extend(raw[start:start + stride])
    data = zlib.compress(bytes(rows), 9)

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        out += struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", data) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- scenes
# Flat editorial vector scenes: layered silhouettes, graded skies,
# small human figures. Every hero and grid card leads with one of
# these storytelling pictures rather than a labelled diagram.

SKY_TOP = (84, 148, 212)
SKY_LOW = (202, 230, 248)
NIGHT_TOP = (12, 20, 58)
NIGHT_LOW = (46, 62, 118)
SEA_C = (36, 118, 176)
SEA_D = (24, 78, 128)
LAND = (82, 150, 78)
LAND_D = (50, 110, 56)
SAND = (222, 200, 150)
STONE = (150, 146, 138)
STONE_D = (104, 100, 94)
ROOF = (120, 70, 56)
WHITE = (250, 248, 240)
FLAME = (238, 120, 40)
FLAME_Y = (250, 196, 80)
SMOKE = (120, 122, 130)
SIL = (38, 42, 58)


def _sky(c, x, y, w, h, dark=False, dusk=False):
    if dark:
        c.vgrad(x, y, w, h, NIGHT_TOP, NIGHT_LOW)
    elif dusk:
        c.vgrad(x, y, w, h, (250, 176, 96), (238, 120, 92))
    else:
        c.vgrad(x, y, w, h, SKY_TOP, SKY_LOW)


def _sun(c, cx, cy, r):
    c.circle(cx, cy, r + 3, (250, 226, 150))
    c.circle(cx, cy, r, (252, 214, 110))


def _cloud(c, cx, cy, s, col=(250, 250, 248)):
    c.circle(cx, cy, s, col)
    c.circle(cx + s * 0.9, cy + s * 0.15, s * 0.75, col)
    c.circle(cx - s * 0.9, cy + s * 0.2, s * 0.7, col)
    c.rect(cx - s * 1.4, cy, s * 2.8, s * 0.55, col)


def _sea(c, x, y, w, h):
    c.vgrad(x, y, w, h, SEA_C, SEA_D)
    for i in range(7):
        wx = x + (i * 37) % max(10, int(w - 14))
        wy = y + 3 + (i * 5) % max(4, int(h - 6))
        c.hline(wx, wy, 10, (170, 205, 225), 1)


def _person(c, cx, base, s, col=SIL):
    c.circle(cx, base - s * 1.55, s * 0.32, col)
    c.rect(cx - s * 0.28, base - s * 1.25, s * 0.56, s * 1.25, col)


def _building(c, x, y, w, h, col=STONE, roof=ROOF, cols=4):
    c.rect(x, y, w, h, col)
    c.triangle(x - 3, y, x + w + 3, y, x + w / 2, y - h * 0.32, roof)
    for i in range(cols):
        wx = x + 4 + i * (w - 8) / max(1, cols)
        c.rect(wx, y + h * 0.25, 3, h * 0.5, (240, 236, 220))


def _tree(c, cx, base, s):
    c.rect(cx - 1, base - s * 0.5, 2, s * 0.5, (90, 66, 44))
    c.circle(cx, base - s * 0.85, s * 0.45, LAND_D)
    c.circle(cx - s * 0.3, base - s * 0.6, s * 0.32, LAND)


def scene_ballot(c, x, y, w, h, rcol):
    _sky(c, x, y, w, h)
    _sun(c, x + w * 0.82, y + h * 0.22, h * 0.09)
    _cloud(c, x + w * 0.2, y + h * 0.16, h * 0.06)
    gy = y + h * 0.72
    c.rect(x, gy, w, h * 0.28, LAND)
    # parliament: dome + colonnade
    bx = x + w * 0.08
    bw = w * 0.52
    bh = h * 0.42
    by = gy - bh
    c.rect(bx, by, bw, bh, STONE)
    c.circle(bx + bw / 2, by - bh * 0.05, bw * 0.16, STONE_D)
    c.rect(bx + bw / 2 - 1, by - bh * 0.34, 2, bh * 0.2, STONE_D)
    for i in range(6):
        c.rect(bx + 5 + i * (bw - 10) / 6, by + bh * 0.22, 3, bh * 0.66,
               (238, 234, 222))
    c.rect(bx - 3, by - 3, bw + 6, 4, STONE_D)
    # flag on dome
    c.vline(bx + bw / 2, by - bh * 0.52, bh * 0.2, SIL, 1)
    c.polygon([(bx + bw / 2, by - bh * 0.52),
               (bx + bw / 2 + 12, by - bh * 0.46),
               (bx + bw / 2, by - bh * 0.4)], rcol)
    # seat diagram panel, right: the deadlock in numbers —
    # right bloc 65, left bloc 58, Opportunity 7 holds balance
    px = x + w * 0.695
    py = y + h * 0.1
    pw = w * 0.285
    ph = h * 0.58
    c.rect(px, py, pw, ph, (250, 248, 240))
    c.frame(px, py, pw, ph, INK, 1)
    c.text_center(px + pw / 2, py + h * 0.11, "PARLIAMENT SEATS",
                  SANSB, SANSB_EM, SANSB_ASC, 6.2, NAVY, 0.3)
    blocs = [("RIGHT", 65, (50, 90, 170)), ("LEFT", 58, (200, 60, 50)),
             ("OPPORTUNITY", 7, (240, 180, 60))]
    barw = pw - 10
    for i, (name, seats, col) in enumerate(blocs):
        by2 = py + h * (0.19 + i * 0.135)
        c.text(px + 5, by2, name, SANSB, SANSB_EM, SANSB_ASC, 5.6, INK, 0.1)
        c.text_right(px + pw - 5, by2, str(seats), SANSB, SANSB_EM,
                     SANSB_ASC, 8.5, col)
        c.rect(px + 5, by2 + h * 0.025, barw * seats / 65, h * 0.05, col)
    # majority marker: 66 seats to govern — neither bloc has it
    mx2 = px + 5 + barw * 66 / 65
    for i in range(4):
        c.vline(mx2, py + h * (0.24 + i * 0.09), h * 0.05, INK, 1)
    c.text(px + 5, py + h * 0.6, "66 TO GOVERN — NEITHER HAS IT",
           SANSB, SANSB_EM, SANSB_ASC, 4.8, RED, 0.1)
    # voters queue
    for i in range(4):
        _person(c, x + w * (0.66 + i * 0.07), gy + h * 0.2, h * 0.11,
                SIL if i % 2 else (70, 60, 80))
    _tree(c, x + w * 0.05, gy + h * 0.16, h * 0.3)
    # detail layer: side wing, path, lamp posts, birds, more voters
    c.rect(bx + bw + 4, by + bh * 0.25, w * 0.1, bh * 0.75, STONE)
    c.triangle(bx + bw + 1, by + bh * 0.25, bx + bw + w * 0.1 + 3,
               by + bh * 0.25, bx + bw + w * 0.05, by + bh * 0.05, ROOF)
    c.polygon([(bx + bw * 0.3, gy + h * 0.28), (bx + bw * 0.62, gy + h * 0.28),
               (bx + bw * 0.56, gy), (bx + bw * 0.36, gy)], (226, 214, 184))
    for i in range(3):
        lx = x + w * (0.14 + i * 0.2)
        c.vline(lx, gy - h * 0.06, h * 0.18, SIL, 1)
        c.circle(lx, gy - h * 0.08, 2.2, (252, 232, 160))
    for i in range(3):
        _person(c, x + w * (0.3 + i * 0.09), gy + h * 0.24, h * 0.1,
                (120, 60, 60) if i % 2 else (50, 70, 110))
    for (bx2, by2) in [(0.42, 0.1), (0.5, 0.07), (0.58, 0.12)]:
        c.line(x + w * bx2 - 3, y + h * by2, x + w * bx2, y + h * by2 - 2,
               SIL, 1)
        c.line(x + w * bx2, y + h * by2 - 2, x + w * bx2 + 3,
               y + h * by2, SIL, 1)


def scene_rocket(c, x, y, w, h, rcol):
    _sky(c, x, y, w, h, dark=True)
    # stars (fixed pattern, no randomness)
    for i in range(26):
        sx = x + (i * 53) % int(w)
        sy = y + (i * 29) % int(h * 0.55)
        c.circle(sx, sy, 1, (230, 236, 250))
    c.circle(x + w * 0.86, y + h * 0.16, h * 0.07, (238, 240, 232))
    c.circle(x + w * 0.83, y + h * 0.14, h * 0.06, NIGHT_TOP)
    gy = y + h * 0.8
    _sea(c, x, gy + h * 0.08, w, h * 0.12)
    c.rect(x, gy, w, h * 0.09, (44, 52, 66))
    # launch tower
    tx = x + w * 0.3
    c.rect(tx, gy - h * 0.52, 4, h * 0.52, (90, 96, 112))
    for i in range(5):
        c.hline(tx - 4, gy - h * (0.1 + i * 0.1), 12, (90, 96, 112), 1)
    # rocket body climbing
    rx = x + w * 0.42
    ry = y + h * 0.1
    rw = w * 0.07
    rh = h * 0.34
    c.polygon([(rx, ry + rh), (rx + rw, ry + rh),
               (rx + rw, ry + rh * 0.25), (rx + rw / 2, ry),
               (rx, ry + rh * 0.25)], WHITE)
    c.rect(rx, ry + rh * 0.55, rw, rh * 0.1, rcol)
    c.circle(rx + rw / 2, ry + rh * 0.4, rw * 0.2, NAVY)
    c.polygon([(rx, ry + rh), (rx - rw * 0.5, ry + rh * 1.14),
               (rx, ry + rh * 0.8)], (200, 70, 60))
    c.polygon([(rx + rw, ry + rh), (rx + rw * 1.5, ry + rh * 1.14),
               (rx + rw, ry + rh * 0.8)], (200, 70, 60))
    # exhaust plume down to pad
    c.polygon([(rx + rw * 0.2, ry + rh), (rx + rw * 0.8, ry + rh),
               (rx + rw * 1.15, gy), (rx - rw * 0.15, gy)], FLAME_Y)
    c.polygon([(rx + rw * 0.35, ry + rh), (rx + rw * 0.65, ry + rh),
               (rx + rw * 0.9, gy), (rx + rw * 0.1, gy)], FLAME)
    # smoke billows at pad
    for i, (dx, s) in enumerate([(0, 0.1), (0.09, 0.13), (0.19, 0.1),
                                 (-0.08, 0.08)]):
        c.circle(rx + w * dx + rw / 2, gy - h * 0.02, h * s, (150, 152, 162))
    c.circle(rx + rw / 2, gy - h * 0.05, h * 0.06, FLAME_Y)
    # detail layer: pad floodlights, hills, flame reflection on sea
    c.polygon([(x, gy), (x + w * 0.18, gy - h * 0.12), (x + w * 0.3, gy)],
              (36, 46, 62))
    c.polygon([(x + w * 0.72, gy), (x + w * 0.88, gy - h * 0.1), (x + w, gy)],
              (36, 46, 62))
    for i in range(4):
        c.circle(x + w * (0.12 + i * 0.24), gy - h * 0.03, 1.8,
                 (252, 232, 160))
    c.rect(rx + rw * 0.15, gy + h * 0.1, rw * 0.7, h * 0.05, FLAME)
    c.rect(rx + rw * 0.3, gy + h * 0.16, rw * 0.4, h * 0.03, FLAME_Y)
    for i in range(10):
        c.circle(x + (i * 97) % int(w), y + (i * 41) % int(h * 0.4), 1,
                 (240, 244, 252))


def scene_jets(c, x, y, w, h, rcol):
    """Taiwan: island, median line, jets circling the island."""
    _sky(c, x, y, w, h)
    _sun(c, x + w * 0.08, y + h * 0.12, h * 0.06)
    _cloud(c, x + w * 0.3, y + h * 0.12, h * 0.045)
    sy = y + h * 0.55
    _sea(c, x, sy, w, h * 0.45)
    # mainland coast, far left
    c.polygon([(x, y + h * 0.3), (x + w * 0.14, y + h * 0.42),
               (x + w * 0.17, sy + h * 0.1), (x + w * 0.1, y + h),
               (x, y + h)], LAND_D)
    c.text(x + 3, y + h * 0.38, "MAINLAND", SANSB, SANSB_EM, SANSB_ASC,
           5.2, (250, 248, 240), 0.2)
    # Taiwan island: elongated, tilted, centre-right
    isl = [(0.6, 0.14), (0.64, 0.26), (0.655, 0.42), (0.64, 0.6),
           (0.615, 0.78), (0.585, 0.9), (0.565, 0.74), (0.555, 0.54),
           (0.56, 0.34), (0.575, 0.2)]
    c.polygon([(x + w * a, y + h * b) for (a, b) in isl], LAND)
    c.polygon([(x + w * a, y + h * b) for (a, b) in
               [(0.6, 0.2), (0.63, 0.34), (0.63, 0.52), (0.61, 0.68),
                (0.59, 0.8), (0.58, 0.62), (0.575, 0.42), (0.58, 0.28)]],
              LAND_D)
    c.text_center(x + w * 0.605, y + h * 0.52, "TAIWAN", SANSB, SANSB_EM,
                  SANSB_ASC, 6.0, (250, 248, 240), 0.2)
    # median line of the strait: dashed, between mainland and island
    mx2 = x + w * 0.37
    for i in range(7):
        c.vline(mx2, y + h * (0.08 + i * 0.12), h * 0.07, (220, 70, 60), 2)
    c.text_center(mx2, y + h * 0.07, "MEDIAN LINE", SANSB, SANSB_EM,
                  SANSB_ASC, 5.2, RED, 0.2)
    # circling path around the island (dashed ellipse)
    cx, cy = x + w * 0.605, y + h * 0.52
    rx, ry = w * 0.3, h * 0.38
    for i in range(28):
        if i % 2:
            continue
        a0 = 2 * math.pi * i / 28
        a1 = 2 * math.pi * (i + 1) / 28
        c.line(cx + rx * math.cos(a0), cy + ry * math.sin(a0),
               cx + rx * math.cos(a1), cy + ry * math.sin(a1),
               (240, 120, 90), 1)
    # eight jets flying the circle, noses along the tangent
    for i in range(8):
        a = 2 * math.pi * i / 8 + 0.4
        px = cx + rx * math.cos(a)
        py = cy + ry * math.sin(a)
        tx2, ty2 = -rx * math.sin(a), ry * math.cos(a)
        tl = math.hypot(tx2, ty2) or 1
        tx2, ty2 = tx2 / tl, ty2 / tl
        u = h * 0.055
        nose = (px + tx2 * u * 1.5, py + ty2 * u * 1.5)
        tail = (px - tx2 * u, py - ty2 * u)
        w1 = (px - tx2 * u * 0.2 - ty2 * u, py - ty2 * u * 0.2 + tx2 * u)
        w2 = (px - tx2 * u * 0.2 + ty2 * u, py - ty2 * u * 0.2 - tx2 * u)
        c.polygon([nose, w1, tail, w2], SIL)
        c.line(px - tx2 * u * 3.2, py - ty2 * u * 3.2, tail[0], tail[1],
               (245, 246, 248), 1)
    # three crossing arrows over the median line
    for i, fy in enumerate((0.3, 0.5, 0.7)):
        ay = y + h * fy
        c.line(mx2 - w * 0.07, ay, mx2 + w * 0.07, ay, RED, 2)
        c.polygon([(mx2 + w * 0.07, ay), (mx2 + w * 0.045, ay - 3),
                   (mx2 + w * 0.045, ay + 3)], RED)


def _grid_base(c, x, y, w, h, rcol, dark=False, dusk=False):
    _sky(c, x, y, w, h, dark=dark, dusk=dusk)
    return y + h * 0.74


def scene_prices(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (210, 196, 170))
    _building(c, x + w * 0.06, gy - h * 0.52, w * 0.5, h * 0.52)
    c.rect(x + w * 0.06, gy - h * 0.3, w * 0.5, h * 0.08, rcol)
    for i in range(5):
        c.triangle(x + w * (0.08 + i * 0.1), gy - h * 0.22,
                   x + w * (0.13 + i * 0.1), gy - h * 0.22,
                   x + w * (0.105 + i * 0.1), gy - h * 0.15, WHITE)
    # rising price tags
    for i, th in enumerate([0.16, 0.26, 0.38]):
        tx = x + w * (0.62 + i * 0.11)
        ty = gy - h * th
        c.polygon([(tx, ty), (tx + w * 0.09, ty), (tx + w * 0.09, ty + h * 0.12),
                   (tx + w * 0.045, ty + h * 0.17), (tx, ty + h * 0.12)],
                  (250, 240, 200))
        c.circle(tx + w * 0.045, ty + h * 0.03, 1.5, rcol)
    c.line(x + w * 0.6, gy - h * 0.1, x + w * 0.92, gy - h * 0.42, RED, 2)
    c.triangle(x + w * 0.92, gy - h * 0.42, x + w * 0.86, gy - h * 0.4,
               x + w * 0.9, gy - h * 0.34, RED)
    # detail layer: skyline behind, awning stripes, shoppers, big tag
    for i, bh2 in enumerate((0.3, 0.44, 0.36, 0.5)):
        c.rect(x + w * (0.58 + i * 0.1), gy - h * bh2, w * 0.08, h * bh2,
               (140, 152, 176))
    for i in range(5):
        c.rect(x + w * (0.06 + i * 0.1), gy - h * 0.3, w * 0.05, h * 0.08,
               WHITE if i % 2 else (220, 90, 80))
    for i in range(3):
        _person(c, x + w * (0.16 + i * 0.14), gy + h * 0.2, h * 0.13,
                (90, 60, 90) if i % 2 else SIL)
    c.polygon([(x + w * 0.8, gy - h * 0.52), (x + w * 0.93, gy - h * 0.52),
               (x + w * 0.93, gy - h * 0.38), (x + w * 0.865, gy - h * 0.32),
               (x + w * 0.8, gy - h * 0.38)], (250, 220, 120))
    c.text_center(x + w * 0.865, gy - h * 0.42, "%", SANSB, SANSB_EM,
                  SANSB_ASC, h * 0.14, RED)
    # Tokyo layer: lattice tower, price board with rising bars
    twx = x + w * 0.47
    c.polygon([(twx, gy), (twx + w * 0.05, gy), (twx + w * 0.03, gy - h * 0.72),
               (twx + w * 0.02, gy - h * 0.72)], (200, 90, 80))
    for i in range(4):
        c.hline(twx + w * (0.006 + i * 0.002), gy - h * (0.16 + i * 0.16),
                w * 0.04 - i * w * 0.004, (160, 60, 50), 1)
    c.vline(twx + w * 0.025, gy - h * 0.86, h * 0.14, (160, 60, 50), 1)
    bx2 = x + w * 0.6
    by2 = gy - h * 0.34
    c.rect(bx2, by2, w * 0.3, h * 0.26, (30, 36, 54))
    for i, bh3 in enumerate((0.08, 0.13, 0.18, 0.22)):
        c.rect(bx2 + w * (0.03 + i * 0.07), by2 + h * 0.24 - h * bh3,
               w * 0.045, h * bh3, (140, 230, 160))
    c.line(bx2 + w * 0.03, by2 + h * 0.18, bx2 + w * 0.27, by2 + h * 0.04,
           (250, 214, 110), 2)


def scene_tanker(c, x, y, w, h, rcol):
    _sky(c, x, y, w, h)
    _sun(c, x + w * 0.84, y + h * 0.2, h * 0.08)
    sy = y + h * 0.58
    _sea(c, x, sy, w, h * 0.42)
    hx = x + w * 0.1
    hw = w * 0.74
    hy = sy - h * 0.16
    c.polygon([(hx, hy), (hx + hw, hy), (hx + hw * 0.92, hy + h * 0.18),
               (hx + hw * 0.08, hy + h * 0.18)], (52, 58, 76))
    c.rect(hx + hw * 0.06, hy - h * 0.14, hw * 0.6, h * 0.14, (196, 84, 60))
    for i in range(4):
        c.circle(hx + hw * (0.16 + i * 0.13), hy - h * 0.07, h * 0.05,
                 (226, 120, 86))
    c.rect(hx + hw * 0.72, hy - h * 0.26, hw * 0.14, h * 0.26, WHITE)
    c.rect(hx + hw * 0.72, hy - h * 0.26, hw * 0.14, h * 0.06, rcol)
    c.hline(hx + hw * 0.74, hy - h * 0.17, hw * 0.1, NAVY, 2)
    c.line(hx + hw * 0.9, hy + h * 0.1, hx + hw * 1.02, hy + h * 0.2,
           (200, 224, 238), 2)
    # detail layer: shore storage tanks, loading pipes, gulls, wake
    for i in range(2):
        tx2 = x + w * (0.86 + i * 0.07)
        c.rect(tx2, sy - h * 0.2, w * 0.055, h * 0.2, (210, 214, 220))
        c.circle(tx2 + w * 0.027, sy - h * 0.2, w * 0.027, (186, 192, 200))
    c.line(hx + hw * 0.8, hy - h * 0.05, x + w * 0.88, sy - h * 0.12,
           (150, 156, 166), 2)
    c.line(hx + hw * 0.02, hy + h * 0.14, hx - w * 0.06, hy + h * 0.24,
           (200, 224, 238), 2)
    for (gx2, gy2) in [(0.3, 0.14), (0.4, 0.1), (0.52, 0.16)]:
        c.line(x + w * gx2 - 3, y + h * gy2, x + w * gx2, y + h * gy2 - 2,
               SIL, 1)
        c.line(x + w * gx2, y + h * gy2 - 2, x + w * gx2 + 3,
               y + h * gy2, SIL, 1)
    # terminal layer: loading crane arm over the ship, jetty, pipes
    crx = x + w * 0.62
    c.vline(crx, sy - h * 0.62, h * 0.62, (90, 96, 112), 2)
    c.line(crx, sy - h * 0.62, crx + w * 0.22, sy - h * 0.52, (90, 96, 112), 2)
    c.line(crx + w * 0.2, sy - h * 0.53, crx + w * 0.2, sy - h * 0.3,
           (90, 96, 112), 1)
    c.rect(crx + w * 0.16, sy - h * 0.3, w * 0.08, h * 0.06, (240, 180, 80))
    c.rect(x + w * 0.8, sy - h * 0.04, w * 0.2, h * 0.05, (110, 104, 96))
    c.line(x + w * 0.88, sy - h * 0.2, hx + hw * 0.6, hy - h * 0.1,
           (170, 176, 186), 2)
    c.circle(hx + hw * 0.35, hy - h * 0.2, h * 0.04, (250, 240, 200))


def scene_fire(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol, dark=True)
    c.rect(x, gy, w, h * 0.26, (70, 62, 58))
    for i in range(3):
        sx = x + w * (0.06 + i * 0.3)
        c.rect(sx, gy - h * 0.3, w * 0.24, h * 0.3, (96, 78, 66))
        c.triangle(sx - 3, gy - h * 0.3, sx + w * 0.24 + 3, gy - h * 0.3,
                   sx + w * 0.12, gy - h * 0.44, (140, 84, 60))
        c.rect(sx + 3, gy - h * 0.2, w * 0.24 - 6, h * 0.08, (240, 220, 170))
    for (fx, fh) in [(0.18, 0.34), (0.42, 0.46), (0.66, 0.38), (0.84, 0.28)]:
        bx = x + w * fx
        by = gy - h * 0.3
        c.polygon([(bx - w * 0.05, by), (bx, by - h * fh), (bx + w * 0.05, by)],
                  FLAME)
        c.polygon([(bx - w * 0.025, by), (bx, by - h * fh * 0.6),
                   (bx + w * 0.025, by)], FLAME_Y)
    for i in range(4):
        c.circle(x + w * (0.2 + i * 0.2), y + h * (0.14 + (i % 2) * 0.07),
                 h * 0.07, SMOKE)
    # detail layer: firefighters with hose arc, embers, stall goods
    for i in range(2):
        fx2 = x + w * (0.3 + i * 0.34)
        _person(c, fx2, gy + h * 0.22, h * 0.15, (60, 50, 40))
        c.circle(fx2, gy + h * 0.22 - h * 0.15 * 1.55, h * 0.045,
                 (250, 200, 60))
    c.line(x + w * 0.32, gy + h * 0.02, x + w * 0.44, gy - h * 0.34,
           (170, 210, 235), 2)
    c.line(x + w * 0.66, gy + h * 0.02, x + w * 0.6, gy - h * 0.3,
           (170, 210, 235), 2)
    for i in range(8):
        c.circle(x + (i * 61) % int(w), gy - h * (0.36 + (i % 3) * 0.09),
                 1.2, FLAME_Y)
    for i in range(3):
        c.rect(x + w * (0.1 + i * 0.3), gy - h * 0.1, w * 0.16, h * 0.05,
               (120, 90, 60))
    # fire-truck layer: engine with ladder, bigger smoke columns
    trx = x + w * 0.72
    try_ = gy + h * 0.02
    c.rect(trx, try_, w * 0.24, h * 0.16, (210, 60, 50))
    c.rect(trx + w * 0.17, try_ - h * 0.08, w * 0.07, h * 0.1, (210, 60, 50))
    c.rect(trx + w * 0.185, try_ - h * 0.06, w * 0.04, h * 0.05,
           (200, 224, 238))
    c.line(trx + w * 0.03, try_, trx + w * 0.2, try_ - h * 0.22,
           (200, 204, 212), 2)
    c.circle(trx + w * 0.05, try_ + h * 0.17, h * 0.045, (30, 30, 36))
    c.circle(trx + w * 0.19, try_ + h * 0.17, h * 0.045, (30, 30, 36))
    c.circle(trx + w * 0.1, try_ - h * 0.03, 2, (120, 180, 250))
    for i in range(3):
        c.circle(x + w * (0.3 + i * 0.22), y + h * 0.1, h * 0.09,
                 (100, 102, 110))
        c.circle(x + w * (0.36 + i * 0.22), y + h * 0.06, h * 0.07,
                 (120, 122, 130))


def scene_court(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (198, 190, 172))
    bx = x + w * 0.14
    bw = w * 0.72
    by = gy - h * 0.58
    c.triangle(bx - 4, by, bx + bw + 4, by, bx + bw / 2, by - h * 0.2, STONE_D)
    c.rect(bx, by, bw, h * 0.06, STONE_D)
    for i in range(5):
        c.rect(bx + 4 + i * (bw - 8) / 5, by + h * 0.08, w * 0.045, h * 0.4,
               STONE)
    c.rect(bx, gy - h * 0.06, bw, h * 0.06, STONE_D)
    # scales of justice, centre
    cx = bx + bw / 2
    cy = by + h * 0.16
    c.vline(cx, cy, h * 0.3, GOLD, 2)
    c.hline(cx - w * 0.13, cy + 2, w * 0.26, GOLD, 2)
    for sgn in (-1, 1):
        px = cx + sgn * w * 0.13
        c.line(px, cy + 2, px - w * 0.04, cy + h * 0.16, GOLD, 1)
        c.line(px, cy + 2, px + w * 0.04, cy + h * 0.16, GOLD, 1)
        c.polygon([(px - w * 0.05, cy + h * 0.16), (px + w * 0.05, cy + h * 0.16),
                   (px, cy + h * 0.22)], GOLD)
    c.circle(cx, cy, 2.5, GOLD)
    # detail layer: front steps, flag poles, people on the steps
    for i in range(3):
        c.rect(bx - 3 - i * 2, gy + h * (0.02 + i * 0.05), bw + 6 + i * 4,
               h * 0.045, STONE_D if i % 2 else STONE)
    for sgn in (-1, 1):
        fx2 = cx + sgn * bw * 0.58
        c.vline(fx2, by - h * 0.34, h * 0.5, SIL, 1)
        c.polygon([(fx2, by - h * 0.34), (fx2 + sgn * w * 0.07, by - h * 0.3),
                   (fx2, by - h * 0.25)], rcol)
    for i in range(3):
        _person(c, bx + bw * (0.2 + i * 0.3), gy + h * 0.16, h * 0.12,
                SIL if i % 2 else (70, 60, 80))
    # gavel layer: judge's gavel and sound block, foreground right
    gx2 = x + w * 0.82
    gy2 = gy + h * 0.1
    c.line(gx2, gy2, gx2 + w * 0.1, gy2 - h * 0.2, (120, 84, 50), 3)
    c.rect(gx2 + w * 0.07, gy2 - h * 0.27, w * 0.09, h * 0.09, (90, 62, 36))
    c.rect(gx2 - w * 0.02, gy2 + h * 0.02, w * 0.12, h * 0.04, (90, 62, 36))
    c.circle(bx + bw / 2, by - h * 0.1, w * 0.03, GOLD)


def scene_fence(c, x, y, w, h, rcol):
    _sky(c, x, y, w, h)
    c.polygon([(x, y + h * 0.55), (x + w * 0.4, y + h * 0.34),
               (x + w * 0.75, y + h * 0.5), (x + w, y + h * 0.42),
               (x + w, y + h), (x, y + h)], LAND)
    c.polygon([(x, y + h * 0.68), (x + w * 0.5, y + h * 0.55),
               (x + w, y + h * 0.64), (x + w, y + h), (x, y + h)], LAND_D)
    fy = y + h * 0.66
    for i in range(9):
        c.vline(x + w * (0.04 + i * 0.11), fy - h * 0.16, h * 0.3, SIL, 2)
    c.hline(x, fy - h * 0.13, w, SIL, 1)
    c.hline(x, fy - h * 0.02, w, SIL, 1)
    # watchtower
    tx = x + w * 0.78
    c.rect(tx, fy - h * 0.52, w * 0.1, h * 0.52, (90, 76, 60))
    c.rect(tx - 3, fy - h * 0.62, w * 0.1 + 6, h * 0.12, (70, 58, 46))
    c.triangle(tx - 5, fy - h * 0.62, tx + w * 0.1 + 5, fy - h * 0.62,
               tx + w * 0.05, fy - h * 0.74, ROOF)
    c.rect(tx + 3, fy - h * 0.58, w * 0.1 - 6, h * 0.05, (250, 236, 180))


def scene_tube(c, x, y, w, h, rcol):
    c.vgrad(x, y, w, h, (44, 46, 60), (30, 32, 44))
    ax = x + w * 0.2
    aw = w * 0.6
    ay = y + h * 0.12
    ah = h * 0.76
    c.rect(ax, ay + ah * 0.3, aw, ah * 0.7, (18, 20, 28))
    c.circle(ax + aw / 2, ay + ah * 0.3, aw / 2, (18, 20, 28))
    tx = ax + aw * 0.14
    tw = aw * 0.72
    ty = ay + ah * 0.34
    th = ah * 0.52
    c.rect(tx, ty, tw, th, (196, 60, 52))
    c.rect(tx, ty, tw, th * 0.18, (240, 238, 230))
    c.rect(tx + tw * 0.08, ty + th * 0.28, tw * 0.36, th * 0.3, (30, 34, 48))
    c.rect(tx + tw * 0.56, ty + th * 0.28, tw * 0.36, th * 0.3, (30, 34, 48))
    c.circle(tx + tw * 0.18, ty + th * 0.78, th * 0.09, (252, 232, 160))
    c.circle(tx + tw * 0.82, ty + th * 0.78, th * 0.09, (252, 232, 160))
    c.rect(tx, ty + th * 0.62, tw, th * 0.08, (240, 238, 230))
    c.hline(x, ay + ah, w, (120, 118, 110), 2)
    c.line(ax + aw / 2, ay + ah, x + w * 0.1, y + h, (120, 118, 110), 1)
    c.line(ax + aw / 2, ay + ah, x + w * 0.9, y + h, (120, 118, 110), 1)
    # detail layer: roundel sign, platform edge, waiting passengers
    c.ring(x + w * 0.1, ay + ah * 0.3, h * 0.11, (196, 60, 52), 3)
    c.rect(x + w * 0.1 - h * 0.13, ay + ah * 0.3 - h * 0.035, h * 0.26,
           h * 0.07, (50, 80, 160))
    c.rect(x, ay + ah + h * 0.04, w * 0.2, h * 0.1, (86, 84, 80))
    c.rect(x + w * 0.8, ay + ah + h * 0.04, w * 0.2, h * 0.1, (86, 84, 80))
    for i in range(2):
        _person(c, x + w * (0.08 + i * 0.05), ay + ah + h * 0.04, h * 0.12,
                (200, 196, 186))
        _person(c, x + w * (0.86 + i * 0.05), ay + ah + h * 0.04, h * 0.12,
                (180, 176, 168))
    c.rect(tx + tw * 0.2, ty + th * 0.32, tw * 0.08, th * 0.16,
           (250, 232, 170))
    c.rect(tx + tw * 0.66, ty + th * 0.32, tw * 0.08, th * 0.16,
           (250, 232, 170))
    # side-carriage layer: carriage stretching right with lit windows
    sx2 = tx + tw * 0.98
    c.rect(sx2, ty + th * 0.08, w * 0.16, th * 0.84, (176, 52, 46))
    for i in range(2):
        c.rect(sx2 + w * (0.02 + i * 0.07), ty + th * 0.3, w * 0.05,
               th * 0.3, (250, 232, 170))
        c.circle(sx2 + w * (0.045 + i * 0.07), ty + th * 0.42, th * 0.06,
                 SIL)
    c.rect(sx2, ty + th * 0.62, w * 0.16, th * 0.08, (240, 238, 230))
    # big foreground silhouettes of waiting passengers, left
    _person(c, x + w * 0.05, y + h * 0.98, h * 0.3, (24, 26, 34))
    _person(c, x + w * 0.13, y + h * 0.98, h * 0.26, (34, 36, 46))


def scene_car(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (170, 166, 156))
    fx = x + w * 0.05
    fw = w * 0.55
    fy = gy - h * 0.44
    c.rect(fx, fy, fw, h * 0.44, (128, 124, 118))
    c.polygon([(fx, fy), (fx + fw * 0.3, fy - h * 0.12), (fx + fw * 0.3, fy)],
              (104, 100, 94))
    c.polygon([(fx + fw * 0.3, fy), (fx + fw * 0.6, fy - h * 0.12),
               (fx + fw * 0.6, fy)], (104, 100, 94))
    c.rect(fx + fw * 0.78, fy - h * 0.3, fw * 0.09, h * 0.3, (104, 100, 94))
    c.circle(fx + fw * 0.82, fy - h * 0.36, h * 0.05, SMOKE)
    for i in range(4):
        c.rect(fx + 4 + i * fw * 0.22, fy + h * 0.14, fw * 0.14, h * 0.12,
               (240, 236, 214))
    # car foreground
    cx = x + w * 0.58
    cy = gy + h * 0.06
    cw2 = w * 0.36
    c.polygon([(cx, cy), (cx + cw2 * 0.12, cy - h * 0.12),
               (cx + cw2 * 0.34, cy - h * 0.2), (cx + cw2 * 0.68, cy - h * 0.2),
               (cx + cw2 * 0.88, cy - h * 0.1), (cx + cw2, cy)], rcol)
    c.polygon([(cx + cw2 * 0.36, cy - h * 0.17), (cx + cw2 * 0.5, cy - h * 0.17),
               (cx + cw2 * 0.5, cy - h * 0.08), (cx + cw2 * 0.3, cy - h * 0.08)],
              (210, 228, 238))
    c.polygon([(cx + cw2 * 0.54, cy - h * 0.17), (cx + cw2 * 0.66, cy - h * 0.17),
               (cx + cw2 * 0.78, cy - h * 0.08), (cx + cw2 * 0.54, cy - h * 0.08)],
              (210, 228, 238))
    c.circle(cx + cw2 * 0.22, cy + 2, h * 0.07, (30, 30, 36))
    c.circle(cx + cw2 * 0.78, cy + 2, h * 0.07, (30, 30, 36))
    c.circle(cx + cw2 * 0.22, cy + 2, h * 0.03, (190, 190, 196))
    c.circle(cx + cw2 * 0.78, cy + 2, h * 0.03, (190, 190, 196))


def scene_vote(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (176, 150, 128))
    bx = x + w * 0.08
    bw = w * 0.56
    by = gy - h * 0.5
    c.rect(bx, by, bw, h * 0.5, STONE)
    c.triangle(bx - 3, by, bx + bw + 3, by, bx + bw / 2, by - h * 0.16, STONE_D)
    for i in range(4):
        c.rect(bx + 4 + i * (bw - 8) / 4, by + h * 0.12, 3, h * 0.3,
               (238, 234, 222))
    # tally board: two columns of dots, close count
    tx = x + w * 0.7
    ty = gy - h * 0.52
    c.rect(tx, ty, w * 0.24, h * 0.52, (40, 44, 62))
    for r in range(5):
        for col in range(4):
            c.circle(tx + w * (0.035 + col * 0.055), ty + h * (0.08 + r * 0.09),
                     2, (240, 240, 236) if col < 2 else (150, 156, 176))
    c.vline(tx + w * 0.12, ty + 3, h * 0.46, (200, 204, 216), 1)


def scene_ferry(c, x, y, w, h, rcol):
    _sky(c, x, y, w, h)
    sy = y + h * 0.6
    _sea(c, x, sy, w, h * 0.4)
    # pier, right
    px = x + w * 0.78
    c.rect(px, sy - h * 0.3, w * 0.22, h * 0.34, (110, 104, 96))
    c.rect(px, sy - h * 0.3, w * 0.22, h * 0.05, (84, 78, 70))
    for i in range(3):
        c.vline(px + 3 + i * w * 0.07, sy + h * 0.04, h * 0.2, (84, 78, 70), 2)
    # ferry approaching
    fx = x + w * 0.08
    fw = w * 0.58
    fy = sy - h * 0.14
    c.polygon([(fx, fy), (fx + fw, fy), (fx + fw * 0.9, fy + h * 0.16),
               (fx + fw * 0.1, fy + h * 0.16)], (46, 96, 140))
    c.rect(fx + fw * 0.08, fy - h * 0.2, fw * 0.7, h * 0.2, WHITE)
    c.rect(fx + fw * 0.08, fy - h * 0.2, fw * 0.7, h * 0.05, rcol)
    for i in range(5):
        c.rect(fx + fw * (0.13 + i * 0.12), fy - h * 0.12, fw * 0.07, h * 0.07,
               (40, 60, 84))
    c.rect(fx + fw * 0.62, fy - h * 0.32, fw * 0.1, h * 0.12, (60, 66, 80))
    c.line(fx + fw * 0.95, fy + h * 0.12, fx + fw * 1.06, fy + h * 0.2,
           (200, 224, 238), 2)
    # detail layer: passengers on deck, wake foam, lighthouse on pier
    for i in range(4):
        _person(c, fx + fw * (0.16 + i * 0.13), fy - h * 0.2, h * 0.09,
                SIL if i % 2 else (90, 60, 90))
    for i in range(3):
        c.hline(fx - w * 0.02 - i * w * 0.03, fy + h * (0.14 + i * 0.04),
                w * 0.05, (220, 238, 248), 1)
    lx = px + w * 0.16
    c.rect(lx, sy - h * 0.52, w * 0.045, h * 0.24, WHITE)
    c.rect(lx, sy - h * 0.52, w * 0.045, h * 0.06, (200, 70, 60))
    c.rect(lx, sy - h * 0.4, w * 0.045, h * 0.05, (200, 70, 60))
    c.circle(lx + w * 0.022, sy - h * 0.55, 2.4, (252, 232, 160))
    # impact layer: splash where the bow meets the pier, foam arcs
    ix = fx + fw * 0.98
    iy = fy + h * 0.08
    for i in range(5):
        c.line(ix, iy, ix + w * (0.02 + i * 0.012), iy - h * (0.1 + (i % 3) * 0.05),
               (220, 240, 250), 2)
    c.circle(ix + w * 0.03, iy - h * 0.04, h * 0.05, (220, 240, 250))
    c.circle(ix + w * 0.05, iy + h * 0.02, h * 0.04, (200, 230, 246))
    c.line(px, sy - h * 0.3, px + w * 0.04, sy - h * 0.22, (60, 54, 46), 2)


def scene_flags(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (196, 188, 168))
    _building(c, x + w * 0.3, gy - h * 0.46, w * 0.42, h * 0.46, cols=3)
    cols = [(200, 70, 60), (240, 200, 80), (70, 140, 90), (70, 110, 190),
            (240, 240, 236), (190, 90, 150)]
    for i, col in enumerate(cols):
        fx = x + w * (0.06 + i * 0.16)
        c.vline(fx, gy - h * 0.62, h * 0.62, SIL, 1)
        c.polygon([(fx, gy - h * 0.62), (fx + w * 0.09, gy - h * 0.57),
                   (fx, gy - h * 0.5)], col)
    for i in range(3):
        _person(c, x + w * (0.2 + i * 0.28), gy + h * 0.18, h * 0.12)
    # detail layer: dome on hall, bunting between poles, sea glimpse
    c.circle(x + w * 0.51, gy - h * 0.48, w * 0.07, (90, 140, 170))
    c.rect(x + w * 0.3, gy - h * 0.48, w * 0.42, h * 0.03, STONE_D)
    for i in range(5):
        fx2 = x + w * (0.06 + i * 0.16)
        c.line(fx2, gy - h * 0.6, fx2 + w * 0.16, gy - h * 0.6, SIL, 1)
        c.triangle(fx2 + w * 0.06, gy - h * 0.6, fx2 + w * 0.1, gy - h * 0.6,
                   fx2 + w * 0.08, gy - h * 0.52, cols[i % len(cols)])
    c.rect(x, gy + h * 0.2, w, h * 0.06, SEA_C)
    # summit layer: long conference table with seated delegates
    tbx = x + w * 0.12
    tby = gy + h * 0.06
    c.polygon([(tbx, tby), (tbx + w * 0.76, tby), (tbx + w * 0.82, tby + h * 0.1),
               (tbx - w * 0.06, tby + h * 0.1)], (110, 80, 56))
    for i in range(5):
        dx = tbx + w * (0.08 + i * 0.15)
        c.circle(dx, tby - h * 0.05, h * 0.035, SIL)
        c.rect(dx - w * 0.02, tby - h * 0.03, w * 0.04, h * 0.05, SIL)
        c.rect(dx - w * 0.025, tby + h * 0.03, w * 0.05, h * 0.03, WHITE)
    c.rect(tbx + w * 0.34, tby - h * 0.12, w * 0.08, h * 0.05,
           (250, 232, 170))


def scene_shoppers(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (206, 198, 182))
    sx = x + w * 0.08
    sw = w * 0.84
    sy = gy - h * 0.54
    c.rect(sx, sy, sw, h * 0.54, (150, 146, 140))
    c.rect(sx, sy, sw, h * 0.12, rcol)
    for i in range(3):
        c.rect(sx + sw * (0.06 + i * 0.32), sy + h * 0.2, sw * 0.24, h * 0.3,
               (250, 232, 180))
    c.rect(sx + sw * 0.4, sy + h * 0.2, sw * 0.2, h * 0.34, (70, 74, 92))
    # crowd with bags
    for i, fx in enumerate([0.14, 0.3, 0.46, 0.62, 0.78, 0.9]):
        px = x + w * fx
        _person(c, px, gy + h * 0.2, h * 0.13,
                SIL if i % 2 else (84, 66, 88))
        c.rect(px + w * 0.03, gy + h * 0.08, w * 0.05, h * 0.09,
               (240, 200, 90) if i % 2 else (200, 90, 80))
    # detail layer: sale bunting, window goods, second crowd row
    for i in range(6):
        c.triangle(sx + sw * (0.04 + i * 0.16), sy + h * 0.13,
                   sx + sw * (0.12 + i * 0.16), sy + h * 0.13,
                   sx + sw * (0.08 + i * 0.16), sy + h * 0.2,
                   (220, 90, 80) if i % 2 else (240, 200, 90))
    for i in range(3):
        c.rect(sx + sw * (0.1 + i * 0.32), sy + h * 0.34, sw * 0.16,
               h * 0.1, (200, 120, 90))
    for i, fx in enumerate([0.22, 0.54, 0.7]):
        _person(c, x + w * fx, gy + h * 0.24, h * 0.1, (60, 70, 100))
    # sale layer: giant hanging % signs and stacked shopping bags
    for i in range(2):
        hx2 = sx + sw * (0.18 + i * 0.5)
        c.vline(hx2, sy + h * 0.12, h * 0.08, SIL, 1)
        c.rect(hx2 - w * 0.045, sy + h * 0.2, w * 0.09, h * 0.14,
               (220, 60, 60))
        c.text_center(hx2, sy + h * 0.3, "%", SANSB, SANSB_EM, SANSB_ASC,
                      h * 0.11, WHITE)
    for i in range(3):
        c.rect(x + w * (0.84 + i * 0.04), gy + h * (0.1 - i * 0.03),
               w * 0.045, h * 0.09, (240, 200, 90) if i % 2 else (120, 180, 220))


def scene_stars(c, x, y, w, h, rcol):
    _sky(c, x, y, w, h)
    gy = y + h * 0.76
    c.rect(x, gy, w, h * 0.24, (196, 188, 168))
    bx = x + w * 0.16
    bw = w * 0.68
    by = gy - h * 0.5
    c.rect(bx, by, bw, h * 0.5, (96, 110, 140))
    for r in range(3):
        for i in range(6):
            c.rect(bx + 4 + i * (bw - 8) / 6, by + h * (0.08 + r * 0.14),
                   bw * 0.09, h * 0.09, (226, 234, 244))
    # circle of twelve gold stars above the building
    cx = bx + bw / 2
    cy = by - h * 0.2
    rr = h * 0.13
    for i in range(12):
        a = 2 * math.pi * i / 12
        c.circle(cx + rr * math.cos(a), cy + rr * math.sin(a), 2.2,
                 (252, 214, 110))
    c.vline(cx, by - h * 0.36, h * 0.16, SIL, 1)
    _tree(c, x + w * 0.08, gy + h * 0.14, h * 0.3)
    _tree(c, x + w * 0.93, gy + h * 0.14, h * 0.3)
    # detail layer: blue flag with gold stars, fountain, people
    fx2 = x + w * 0.86
    c.vline(fx2, gy - h * 0.66, h * 0.66, SIL, 1)
    c.rect(fx2, gy - h * 0.66, w * 0.1, h * 0.16, (40, 70, 170))
    for i in range(6):
        a = 2 * math.pi * i / 6
        c.circle(fx2 + w * 0.05 + h * 0.045 * math.cos(a),
                 gy - h * 0.58 + h * 0.045 * math.sin(a), 1.4,
                 (252, 214, 110))
    c.circle(x + w * 0.5, gy + h * 0.12, w * 0.06, SEA_C)
    c.line(x + w * 0.5, gy + h * 0.12, x + w * 0.5, gy - h * 0.02,
           (200, 224, 238), 2)
    for i in range(3):
        _person(c, x + w * (0.3 + i * 0.18), gy + h * 0.2, h * 0.12,
                SIL if i % 2 else (70, 60, 80))
    # parliament layer: stepped curved facade wings, seat rows
    for i in range(3):
        c.rect(bx - w * (0.05 + i * 0.035), by + h * (0.1 + i * 0.12),
               w * 0.05, h * (0.4 - i * 0.12), (110, 124, 152))
        c.rect(bx + bw + i * w * 0.035, by + h * (0.1 + i * 0.12),
               w * 0.05, h * (0.4 - i * 0.12), (110, 124, 152))
    for r in range(2):
        for i in range(7):
            c.circle(x + w * (0.3 + i * 0.06), gy + h * (0.08 + r * 0.06),
                     1.8, (90, 110, 170) if (i + r) % 2 else (200, 120, 90))


def scene_f1car(c, x, y, w, h, rcol):
    gy = _grid_base(c, x, y, w, h, rcol, dusk=True)
    c.rect(x, gy, w, h * 0.26, (92, 90, 96))
    c.hline(x, gy + h * 0.1, w, (240, 236, 214), 1)
    # speed lines
    for i in range(3):
        c.hline(x + w * 0.04, gy - h * (0.16 + i * 0.12), w * 0.2,
                (214, 210, 196), 1)
    # F1 car: low nose, halo, rear wing, big wheels
    cx = x + w * 0.3
    cy = gy + h * 0.08
    cw2 = w * 0.62
    c.polygon([(cx, cy), (cx + cw2 * 0.3, cy - h * 0.1),
               (cx + cw2 * 0.55, cy - h * 0.14), (cx + cw2 * 0.8, cy - h * 0.16),
               (cx + cw2 * 0.92, cy - h * 0.3), (cx + cw2, cy - h * 0.3),
               (cx + cw2 * 0.94, cy)], rcol)
    c.rect(cx + cw2 * 0.86, cy - h * 0.42, cw2 * 0.13, h * 0.12, (30, 30, 36))
    c.rect(cx + cw2 * 0.9, cy - h * 0.3, 3, h * 0.16, (30, 30, 36))
    c.polygon([(cx + cw2 * 0.42, cy - h * 0.13), (cx + cw2 * 0.58, cy - h * 0.13),
               (cx + cw2 * 0.55, cy - h * 0.24), (cx + cw2 * 0.45, cy - h * 0.24)],
              (30, 30, 36))
    c.circle(cx + cw2 * 0.2, cy + 2, h * 0.1, (24, 24, 30))
    c.circle(cx + cw2 * 0.8, cy + 2, h * 0.1, (24, 24, 30))
    c.circle(cx + cw2 * 0.2, cy + 2, h * 0.045, (190, 190, 196))
    c.circle(cx + cw2 * 0.8, cy + 2, h * 0.045, (190, 190, 196))
    # detail layer: grandstand crowd, checkered flag, kerb stripes
    c.rect(x, y + h * 0.06, w, h * 0.16, (120, 126, 140))
    for i in range(14):
        c.circle(x + w * (0.04 + i * 0.07), y + h * (0.12 + (i % 2) * 0.05),
                 1.8, (240, 236, 220) if i % 3 else (200, 90, 80))
    for i in range(6):
        c.rect(x + i * w / 6, gy + h * 0.2, w / 12, h * 0.05,
               (220, 70, 60) if i % 2 else WHITE)
    fx2 = x + w * 0.08
    c.vline(fx2, gy - h * 0.5, h * 0.5, SIL, 1)
    for r in range(3):
        for col in range(3):
            c.rect(fx2 + col * w * 0.03, gy - h * 0.5 + r * h * 0.045,
                   w * 0.03, h * 0.045,
                   (30, 30, 36) if (r + col) % 2 else WHITE)
    # race layer: start-lights gantry, second car behind, sunset sun
    _sun(c, x + w * 0.9, y + h * 0.3, h * 0.07)
    gx2 = x + w * 0.55
    c.vline(gx2, gy - h * 0.56, h * 0.56, (60, 64, 76), 2)
    c.vline(gx2 + w * 0.3, gy - h * 0.56, h * 0.56, (60, 64, 76), 2)
    c.rect(gx2, gy - h * 0.6, w * 0.3, h * 0.09, (30, 32, 40))
    for i in range(4):
        c.circle(gx2 + w * (0.05 + i * 0.07), gy - h * 0.555, 2.2,
                 (140, 230, 160) if i < 3 else (240, 90, 80))
    cx2 = x + w * 0.06
    cy2 = gy + h * 0.02
    c.polygon([(cx2, cy2), (cx2 + w * 0.1, cy2 - h * 0.07),
               (cx2 + w * 0.2, cy2 - h * 0.09), (cx2 + w * 0.26, cy2)],
              (60, 90, 170))
    c.circle(cx2 + w * 0.06, cy2 + 1, h * 0.06, (24, 24, 30))
    c.circle(cx2 + w * 0.2, cy2 + 1, h * 0.06, (24, 24, 30))


def scene_chart(c, x, y, w, h, rcol):
    """Wall Street: exchange facade, ticker board, rising arrow."""
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (170, 166, 156))
    # skyline behind
    for i, bh2 in enumerate((0.4, 0.58, 0.46, 0.66, 0.5)):
        c.rect(x + w * (0.02 + i * 0.19), gy - h * bh2, w * 0.13, h * bh2,
               (150, 160, 184))
    # exchange facade: pediment + columns, centre
    bx = x + w * 0.3
    bw = w * 0.44
    by = gy - h * 0.5
    c.triangle(bx - 3, by, bx + bw + 3, by, bx + bw / 2, by - h * 0.18,
               STONE_D)
    c.rect(bx, by, bw, h * 0.05, STONE_D)
    for i in range(5):
        c.rect(bx + 3 + i * (bw - 6) / 5, by + h * 0.07, w * 0.035,
               h * 0.36, (238, 234, 222))
    c.rect(bx, gy - h * 0.05, bw, h * 0.05, STONE_D)
    c.vline(bx + bw / 2, by - h * 0.3, h * 0.12, SIL, 1)
    c.polygon([(bx + bw / 2, by - h * 0.3), (bx + bw / 2 + w * 0.08, by - h * 0.27),
               (bx + bw / 2, by - h * 0.23)], (200, 70, 60))
    # ticker board, left, with green rising line
    tx = x + w * 0.04
    ty = gy - h * 0.44
    c.rect(tx, ty, w * 0.22, h * 0.34, (26, 34, 30))
    c.line(tx + w * 0.02, ty + h * 0.26, tx + w * 0.09, ty + h * 0.18,
           (140, 230, 160), 2)
    c.line(tx + w * 0.09, ty + h * 0.18, tx + w * 0.14, ty + h * 0.22,
           (140, 230, 160), 2)
    c.line(tx + w * 0.14, ty + h * 0.22, tx + w * 0.2, ty + h * 0.07,
           (140, 230, 160), 2)
    for i in range(3):
        c.hline(tx + w * 0.02, ty + h * (0.06 + i * 0.05), w * 0.07,
               (140, 230, 160), 1)
    # big rising arrow, right
    c.line(x + w * 0.78, gy - h * 0.1, x + w * 0.94, gy - h * 0.44,
           (60, 170, 90), 3)
    c.polygon([(x + w * 0.94, gy - h * 0.44), (x + w * 0.88, gy - h * 0.42),
               (x + w * 0.92, gy - h * 0.34)], (60, 170, 90))
    # gold coins at the steps
    for i in range(3):
        c.circle(x + w * (0.36 + i * 0.12), gy + h * 0.1, h * 0.04,
                 (252, 214, 110))
        c.ring(x + w * (0.36 + i * 0.12), gy + h * 0.1, h * 0.04,
               (196, 150, 50), 1)


def scene_market(c, x, y, w, h, rcol):
    """Spain CPI: supermarket front, shelves, cart, price tags."""
    gy = _grid_base(c, x, y, w, h, rcol)
    c.rect(x, gy, w, h * 0.26, (206, 198, 182))
    sx = x + w * 0.06
    sw = w * 0.62
    sy = gy - h * 0.56
    c.rect(sx, sy, sw, h * 0.56, (168, 160, 148))
    c.rect(sx, sy, sw, h * 0.12, (210, 90, 60))
    for i in range(4):
        c.rect(sx + sw * (0.05 + i * 0.24), sy + h * 0.12, sw * 0.2,
               h * 0.07, WHITE if i % 2 else (220, 90, 80))
    # shelves with colourful goods inside the windows
    for r in range(2):
        for i in range(6):
            gx2 = sx + sw * (0.06 + i * 0.15)
            gy2 = sy + h * (0.24 + r * 0.16)
            c.rect(gx2, gy2, sw * 0.11, h * 0.1,
                   [(220, 120, 80), (120, 180, 90), (240, 200, 90),
                    (120, 160, 220)][(i + r) % 4])
        c.hline(sx + sw * 0.04, sy + h * (0.36 + r * 0.16), sw * 0.9,
                (90, 84, 76), 1)
    # shopping cart with bags, right foreground
    cx = x + w * 0.74
    cy = gy + h * 0.02
    c.polygon([(cx, cy - h * 0.2), (cx + w * 0.2, cy - h * 0.2),
               (cx + w * 0.17, cy - h * 0.04), (cx + w * 0.03, cy - h * 0.04)],
              (120, 126, 138))
    c.rect(cx + w * 0.04, cy - h * 0.28, w * 0.07, h * 0.1, (240, 200, 90))
    c.rect(cx + w * 0.12, cy - h * 0.26, w * 0.06, h * 0.08, (120, 180, 90))
    c.circle(cx + w * 0.05, cy + h * 0.02, h * 0.035, (40, 42, 50))
    c.circle(cx + w * 0.16, cy + h * 0.02, h * 0.035, (40, 42, 50))
    c.line(cx + w * 0.2, cy - h * 0.2, cx + w * 0.24, cy - h * 0.26, SIL, 2)
    _person(c, cx + w * 0.27, gy + h * 0.16, h * 0.16, (90, 60, 90))
    # hanging price tags over the shelves
    for i in range(3):
        tx = sx + sw * (0.14 + i * 0.3)
        c.vline(tx, sy + h * 0.19, h * 0.06, SIL, 1)
        c.polygon([(tx - w * 0.03, sy + h * 0.25), (tx + w * 0.03, sy + h * 0.25),
                   (tx + w * 0.03, sy + h * 0.35), (tx, sy + h * 0.39),
                   (tx - w * 0.03, sy + h * 0.35)], (250, 240, 200))
        c.text_center(tx, sy + h * 0.325, "%", SANSB, SANSB_EM, SANSB_ASC,
                      h * 0.09, RED)


SCENES = {
    "ballot": scene_ballot, "rocket": scene_rocket, "jets": scene_jets,
    "prices": scene_prices, "tanker": scene_tanker, "fire": scene_fire,
    "court": scene_court, "fence": scene_fence, "tube": scene_tube,
    "car": scene_car, "vote": scene_vote, "ferry": scene_ferry,
    "flags": scene_flags, "shoppers": scene_shoppers, "stars": scene_stars,
    "f1car": scene_f1car, "chart": scene_chart, "market": scene_market,
}

# ---------------------------------------------------------------- world map
# Coarse land mask, 72 x 30 cells (5 degrees each), drawn from
# memory of the atlas; pins carry the precision, the coastlines
# only need to read as a world map at thumbnail size.
LANDGRID = [
    "    ###########           #####                 ####################### ",
    "   ##################      ####       ##### ############################",
    "   ####################         #    #####################################",
    "    ####################           # ################################   ",
    "     ####################          ################################     ",
    "      ####################         ###############################       ",
    "      #####################      ###### ###########################     ",
    "      ####################       ###################################    ",
    "       ##################       ###################################     ",
    "         ############           #################################       ",
    "          #########             ###############    #############        ",
    "            ######               #############      ##### #####         ",
    "               ##########        #############       ###  ####          ",
    "                ###########         ###########              ######     ",
    "                 ###########        ##########             ########     ",
    "                  ##########        #########               ########    ",
    "                   ########         #######                 ######      ",
    "                   #######          ######                 ########     ",
    "                   ######           ####                  ########      ",
    "                   #####                     #             ########       ",
    "                   ####                                     ######   ## ",
    "                   ###                                      ####    ##  ",
    "                   ##                                               #   ",
    "                   #                                                #   ",
    "", "", "", "", "", "",
]


def draw_map(c, x, y, w, h, pins):
    c.vgrad(x, y, w, h, (170, 205, 232), (140, 185, 220))
    c.frame(x, y, w, h, RULE, 1)
    cols = 72
    rows = 24
    cw = w / cols
    ch = h / rows
    for r in range(rows):
        line = LANDGRID[r] if r < len(LANDGRID) else ""
        for i in range(cols):
            ch2 = line[i] if i < len(line) else " "
            if ch2 != " ":
                c.rect(x + i * cw, y + r * ch, cw + 0.6, ch + 0.6,
                       (116, 158, 88))
    for (lon, lat, rcol, num) in pins:
        px = x + (lon + 180) / 360 * w
        py = y + (75 - lat) / 135 * h
        c.circle(px, py, 6.4, WHITE)
        c.circle(px, py, 5.4, rcol)
        c.text_center(px, py + 2.3, str(num), SANSB, SANSB_EM,
                      SANSB_ASC, 6.4, WHITE)


# ---------------------------------------------------------------- layout
def stories_of(kind):
    return [s for s in STORIES if s[0] == kind]


def region_counts():
    counts = [0] * len(REGIONS)
    for s in STORIES:
        counts[s[7]] += 1
    return counts


def source_count():
    return len({s[6] for s in STORIES})


def field_count():
    return len({s[8] for s in STORIES})


def draw_badge(c, right, y, text):
    """Confidence badge: small outlined pill, right-aligned at y (top)."""
    size = 7.0
    tw = text_width(text, SANSB, SANSB_EM, size, 0.4)
    bw = tw + 8
    bh = 11
    col = RED if text == "CLAIM" else GREY
    c.frame(right - bw, y, bw, bh, col, 1)
    c.text(right - bw + 4, y + bh - 3.2, text, SANSB, SANSB_EM, SANSB_ASC,
           size, col, 0.4)
    return bw


def draw_chip(c, x, y, text):
    """Small dark label over a scene's top-left corner."""
    if not text:
        return
    size = 8.5
    tw = text_width(text, SANSB, SANSB_EM, size, 0.3)
    c.rect(x, y, tw + 10, 14, INK)
    c.text(x + 5, y + 10.5, text, SANSB, SANSB_EM, SANSB_ASC, size,
           (250, 246, 230), 0.3)


def draw_chip_right(c, right, y, text):
    """Stat chip in the card's text area, right-aligned at y (top).

    Kept off the artwork: it sits on the kicker row, clear of the
    scene above and the headline below.
    """
    if not text:
        return
    size = 7.6
    tw = text_width(text, SANSB, SANSB_EM, size, 0.3)
    bw = tw + 9
    bh = 12
    c.rect(right - bw, y, bw, bh, INK)
    c.text(right - bw + 4.5, y + bh - 3.4, text, SANSB, SANSB_EM,
           SANSB_ASC, size, (250, 246, 230), 0.3)


def draw_numbers_panel(c, x, y, w, h):
    """THE DAY IN NUMBERS: dark navy panel, big coloured figures."""
    c.rect(x, y, w, h, (22, 36, 72))
    c.frame(x, y, w, h, (176, 132, 46), 1)
    c.text(x + 8, y + 12, "THE DAY IN NUMBERS",
           SANSB, SANSB_EM, SANSB_ASC, 8.5, (252, 214, 110), 0.4)
    c.text_right(x + w - 8, y + 12, "CLOSING FIGURES",
                 SANSB, SANSB_EM, SANSB_ASC, 6.2, (180, 192, 220), 0.3)
    c.hline(x + 8, y + 16, w - 16, (90, 110, 160), 1)
    cols = 3
    qw = (w - 16) / cols
    val_cols = [(252, 214, 110), (140, 230, 160), (250, 248, 240)]
    for i, (value, label) in enumerate(NUMBERS):
        cx = x + 8 + qw * (i % cols) + qw / 2
        ry = y + 16 + (i // cols) * 19
        c.text_center(cx, ry + 13, value, SERIF, SERIF_EM, SERIF_ASC,
                      13, val_cols[i % 3])
        c.text_center(cx, ry + 20, label, SANSB, SANSB_EM, SANSB_ASC,
                      5.8, (180, 192, 220), 0.2)


def draw_top(c):
    c.hline(MX, 20, CW, INK, 2)
    c.text(MX, 36, "THE WORLD IN ONE DAY · ALL TIMES UTC",
           SANSB, SANSB_EM, SANSB_ASC, 8.5, INK, 0.6)
    c.text_right(MX + CW, 36, "ONE DAY · ONE PAGE · @BADD-AIRDROP2",
                 SANSB, SANSB_EM, SANSB_ASC, 8.5, GREY, 0.6)
    # the date is the biggest element on the page
    c.text(MX, 94, "FRIDAY 27 NOVEMBER 2026",
           SERIF, SERIF_EM, SERIF_ASC, 40, INK, 0.4)
    # red subhead: the day's three leading stories
    c.text(MX, 116,
           "NZ ELECTION DEADLOCK · ELECTRON NIGHT LAUNCH · "
           "TAIWAN VOTES AS JETS CIRCLE",
           SANSB, SANSB_EM, SANSB_ASC, 11, RED, 0.3)
    c.text(MX, 132,
           "The day's world news, drawn only from verified reports",
           SERIFR, SERIFR_EM, SERIFR_ASC, 11.5, NAVY)
    # story/region counts, top right
    counts = region_counts()
    present = sum(1 for n in counts if n > 0)
    rx = MX + 692
    c.vline(rx - 14, 46, 118, RULE, 1)
    c.text(rx, 78, str(len(STORIES)), SERIF, SERIF_EM, SERIF_ASC,
           30, NAVY)
    c.text(rx, 91, "STORIES, ALL VERIFIED",
           SANSB, SANSB_EM, SANSB_ASC, 7.0, GREY, 0.4)
    c.text(rx + 140, 78, str(present), SERIF, SERIF_EM, SERIF_ASC,
           30, NAVY)
    c.text(rx + 140, 91, "REGIONS OF THE WORLD",
           SANSB, SANSB_EM, SANSB_ASC, 7.0, GREY, 0.4)
    c.text(rx, 103, "%d NAMED SOURCES · %d FIELDS OF NEWS"
           % (source_count(), field_count()),
           SANSB, SANSB_EM, SANSB_ASC, 7.0, GREY, 0.4)
    # dark closing-figures panel, top right under the counts
    draw_numbers_panel(c, rx, 108, CW - 692, 56)
    c.hline(MX, 168, CW, INK, 2)
    c.hline(MX, 172, CW, INK, 1)


def draw_stats(c, y):
    counts = region_counts()
    present = sum(1 for n in counts if n > 0)
    stats = [
        (str(len(STORIES)), "STORIES, ALL VERIFIED"),
        (str(present), "REGIONS OF THE WORLD"),
        (str(source_count()), "NAMED SOURCES"),
        (str(field_count()), "FIELDS OF NEWS"),
    ]
    qw = CW / 4
    for i, (num, label) in enumerate(stats):
        cx = MX + qw * i + qw / 2
        c.text_center(cx, y + 20, num, SERIF, SERIF_EM, SERIF_ASC, 21, NAVY)
        c.text_center(cx, y + 32, label, SANSB, SANSB_EM, SANSB_ASC, 7.2,
                      GREY, 0.5)
        if i:
            c.vline(MX + qw * i, y + 2, 32, RULE, 1)
    return y + 38


def draw_region_bar(c, y):
    counts = region_counts()
    total = sum(counts)
    x = MX
    for i, n in enumerate(counts):
        if n == 0:
            continue
        wseg = CW * n / total
        c.rect(x, y, wseg - 1, 10, REGIONS[i][1])
        x += wseg
    # region pills: big coloured chips with counts, readable
    # at thumbnail size
    present = [i for i, n in enumerate(counts) if n > 0]
    step = CW / len(present)
    for k, i in enumerate(present):
        px = MX + step * k + 1.5
        pw = step - 3
        c.rect(px, y + 14, pw, 20, REGIONS[i][1])
        c.text_center(px + pw / 2, y + 28, "%s %d" % (REGION_SHORT[i],
                      counts[i]), SANSB, SANSB_EM, SANSB_ASC, 7.4,
                      (250, 248, 240), 0.2)
    return y + 36


def draw_hero(c, x, y, w, h, num, s):
    (_k, art, place, cat, head, summ, src, region, _f, conf, chip,
     _pin) = s
    rcol = REGIONS[region][1]
    c.rect(x, y, w, h, CREAM)
    c.frame(x, y, w, h, RULE, 1)
    sh = 62
    c.set_clip(x + 1, y + 1, w - 2, sh)
    SCENES[art](c, x + 1, y + 1, w - 2, sh, rcol)
    c.clear_clip()
    c.hline(x + 1, y + 1 + sh, w - 2, rcol, 3)
    draw_chip(c, x + 7, y + 7, chip)
    c.circle(x + w - 16, y + 15, 10, INK)
    c.text_center(x + w - 16, y + 19.5, str(num), SANSB, SANSB_EM,
                  SANSB_ASC, 11, (250, 246, 230))
    ty = y + sh + 16
    c.text(x + 9, ty, "%s · %s · %s" % (REGION_SHORT[region], place, cat),
           SANSB, SANSB_EM, SANSB_ASC, 9.6, rcol, 0.5)
    ty = c.para(x + 9, ty + 15, head, SERIF, SERIF_EM, SERIF_ASC, 16,
                INK, w - 18, leading=15.6)
    ty = c.para(x + 9, ty + 0.5, summ, SANS, SANS_EM, SANS_ASC, 9.8,
                (52, 56, 68), w - 18, leading=11.0)
    by = y + h - 15
    c.text(x + 9, by + 8, src, SANSB, SANSB_EM, SANSB_ASC, 7.2, GREY, 0.3)
    draw_badge(c, x + w - 8, by - 2, conf)


def draw_grid_card(c, x, y, w, h, num, s):
    (_k, art, place, cat, head, summ, src, region, _f, conf, chip,
     _pin) = s
    rcol = REGIONS[region][1]
    c.rect(x, y, w, h, CREAM)
    c.frame(x, y, w, h, RULE, 1)
    sh = 46
    c.set_clip(x + 1, y + 1, w - 2, sh)
    SCENES[art](c, x + 1, y + 1, w - 2, sh, rcol)
    c.clear_clip()
    c.hline(x + 1, y + 1 + sh, w - 2, rcol, 2)
    c.circle(x + w - 12, y + 12, 8.5, INK)
    c.text_center(x + w - 12, y + 15.5, str(num), SANSB, SANSB_EM,
                  SANSB_ASC, 9, (250, 246, 230))
    ty = y + sh + 11
    c.text(x + 7, ty, "%s · %s · %s" % (REGION_SHORT[region], place, cat),
           SANSB, SANSB_EM, SANSB_ASC, 7.4, rcol, 0.3)
    draw_chip_right(c, x + w - 7, ty - 9.5, chip)
    ty = c.para(x + 7, ty + 10, head, SANSB, SANSB_EM, SANSB_ASC, 11.2,
                INK, w - 14, leading=10.8)
    ty = c.para(x + 7, ty + 0.5, summ, SANS, SANS_EM, SANS_ASC, 8.0,
                (60, 64, 76), w - 14, leading=9.4)
    by = y + h - 10
    c.text(x + 7, by + 7, src, SANSB, SANSB_EM, SANSB_ASC, 6.4, GREY, 0.2)
    draw_badge(c, x + w - 6, by - 2, conf)


def draw_flag(c, x, y, place):
    """Mini country flag (15x10), stylised stripes/discs per place."""
    w, h = 15, 10
    R = (200, 60, 50)
    Wc = (250, 248, 240)
    B = (40, 80, 170)
    G = (60, 150, 80)
    Y = (250, 200, 60)
    K = (30, 30, 36)
    if place == "MELBOURNE":        # Australia
        c.rect(x, y, w, h, B)
        c.rect(x, y, 7, 5, (30, 60, 140))
        c.circle(x + 3.5, y + 2.5, 1.2, Wc)
        c.circle(x + 11, y + 3, 1, Wc)
        c.circle(x + 9, y + 7, 1, Wc)
    elif place == "NEW DELHI":      # India
        c.rect(x, y, w, 3.4, (240, 130, 50))
        c.rect(x, y + 3.4, w, 3.3, Wc)
        c.rect(x, y + 6.7, w, 3.3, G)
        c.circle(x + 7.5, y + 5, 1.2, B)
    elif place == "ANKARA":         # Turkey
        c.rect(x, y, w, h, (210, 50, 50))
        c.circle(x + 6, y + 5, 2.6, Wc)
        c.circle(x + 7, y + 5, 2.2, (210, 50, 50))
        c.circle(x + 10.5, y + 5, 1, Wc)
    elif place == "HANOI":          # Vietnam
        c.rect(x, y, w, h, (210, 50, 50))
        c.circle(x + 7.5, y + 5, 1.8, Y)
    elif place == "PARIS":          # France
        c.rect(x, y, 5, h, B)
        c.rect(x + 5, y, 5, h, Wc)
        c.rect(x + 10, y, 5, h, R)
    elif place == "WARSAW":         # Poland
        c.rect(x, y, w, 5, Wc)
        c.rect(x, y + 5, w, 5, R)
    elif place == "JOHANNESBURG":   # South Africa
        c.rect(x, y, w, 3.4, R)
        c.rect(x, y + 3.4, w, 3.3, Wc)
        c.rect(x, y + 6.7, w, 3.3, B)
        c.triangle(x, y, x, y + h, x + 6, y + 5, G)
        c.triangle(x, y + 1.5, x, y + h - 1.5, x + 4, y + 5, Y)
    elif place == "GAZA":           # Palestine
        c.rect(x, y, w, 3.4, K)
        c.rect(x, y + 3.4, w, 3.3, Wc)
        c.rect(x, y + 6.7, w, 3.3, G)
        c.triangle(x, y, x, y + h, x + 5, y + 5, R)
    elif place in ("TAIYUAN", "BEIJING"):   # China
        c.rect(x, y, w, h, (210, 50, 50))
        c.circle(x + 3.5, y + 3, 1.4, Y)
        c.circle(x + 6.5, y + 2, 0.8, Y)
        c.circle(x + 6.5, y + 4.5, 0.8, Y)
    elif place == "BRASÍLIA":       # Brazil
        c.rect(x, y, w, h, G)
        c.polygon([(x + 7.5, y + 1), (x + 13, y + 5), (x + 7.5, y + 9),
                   (x + 2, y + 5)], Y)
        c.circle(x + 7.5, y + 5, 1.8, B)
    elif place == "OTTAWA":         # Canada
        c.rect(x, y, 4, h, R)
        c.rect(x + 4, y, 7, h, Wc)
        c.rect(x + 11, y, 4, h, R)
        c.circle(x + 7.5, y + 5, 1.5, R)
    else:                           # WORLD / global
        c.rect(x, y, w, h, (120, 180, 220))
        c.circle(x + 7.5, y + 5, 2.6, Wc)
        c.circle(x + 7.5, y + 5, 1.2, (120, 180, 220))
    c.frame(x, y, w, h, (150, 146, 138), 1)


def draw_also(c, y, budget_h):
    items = stories_of("also")
    c.text(MX, y + 10, "ALSO TODAY — MORE VERIFIED STORIES",
           SANSB, SANSB_EM, SANSB_ASC, 10, NAVY, 0.5)
    c.hline(MX, y + 14, CW, RULE, 1)
    cols = 3
    gap = 14
    colw = (CW - gap * (cols - 1)) / cols
    # sequential columns keep the numbering readable top-down
    per = (len(items) + cols - 1) // cols
    top = y + 30
    for ci in range(cols):
        cx = MX + ci * (colw + gap)
        cy = top
        for s in items[ci * per:(ci + 1) * per]:
            num = 16 + items.index(s)
            draw_flag(c, cx, cy - 8, s[2])
            c.text(cx + 19, cy, "%d. %s" % (num, s[4]),
                   SANSB, SANSB_EM, SANSB_ASC, 7.8, INK, 0.1)
            c.text(cx + 19, cy + 9.5, "%s · %s" % (s[2], s[6]),
                   SANS, SANS_EM, SANS_ASC, 6.8, GREY, 0.2)
            cy += 21
    return y + budget_h


def draw_timeline(c, y):
    c.text(MX, y + 10, "THE DAY IN UTC", SANSB, SANSB_EM, SANSB_ASC, 9,
           NAVY, 0.5)
    ly = y + 16
    c.hline(MX + 90, ly, CW - 90, RULE, 1)
    n = len(TIMELINE)
    step = (CW - 90) / n
    for i, (t, label) in enumerate(TIMELINE):
        cx = MX + 90 + step * i + step / 2
        c.circle(cx, ly, 2.6, GOLD)
        c.text_center(cx, ly + 10, t, SANSB, SANSB_EM, SANSB_ASC, 8.2, INK)
        c.text_center(cx, ly + 18, label, SANS, SANS_EM, SANS_ASC, 7.2, GREY)


def draw_datecheck(c, y):
    c.text(MX, y + 10, "DATE CHECK — IN TODAY'S FEEDS, BUT NOT TODAY'S NEWS",
           SANSB, SANSB_EM, SANSB_ASC, 9, RED, 0.4)
    c.hline(MX, y + 14, CW, RED, 1)
    cols = 2
    colw = CW / cols
    per = (len(DATECHECK) + cols - 1) // cols
    size = 8.0
    leading = 7.2
    for ci in range(cols):
        cx = MX + ci * colw
        cy = y + 24
        for item in DATECHECK[ci * per:(ci + 1) * per]:
            c.text(cx, cy, "✗", SANSB, SANSB_EM, SANSB_ASC, size, RED)
            c.text(cx + 11, cy, item, SANS, SANS_EM, SANS_ASC, size,
                   (70, 66, 60))
            cy += leading
    return y + 24 + per * leading


def draw_footer(c, y):
    c.hline(MX, y, CW, INK, 1)
    c.text_center(W / 2, y + 10,
                  "Every story above happened or was first reported on "
                  "Friday 27 November 2026. Forecasts and claims are "
                  "labelled as such; nothing is invented.",
                  SERIFR, SERIFR_EM, SERIFR_ASC, 8.5, (70, 66, 60))


# ---------------------------------------------------------------- build
def _validate():
    heroes = stories_of("hero")
    grid = stories_of("grid")
    assert len(heroes) == 3, "need exactly 3 heroes"
    assert len(grid) == 12, "need exactly 12 grid cards"
    assert len(stories_of("also")) == 13, "need exactly 13 ALSO lines"
    assert len(STORIES) == 28, "need exactly 28 stories"
    for s in heroes + grid:
        assert s[1] in SCENES, "unknown art: %s" % s[1]
    for s in STORIES:
        assert 0 <= s[7] < len(REGIONS), "bad region"
        assert s[9] in ("OFFICIAL", "CONFIRMED", "REPORTED", "CLAIM")


def build():
    _validate()
    c = Canvas(W, H, PAPER)
    draw_top(c)                     # masthead + counts + numbers panel
    y = draw_region_bar(c, 176)     # region pills strip -> 212
    draw_timeline(c, 216)           # UTC strip, ends ~250

    heroes = stories_of("hero")
    hw = (CW - 20) / 3
    for i, s in enumerate(heroes):
        draw_hero(c, MX + i * (hw + 10), 256, hw, 146, i + 1, s)

    grid = stories_of("grid")
    gw = (CW - 30) / 4
    for i, s in enumerate(grid):
        gx = MX + (i % 4) * (gw + 10)
        gy = 408 + (i // 4) * 104
        draw_grid_card(c, gx, gy, gw, 100, i + 4, s)

    draw_also(c, 722, 132)          # numbered 16..28, flags

    # numbered map pins for every story that has a place;
    # duplicate coordinates nudge apart so numbers stay readable
    pins = []
    seen = {}
    for num, s in enumerate(STORIES, start=1):
        if s[11] is None:
            continue
        lon, lat = s[11]
        k = seen.get((lon, lat), 0)
        seen[(lon, lat)] = k + 1
        pins.append((lon + k * 1.6, lat - k * 1.1,
                     REGIONS[s[7]][1], num))
    draw_map(c, MX, 858, CW, 92, pins)
    c.rect(MX + 4, 862, 214, 12, PAPER)
    c.text(MX + 8, 871, "WHERE IT HAPPENED · NUMBERS = STORIES",
           SANSB, SANSB_EM, SANSB_ASC, 7.0, NAVY, 0.3)

    draw_datecheck(c, 956)
    draw_footer(c, 1011)
    return c


def main():
    canvas = build()
    raw = canvas.downsample()
    data = png_bytes(raw)
    out = os.environ.get("ENTRY_OUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()
