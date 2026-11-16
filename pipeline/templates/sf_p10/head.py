"""THE SOLAR FLASH · Ep 10 "Eleven Days". Usage: scenes.py still t.. | render a b out"""
import cairo, math, sys, json, random, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/sf")
from flat import *
import importlib.util as _iu
def _load(name, path):
    sp = _iu.spec_from_file_location(name, path); m = _iu.module_from_spec(sp); sp.loader.exec_module(m); return m
P1 = _load("ep1s", "/home/claude/sf/p1/scenes.py"); O = _load("ep2s", "/home/claude/sf/p2/scenes.py"); P3 = _load("ep3s", "/home/claude/sf/p3/scenes.py")
B = "/home/claude/sf/p10/"; FPS = 30
TL = json.load(open(B + "timeline.json")); LINES = TL["lines"]; TOTAL = TL["total"] + 0.4
NIDX = {e["i"]: k for k, e in enumerate(LINES) if e["who"] == "nar"}
T0 = lambda i: LINES[NIDX[i]]["t0"]; T1 = lambda i: LINES[NIDX[i]]["t1"]
def WORD(i, w, n=1):
    hits = [t for x, t in LINES[NIDX[i]]["words"] if x.lower().strip(".,?!:…$") == w]
    return hits[n - 1] if len(hits) >= n else T0(i)
def env_of(path):
    m, sr = sf.read(path); f = sr // FPS
    e = np.array([np.sqrt(np.mean(m[i * f:(i + 1) * f] ** 2)) if (i + 1) * f <= len(m) else 0 for i in range(int(len(m) / f) + 2)]); return e / (e.max() + 1e-9)
MENV = env_of(B + "vo_mia.wav")
def mtalk(t): i = int(t * FPS); v = float(MENV[i]) if i < len(MENV) else 0; return clamp((v - 0.06) * 2.2) * (0.7 + 0.3 * math.sin(t * 38))
MIAS = [e for e in LINES if e["who"] == "mia"]; MIA = [m["t0"] for m in MIAS]
hillscape = P3.hillscape; interior = P3.interior; label = P3.label; chip = P3.chip; section = P3.section
excavator = P1.excavator; crane = P1.crane; mixer_truck = P1.mixer_truck; namecard = P1.namecard; clock = O.clock
GREEN = (0.18, 0.66, 0.36); BLUE = (0.2, 0.45, 0.8); CONC = (0.62, 0.62, 0.6); CONC2 = (0.5, 0.5, 0.48)
STEEL = (0.55, 0.58, 0.63); STEEL2 = (0.4, 0.43, 0.48); STEEL3 = (0.7, 0.73, 0.78); SOIL = (0.45, 0.33, 0.23); SOIL2 = (0.38, 0.27, 0.18)
def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k
def W_(i, w, d=0.0): return WORD(i, w) - 0.1 if WORD(i, w) != T0(i) else T0(i) + d
def money(v): return "${:,}".format(int(round(v / 1000) * 1000))
def DAYS(t): return [d for at, d in DAYCHG if t >= at][-1]
FEATS = [("OFF-GRID", T0(2) + 2.5), ("CAGE", T0(3) + 2.5), ("ARRESTORS", T0(4) + 2.5), ("WATER", T0(5) + 2.0), ("STOCKED", T0(6) + 2.0), ("SURVIVED", T0(9) + 2.0)]
def feature_bar(c, t):
    n = len(FEATS); x0 = 40; w = (W - 80 - (n - 1) * 10) / n
    for k, (lab, at) in enumerate(FEATS):
        x = x0 + k * (w + 10); on = t >= at; u = clamp((t - at) / 0.35); s = 1 + 0.25 * (1 - u) * (1 if on else 0)
        c.save(); c.translate(x + w / 2, 1640); c.scale(s, s); c.translate(-(x + w / 2), -1640)
        rr(c, x, 1614, w, 52, 16, GREEN if on else (0.16, 0.16, 0.2), 0.95); txt(c, lab, x + w / 2, 1640, 22, WHITE if on else (0.55, 0.55, 0.6)); c.restore()
def hud(c, t, feats=True):
    bud = START_BUDGET; pop = None; pb = 0.0
    for at, dv, a, b in EV:
        if t > at: bud += dv * ease(clamp((t - at) / 0.7)); pop = (a, b, (0.85, 0.25, 0.22), (t - at) / 2.8); pb = max(0.0, 1 - (t - at) / 0.35)
    d = DAYS(t); pd = 0.0
    for at, _ in DAYCHG[1:]:
        if 0 <= t - at < 0.35: pd = 1 - (t - at) / 0.35
    ui_counters(c, d, money(bud), pulse_d=pd, pulse_b=pb, days_frac=d / 365)
    if pop: ui_pop(c, pop[0], pop[1], pop[2], pop[3])
    if feats: feature_bar(c, t)
def fixcard(c, t, at, what):
    u = clamp((t - at) / 0.3); k = back(u)
    c.save(); c.translate(540, 600); c.scale(k, k); c.translate(-540, -600); chip(c, "FIX: " + what, GREEN, 600, 1.0, 44); c.restore()
def shake(c, amt, t):
    if amt > 0: c.translate(amt * math.sin(t * 53), amt * math.cos(t * 41))
def ground_section(c, t, k=0.0):
    vgrad(c, 0, 900, mix((0.55, 0.78, 0.95), (0.05, 0.06, 0.14), k), mix((0.85, 0.92, 0.98), (0.1, 0.12, 0.22), k))
    rect(c, 0, 880, W, 30, mix((0.42, 0.62, 0.32), (0.14, 0.2, 0.12), k)); rect(c, 0, 910, W, H - 910, SOIL)
    for j in range(14): line(c, [(0, 950 + j * 70), (W, 950 + j * 70 + 8 * math.sin(j))], 3, SOIL2, 0.5)
BW0, BW1, BT, BB = 620, 1080, 1180, 1460   # bunker wall in side section: wall face at x=620
