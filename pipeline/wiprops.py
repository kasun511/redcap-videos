# ------------------------------------------------------------------ space / sun props
SKYD = (0.03, 0.04, 0.09); SKYD2 = (0.01, 0.01, 0.03)
DAY0 = (0.35, 0.66, 0.96); DAY1 = (0.82, 0.92, 1.0)
SUNC = (1.0, 0.86, 0.3); EARTHB = (0.2, 0.55, 0.9); EARTHG = (0.35, 0.72, 0.4)
ICE = (0.75, 0.92, 1.0)
def SS(c, k):
    k = max(abs(k), 2e-3); c.scale(k, k)
def lab(c, x, y, s, col=INK, a=1.0, size=34, bg=WHITE):
    if a <= 0: return
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size); w = c.text_extents(s).x_advance + 40
    k = back(a); c.save(); c.translate(x, y); SS(c, k); shadow_rr(c, -w / 2, -size * 0.85, w, size * 1.7, size * 0.55, bg, min(1, a * 2)); txt(c, s, 0, 0, size, col, a=min(1, a * 2)); c.restore()
def bigtxt(c, s, y, size, col, t, at, a=1.0, x=540):
    if t < at: return
    k = back(clamp((t - at) / 0.3)); c.save(); c.translate(x, y); SS(c, k); txt(c, s, 0, 0, size, col, stroke=10, a=a); c.restore()
def starfield(c, t, a=1.0, n=90, seed=7):
    R = random.Random(seed)
    for k in range(n):
        x = R.uniform(0, W); y = R.uniform(0, 1700); r = R.uniform(1.6, 4.2)
        tw = 0.55 + 0.45 * math.sin(t * R.uniform(1.0, 3.0) + k)
        ell(c, x, y, r, r, WHITE, a * tw)
def space(c, t, a=1.0):
    c.save(); c.identity_matrix(); vgrad(c, 0, H, SKYD, SKYD2); starfield(c, t, a); c.restore()
def daysky(c, t, k=0.0):
    """k = 0 day, 1 fully dark"""
    c.save(); c.identity_matrix()
    vgrad(c, 0, H, mix(DAY0, SKYD, k), mix(DAY1, SKYD2, k))
    if k > 0.25: starfield(c, t, (k - 0.25) / 0.75)
    c.restore()
def ground(c, k=0.0, snow=0.0):
    col = mix(mix((0.42, 0.66, 0.34), (0.16, 0.2, 0.22), k), ICE, snow)
    rect(c, 0, 1640, W, H - 1640, col); rect(c, 0, 1640, W, 16, mix(col, INK, 0.25))
def sunball(c, x, y, r, t, a=1.0, flare=1.0):
    if a <= 0: return
    glow(c, x, y, r * (2.4 + 0.25 * math.sin(t * 2)), (1, 0.75, 0.2), 0.5 * a * flare)
    ell(c, x, y, r, r, SUNC, a)
    ell(c, x - r * 0.25, y - r * 0.25, r * 0.5, r * 0.5, (1, 0.96, 0.7), 0.5 * a)
    for k in range(12):
        an = k * TAU / 12 + t * 0.4; L = r * (1.25 + 0.14 * math.sin(t * 5 + k))
        line(c, [(x + math.cos(an) * r * 1.02, y + math.sin(an) * r * 1.02), (x + math.cos(an) * L, y + math.sin(an) * L)], r * 0.13, SUNC, a * 0.9 * flare)
def earthball(c, x, y, r, t, a=1.0, ice=0.0, lit=1.0):
    ell(c, x, y, r, r, mix(EARTHB, (0.1, 0.16, 0.3), 1 - lit), a)
    c.save(); c.new_path(); c.arc(x, y, r, 0, TAU); c.clip()
    for k, (dx, dy, rx, ry) in enumerate([(-0.5, -0.3, 0.38, 0.3), (0.3, 0.15, 0.32, 0.42), (-0.2, 0.55, 0.26, 0.22), (0.62, -0.58, 0.24, 0.18)]):
        ox = ((dx + t * 0.1 + 1.6) % 3.2) - 1.6
        ell(c, x + ox * r, y + dy * r, rx * r, ry * r, mix(mix(EARTHG, (0.12, 0.18, 0.16), 1 - lit), ICE, ice), a)
    if ice > 0:
        ell(c, x, y - r * 0.95, r * 0.8, r * 0.42, ICE, a * ice); ell(c, x, y + r * 0.95, r * 0.8, r * 0.42, ICE, a * ice)
    c.restore()
    if lit > 0.2: glow(c, x - r * 0.3, y - r * 0.3, r * 0.95, WHITE, 0.16 * a * lit)
def planet(c, x, y, r, col, t, a=1.0, ring=False):
    ell(c, x, y, r, r, col, a)
    ell(c, x - r * 0.3, y - r * 0.3, r * 0.45, r * 0.45, mix(col, WHITE, 0.4), a * 0.5)
    if ring:
        c.save(); c.translate(x, y); c.rotate(-0.4); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, r * 1.9, 0, TAU)
        c.set_line_width(r * 0.42); c.set_source_rgba(*mix(col, WHITE, 0.45), a * 0.9); c.stroke(); c.restore()
def moonball(c, x, y, r, t, a=1.0):
    ell(c, x, y, r, r, (0.82, 0.82, 0.86), a)
    R = random.Random(3)
    for k in range(6):
        an = R.uniform(0, TAU); d = R.uniform(0.1, 0.62) * r
        ell(c, x + math.cos(an) * d, y + math.sin(an) * d, r * R.uniform(0.08, 0.17), r * R.uniform(0.08, 0.17), (0.66, 0.66, 0.72), a)
def raybeam(c, x0, y0, x1, y1, u, a=1.0, w=16):
    """light front travelling from sun to earth, u in 0..1"""
    xe = x0 + (x1 - x0) * u; ye = y0 + (y1 - y0) * u
    line(c, [(x0, y0), (xe, ye)], w, SUNC, 0.75 * a)
    glow(c, xe, ye, 70, SUNC, 0.8 * a); ell(c, xe, ye, 16, 16, WHITE, a)
def clockface(c, x, y, r, s, a=1.0, col=WHITE):
    if a <= 0: return
    k = back(a); c.save(); c.translate(x, y); SS(c, k)
    c.new_path(); c.arc(0, 0, r, 0, TAU); c.set_source_rgba(0.08, 0.09, 0.13, 0.96); c.fill()
    c.new_path(); c.arc(0, 0, r, 0, TAU); c.set_line_width(10); c.set_source_rgba(*col, 1); c.stroke()
    txt(c, s, 0, 4, r * 0.62, col); c.restore()
def therm(c, x, y, h, lvl, s, col, a=1.0):
    """vertical thermometer; lvl 0..1 from the bottom"""
    rr(c, x - 34, y - h, 68, h + 40, 34, WHITE, a)
    rr(c, x - 16, y - h * lvl - 10, 32, h * lvl + 40, 16, col, a); ell(c, x, y + 36, 46, 46, col, a)
    txt(c, s, x + 110, y - h * 0.55, 62, col, stroke=8, a=a)
def leaf(c, x, y, s, t, dead=0.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s); c.rotate(0.45 * dead + 0.05 * math.sin(t * 1.6))
    col = mix((0.28, 0.72, 0.34), (0.46, 0.33, 0.14), dead)
    c.new_path(); c.move_to(0, 80)
    c.curve_to(-78, 20, -72, -70, 0, -120); c.curve_to(72, -70, 78, 20, 0, 80); c.close_path()
    c.set_source_rgba(*col, a); c.fill()
    line(c, [(0, 80), (0, -110)], 7, mix(col, INK, 0.35), a)
    for k in range(4):
        yy = 46 - k * 42; w_ = 56 - k * 9
        line(c, [(0, yy), (-w_, yy - 26)], 5, mix(col, INK, 0.3), a * 0.85)
        line(c, [(0, yy), (w_, yy - 26)], 5, mix(col, INK, 0.3), a * 0.85)
    c.restore()
def arrowline(c, x0, y0, x1, y1, col, w=12, a=1.0):
    an = math.atan2(y1 - y0, x1 - x0); hl = w * 2.6
    line(c, [(x0, y0), (x1 - math.cos(an) * hl * 0.6, y1 - math.sin(an) * hl * 0.6)], w, col, a)
    poly(c, [(x1, y1), (x1 - math.cos(an - 0.5) * hl, y1 - math.sin(an - 0.5) * hl), (x1 - math.cos(an + 0.5) * hl, y1 - math.sin(an + 0.5) * hl)], col, a)
def oceanslab(c, t, y, k=0.0, ice=0.0):
    """cross-section of sea with warm glow below"""
    rect(c, 90, y, 900, 300, mix((0.12, 0.38, 0.68), (0.07, 0.2, 0.4), k))
    for q in range(5):
        yy = y + 40 + q * 56
        line(c, [(110 + 20 * math.sin(t * 1.2 + q), yy), (970, yy)], 7, (0.22, 0.55, 0.88), 0.5)
    if ice > 0: rect(c, 90, y, 900, 56 * ice, ICE)
    rect(c, 90, y + 300, 900, 70, (0.5, 0.4, 0.26))
    for q in range(6): glow(c, 170 + q * 140, y + 250, 120, (1, 0.5, 0.2), 0.22)
# ------------------------------------------------------------------ shared What-If extras
def chipx(c, s, col, y=1330, a=1.0, size=52, x=540):
    chip(c, s, col, y, a, size, x)
def crowdrow(c, y, n, t, s=0.5, jump=0.0, a=1.0, seed=1, cols=None):
    R = random.Random(seed)
    cols = cols or [(0.2, 0.45, 0.8), (0.75, 0.3, 0.3), (0.25, 0.6, 0.4), (0.8, 0.6, 0.2), (0.5, 0.35, 0.7)]
    for k in range(n):
        x = 60 + (W - 120) * (k + 0.5) / n + R.uniform(-10, 10)
        hop = abs(math.sin(t * 2.2 + R.uniform(0, 3))) * 90 * jump
        col = cols[k % len(cols)]
        c.save(); c.translate(x, y - hop); SS(c, s)
        rr(c, -26, -96, 52, 104, 20, col, a); ell(c, 0, -126, 30, 30, (0.95, 0.8, 0.65), a)
        rect(c, -22, 4, 18, 54, (0.2, 0.22, 0.3), a); rect(c, 6, 4, 18, 54, (0.2, 0.22, 0.3), a)
        c.restore()
def scalebar(c, x, y, w, h, frac, col, label, sub, a=1.0):
    rr(c, x, y, w, h, 18, (0.16, 0.17, 0.22), a)
    hh = max(h * clamp(frac), 18)
    rr(c, x, y + h - hh, w, hh, 18, col, a)
    txt(c, label, x + w / 2, y + h + 54, 40, WHITE, stroke=6, a=a)
    txt(c, sub, x + w / 2, y + h + 100, 30, (0.78, 0.8, 0.86), a=a)
def seismo(c, x, y, w, h, t, amp=1.0, a=1.0):
    shadow_rr(c, x - w / 2, y - h / 2, w, h, 24, (0.1, 0.11, 0.15), a)
    pts = []
    R = random.Random(5)
    for k in range(80):
        u = k / 79; v = math.sin(u * 40 + t * 6) * R.uniform(0.2, 1.0)
        env = math.exp(-abs(u - 0.5) * 6) if amp > 0 else 0
        pts.append((x - w / 2 + 20 + (w - 40) * u, y + v * env * h * 0.42 * amp))
    line(c, pts, 6, (0.3, 1.0, 0.55), a)
def quakeicon(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    for k in range(3):
        rr_ = 60 + k * 50; ph = (t * 1.2 + k / 3) % 1
        c.new_path(); c.arc(0, 0, rr_ * (0.7 + ph * 0.6), -2.4, -0.74); c.set_line_width(12); c.set_source_rgba(*RED, a * (1 - ph)); c.stroke()
    ell(c, 0, 0, 26, 26, RED, a); c.restore()
def tiny_earth_move(c, x, y, r, t, off, a=1.0):
    earthball(c, x + off, y, r, t, a)
def pan(c, x, y, s, t, hot=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -150, -40, 300, 80, 26, (0.22, 0.24, 0.3), a); rr(c, 140, -22, 190, 42, 20, (0.3, 0.32, 0.38), a)
    if hot > 0:
        for k in range(4):
            ph = (t * 0.9 + k / 4) % 1
            ell(c, -80 + k * 55, -60 - 110 * ph, 20 + 24 * ph, 18 + 22 * ph, (0.95, 0.85, 0.75), 0.45 * (1 - ph) * hot * a)
        glow(c, 0, -10, 190, (1, 0.5, 0.2), 0.35 * hot * a)
    c.restore()
def alarmbell(c, x, y, s, t, a=1.0, ring=1.0):
    c.save(); c.translate(x, y); SS(c, s); c.rotate(0.22 * math.sin(t * 16) * ring)
    poly(c, [(-70, 40), (-50, -40), (50, -40), (70, 40)], GOLD, a); rr(c, -82, 36, 164, 26, 12, GOLD, a)
    ell(c, 0, -52, 18, 18, GOLD, a); ell(c, 0, 72, 18, 18, GOLD, a)
    if ring > 0:
        for sd in (-1, 1):
            for k in range(2):
                c.new_path(); c.arc(sd * 110, 0, 40 + k * 34, -0.9 if sd > 0 else 2.24, 0.9 if sd > 0 else 4.04)
                c.set_line_width(9); c.set_source_rgba(*GOLD, a * ring * (0.8 - k * 0.3)); c.stroke()
    c.restore()
def cellsplit(c, x, y, r, t, burst=0.0, a=1.0):
    if burst < 1:
        ell(c, x, y, r * (1 + 0.5 * burst), r * (1 + 0.5 * burst), (0.95, 0.55, 0.5), a)
        ell(c, x, y, r * 0.42, r * 0.42, (0.7, 0.25, 0.3), a)
    if burst > 0:
        for k in range(10):
            an = k * TAU / 10; d = r * (1 + 3.0 * burst)
            ell(c, x + math.cos(an) * d, y + math.sin(an) * d, 12 * (1 - burst) + 4, 12 * (1 - burst) + 4, (0.95, 0.55, 0.5), a * (1 - burst))
def fish(c, x, y, s, t, col=(0.4, 0.62, 0.85), a=1.0, dead=0.0, face=1):
    c.save(); c.translate(x, y); SS(c, s); c.scale(face, 1 if dead < 0.5 else -1)
    poly(c, [(-70, 0), (-120, -40), (-120, 40)], mix(col, INK, 0.2), a)
    ell(c, 0, 0, 78, 46, col, a); ell(c, 10, 8, 56, 28, mix(col, WHITE, 0.5), a)
    poly(c, [(-10, -42), (20, -86), (36, -40)], mix(col, INK, 0.15), a)
    if dead > 0.5:
        line(c, [(42, -16), (62, 4)], 5, INK, a); line(c, [(62, -16), (42, 4)], 5, INK, a)
    else:
        ell(c, 52, -10, 9, 9, INK, a)
    c.restore()
def conveyor(c, t, a=1.0, on=1.0):
    pts = [(120, 1180), (330, 1080), (620, 1180), (900, 1060), (960, 1240), (640, 1340), (300, 1280), (120, 1180)]
    line(c, pts, 16, (0.25, 0.5, 0.85), 0.45 * a)
    if on > 0:
        for k in range(8):
            ph = (t * 0.25 * on + k / 8) % 1; seg = ph * (len(pts) - 1); i = int(seg); f = seg - i
            x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
            ell(c, x, y, 15, 15, mix(BLUE, RED, 0.5 - 0.5 * math.cos(ph * TAU)), a)
def cal(c, x, y, s, label, sub, t, a=1.0, col=None):
    c.save(); c.translate(x, y); SS(c, s)
    shadow_rr(c, -130, -150, 260, 300, 28, (0.96, 0.96, 0.98), a); rr(c, -130, -150, 260, 72, 28, col or RED, a)
    txt(c, label, 0, 20, 86, INK, a=a); txt(c, sub, 0, -108, 36, WHITE, a=a); c.restore()
def dna(c, x, y, h, t, a=1.0, broken=0.0):
    for k in range(14):
        u = k / 13; yy = y - h / 2 + h * u; ph = u * 7 + t * 1.2
        x1 = x + math.sin(ph) * 70; x2 = x - math.sin(ph) * 70
        line(c, [(x1, yy), (x2, yy)], 6, mix((0.5, 0.8, 1.0), (0.6, 0.6, 0.65), broken), a * (1 - broken * (0.6 if k % 3 else 0)))
        ell(c, x1, yy, 11, 11, (0.3, 0.7, 1.0), a); ell(c, x2, yy, 11, 11, (1.0, 0.5, 0.6), a)
def W_(i, w, d=None):
    return WORD(i, w, 1, d)
