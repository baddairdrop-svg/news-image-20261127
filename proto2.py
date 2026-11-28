#!/usr/bin/env python3
"""P1 (NZ parliament) — three rendering-technique treatments of the
same composition, identical size, for visual comparison:
  T1 procedural texture & material
  T2 soft raster compositing (haze, bloom, vignette, soft edges)
  T3 engraving vector painting (hatching, linework, stipple)
Branch proto-illustrations. Production untouched.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main as M

C = M.Canvas(1024, 1024, (250, 246, 230))
INK = M.INK
NAVY = M.NAVY
WHITE = (250, 248, 240)
SIL = (38, 42, 58)
BLUE = (50, 90, 170)
RED = (200, 60, 50)
GOLD = (240, 180, 60)


def label(x, y, s):
    C.text(x, y, s, M.SANSB, M.SANSB_EM, M.SANSB_ASC, 13, NAVY, 0.4)


def hemicycle(cx, cy, w, h, panel=True):
    if panel:
        C.rect(cx - w * 0.17, cy - h * 0.68, w * 0.34, h * 0.62, WHITE)
        C.frame(cx - w * 0.17, cy - h * 0.68, w * 0.34, h * 0.62, INK, 2)
    C.text_center(cx, cy - h * 0.6, "PARLIAMENT SEATS", M.SANSB,
                  M.SANSB_EM, M.SANSB_ASC, 13, NAVY, 0.4)
    rows = [(0.30, 46), (0.24, 38), (0.18, 28), (0.12, 18)]
    seat = 0
    for (rr, count) in rows:
        for i in range(count):
            a = math.pi * (0.08 + 0.84 * i / max(1, count - 1))
            px = cx + w * rr * 0.42 * math.cos(a)
            py = cy - h * rr * 1.35 * math.sin(a)
            col = BLUE if seat < 65 else (RED if seat < 123 else GOLD)
            C.circle(px, py, 4.2, col)
            seat += 1
    C.text_center(cx, cy + h * 0.1, "RIGHT 65 · LEFT 58 · OPPORTUNITY 7",
                  M.SANSB, M.SANSB_EM, M.SANSB_ASC, 11.5, INK, 0.2)
    C.text_center(cx, cy + h * 0.17, "66 TO GOVERN — NEITHER HAS IT",
                  M.SANSB, M.SANSB_EM, M.SANSB_ASC, 11, (178, 40, 32), 0.2)


def beehive(x, y, w, h, gy, style, rng):
    bx = x + w * 0.16
    bw = w * 0.2
    by = gy - h * 0.52
    tiers = 6
    for i in range(tiers):
        t = i / tiers
        tw = bw * (1 - t * 0.55)
        ty = by + h * 0.52 * t
        th = h * 0.52 / tiers
        tx0 = bx + (bw - tw) / 2
        if style == "engrave":
            C.path_fill([("M", tx0, ty + th),
                         ("C", tx0 - 4, ty + th * 0.4, tx0 + 2, ty,
                          bx + bw / 2 - tw * 0.32, ty),
                         ("L", bx + bw / 2 + tw * 0.32, ty),
                         ("C", tx0 + tw - 2, ty, tx0 + tw + 4, ty + th * 0.4,
                          tx0 + tw, ty + th), ("Z",)], (244, 240, 228))
            C.path_stroke([("M", tx0, ty + th),
                           ("C", tx0 - 4, ty + th * 0.4, tx0 + 2, ty,
                            bx + bw / 2 - tw * 0.32, ty),
                           ("L", bx + bw / 2 + tw * 0.32, ty),
                           ("C", tx0 + tw - 2, ty, tx0 + tw + 4, ty + th * 0.4,
                            tx0 + tw, ty + th)], INK, 1.6)
            C.hatch(tx0 + tw * 0.55, ty + 2, tw * 0.42, th - 3, 7,
                    (90, 96, 110), 1)
        elif style == "texture":
            C.path_fill([("M", tx0, ty + th),
                         ("C", tx0 - 4, ty + th * 0.4, tx0 + 2, ty,
                          bx + bw / 2 - tw * 0.32, ty),
                         ("L", bx + bw / 2 + tw * 0.32, ty),
                         ("C", tx0 + tw - 2, ty, tx0 + tw + 4, ty + th * 0.4,
                          tx0 + tw, ty + th), ("Z",)], (214, 204, 186))
            C.path_fill([("M", tx0, ty + th),
                         ("L", tx0 + tw, ty + th), ("L", tx0 + tw, ty + th * 0.55),
                         ("L", tx0, ty + th * 0.55), ("Z",)], (120, 108, 88), 70)
            C.path_fill([("M", tx0 + tw * 0.62, ty), ("L", tx0 + tw, ty),
                         ("L", tx0 + tw, ty + th), ("L", tx0 + tw * 0.62, ty + th),
                         ("Z",)], (90, 80, 66), 60)
            C.speckle(tx0, ty, tw, th, 26,
                      [(150, 138, 116), (230, 222, 204), (120, 108, 88)],
                      rng, 1.4, 120)
        else:  # soft
            C.path_fill([("M", tx0, ty + th),
                         ("C", tx0 - 4, ty + th * 0.4, tx0 + 2, ty,
                          bx + bw / 2 - tw * 0.32, ty),
                         ("L", bx + bw / 2 + tw * 0.32, ty),
                         ("C", tx0 + tw - 2, ty, tx0 + tw + 4, ty + th * 0.4,
                          tx0 + tw, ty + th), ("Z",)], (208, 198, 180))
            C.ellipse(tx0 + tw * 0.5, ty + th * 0.5, tw * 0.48, th * 0.4,
                      (255, 250, 238), 40)
        for k in range(5):
            wx = bx + bw / 2 - tw * 0.3 + k * tw * 0.15
            if style == "engrave":
                C.frame(wx, ty + th * 0.3, 6, th * 0.36, INK, 1)
                C.vline(wx + 3, ty + th * 0.3, th * 0.36, INK, 1)
            elif style == "texture":
                C.rect(wx, ty + th * 0.3, 6, th * 0.36, (84, 104, 136))
                C.line(wx, ty + th * 0.6, wx + 6, ty + th * 0.32,
                       (200, 224, 248), 1)
            else:
                C.rect(wx, ty + th * 0.3, 6, th * 0.36, (110, 136, 172))
                C.ellipse(wx + 3, ty + th * 0.48, 6, th * 0.3,
                          (200, 224, 248), 60)
    C.rect(bx + bw / 2 - 2, by - h * 0.1, 4, h * 0.1, SIL)
    C.path_fill([("M", bx + bw / 2, by - h * 0.1),
                 ("C", bx + bw / 2 + 16, by - h * 0.12, bx + bw / 2 + 26,
                  by - h * 0.06, bx + bw / 2 + 34, by - h * 0.08),
                 ("C", bx + bw / 2 + 20, by - h * 0.03, bx + bw / 2 + 10,
                  by - h * 0.05, bx + bw / 2, by - h * 0.04), ("Z",)], RED)


def house(x, y, w, h, gy, style, rng):
    hx = x + w * 0.4
    hw = w * 0.16
    hy = gy - h * 0.3
    if style == "engrave":
        C.rect(hx, hy, hw, h * 0.3, (244, 240, 228))
        C.frame(hx, hy, hw, h * 0.3, INK, 1.6)
        C.hatch(hx + hw * 0.6, hy + 2, hw * 0.38, h * 0.3 - 4, 4, INK, 1)
        C.path_stroke([("M", hx - 8, hy),
                       ("C", hx + hw * 0.3, hy - h * 0.14, hx + hw * 0.7,
                        hy - h * 0.14, hx + hw + 8, hy)], INK, 2)
        for i in range(5):
            C.path_stroke([("M", hx - 8 + i * 4, hy - i * 2),
                           ("C", hx + hw * 0.3, hy - h * 0.14 - i * 2,
                            hx + hw * 0.7, hy - h * 0.14 - i * 2,
                            hx + hw + 8 - i * 4, hy - i * 2)], INK, 0.8)
    elif style == "texture":
        C.vgrad(hx, hy, hw, h * 0.3, (224, 216, 200), (188, 178, 158))
        for i in range(7):
            C.hline(hx, hy + i * h * 0.045, hw, (170, 160, 140), 1)
        C.speckle(hx, hy, hw, h * 0.3, 40,
                  [(160, 150, 130), (236, 230, 216)], rng, 1.3, 110)
        C.path_fill([("M", hx - 8, hy),
                     ("C", hx + hw * 0.3, hy - h * 0.14, hx + hw * 0.7,
                      hy - h * 0.14, hx + hw + 8, hy), ("Z",)], (120, 70, 56))
        for i in range(4):
            C.path_stroke([("M", hx - 4 + i * 5, hy - 1),
                           ("C", hx + hw * 0.3, hy - h * 0.13 + i * 3,
                            hx + hw * 0.7, hy - h * 0.13 + i * 3,
                            hx + hw + 4 - i * 5, hy - 1)],
                          (90, 52, 42), 1)
    else:
        C.rect(hx, hy, hw, h * 0.3, (216, 208, 192))
        C.ellipse(hx + hw / 2, hy + h * 0.12, hw * 0.55, h * 0.16,
                  (255, 250, 238), 36)
        C.path_fill([("M", hx - 8, hy),
                     ("C", hx + hw * 0.3, hy - h * 0.14, hx + hw * 0.7,
                      hy - h * 0.14, hx + hw + 8, hy), ("Z",)], (126, 76, 62))
    for i in range(4):
        cxp = hx + 8 + i * (hw - 16) / 4
        if style == "engrave":
            C.frame(cxp, hy + h * 0.08, 7, h * 0.18, INK, 1.2)
            C.vline(cxp + 3.5, hy + h * 0.08, h * 0.18, INK, 1)
        elif style == "texture":
            C.vgrad(cxp, hy + h * 0.08, 7, h * 0.18,
                    (246, 242, 228), (196, 188, 168))
        else:
            C.rect(cxp, hy + h * 0.08, 7, h * 0.18, (242, 238, 226))


def crowd(x, y, w, h, style, rng):
    for i, fx in enumerate((0.06, 0.14, 0.24, 0.34, 0.46, 0.58, 0.9)):
        px = x + w * fx
        if style == "soft":
            C.soft_shadow(px, y + h * 0.99, 22, 8, (50, 80, 46))
            M._person(C, px, y + h * 1.0, h * 0.1, (36, 44, 40))
            C.ellipse(px, y + h * 0.94, 8, 13, (36, 44, 40), 60)
        else:
            C.soft_shadow(px, y + h * 0.99, 20, 7, (50, 80, 46))
            M._person(C, px, y + h * 1.0, h * 0.1, (36, 44, 40))
            if style == "texture":
                C.path_stroke([("M", px + 4, y + h * 0.9),
                               ("L", px + 5, y + h * 0.99)],
                              (250, 226, 170), 1.2, 160)
        if i % 2 == 0:
            C.vline(px + 6, y + h * 0.9, h * 0.07, SIL, 2)
            C.rect(px + 1, y + h * 0.855, 20, 10, WHITE)
            C.frame(px + 1, y + h * 0.855, 20, 10, INK, 1)


# ---------------------------------------------------------------- T1
def t1_texture(x, y, w, h):
    rng = M.LCG(2701)
    C.vgrad(x, y, w, h, (96, 160, 220), (210, 232, 248))
    C.speckle(x, y, w, h * 0.4, 60, [(240, 248, 255)], rng, 1.2, 40)
    C.ellipse(x + w * 0.88, y + h * 0.16, 36, 36, (252, 226, 150), 90)
    C.circle(x + w * 0.88, y + h * 0.16, 20, (252, 214, 110))
    for (cx, cy, s) in [(0.18, 0.14, 1.0), (0.52, 0.1, 0.7)]:
        bx, by = x + w * cx, y + h * cy
        u = 26 * s
        C.path_fill([("M", bx - u * 2, by + u * 0.4),
                     ("C", bx - u * 2, by - u * 0.6, bx - u * 0.8, by - u,
                      bx - u * 0.2, by - u * 0.5),
                     ("C", bx + u * 0.3, by - u * 1.1, bx + u * 1.1, by - u * 0.7,
                      bx + u * 1.2, by - u * 0.1),
                     ("C", bx + u * 2, by, bx + u * 1.9, by + u * 0.5,
                      bx + u * 1.2, by + u * 0.5),
                     ("L", bx - u * 1.4, by + u * 0.5), ("Z",)],
                    (255, 255, 252), 235)
        C.speckle(bx - u * 1.6, by - u * 0.6, u * 3.2, u * 1.0, 22,
                  [(214, 228, 244)], rng, 1.6, 90)
    gy = y + h * 0.78
    C.path_fill([("M", x, gy), ("C", x + w * 0.2, gy - h * 0.3,
                  x + w * 0.4, gy - h * 0.05, x + w * 0.62, gy - h * 0.18),
                 ("C", x + w * 0.8, gy - h * 0.28, x + w * 0.92, gy - h * 0.08,
                  x + w, gy - h * 0.12), ("L", x + w, gy), ("Z",)],
                (150, 182, 146))
    C.foliage(x + w * 0.3, gy - h * 0.1, w * 0.28, h * 0.07, 120,
              [(120, 164, 112), (170, 198, 156), (96, 140, 92)], rng, 150)
    C.path_fill([("M", x, gy + h * 0.04),
                 ("C", x + w * 0.3, gy - h * 0.1, x + w * 0.55, gy + h * 0.06,
                  x + w, gy - h * 0.04), ("L", x + w, y + h), ("L", x, y + h),
                 ("Z",)], (96, 150, 88))
    C.rect(x, gy + h * 0.06, w, h * 0.16, (84, 140, 78))
    C.grass(x, gy + h * 0.08, w, h * 0.13, 520,
            [(60, 120, 58), (110, 170, 96), (140, 190, 120)], rng)
    C.soft_shadow(x + w * 0.26, gy + h * 0.07, w * 0.24, 14)
    C.soft_shadow(x + w * 0.48, gy + h * 0.07, w * 0.18, 12)
    beehive(x, y, w, h, gy, "texture", rng)
    house(x, y, w, h, gy, "texture", rng)
    hemicycle(x + w * 0.79, gy - h * 0.02, w, h)
    crowd(x, y, w, h, "texture", rng)


# ---------------------------------------------------------------- T2
def t2_soft(x, y, w, h):
    rng = M.LCG(2702)
    C.vgrad(x, y, w, h, (110, 168, 224), (216, 234, 248))
    # bloom sun
    for (r, a) in [(70, 26), (52, 40), (38, 60)]:
        C.ellipse(x + w * 0.88, y + h * 0.16, r, r, (252, 226, 150), a)
    C.circle(x + w * 0.88, y + h * 0.16, 20, (252, 220, 130))
    for (cx, cy, s) in [(0.18, 0.14, 1.0), (0.52, 0.1, 0.7)]:
        bx, by = x + w * cx, y + h * cy
        u = 26 * s
        for (ox, oy, rr, a) in [(0, 0, 1.5, 120), (-0.8, 0.15, 1.0, 110),
                                (0.8, 0.1, 1.1, 110), (0.2, -0.3, 0.9, 100)]:
            C.ellipse(bx + ox * u, by + oy * u, u * rr, u * rr * 0.45,
                      (255, 255, 252), a)
    gy = y + h * 0.78
    # soft hills: stacked translucent ellipses along ridges
    for i in range(16):
        t = i / 15
        hx = x + w * t
        hy = gy - h * (0.1 + 0.1 * math.sin(t * 5.2))
        C.ellipse(hx, hy + h * 0.1, w * 0.09, h * 0.1, (150, 182, 146), 55)
    C.path_fill([("M", x, gy + h * 0.04),
                 ("C", x + w * 0.3, gy - h * 0.1, x + w * 0.55, gy + h * 0.06,
                  x + w, gy - h * 0.04), ("L", x + w, y + h), ("L", x, y + h),
                 ("Z",)], (96, 150, 88))
    # horizon haze
    C.ellipse(x + w * 0.5, gy - h * 0.04, w * 0.55, h * 0.05,
              (235, 244, 250), 70)
    C.rect(x, gy + h * 0.06, w, h * 0.16, (88, 144, 80))
    C.soft_shadow(x + w * 0.26, gy + h * 0.07, w * 0.26, 18)
    C.soft_shadow(x + w * 0.48, gy + h * 0.07, w * 0.2, 15)
    beehive(x, y, w, h, gy, "soft", rng)
    house(x, y, w, h, gy, "soft", rng)
    hemicycle(x + w * 0.79, gy - h * 0.02, w, h)
    crowd(x, y, w, h, "soft", rng)
    # warm grade + vignette
    C.ellipse(x + w * 0.5, y + h * 1.05, w * 0.6, h * 0.35,
              (250, 220, 160), 26)
    for (vx, vy) in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
        C.ellipse(vx, vy, w * 0.16, h * 0.2, (30, 36, 54), 20)


# ---------------------------------------------------------------- T3
def t3_engrave(x, y, w, h):
    rng = M.LCG(2703)
    C.rect(x, y, w, h, (248, 244, 232))
    # engraved sky: fine horizontal lines, denser at top
    for i in range(11):
        yy = y + 4 + i * (h * 0.3 / 11)
        C.hline(x, yy, w, (186, 200, 218), 1)
    C.stipple(x + w * 0.8, y + h * 0.05, w * 0.16, h * 0.2, 90,
              (220, 170, 70), rng, 1.3)
    C.ring(x + w * 0.88, y + h * 0.16, 20, (220, 170, 70), 2)
    C.ring(x + w * 0.88, y + h * 0.16, 27, (220, 170, 70), 1)
    for (cx, cy, s) in [(0.18, 0.14, 1.0), (0.52, 0.1, 0.7)]:
        bx, by = x + w * cx, y + h * cy
        u = 26 * s
        C.path_stroke([("M", bx - u * 2, by + u * 0.4),
                       ("C", bx - u * 2, by - u * 0.6, bx - u * 0.8, by - u,
                        bx - u * 0.2, by - u * 0.5),
                       ("C", bx + u * 0.3, by - u * 1.1, bx + u * 1.1,
                        by - u * 0.7, bx + u * 1.2, by - u * 0.1),
                       ("C", bx + u * 2, by, bx + u * 1.9, by + u * 0.5,
                        bx + u * 1.2, by + u * 0.5),
                       ("L", bx - u * 1.4, by + u * 0.5)], INK, 1.4)
    gy = y + h * 0.78
    # contour-line hills
    for i in range(5):
        off = i * h * 0.035
        C.path_stroke([("M", x, gy - off),
                       ("C", x + w * 0.2, gy - h * 0.3 - off,
                        x + w * 0.4, gy - h * 0.05 - off,
                        x + w * 0.62, gy - h * 0.18 - off),
                       ("C", x + w * 0.8, gy - h * 0.28 - off,
                        x + w * 0.92, gy - h * 0.08 - off,
                        x + w, gy - h * 0.12 - off)], (90, 130, 84), 1.2)
    C.hline(x, gy, w, INK, 1.6)
    C.hatch(x, gy + 3, w, h * 0.2, 11, (110, 150, 100), 1, 0.6)
    beehive(x, y, w, h, gy, "engrave", rng)
    house(x, y, w, h, gy, "engrave", rng)
    hemicycle(x + w * 0.79, gy - h * 0.02, w, h)
    crowd(x, y, w, h, "engrave", rng)


t1_texture(24, 24, 976, 300)
label(24, 348, "T1 — PROCEDURAL TEXTURE & MATERIAL")
t2_soft(24, 360, 976, 300)
label(24, 684, "T2 — SOFT RASTER COMPOSITING")
t3_engrave(24, 696, 976, 300)
label(24, 1020, "T3 — ENGRAVING VECTOR PAINTING")

out = os.environ.get("PROTO2_OUT", "/tmp/proto2-sheet.png")
with open(out, "wb") as f:
    f.write(M.png_bytes(C.downsample()))
print("wrote", out)
