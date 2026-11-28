#!/usr/bin/env python3
"""Refined T1 (procedural texture & material + T2 lighting /
layered compositing) applied to P1 NZ, P2 Electron, P3 Taiwan.
Same composition references as prototypes C, identical resolution.
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


def hemicycle(cx, cy, w, h):
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


def tree(cx, base, s, rng):
    C.rect(cx - 2, base - s * 0.5, 4, s * 0.5, (96, 70, 46))
    C.foliage(cx, base - s * 0.85, s * 0.5, s * 0.4, 26,
              [(66, 124, 60), (96, 156, 80), (52, 104, 52)], rng, 200)


# ---------------------------------------------------------------- P1
def p1_nz(x, y, w, h):
    rng = M.LCG(2801)
    C.vgrad(x, y, w, h, (96, 160, 220), (210, 232, 248))
    C.speckle(x, y, w, h * 0.35, 24, [(240, 248, 255)], rng, 1.1, 36)
    # sun with T2-style bloom
    for (r, a) in [(54, 30), (40, 48)]:
        C.ellipse(x + w * 0.88, y + h * 0.16, r, r, (252, 226, 150), a)
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
        C.speckle(bx - u * 1.6, by - u * 0.6, u * 3.2, u * 1.0, 12,
                  [(214, 228, 244)], rng, 1.5, 80)
    gy = y + h * 0.78
    C.path_fill([("M", x, gy), ("C", x + w * 0.2, gy - h * 0.3,
                  x + w * 0.4, gy - h * 0.05, x + w * 0.62, gy - h * 0.18),
                 ("C", x + w * 0.8, gy - h * 0.28, x + w * 0.92, gy - h * 0.08,
                  x + w, gy - h * 0.12), ("L", x + w, gy), ("Z",)],
                (150, 182, 146))
    C.foliage(x + w * 0.3, gy - h * 0.1, w * 0.28, h * 0.07, 70,
              [(120, 164, 112), (170, 198, 156), (96, 140, 92)], rng, 140)
    C.path_fill([("M", x, gy + h * 0.04),
                 ("C", x + w * 0.3, gy - h * 0.1, x + w * 0.55, gy + h * 0.06,
                  x + w, gy - h * 0.04), ("L", x + w, y + h), ("L", x, y + h),
                 ("Z",)], (96, 150, 88))
    C.rect(x, gy + h * 0.06, w, h * 0.16, (84, 140, 78))
    # horizon haze (T2 compositing)
    C.ellipse(x + w * 0.5, gy - h * 0.03, w * 0.55, h * 0.045,
              (235, 244, 250), 56)
    # gravel path to the buildings (material-following, sparse)
    C.polygon([(x + w * 0.3, y + h), (x + w * 0.42, y + h),
               (x + w * 0.4, gy + h * 0.05), (x + w * 0.33, gy + h * 0.05)],
              (206, 198, 178))
    C.speckle(x + w * 0.32, gy + h * 0.06, w * 0.09, h * 0.15, 30,
              [(170, 160, 140), (226, 218, 198)], rng, 1.2, 130)
    # foreground grass: sparse, longer near the bottom (perspective)
    for _ in range(170):
        px = x + rng.next() * w
        t = rng.next()
        py = gy + h * (0.1 + 0.11 * t)
        ln = 2 + t * 3.5
        col = [(60, 120, 58), (110, 170, 96), (140, 190, 120)][
            int(rng.next() * 3) % 3]
        C.line(px, py, px + (rng.next() - 0.5) * 2, py - ln, col, 1)
    C.soft_shadow(x + w * 0.26, gy + h * 0.07, w * 0.24, 14)
    C.soft_shadow(x + w * 0.48, gy + h * 0.07, w * 0.18, 12)
    # Beehive with cornices, entrance steps, door
    bx, bw, by = x + w * 0.16, w * 0.2, gy - h * 0.52
    tiers = 6
    for i in range(tiers):
        t = i / tiers
        tw = bw * (1 - t * 0.55)
        ty = by + h * 0.52 * t
        th = h * 0.52 / tiers
        tx0 = bx + (bw - tw) / 2
        C.path_fill([("M", tx0, ty + th),
                     ("C", tx0 - 4, ty + th * 0.4, tx0 + 2, ty,
                      bx + bw / 2 - tw * 0.32, ty),
                     ("L", bx + bw / 2 + tw * 0.32, ty),
                     ("C", tx0 + tw - 2, ty, tx0 + tw + 4, ty + th * 0.4,
                      tx0 + tw, ty + th), ("Z",)], (214, 204, 186))
        C.path_fill([("M", tx0, ty + th), ("L", tx0 + tw, ty + th),
                     ("L", tx0 + tw, ty + th * 0.55), ("L", tx0, ty + th * 0.55),
                     ("Z",)], (120, 108, 88), 64)
        C.path_fill([("M", tx0 + tw * 0.62, ty), ("L", tx0 + tw, ty),
                     ("L", tx0 + tw, ty + th), ("L", tx0 + tw * 0.62, ty + th),
                     ("Z",)], (90, 80, 66), 54)
        C.hline(tx0 + 2, ty + 1.5, tw - 4, (240, 234, 220), 1.6)
        C.speckle(tx0, ty, tw, th, 12,
                  [(150, 138, 116), (230, 222, 204)], rng, 1.3, 110)
        for k in range(5):
            wx = bx + bw / 2 - tw * 0.3 + k * tw * 0.15
            C.rect(wx, ty + th * 0.3, 6, th * 0.36, (84, 104, 136))
            C.line(wx, ty + th * 0.6, wx + 6, ty + th * 0.32,
                   (200, 224, 248), 1)
    C.rect(bx + bw / 2 - 7, gy - h * 0.09, 14, h * 0.09, (70, 58, 44))
    for i in range(3):
        C.hline(bx + bw / 2 - 12 - i * 3, gy + i * 3, 24 + i * 6,
                (176, 168, 150), 2)
    C.rect(bx + bw / 2 - 2, by - h * 0.1, 4, h * 0.1, SIL)
    C.circle(bx + bw / 2, by - h * 0.105, 3, GOLD)
    C.path_fill([("M", bx + bw / 2, by - h * 0.1),
                 ("C", bx + bw / 2 + 16, by - h * 0.12, bx + bw / 2 + 26,
                  by - h * 0.06, bx + bw / 2 + 34, by - h * 0.08),
                 ("C", bx + bw / 2 + 20, by - h * 0.03, bx + bw / 2 + 10,
                  by - h * 0.05, bx + bw / 2, by - h * 0.04), ("Z",)], RED)
    # parliament house: pediment, door, steps
    hx, hw, hy = x + w * 0.4, w * 0.16, gy - h * 0.3
    C.vgrad(hx, hy, hw, h * 0.3, (224, 216, 200), (192, 182, 162))
    for i in range(7):
        C.hline(hx, hy + i * h * 0.045, hw, (176, 166, 146), 1)
    C.speckle(hx, hy, hw, h * 0.3, 18, [(160, 150, 130), (236, 230, 216)],
              rng, 1.2, 100)
    C.path_fill([("M", hx - 8, hy),
                 ("C", hx + hw * 0.3, hy - h * 0.14, hx + hw * 0.7,
                  hy - h * 0.14, hx + hw + 8, hy), ("Z",)], (120, 70, 56))
    C.polygon([(hx + hw * 0.32, hy - h * 0.015), (hx + hw * 0.68, hy - h * 0.015),
               (hx + hw * 0.5, hy - h * 0.085)], (240, 236, 220))
    for i in range(4):
        C.path_stroke([("M", hx - 4 + i * 5, hy - 1),
                       ("C", hx + hw * 0.3, hy - h * 0.13 + i * 3,
                        hx + hw * 0.7, hy - h * 0.13 + i * 3,
                        hx + hw + 4 - i * 5, hy - 1)], (90, 52, 42), 1)
    for i in range(4):
        cxp = hx + 8 + i * (hw - 16) / 4
        C.vgrad(cxp, hy + h * 0.08, 7, h * 0.18,
                (246, 242, 228), (200, 192, 172))
    C.rect(hx + hw / 2 - 6, gy - h * 0.11, 12, h * 0.11, (70, 58, 44))
    # trees + lamp posts (environmental detail)
    tree(x + w * 0.6, gy + h * 0.06, h * 0.2, rng)
    tree(x + w * 0.65, gy + h * 0.05, h * 0.16, rng)
    tree(x + w * 0.09, gy + h * 0.06, h * 0.18, rng)
    for lx in (0.37, 0.58):
        C.vline(x + w * lx, gy - h * 0.12, h * 0.18, SIL, 2)
        C.circle(x + w * lx, gy - h * 0.13, 3.4, (252, 232, 160))
    hemicycle(x + w * 0.79, gy - h * 0.02, w, h)
    # crowd
    for i, fx in enumerate((0.06, 0.14, 0.24, 0.34, 0.46, 0.58, 0.9)):
        px = x + w * fx
        C.soft_shadow(px, y + h * 0.99, 20, 7, (50, 80, 46))
        M._person(C, px, y + h * 1.0, h * 0.1, (36, 44, 40))
        C.path_stroke([("M", px + 4, y + h * 0.9), ("L", px + 5, y + h * 0.99)],
                      (250, 226, 170), 1.2, 150)
        if i % 2 == 0:
            C.vline(px + 6, y + h * 0.9, h * 0.07, SIL, 2)
            C.rect(px + 1, y + h * 0.855, 20, 10, WHITE)
            C.frame(px + 1, y + h * 0.855, 20, 10, INK, 1)
    # gentle warm grade + vignette (T2 compositing, subtle)
    C.ellipse(x + w * 0.5, y + h * 1.06, w * 0.6, h * 0.34,
              (250, 220, 160), 20)
    for (vx, vy) in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
        C.ellipse(vx, vy, w * 0.15, h * 0.19, (30, 36, 54), 14)


# ---------------------------------------------------------------- P2
def p2_electron(x, y, w, h):
    rng = M.LCG(2802)
    C.vgrad(x, y, w, h, (8, 12, 36), (40, 54, 104))
    for i in range(30):
        t = i / 29
        C.ellipse(x + w * (0.08 + 0.6 * t) + (i * 37 % 13) - 6,
                  y + h * (0.55 - 0.42 * t) + (i * 53 % 11) - 5,
                  30 - i * 0.5, 9, (220, 228, 248), 11)
    for i in range(90):
        C.circle(x + (i * 137) % int(w), y + (i * 83) % int(h * 0.62),
                 1.4 if i % 5 else 2.2, (238, 242, 252))
    for (r, a) in [(52, 34), (38, 52)]:
        C.ellipse(x + w * 0.9, y + h * 0.14, r, r, (230, 236, 248), a)
    C.circle(x + w * 0.9, y + h * 0.14, 24, (240, 242, 234))
    C.circle(x + w * 0.9 - 8, y + h * 0.14 - 4, 20, (14, 20, 48))
    sy = y + h * 0.8
    C.vgrad(x, sy, w, h * 0.2, (36, 92, 140), (18, 52, 92))
    # ocean wave texture: sparse short strokes following the surface
    for _ in range(70):
        px = x + rng.next() * w
        py = sy + 4 + rng.next() * h * 0.17
        ln = 6 + rng.next() * 14
        C.hline(px, py, ln, (120, 180, 220), 1)
    for i in range(7):
        C.ellipse(x + w * 0.9 + (i % 2) * 8 - 4, sy + 8 + i * 8,
                  26 - i * 2, 3.5, (220, 232, 248), 66)
    # launch tower: lattice detail + crane arm + fuel tanks
    tx = x + w * 0.14
    C.rect(tx, sy - h * 0.5, 8, h * 0.5, (70, 78, 96))
    C.rect(tx + 22, sy - h * 0.5, 8, h * 0.5, (70, 78, 96))
    for i in range(6):
        yy = sy - h * (0.06 + i * 0.085)
        C.hline(tx - 4, yy, 38, (70, 78, 96), 2)
        C.line(tx, yy, tx + 30, yy - h * 0.08, (70, 78, 96), 1.4)
        C.line(tx + 30, yy, tx, yy - h * 0.08, (70, 78, 96), 1.4)
    C.line(tx + 30, sy - h * 0.46, tx + 64, sy - h * 0.4, (70, 78, 96), 3)
    C.rect(tx - 34, sy - h * 0.12, 96, h * 0.12, (52, 60, 76))
    C.speckle(tx - 34, sy - h * 0.12, 96, h * 0.12, 22,
              [(90, 98, 114), (40, 46, 60)], rng, 1.2, 120)
    for i in range(4):
        C.circle(tx - 24 + i * 26, sy - h * 0.05, 3, (252, 232, 160))
        C.ellipse(tx - 24 + i * 26, sy - h * 0.05, 8, 8, (252, 232, 160), 50)
    for i in range(2):
        fx = tx - 30 + i * 26
        C.vgrad(fx, sy - h * 0.24, 20, h * 0.12, (210, 214, 222), (140, 146, 158))
        C.ellipse(fx + 10, sy - h * 0.24, 10, 4, (226, 230, 238))
    # rocket: panel lines, metallic shading, detailed fins
    rx, ry = x + w * 0.46, y + h * 0.12
    rw, rh = w * 0.055, h * 0.42
    C.path_fill([("M", rx + rw * 0.15, ry + rh),
                 ("C", rx - rw * 0.6, ry + rh * 1.5, rx - rw * 0.2, sy - h * 0.06,
                  rx + rw * 0.5, sy),
                 ("C", rx + rw * 1.2, sy - h * 0.06, rx + rw * 1.6, ry + rh * 1.5,
                  rx + rw * 0.85, ry + rh), ("Z",)], (238, 120, 40), 140)
    C.path_fill([("M", rx + rw * 0.3, ry + rh),
                 ("C", rx, ry + rh * 1.45, rx + rw * 0.1, sy - h * 0.1,
                  rx + rw * 0.5, sy - h * 0.02),
                 ("C", rx + rw * 0.9, sy - h * 0.1, rx + rw, ry + rh * 1.45,
                  rx + rw * 0.7, ry + rh), ("Z",)], (250, 196, 80), 180)
    C.path_fill([("M", rx + rw * 0.42, ry + rh),
                 ("C", rx + rw * 0.3, ry + rh * 1.3, rx + rw * 0.35, sy - h * 0.16,
                  rx + rw * 0.5, sy - h * 0.08),
                 ("C", rx + rw * 0.65, sy - h * 0.16, rx + rw * 0.7, ry + rh * 1.3,
                  rx + rw * 0.58, ry + rh), ("Z",)], (255, 246, 220), 225)
    # embers inside the plume (material-following)
    for _ in range(36):
        t = rng.next()
        px = rx + rw * (0.5 + (rng.next() - 0.5) * (0.4 + t))
        py = ry + rh + t * (sy - ry - rh) * 0.92
        C.circle(px, py, 1 + rng.next() * 1.6,
                 (252, 214, 110) if rng.next() > 0.4 else (250, 150, 60))
    C.path_fill([("M", rx, ry + rh), ("L", rx + rw, ry + rh),
                 ("L", rx + rw, ry + rh * 0.3),
                 ("C", rx + rw, ry + rh * 0.12, rx + rw * 0.7, ry + rh * 0.02,
                  rx + rw / 2, ry),
                 ("C", rx + rw * 0.3, ry + rh * 0.02, rx, ry + rh * 0.12,
                  rx, ry + rh * 0.3), ("Z",)], (250, 248, 242))
    C.path_fill([("M", rx + rw * 0.68, ry + rh * 0.28), ("L", rx + rw, ry + rh * 0.3),
                 ("L", rx + rw, ry + rh), ("L", rx + rw * 0.68, ry + rh), ("Z",)],
                (120, 124, 140), 70)
    for i in range(4):
        C.hline(rx + 2, ry + rh * (0.34 + i * 0.16), rw - 4, (196, 198, 206), 1)
    C.vline(rx + rw * 0.5, ry + rh * 0.3, rh * 0.68, (206, 208, 216), 1)
    C.rect(rx, ry + rh * 0.55, rw, rh * 0.09, RED)
    C.circle(rx + rw / 2, ry + rh * 0.38, rw * 0.22, NAVY)
    C.circle(rx + rw / 2, ry + rh * 0.38, rw * 0.12, (140, 190, 230))
    C.line(rx + rw * 0.4, ry + rh * 0.44, rx + rw * 0.62, ry + rh * 0.34,
           (230, 244, 255), 1.4)
    C.path_fill([("M", rx, ry + rh), ("C", rx - rw * 0.7, ry + rh * 1.08,
                  rx - rw * 0.5, ry + rh * 0.86, rx, ry + rh * 0.78), ("Z",)], RED)
    C.path_fill([("M", rx + rw, ry + rh), ("C", rx + rw * 1.7, ry + rh * 1.08,
                  rx + rw * 1.5, ry + rh * 0.86, rx + rw, ry + rh * 0.78),
                 ("Z",)], RED)
    C.path_stroke([("M", rx + rw, ry + rh * 0.3),
                   ("C", rx + rw, ry + rh * 0.12, rx + rw * 0.7, ry + rh * 0.02,
                    rx + rw / 2, ry)], (252, 220, 160), 2.5, 200)
    # plume light cast on pad + smoke clusters
    C.ellipse(rx + rw / 2, sy - h * 0.05, w * 0.09, h * 0.07,
              (250, 196, 80), 60)
    for (dx, dy, r, a) in [(-0.05, -0.03, 0.07, 150), (0.01, -0.06, 0.09, 170),
                           (0.08, -0.03, 0.07, 150), (-0.1, -0.01, 0.05, 130),
                           (0.14, -0.01, 0.05, 120), (0.03, -0.1, 0.06, 110)]:
        C.ellipse(rx + rw / 2 + w * dx, sy + h * dy, w * r * 0.42,
                  h * r * 0.5, (150, 152, 164), a)
    C.foliage(rx + rw / 2, sy - h * 0.04, w * 0.09, h * 0.05, 30,
              [(170, 172, 184), (128, 130, 142)], rng, 120)
    C.ellipse(rx + rw / 2, sy - h * 0.04, w * 0.03, h * 0.05,
              (250, 196, 80), 210)
    # foreground dunes with sparse grass tufts
    C.path_fill([("M", x, y + h), ("C", x + w * 0.2, y + h * 0.9,
                  x + w * 0.4, y + h * 0.97, x + w * 0.62, y + h * 0.93),
                 ("C", x + w * 0.8, y + h * 0.9, x + w * 0.92, y + h * 0.96,
                  x + w, y + h * 0.94), ("L", x + w, y + h), ("Z",)],
                (16, 22, 38))
    for _ in range(40):
        px = x + rng.next() * w
        py = y + h * (0.93 + rng.next() * 0.06)
        C.line(px, py, px + (rng.next() - 0.5) * 2, py - 3 - rng.next() * 3,
               (52, 66, 52), 1)


# ---------------------------------------------------------------- P3
def p3_taiwan(x, y, w, h):
    rng = M.LCG(2803)
    C.vgrad(x, y, w, h, (120, 180, 224), (70, 140, 200))
    C.hgrad(x, y, w, h, (90, 150, 210), (60, 130, 195))
    # sea texture: sparse wave strokes + sun glints
    for _ in range(80):
        px = x + rng.next() * w
        py = y + rng.next() * h
        C.hline(px, py, 5 + rng.next() * 11, (170, 212, 240), 1)
    for _ in range(18):
        C.hline(x + rng.next() * w * 0.4, y + rng.next() * h * 0.3,
                4 + rng.next() * 8, (250, 240, 200), 1)
    for (r, a) in [(46, 30), (32, 46)]:
        C.ellipse(x + w * 0.06, y + h * 0.08, r, r, (252, 226, 150), a)
    C.circle(x + w * 0.06, y + h * 0.08, 14, (252, 214, 110))
    # mainland coast with terrain texture
    C.path_fill([("M", x, y), ("C", x + w * 0.16, y + h * 0.12,
                  x + w * 0.1, y + h * 0.3, x + w * 0.18, y + h * 0.48),
                 ("C", x + w * 0.24, y + h * 0.62, x + w * 0.12, y + h * 0.78,
                  x + w * 0.16, y + h), ("L", x, y + h), ("Z",)],
                (110, 150, 96))
    C.foliage(x + w * 0.07, y + h * 0.5, w * 0.06, h * 0.34, 60,
              [(88, 130, 78), (130, 170, 112), (72, 112, 66)], rng, 150)
    C.path_stroke([("M", x + w * 0.05, y + h * 0.15),
                   ("C", x + w * 0.09, y + h * 0.4, x + w * 0.07, y + h * 0.65,
                    x + w * 0.09, y + h * 0.88)], (72, 112, 66), 1.4)
    C.text(x + 10, y + h * 0.3, "MAINLAND", M.SANSB, M.SANSB_EM,
           M.SANSB_ASC, 12, WHITE, 0.3)
    # island soft shadow in the sea
    C.ellipse(x + w * 0.635, y + h * 0.56, w * 0.075, h * 0.44,
              (30, 84, 124), 36)
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
    C.foliage(x + w * 0.625, y + h * 0.5, w * 0.035, h * 0.3, 44,
              [(66, 118, 60), (120, 176, 104), (52, 100, 50)], rng, 160)
    C.path_fill([("M", x + w * 0.62, y + h * 0.14),
                 ("C", x + w * 0.65, y + h * 0.34, x + w * 0.64, y + h * 0.55,
                  x + w * 0.61, y + h * 0.8),
                 ("C", x + w * 0.6, y + h * 0.6, x + w * 0.6, y + h * 0.34,
                  x + w * 0.62, y + h * 0.14), ("Z",)], (66, 118, 60), 150)
    C.path_stroke([("M", x + w * 0.62, y + h * 0.08),
                   ("C", x + w * 0.68, y + h * 0.2, x + w * 0.7, y + h * 0.38,
                    x + w * 0.68, y + h * 0.55),
                   ("C", x + w * 0.66, y + h * 0.72, x + w * 0.63, y + h * 0.86,
                    x + w * 0.6, y + h * 0.94)], (220, 240, 210), 1.6)
    C.text_center(x + w * 0.625, y + h * 0.52, "TAIWAN", M.SANSB,
                  M.SANSB_EM, M.SANSB_ASC, 13, WHITE, 0.3)
    for i in range(9):
        t0 = i / 9
        t1 = t0 + 0.055
        mx0 = x + w * (0.4 - 0.04 * math.sin(t0 * math.pi))
        mx1 = x + w * (0.4 - 0.04 * math.sin(t1 * math.pi))
        C.line(mx0, y + h * (0.05 + 0.9 * t0), mx1, y + h * (0.05 + 0.9 * t1),
               (220, 70, 60), 3)
    C.text_center(x + w * 0.39, y + h * 0.05, "MEDIAN LINE", M.SANSB,
                  M.SANSB_EM, M.SANSB_ASC, 11, (178, 40, 32), 0.3)
    C.polygon_alpha([(x + w * 0.62, y + h * 0.5),
                     (x + w * 0.38, y + h * 0.3), (x + w * 0.4, y + h * 0.46)],
                    (250, 240, 190), 26)
    jets = [(0.5, 0.18, 0.5), (0.78, 0.24, 1.2), (0.84, 0.52, 1.9),
            (0.76, 0.8, 2.6), (0.52, 0.86, 3.3), (0.44, 0.56, 4.0)]
    for (jx, jy, ang) in jets:
        px, py = x + w * jx, y + h * jy
        u = h * 0.055
        dx, dy = math.cos(ang), math.sin(ang)
        C.ellipse(px + 4, py + h * 0.05, u * 1.2, u * 0.4, (30, 84, 124), 70)
        C.path_stroke([("M", px - dx * u * 5, py - dy * u * 5 + u * 1.6),
                       ("C", px - dx * u * 3, py - dy * u * 3 - u * 0.8,
                        px - dx * u * 1.6, py - dy * u * 1.6 + u * 0.6,
                        px - dx * u * 0.8, py - dy * u * 0.8)],
                      (250, 250, 248), 2.2, 140)
        nose = (px + dx * u * 2.4, py + dy * u * 2.4)
        tail = (px - dx * u * 1.3, py - dy * u * 1.3)
        w1 = (px - dx * u * 0.9 - dy * u * 1.35, py - dy * u * 0.9 + dx * u * 1.35)
        w2 = (px - dx * u * 0.9 + dy * u * 1.35, py - dy * u * 0.9 - dx * u * 1.35)
        C.path_fill([("M", nose[0], nose[1]),
                     ("C", px + dx * u * 1.1 - dy * u * 0.08,
                      py + dy * u * 1.1 + dx * u * 0.08, w1[0], w1[1],
                      tail[0] - dy * u * 0.26, tail[1] + dx * u * 0.26),
                     ("L", tail[0], tail[1]),
                     ("L", tail[0] + dy * u * 0.26, tail[1] - dx * u * 0.26),
                     ("C", w2[0], w2[1], px + dx * u * 1.1 + dy * u * 0.08,
                      py + dy * u * 1.1 - dx * u * 0.08, nose[0], nose[1]),
                     ("Z",)], (44, 50, 66))
        C.line(px - dx * u * 0.9, py - dy * u * 0.9, px + dx * u * 1.4,
               py + dy * u * 1.4, (120, 130, 150), 1)
        C.circle(px + dx * u * 0.7, py + dy * u * 0.7, u * 0.18,
                 (150, 200, 240))
    for fy in (0.32, 0.52, 0.72):
        ay = y + h * fy
        mx = x + w * (0.4 - 0.04 * math.sin(fy * math.pi))
        C.line(mx - w * 0.06, ay, mx + w * 0.06, ay, (220, 70, 60), 3)
        C.polygon([(mx + w * 0.06, ay), (mx + w * 0.04, ay - 5),
                   (mx + w * 0.04, ay + 5)], (220, 70, 60))
    ccx, ccy = x + w * 0.93, y + h * 0.12
    C.circle(ccx, ccy, 16, WHITE)
    C.ring(ccx, ccy, 16, NAVY, 2)
    C.polygon([(ccx, ccy - 13), (ccx + 4, ccy), (ccx - 4, ccy)], RED)
    C.polygon([(ccx, ccy + 13), (ccx + 4, ccy), (ccx - 4, ccy)], NAVY)
    C.text_center(ccx, ccy - 20, "N", M.SANSB, M.SANSB_EM, M.SANSB_ASC,
                  11, NAVY)


p1_nz(24, 24, 976, 300)
label(24, 348, "P1 REFINED T1 — NEW ZEALAND ELECTION DEADLOCK")
p2_electron(24, 360, 976, 300)
label(24, 684, "P2 REFINED T1 — ELECTRON NIGHT LAUNCH")
p3_taiwan(24, 696, 976, 300)
label(24, 1020, "P3 REFINED T1 — TAIWAN VOTES AS JETS CIRCLE")

out = os.environ.get("PROTO3_OUT", "/tmp/proto3-sheet.png")
with open(out, "wb") as f:
    f.write(M.png_bytes(C.downsample()))
print("wrote", out)
