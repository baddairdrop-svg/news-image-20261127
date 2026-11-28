#!/usr/bin/env python3
"""Prototype sheet: 3 redesigned hero illustrations (branch
proto-illustrations). New compositions built on the extended
renderer: bezier paths, alpha fills, ellipses, gradients.
Renders a 1024x1024 sheet with the three scenes stacked.
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


def label(x, y, s, size=13, col=NAVY):
    C.text(x, y, s, M.SANSB, M.SANSB_EM, M.SANSB_ASC, size, col, 0.4)


# ---------------------------------------------------------------- proto 1
def proto_nz(x, y, w, h):
    """NZ deadlock: Beehive + hemicycle seat chart + crowd."""
    C.vgrad(x, y, w, h, (96, 160, 220), (210, 232, 248))
    # sun + glow
    C.ellipse(x + w * 0.88, y + h * 0.16, 34, 34, (252, 226, 150), 90)
    C.circle(x + w * 0.88, y + h * 0.16, 20, (252, 214, 110))
    # bezier clouds
    for (cx, cy, s) in [(0.18, 0.14, 1.0), (0.52, 0.1, 0.7), (0.7, 0.2, 0.55)]:
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
    gy = y + h * 0.78
    # layered hills (background -> midground)
    C.path_fill([("M", x, gy), ("C", x + w * 0.2, gy - h * 0.3,
                  x + w * 0.4, gy - h * 0.05, x + w * 0.62, gy - h * 0.18),
                 ("C", x + w * 0.8, gy - h * 0.28, x + w * 0.92, gy - h * 0.08,
                  x + w, gy - h * 0.12), ("L", x + w, gy), ("Z",)],
                (150, 182, 146))
    C.path_fill([("M", x, gy + h * 0.04),
                 ("C", x + w * 0.3, gy - h * 0.1, x + w * 0.55, gy + h * 0.06,
                  x + w, gy - h * 0.04), ("L", x + w, y + h), ("L", x, y + h),
                 ("Z",)], (96, 150, 88))
    C.rect(x, gy + h * 0.06, w, h * 0.16, (84, 140, 78))
    # Beehive: tiered conical parliament building
    bx = x + w * 0.16
    bw = w * 0.2
    by = gy - h * 0.52
    C.soft_shadow(bx + bw / 2, gy + h * 0.07, bw * 1.15, 14)
    tiers = 6
    for i in range(tiers):
        t = i / tiers
        tw = bw * (1 - t * 0.55)
        ty = by + h * 0.52 * t
        th = h * 0.52 / tiers
        C.path_fill([("M", bx + (bw - tw) / 2, ty + th),
                     ("C", bx + (bw - tw) / 2 - 4, ty + th * 0.4,
                      bx + (bw - tw) / 2 + 2, ty, bx + bw / 2 - tw * 0.32, ty),
                     ("L", bx + bw / 2 + tw * 0.32, ty),
                     ("C", bx + (bw + tw) / 2 - 2, ty,
                      bx + (bw + tw) / 2 + 4, ty + th * 0.4,
                      bx + (bw + tw) / 2, ty + th), ("Z",)],
                    (196, 186, 168) if i % 2 else (210, 200, 182))
        for k in range(5):
            C.rect(bx + bw / 2 - tw * 0.3 + k * tw * 0.15, ty + th * 0.35,
                   5, th * 0.3, (90, 110, 140))
    C.rect(bx + bw / 2 - 2, by - h * 0.1, 4, h * 0.1, SIL)
    C.path_fill([("M", bx + bw / 2, by - h * 0.1),
                 ("C", bx + bw / 2 + 16, by - h * 0.12,
                  bx + bw / 2 + 26, by - h * 0.06, bx + bw / 2 + 34, by - h * 0.08),
                 ("C", bx + bw / 2 + 20, by - h * 0.03, bx + bw / 2 + 10,
                  by - h * 0.05, bx + bw / 2, by - h * 0.04), ("Z",)],
                (200, 60, 50))
    # parliament house beside the Beehive
    hx = x + w * 0.4
    hw = w * 0.16
    hy = gy - h * 0.3
    C.soft_shadow(hx + hw / 2, gy + h * 0.07, hw * 1.1, 12)
    C.rect(hx, hy, hw, h * 0.3, (214, 206, 190))
    C.path_fill([("M", hx - 8, hy), ("C", hx + hw * 0.3, hy - h * 0.14,
                  hx + hw * 0.7, hy - h * 0.14, hx + hw + 8, hy), ("Z",)],
                (120, 70, 56))
    for i in range(4):
        C.rect(hx + 8 + i * (hw - 16) / 4, hy + h * 0.08, 7, h * 0.18,
               (240, 236, 220))
    # hemicycle seat chart, right: 130 dots in 4 arcs
    cx, cy = x + w * 0.79, gy - h * 0.02
    C.rect(cx - w * 0.17, y + h * 0.08, w * 0.34, h * 0.62, (250, 248, 240))
    C.frame(cx - w * 0.17, y + h * 0.08, w * 0.34, h * 0.62, INK, 2)
    C.text_center(cx, y + h * 0.16, "PARLIAMENT SEATS", M.SANSB,
                  M.SANSB_EM, M.SANSB_ASC, 13, NAVY, 0.4)
    rows = [(0.30, 46), (0.24, 38), (0.18, 28), (0.12, 18)]
    seat = 0
    for (rr, count) in rows:
        for i in range(count):
            a = math.pi * (0.08 + 0.84 * i / max(1, count - 1))
            px = cx + w * rr * 0.42 * math.cos(a)
            py = cy - h * rr * 1.35 * math.sin(a)
            col = (50, 90, 170) if seat < 65 else (
                (200, 60, 50) if seat < 123 else (240, 180, 60))
            C.circle(px, py, 4.2, col)
            seat += 1
    C.text_center(cx, cy + h * 0.1, "RIGHT 65 · LEFT 58 · OPPORTUNITY 7",
                  M.SANSB, M.SANSB_EM, M.SANSB_ASC, 11.5, INK, 0.2)
    C.text_center(cx, cy + h * 0.17, "66 TO GOVERN — NEITHER HAS IT",
                  M.SANSB, M.SANSB_EM, M.SANSB_ASC, 11, (178, 40, 32), 0.2)
    # foreground crowd with placards
    for i, fx in enumerate((0.06, 0.14, 0.24, 0.34, 0.46, 0.58, 0.9)):
        px = x + w * fx
        s = h * 0.1
        C.soft_shadow(px, y + h * 0.99, 20, 7, (50, 80, 46))
        M._person(C, px, y + h * 1.0, s, (36, 44, 40))
        if i % 2 == 0:
            C.vline(px + 6, y + h * 0.9, h * 0.07, SIL, 2)
            C.rect(px + 1, y + h * 0.855, 20, 10, WHITE)
            C.frame(px + 1, y + h * 0.855, 20, 10, INK, 1)


# ---------------------------------------------------------------- proto 2
def proto_electron(x, y, w, h):
    """Electron night launch: dramatic ascent, Milky Way, ocean."""
    C.vgrad(x, y, w, h, (8, 12, 36), (40, 54, 104))
    # Milky Way diagonal band (faint, scattered)
    for i in range(30):
        t = i / 29
        mx = x + w * (0.08 + 0.6 * t) + (i * 37 % 13) - 6
        my = y + h * (0.55 - 0.42 * t) + (i * 53 % 11) - 5
        C.ellipse(mx, my, 30 - i * 0.5, 9, (220, 228, 248), 13)
    for i in range(90):
        sx = x + (i * 137) % int(w)
        sy = y + (i * 83) % int(h * 0.62)
        C.circle(sx, sy, 1.4 if i % 5 else 2.2, (238, 242, 252))
    # moon + glow
    C.ellipse(x + w * 0.9, y + h * 0.14, 44, 44, (230, 236, 248), 60)
    C.circle(x + w * 0.9, y + h * 0.14, 24, (240, 242, 234))
    C.circle(x + w * 0.9 - 8, y + h * 0.14 - 4, 20, (14, 20, 48))
    sy = y + h * 0.8
    C.vgrad(x, sy, w, h * 0.2, (36, 92, 140), (18, 52, 92))
    # moon reflection path
    for i in range(7):
        C.ellipse(x + w * 0.9 + (i % 2) * 8 - 4, sy + 8 + i * 8,
                  26 - i * 2, 3.5, (220, 232, 248), 70)
    # launch complex silhouette, left
    tx = x + w * 0.14
    C.rect(tx, sy - h * 0.5, 8, h * 0.5, (70, 78, 96))
    for i in range(6):
        C.hline(tx - 8, sy - h * (0.08 + i * 0.08), 24, (70, 78, 96), 2)
    C.rect(tx - 30, sy - h * 0.12, 90, h * 0.12, (52, 60, 76))
    for i in range(4):
        C.circle(tx - 20 + i * 24, sy - h * 0.05, 3, (252, 232, 160))
    # rocket, tilted ascent, centre
    rx, ry = x + w * 0.46, y + h * 0.12
    rw, rh = w * 0.055, h * 0.42
    # curved exhaust plume (layered bezier teardrops)
    C.path_fill([("M", rx + rw * 0.15, ry + rh),
                 ("C", rx - rw * 0.6, ry + rh * 1.5, rx - rw * 0.2, sy - h * 0.06,
                  rx + rw * 0.5, sy),
                 ("C", rx + rw * 1.2, sy - h * 0.06, rx + rw * 1.6, ry + rh * 1.5,
                  rx + rw * 0.85, ry + rh), ("Z",)], (238, 120, 40), 150)
    C.path_fill([("M", rx + rw * 0.3, ry + rh),
                 ("C", rx, ry + rh * 1.45, rx + rw * 0.1, sy - h * 0.1,
                  rx + rw * 0.5, sy - h * 0.02),
                 ("C", rx + rw * 0.9, sy - h * 0.1, rx + rw, ry + rh * 1.45,
                  rx + rw * 0.7, ry + rh), ("Z",)], (250, 196, 80), 190)
    C.path_fill([("M", rx + rw * 0.42, ry + rh),
                 ("C", rx + rw * 0.3, ry + rh * 1.3, rx + rw * 0.35, sy - h * 0.16,
                  rx + rw * 0.5, sy - h * 0.08),
                 ("C", rx + rw * 0.65, sy - h * 0.16, rx + rw * 0.7, ry + rh * 1.3,
                  rx + rw * 0.58, ry + rh), ("Z",)], (255, 246, 220), 230)
    # body with curved nose
    C.path_fill([("M", rx, ry + rh), ("L", rx + rw, ry + rh),
                 ("L", rx + rw, ry + rh * 0.3),
                 ("C", rx + rw, ry + rh * 0.12, rx + rw * 0.7, ry + rh * 0.02,
                  rx + rw / 2, ry),
                 ("C", rx + rw * 0.3, ry + rh * 0.02, rx, ry + rh * 0.12,
                  rx, ry + rh * 0.3), ("Z",)], (250, 248, 242))
    C.rect(rx, ry + rh * 0.55, rw, rh * 0.09, (200, 60, 50))
    C.circle(rx + rw / 2, ry + rh * 0.38, rw * 0.22, NAVY)
    C.circle(rx + rw / 2, ry + rh * 0.38, rw * 0.12, (140, 190, 230))
    # fins (bezier)
    C.path_fill([("M", rx, ry + rh), ("C", rx - rw * 0.7, ry + rh * 1.08,
                  rx - rw * 0.5, ry + rh * 0.86, rx, ry + rh * 0.78), ("Z",)],
                (200, 60, 50))
    C.path_fill([("M", rx + rw, ry + rh), ("C", rx + rw * 1.7, ry + rh * 1.08,
                  rx + rw * 1.5, ry + rh * 0.86, rx + rw, ry + rh * 0.78),
                 ("Z",)], (200, 60, 50))
    # rim light on the body edge
    C.path_stroke([("M", rx + rw, ry + rh * 0.3),
                   ("C", rx + rw, ry + rh * 0.12, rx + rw * 0.7, ry + rh * 0.02,
                    rx + rw / 2, ry)], (252, 220, 160), 2.5, 200)
    # layered smoke at the pad (billowing upward)
    for (dx, dy, r, a) in [(-0.05, -0.03, 0.07, 160), (0.01, -0.06, 0.09, 180),
                           (0.08, -0.03, 0.07, 160), (-0.1, -0.01, 0.05, 140),
                           (0.14, -0.01, 0.05, 130), (0.03, -0.1, 0.06, 120)]:
        C.ellipse(rx + rw / 2 + w * dx, sy + h * dy, w * r * 0.42,
                  h * r * 0.5, (150, 152, 164), a)
    C.ellipse(rx + rw / 2, sy - h * 0.04, w * 0.03, h * 0.05,
              (250, 196, 80), 220)
    # foreground dunes
    C.path_fill([("M", x, y + h), ("C", x + w * 0.2, y + h * 0.9,
                  x + w * 0.4, y + h * 0.97, x + w * 0.62, y + h * 0.93),
                 ("C", x + w * 0.8, y + h * 0.9, x + w * 0.92, y + h * 0.96,
                  x + w, y + h * 0.94), ("L", x + w, y + h), ("Z",)],
                (16, 22, 38))


# ---------------------------------------------------------------- proto 3
def proto_taiwan(x, y, w, h):
    """Taiwan: curved island, median line, jets with contrails."""
    C.vgrad(x, y, w, h, (120, 180, 224), (70, 140, 200))
    C.hgrad(x, y, w, h, (90, 150, 210), (60, 130, 195))
    # mainland coast, left (bezier coastline)
    C.path_fill([("M", x, y), ("C", x + w * 0.16, y + h * 0.12,
                  x + w * 0.1, y + h * 0.3, x + w * 0.18, y + h * 0.48),
                 ("C", x + w * 0.24, y + h * 0.62, x + w * 0.12, y + h * 0.78,
                  x + w * 0.16, y + h), ("L", x, y + h), ("Z",)],
                (110, 150, 96))
    C.path_fill([("M", x, y + h * 0.2), ("C", x + w * 0.08, y + h * 0.3,
                  x + w * 0.06, y + h * 0.5, x + w * 0.1, y + h * 0.7),
                 ("L", x, y + h * 0.75), ("Z",)], (88, 130, 78))
    C.text(x + 10, y + h * 0.3, "MAINLAND", M.SANSB, M.SANSB_EM,
           M.SANSB_ASC, 12, WHITE, 0.3)
    # Taiwan island: smooth bezier coastline
    isl = [("M", x + w * 0.62, y + h * 0.08),
           ("C", x + w * 0.68, y + h * 0.2, x + w * 0.7, y + h * 0.38,
            x + w * 0.68, y + h * 0.55),
           ("C", x + w * 0.66, y + h * 0.72, x + w * 0.63, y + h * 0.86,
            x + w * 0.6, y + h * 0.94),
           ("C", x + w * 0.57, y + h * 0.8, x + w * 0.56, y + h * 0.62,
            x + w * 0.57, y + h * 0.44),
           ("C", x + w * 0.58, y + h * 0.28, x + w * 0.59, y + h * 0.16,
            x + w * 0.62, y + h * 0.08), ("Z",)]
    C.path_fill(isl, (96, 158, 88))
    # mountain ridge shading inside the island
    C.path_fill([("M", x + w * 0.62, y + h * 0.14),
                 ("C", x + w * 0.65, y + h * 0.34, x + w * 0.64, y + h * 0.55,
                  x + w * 0.61, y + h * 0.8),
                 ("C", x + w * 0.6, y + h * 0.6, x + w * 0.6, y + h * 0.34,
                  x + w * 0.62, y + h * 0.14), ("Z",)], (66, 118, 60), 170)
    C.text_center(x + w * 0.625, y + h * 0.52, "TAIWAN", M.SANSB,
                  M.SANSB_EM, M.SANSB_ASC, 13, WHITE, 0.3)
    # median line: dashed curve through the strait
    for i in range(9):
        t0 = i / 9
        t1 = t0 + 0.055
        mx0 = x + w * (0.4 - 0.04 * math.sin(t0 * math.pi))
        mx1 = x + w * (0.4 - 0.04 * math.sin(t1 * math.pi))
        C.line(mx0, y + h * (0.05 + 0.9 * t0), mx1, y + h * (0.05 + 0.9 * t1),
               (220, 70, 60), 3)
    C.text_center(x + w * 0.39, y + h * 0.05, "MEDIAN LINE", M.SANSB,
                  M.SANSB_EM, M.SANSB_ASC, 11, (178, 40, 32), 0.3)
    # radar sweep wedge from the island (translucent)
    C.polygon_alpha([(x + w * 0.62, y + h * 0.5),
                     (x + w * 0.38, y + h * 0.3), (x + w * 0.4, y + h * 0.46)],
                    (250, 240, 190), 34)
    # jets with curved contrails around the island
    jets = [(0.5, 0.18, 0.5), (0.78, 0.24, 1.2), (0.84, 0.52, 1.9),
            (0.76, 0.8, 2.6), (0.52, 0.86, 3.3), (0.44, 0.56, 4.0)]
    for (jx, jy, ang) in jets:
        px, py = x + w * jx, y + h * jy
        u = h * 0.055
        dx, dy = math.cos(ang), math.sin(ang)
        # curved contrail behind the jet
        C.path_stroke([("M", px - dx * u * 5, py - dy * u * 5 + u * 1.6),
                       ("C", px - dx * u * 3, py - dy * u * 3 - u * 0.8,
                        px - dx * u * 1.6, py - dy * u * 1.6 + u * 0.6,
                        px - dx * u * 0.8, py - dy * u * 0.8)],
                      (250, 250, 248), 2.2, 150)
        # detailed jet: long bezier fuselage + swept wings
        nose = (px + dx * u * 2.1, py + dy * u * 2.1)
        tail = (px - dx * u * 1.2, py - dy * u * 1.2)
        w1 = (px - dx * u * 0.5 - dy * u * 1.35, py - dy * u * 0.5 + dx * u * 1.35)
        w2 = (px - dx * u * 0.5 + dy * u * 1.35, py - dy * u * 0.5 - dx * u * 1.35)
        C.path_fill([("M", nose[0], nose[1]),
                     ("C", px + dx * u * 0.9 - dy * u * 0.16,
                      py + dy * u * 0.9 + dx * u * 0.16, w1[0], w1[1],
                      tail[0] - dy * u * 0.3, tail[1] + dx * u * 0.3),
                     ("L", tail[0], tail[1]),
                     ("L", tail[0] + dy * u * 0.3, tail[1] - dx * u * 0.3),
                     ("C", w2[0], w2[1], px + dx * u * 0.9 + dy * u * 0.16,
                      py + dy * u * 0.9 - dx * u * 0.16, nose[0], nose[1]),
                     ("Z",)], (44, 50, 66))
        C.circle(px + dx * u * 0.7, py + dy * u * 0.7, u * 0.18,
                 (150, 200, 240))
    # crossing arrows over the median line
    for fy in (0.32, 0.52, 0.72):
        ay = y + h * fy
        mx = x + w * (0.4 - 0.04 * math.sin(fy * math.pi))
        C.line(mx - w * 0.06, ay, mx + w * 0.06, ay, (220, 70, 60), 3)
        C.polygon([(mx + w * 0.06, ay), (mx + w * 0.04, ay - 5),
                   (mx + w * 0.04, ay + 5)], (220, 70, 60))
    # compass rose, top right
    ccx, ccy = x + w * 0.93, y + h * 0.12
    C.circle(ccx, ccy, 16, WHITE)
    C.ring(ccx, ccy, 16, NAVY, 2)
    C.polygon([(ccx, ccy - 13), (ccx + 4, ccy), (ccx - 4, ccy)], (200, 60, 50))
    C.polygon([(ccx, ccy + 13), (ccx + 4, ccy), (ccx - 4, ccy)], NAVY)
    C.text_center(ccx, ccy - 20, "N", M.SANSB, M.SANSB_EM, M.SANSB_ASC,
                  11, NAVY)


proto_nz(24, 24, 976, 300)
label(24, 348, "PROTOTYPE 1 — NEW ZEALAND ELECTION DEADLOCK (new composition)")
proto_electron(24, 360, 976, 300)
label(24, 684, "PROTOTYPE 2 — ELECTRON NIGHT LAUNCH (new composition)")
proto_taiwan(24, 696, 976, 300)
label(24, 1020, "PROTOTYPE 3 — TAIWAN VOTES AS JETS CIRCLE (new composition)")

out = os.environ.get("PROTO_OUT", "/tmp/proto-sheet.png")
with open(out, "wb") as f:
    f.write(M.png_bytes(C.downsample()))
print("wrote", out)
