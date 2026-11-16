"""EVERYONE JUMPS AT ONCE - knowledge reel. Usage: scenes.py still t.. | render a b out"""
import cairo, math, sys, json, random, subprocess
sys.path.insert(0, "/home/claude/sf")
from flat import *
B = "/home/claude/kb/hole/"; FPS = 30
TL = json.load(open(B + "timeline.json")); LINES = TL["lines"]; TOTAL = TL["total"] + 0.4
T0 = lambda i: LINES[i]["t0"]; T1 = lambda i: LINES[i]["t1"]
def WORD(i, w, n=1, d=None):
    hits = [t for x, t in LINES[i]["words"] if x.lower().strip(".,?!:…$") == w]
    return hits[n - 1] if len(hits) >= n else (T0(i) + (d if d is not None else 0))
def tw(t, a, dur=0.3): return clamp((t - a) / dur)
STEEL = (0.62, 0.66, 0.72); STEEL_D = (0.38, 0.42, 0.5); STEEL_L = (0.86, 0.89, 0.93)
GREEN = (0.16, 0.68, 0.38); BLUE = (0.18, 0.46, 0.86); AMBER = (1.0, 0.66, 0.1); DARK = (0.12, 0.14, 0.2)
CARC = (0.9, 0.91, 0.94); CWC = (0.3, 0.33, 0.4)
# ------------------------------------------------------------------ 3D-style primitives
def lgrad(c, x0, y0, x1, y1, c0, c1):
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgb(0, *c0); g.add_color_stop_rgb(1, *c1); return g
def box3d(c, x, y, w, h, d, col, a=1.0):
    dx, dy = d * 0.6, -d * 0.4
    poly(c, [(x, y), (x + dx, y + dy), (x + w + dx, y + dy), (x + w, y)], mix(col, WHITE, 0.35), a)
    poly(c, [(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + h + dy), (x + w, y + h)], mix(col, INK, 0.35), a)
    c.new_path(); c.rectangle(x, y, w, h); g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgba(0, *mix(col, WHITE, 0.12), a); g.add_color_stop_rgba(1, *mix(col, INK, 0.12), a); c.set_source(g); c.fill()
def mline(c, pts, w, col=STEEL, a=1.0):
    line(c, pts, w, mix(col, INK, 0.25), a, cap=cairo.LINE_CAP_BUTT); line(c, [(x - w * 0.18, y) for x, y in pts], w * 0.3, mix(col, WHITE, 0.6), a, cap=cairo.LINE_CAP_BUTT)
def rope(c, pts, w=7, col=(0.5, 0.52, 0.56), a=1.0):
    line(c, pts, w, mix(col, INK, 0.3), a); line(c, pts, w * 0.35, mix(col, WHITE, 0.5), a)
def wheel(c, x, y, r, ang, col=STEEL, depth=16, spokes=5, a=1.0):
    ell(c, x + depth * 0.6, y - depth * 0.4, r, r, mix(col, INK, 0.45), a)
    c.new_path(); c.arc(x, y, r, 0, TAU); c.set_source(lgrad(c, x - r, y - r, x + r, y + r, mix(col, WHITE, 0.35), mix(col, INK, 0.3))); c.fill()
    ell(c, x, y, r * 0.78, r * 0.78, mix(col, INK, 0.5), a)
    for k in range(spokes):
        an = ang + k * TAU / spokes; line(c, [(x, y), (x + math.cos(an) * r * 0.8, y + math.sin(an) * r * 0.8)], r * 0.14, mix(col, WHITE, 0.15), a)
    ell(c, x, y, r * 0.22, r * 0.22, mix(col, WHITE, 0.4), a); ell(c, x, y, r * 0.09, r * 0.09, INK, a)
def soft_shadow(c, x, y, rx, ry, a=0.25): glow(c, x, y, rx, (0, 0, 0), a) if rx > 0 else None
def lab(c, x, y, s, col=INK, a=1.0, size=34, bg=WHITE):
    if a <= 0: return
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size); w = c.text_extents(s).x_advance + 40
    k = back(a); c.save(); c.translate(x, y); c.scale(k, k); shadow_rr(c, -w / 2, -size * 0.85, w, size * 1.7, size * 0.55, bg, min(1, a * 2)); txt(c, s, 0, 0, size, col, a=min(1, a * 2)); c.restore()
def chip(c, s, col, y=1330, a=1.0, size=52, x=540):
    if a <= 0: return
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size); w = c.text_extents(s).x_advance + 80
    k = back(a); c.save(); c.translate(x, y); c.scale(k, k); shadow_rr(c, -w / 2, -size * 0.9, w, size * 1.8, size * 0.6, col, min(1, a * 2)); txt(c, s, 0, 0, size, WHITE, a=min(1, a * 2)); c.restore()
def arrow(c, x0, y0, x1, y1, col, w=12, a=1.0):
    an = math.atan2(y1 - y0, x1 - x0); hl = w * 2.6
    line(c, [(x0, y0), (x1 - math.cos(an) * hl * 0.6, y1 - math.sin(an) * hl * 0.6)], w, col, a)
    poly(c, [(x1, y1), (x1 - math.cos(an - 0.5) * hl, y1 - math.sin(an - 0.5) * hl), (x1 - math.cos(an + 0.5) * hl, y1 - math.sin(an + 0.5) * hl)], col, a)
def sparks(c, x, y, t, n=14, r=90, seed=1, a=1.0):
    R = random.Random(seed + int(t * 24))
    for _ in range(n):
        an = R.uniform(0, TAU); l0 = R.uniform(8, r * 0.4); l1 = l0 + R.uniform(15, r * 0.6)
        line(c, [(x + math.cos(an) * l0, y + math.sin(an) * l0), (x + math.cos(an) * l1, y + math.sin(an) * l1)], R.uniform(3, 6), mix(AMBER, WHITE, R.random() * 0.6), a)
    glow(c, x, y, r * 0.8, (1, 0.8, 0.3), 0.5 * a)
def cross(c, x, y, r, col=RED, w=14, a=1.0): line(c, [(x - r, y - r), (x + r, y + r)], w, col, a); line(c, [(x + r, y - r), (x - r, y + r)], w, col, a)
def check(c, x, y, r, a=1.0): ell(c, x, y, r, r, GREEN, a); line(c, [(x - r * 0.45, y), (x - r * 0.1, y + r * 0.35), (x + r * 0.5, y - r * 0.35)], r * 0.24, WHITE, a)
def bolt(c, x, y, s, col=AMBER, a=1.0): poly(c, [(x + 10 * s, y - 40 * s), (x - 22 * s, y + 6 * s), (x - 2 * s, y + 6 * s), (x - 12 * s, y + 40 * s), (x + 24 * s, y - 8 * s), (x + 4 * s, y - 8 * s)], col, a)
def studio(c, top=(0.9, 0.93, 0.97), bot=(0.72, 0.79, 0.9)):
    c.save(); c.identity_matrix(); vgrad(c, 0, H, top, bot); glow(c, 540, 850, 900, WHITE, 0.45 if top[0] > 0.5 else 0.08); c.restore()
def sv(c): c.save(); c.translate(540, 450); c.scale(1.2, 1.2); c.translate(-540, -306)
CHY = 1500
