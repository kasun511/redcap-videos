"""Flat vector style kit for THE SOLAR FLASH (no outlines, soft flat colours)."""
import cairo, math, random
from fontTools.ttLib import TTFont as _TT
W, H = 1080, 1920; TAU = 2 * math.pi
_CMAP = set(_TT("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf").getBestCmap())
WHITE = (1, 1, 1); INK = (0.08, 0.08, 0.1); GOLD = (1, 0.78, 0.25); RED = (0.9, 0.22, 0.2); ORANGE = (1, 0.55, 0.15)
SKIN = (1.0, 0.84, 0.70); HOOD = (0.16, 0.36, 0.55); HOOD2 = (0.12, 0.28, 0.44); JEAN = (0.18, 0.2, 0.3); CAP = (0.86, 0.16, 0.16); CAP2 = (0.72, 0.1, 0.1); HAIR = (0.35, 0.22, 0.14)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(lerp(a, b, t) for a, b in zip(c1, c2))
def ease(t): t = clamp(t); return 1 - (1 - t) ** 3
def eio(t): t = clamp(t); return t * t * (3 - 2 * t)
def back(t): t = clamp(t); s = 1.7; t -= 1; return t * t * ((s + 1) * t + s) + 1
def rr(c, x, y, w, h, r, col, a=1.0):
    r = min(r, w / 2, h / 2); c.new_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path(); c.set_source_rgba(*col, a); c.fill()
def rect(c, x, y, w, h, col, a=1.0): c.new_path(); c.rectangle(x, y, w, h); c.set_source_rgba(*col, a); c.fill()
def ell(c, x, y, rx, ry, col, a=1.0):
    if rx <= 0 or ry <= 0: return
    c.save(); c.translate(x, y); c.scale(rx, ry); c.new_path(); c.arc(0, 0, 1, 0, TAU); c.restore(); c.set_source_rgba(*col, a); c.fill()
def poly(c, pts, col, a=1.0):
    c.new_path(); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); c.set_source_rgba(*col, a); c.fill()
def line(c, pts, w, col, a=1.0, cap=cairo.LINE_CAP_ROUND):
    c.new_path(); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.set_line_width(w); c.set_line_cap(cap); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_source_rgba(*col, a); c.stroke()
def glow(c, x, y, r, col, a=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r); g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0); c.new_path(); c.arc(x, y, r, 0, TAU); c.set_source(g); c.fill()
def vgrad(c, y0, y1, c0, c1, x0=0, x1=W):
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *c0); g.add_color_stop_rgb(1, *c1); c.new_path(); c.rectangle(x0, y0, x1 - x0, y1 - y0); c.set_source(g); c.fill()
def txt(c, s, x, y, size, col, anchor="c", stroke=0, a=1.0, font="Poppins", bold=True):
    if font == "Poppins" and any(ord(ch) not in _CMAP for ch in s if not ch.isspace()): font = "DejaVu Sans"
    c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
    e = c.text_extents(s); fe = c.font_extents(); dx = {"c": -e.width / 2 - e.x_bearing, "l": -e.x_bearing, "r": -e.width - e.x_bearing}[anchor]
    c.new_path(); c.move_to(x + dx, y + (fe[0] - fe[1]) / 2 - 2); c.text_path(s)
    if stroke: c.set_source_rgba(*INK, a); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    c.set_source_rgba(*col, a); c.fill(); return e.width
# ------------------------------------------------------------------ character
def limb(c, x0, y0, ang, L, w, col, hand=None, hcol=SKIN):
    x1, y1 = x0 + math.sin(ang) * L, y0 + math.cos(ang) * L
    line(c, [(x0, y0), (x1, y1)], w, col)
    if hand: ell(c, x1, y1, hand, hand, hcol)
    return x1, y1
def redcap(c, x, y, s=1.0, face=1, t=0.0, mode="stand", mood="calm", look=0.0, talk=0.0, blink=True, hold=None, phase=0.0, alpha=1.0):
    """face: 1 right / -1 left / 0 front. y = feet. mode: stand, walk, point_down, phone, torch, scared, shrug."""
    if alpha < 1: c.push_group()
    c.save(); c.translate(x, y); c.scale(s, s)
    br = math.sin(t * 2.2 + phase) * 3
    sw = math.sin(t * 7 + phase) if mode == "walk" else 0.0
    bob = -abs(math.sin(t * 7 + phase)) * 8 if mode == "walk" else 0.0
    c.translate(0, bob)
    fx = face if face != 0 else 1
    # legs
    hip = -150
    for k, side in enumerate((-1, 1)):
        a = sw * 0.45 * (1 if k else -1)
        lx = side * 24
        kx, ky = limb(c, lx, hip, a, 140, 42, JEAN)
        rr(c, kx - 30 + (8 * fx if face else 0), ky - 14, 60, 26, 12, (0.96, 0.96, 0.96))
    # body
    tilt = 0.06 * fx if mode == "scared" else 0
    c.save(); c.translate(0, hip); c.rotate(tilt)
    rr(c, -70, -190 + br, 140, 210, 42, HOOD)
    if face == 0: rr(c, -40, -90 + br, 80, 48, 18, HOOD2)
    else: rr(c, -20 + 15 * fx, -90 + br, 50, 48, 16, HOOD2)
    # arms (shoulders)
    shL, shR = (-60, -168 + br), (60, -168 + br)
    def arm(sh, ang, hand_obj=None):
        x1, y1 = limb(c, sh[0], sh[1], ang, 150, 40, HOOD, hand=22)
        return x1, y1
    if mode in ("stand", "walk"):
        aL, aR = 0.18 + sw * 0.5, -0.18 - sw * 0.5
    elif mode == "point_down": aL, aR = 0.15, -0.6
    elif mode == "phone": aL, aR = 0.15, -2.4
    elif mode == "torch": aL, aR = 0.15, -1.75
    elif mode == "scared": aL, aR = 2.6 + 0.08 * math.sin(t * 20), -2.6 - 0.08 * math.sin(t * 20)
    elif mode == "shrug": aL, aR = 1.2, -1.2
    else: aL, aR = 0.18, -0.18
    if face == -1: aL, aR = -aR, -aL
    pL = arm(shL, aL); pR = arm(shR, aR)
    hp = pR if fx > 0 else pL
    if mode == "phone":
        rr(c, hp[0] - 28, hp[1] - 70, 56, 96, 10, INK); rr(c, hp[0] - 22, hp[1] - 62, 44, 80, 6, hold or (0.95, 0.25, 0.25))
    if mode == "torch":
        rr(c, hp[0] - 12 * fx - 8, hp[1] - 14, 46 if fx > 0 else 46, 26, 8, (0.3, 0.3, 0.33))
    c.restore()
    # head
    hy = hip - 190 - 88 + br * 1.2
    c.save(); c.translate(look * 6 * fx, hy)
    if mode == "scared": c.translate(2 * math.sin(t * 40), 0)
    ell(c, 0, 0, 84, 90, SKIN)
    if face == 0:
        ell(c, -84, 4, 14, 20, SKIN); ell(c, 84, 4, 14, 20, SKIN)
    else:
        ell(c, -50 * fx, 8, 14, 20, SKIN)
    c.new_path(); c.arc(0, -8, 86, math.pi * 1.02, math.pi * 1.98); c.close_path(); c.set_source_rgb(*HAIR); c.fill()
    c.new_path(); c.arc(0, -26, 88, math.pi, TAU); c.close_path(); c.set_source_rgb(*CAP); c.fill()
    rr(c, -100, -40, 200, 22, 11, CAP2)
    if face == 0: rr(c, -150, -48, 70, 20, 10, CAP2)
    else: rr(c, -170 * fx if fx > 0 else 100, -46, 70, 20, 10, CAP2)
    ell(c, 0, -112, 12, 8, CAP2)
    # face
    ex = 12 * fx if face else 0; open_ = 1.0
    if blink and (t * 1.0 + phase) % 3.7 < 0.12: open_ = 0.12
    eyr = 12 if mood != "scared" else 15
    for sx in (-29, 30):
        ell(c, sx + ex, 10, 9 if mood != "scared" else 11, eyr * open_, INK)
        if open_ > 0.5: ell(c, sx + ex + 3, 6, 3, 3, WHITE)
    c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if mood in ("worried", "scared"):
        c.move_to(-46 + ex, -16); c.line_to(-14 + ex, -24); c.move_to(48 + ex, -16); c.line_to(16 + ex, -24); c.stroke()
    my = 52
    if talk > 0.05: ell(c, 2 + ex, my, 16, 6 + 12 * talk, (0.45, 0.12, 0.12))
    elif mood == "happy": c.new_path(); c.arc(2 + ex, my - 16, 18, 0.2, math.pi - 0.2); c.stroke()
    elif mood == "scared": ell(c, 2 + ex, my, 12, 15, (0.45, 0.12, 0.12))
    elif mood == "worried": c.new_path(); c.arc(2 + ex, my + 12, 14, math.pi * 1.15, math.pi * 1.85); c.stroke()
    else: line(c, [(-10 + ex, my), (14 + ex, my)], 5, INK)
    ell(c, -48 + ex, 34, 12, 7, (1, 0.6, 0.6), 0.5); ell(c, 50 + ex, 34, 12, 7, (1, 0.6, 0.6), 0.5)
    if mood == "scared": ell(c, 70 * fx, -30, 6, 10, (0.6, 0.85, 1.0), 0.9)
    c.restore(); c.restore()
    if alpha < 1: c.pop_group_to_source(); c.paint_with_alpha(alpha)
def anchor(c, x, y, s, t, talk=0.0):
    """News anchor at a desk, chest-up (y = desk top)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -110, -170, 220, 200, 60, (0.25, 0.25, 0.32))
    poly(c, [(-30, -170), (0, -110), (30, -170)], WHITE)
    ell(c, 0, -250, 70, 78, (0.85, 0.66, 0.52))
    c.new_path(); c.arc(0, -262, 78, math.pi * 0.95, math.pi * 2.05); c.close_path(); c.set_source_rgb(0.15, 0.1, 0.08); c.fill()
    rr(c, -82, -270, 30, 110, 14, (0.15, 0.1, 0.08)); rr(c, 52, -270, 30, 110, 14, (0.15, 0.1, 0.08))
    open_ = 0.12 if (t % 4.1) < 0.12 else 1
    for sx in (-24, 24): ell(c, sx, -250, 7, 10 * open_, INK)
    if talk > 0.05: ell(c, 0, -212, 13, 4 + 9 * talk, (0.5, 0.15, 0.15))
    else: line(c, [(-10, -212), (10, -212)], 4, INK)
    rect(c, -260, 0, 520, 140, (0.12, 0.2, 0.38))
    c.restore()
# ------------------------------------------------------------------ world pieces
def city(c, ground, k=0.0, burn=0.0, seed=1):
    R = random.Random(seed); x = -30
    base = mix((0.55, 0.62, 0.75), (0.6, 0.35, 0.25), k)
    while x < W + 30:
        w = R.randint(120, 200); h = R.randint(350, 720)
        col = mix(base, (0.95, 0.45, 0.15), burn)
        rect(c, x, ground - h, w, h, col)
        for yy in range(int(ground - h + 40), int(ground - 30), 70):
            for xx in range(x + 20, x + w - 30, 45): rect(c, xx, yy, 22, 34, WHITE, 0.25 * (1 - burn) + 0.0)
        x += w + R.randint(-10, 20)
def sky(c, k=0.0, y1=1300):
    """k: 0 blue day -> 1 burning orange."""
    vgrad(c, 0, y1, mix((0.55, 0.78, 0.95), (0.95, 0.45, 0.15), k), mix((0.85, 0.92, 0.98), (1.0, 0.8, 0.45), k))
def sun(c, x, y, r, t, k=0.0):
    p = 1 + 0.04 * math.sin(t * 3)
    glow(c, x, y, r * 2.4 * p, mix((1, 0.9, 0.5), (1, 0.55, 0.1), k), 0.55)
    ell(c, x, y, r * p, r * p, mix((1, 0.9, 0.45), (1, 0.75, 0.3), k))
def ground(c, y, grass=True, k=0.0):
    if grass: rect(c, 0, y, W, 60, mix((0.42, 0.62, 0.32), (0.55, 0.45, 0.2), k))
    rect(c, 0, y + (60 if grass else 0), W, H - y, (0.36, 0.27, 0.2))
def counters(c, days, budget=None, pop=None, pop_a=1.0, pc=(1, 0.3, 0.25), flash=0.0):
    rr(c, 40, 230, 330, 150, 22, (0.11, 0.11, 0.14), 0.92)
    c.new_path(); c.rectangle(44, 234, 322, 142); c.set_line_width(5); c.set_source_rgba(*RED, 0.9); c.stroke()
    txt(c, "UNTIL THE FLASH", 205, 272, 30, WHITE); txt(c, f"{days} DAYS", 205, 332, 62, mix((1, 0.3, 0.25), WHITE, flash))
    if budget is not None:
        rr(c, 710, 230, 330, 150, 22, (0.11, 0.11, 0.14), 0.92)
        txt(c, "BUDGET", 875, 272, 30, WHITE); txt(c, budget, 875, 332, 60, mix(GOLD, WHITE, flash))
        if pop and pop_a > 0:
            txt(c, pop[0], 1030, 418, 46, pc, "r", stroke=7, a=pop_a); txt(c, pop[1], 1030, 462, 26, WHITE, "r", stroke=5, a=pop_a)
def step(c, n, s, a=1.0):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(50); w = c.text_extents(f"{n}. {s}").width + 80
    rr(c, W / 2 - w / 2, 470, w, 84, 20, WHITE, a); txt(c, f"{n}.", W / 2 - w / 2 + 40, 512, 50, RED, "l", a=a); txt(c, s, W / 2 - w / 2 + 95, 512, 50, INK, "l", a=a)
def fact_badge(c, x, y, a=1.0):
    rr(c, x - 120, y - 32, 240, 64, 32, (0.16, 0.6, 0.36), a); txt(c, "REAL FACT", x, y, 34, WHITE, a=a)
def vignette(c, a=0.5):
    g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1250); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, a)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
# ------------------------------------------------------------------ adult cast (v2)
MIA_JK = (0.22, 0.55, 0.45); MIA_JK2 = (0.17, 0.45, 0.37); MIA_HAIR = (0.96, 0.8, 0.42); MIA_HAIR2 = (0.85, 0.65, 0.3); MIA_SKIN = (0.93, 0.74, 0.6); MIA_PANT = (0.25, 0.22, 0.3)
def person(c, x, y, s=1.0, who="red", face=1, t=0.0, mode="stand", mood="calm", talk=0.0, blink=True, phase=0.0, alpha=1.0, look=0.0, hold=None):
    """Adult proportions (~7 heads). y = feet. who: red | mia. mode: stand, walk, point_down, phone, torch, scared, shrug, dig, carry"""
    if alpha < 1: c.push_group()
    red = who == "red"
    skin = SKIN if red else MIA_SKIN; top = HOOD if red else MIA_JK; top2 = HOOD2 if red else MIA_JK2; pant = JEAN if red else MIA_PANT
    c.save(); c.translate(x, y); c.scale(s, s)
    br = math.sin(t * 2.2 + phase) * 2.5
    sw = math.sin(t * 7 + phase) if mode == "walk" else 0.0
    if mode == "walk": c.translate(0, -abs(math.sin(t * 7 + phase)) * 7)
    fx = face if face != 0 else 1
    hip = -230; bw = 120 if red else 104
    for k, side in enumerate((-1, 1)):
        a = sw * 0.4 * (1 if k else -1)
        kx, ky = limb(c, side * (22 if red else 18), hip, a, 222, 40 if red else 34, pant)
        rr(c, kx - 26 + (8 * fx if face else 0), ky - 12, 54, 22, 10, (0.96, 0.96, 0.96) if red else (0.85, 0.35, 0.3))
    c.save(); c.translate(0, hip)
    rr(c, -bw / 2, -250 + br, bw, 270, 34, top)
    if red:
        rr(c, -34, -110 + br, 68, 40, 14, top2) if face == 0 else rr(c, -16 + 14 * fx, -110 + br, 44, 40, 14, top2)
    else:
        line(c, [(0, -245 + br), (0, 10)], 5, top2); rr(c, -bw / 2, -20 + br, bw, 26, 8, top2)
    shL, shR = (-bw / 2 + 8, -228 + br), (bw / 2 - 8, -228 + br)
    if mode in ("stand", "walk"): aL, aR = 0.12 + sw * 0.45, -0.12 - sw * 0.45
    elif mode == "point_down": aL, aR = 0.12, -0.6
    elif mode == "phone": aL, aR = 0.12, -2.4
    elif mode == "torch": aL, aR = 0.12, -1.7
    elif mode == "scared": aL, aR = 2.6 + 0.07 * math.sin(t * 20), -2.6 - 0.07 * math.sin(t * 20)
    elif mode == "shrug": aL, aR = 1.15, -1.15
    elif mode == "dig": aL, aR = 0.9 + 0.5 * math.sin(t * 5), -0.9 - 0.5 * math.sin(t * 5)
    elif mode == "point": aL, aR = 0.12, -1.55
    else: aL, aR = 0.12, -0.12
    if face == -1: aL, aR = -aR, -aL
    pL = limb(c, shL[0], shL[1], aL, 200, 34 if red else 28, top, hand=18, hcol=skin)
    pR = limb(c, shR[0], shR[1], aR, 200, 34 if red else 28, top, hand=18, hcol=skin)
    hp = pR if fx > 0 else pL
    if mode == "phone": rr(c, hp[0] - 22, hp[1] - 56, 44, 78, 8, INK); rr(c, hp[0] - 17, hp[1] - 50, 34, 64, 5, hold or (0.95, 0.25, 0.25))
    if mode == "torch": rr(c, hp[0] - 10, hp[1] - 12, 40, 22, 7, (0.3, 0.3, 0.33))
    c.restore()
    hr = 62 if red else 58; hy = hip - 250 - hr - 18 + br * 1.1
    rect(c, -14, hip - 250 - 26 + br, 28, 30, skin)
    c.save(); c.translate(look * 5 * fx, hy)
    if mode == "scared": c.translate(2 * math.sin(t * 40), 0)
    if not red:  # wavy blonde hair, high ponytail-free, past the shoulders
        sway = 3 * math.sin(t * 2.5 + phase)
        c.new_path(); c.move_to(-hr - 4, -16)
        c.curve_to(-hr - 20, 50, -hr - 2 + sway, 90, -hr - 14 + sway, 150)
        for k in range(5):
            x0 = -hr - 14 + k * (2 * hr + 28) / 5 + sway; x1 = x0 + (2 * hr + 28) / 5
            c.curve_to(x0 + 6, 175, x1 - 6, 175, x1, 150)
        c.curve_to(hr + 2 + sway, 90, hr + 20, 50, hr + 4, -16); c.close_path(); c.set_source_rgb(*MIA_HAIR2); c.fill()
    ell(c, 0, 0, hr, hr * 1.1, skin)
    if face == 0: ell(c, -hr, 4, 11, 16, skin); ell(c, hr, 4, 11, 16, skin)
    if red:
        c.new_path(); c.arc(0, -10, hr + 2, math.pi * 1.03, math.pi * 1.97); c.close_path(); c.set_source_rgb(*HAIR); c.fill()
        c.new_path(); c.arc(0, -22, hr + 4, math.pi, TAU); c.close_path(); c.set_source_rgb(*CAP); c.fill()
        rr(c, -hr - 12, -32, 2 * hr + 24, 18, 9, CAP2)
        if face == 0: rr(c, -hr - 58, -38, 56, 16, 8, CAP2)
        else: rr(c, (-hr - 62) if fx > 0 else (hr + 6), -36, 56, 16, 8, CAP2)
        ell(c, 0, -hr - 22, 9, 6, CAP2)
        # light stubble / adult jaw
        c.new_path(); c.arc(0, 8, hr * 0.92, 0.35, math.pi - 0.35); c.set_line_width(6); c.set_source_rgba(0.5, 0.36, 0.28, 0.25); c.stroke()
    else:
        c.new_path(); c.arc(0, -12, hr + 4, math.pi * 1.0, TAU); c.close_path(); c.set_source_rgb(*MIA_HAIR); c.fill()
        # side-swept fringe from a side parting
        c.new_path(); c.move_to(hr * 0.35, -hr * 1.05); c.curve_to(-hr * 0.2, -hr * 0.85, -hr * 0.85, -hr * 0.4, -hr * 0.98, 10)
        c.curve_to(-hr * 0.7, -hr * 0.2, -hr * 0.1, -hr * 0.45, hr * 0.5, -hr * 0.55); c.close_path(); c.set_source_rgb(*MIA_HAIR); c.fill()
        c.new_path(); c.move_to(hr * 0.35, -hr * 1.05); c.curve_to(hr * 0.8, -hr * 0.8, hr * 1.0, -hr * 0.3, hr * 1.0, 0); c.line_to(hr * 0.85, -hr * 0.2); c.curve_to(hr * 0.7, -hr * 0.5, hr * 0.5, -hr * 0.6, hr * 0.35, -hr * 1.05); c.close_path(); c.fill()
        line(c, [(hr * 0.35, -hr * 1.05), (hr * 0.2, -hr * 0.8)], 3, MIA_HAIR2)
        # strands framing the face
        for sx in (-1, 1):
            c.new_path(); c.move_to(sx * hr * 0.95, -10); c.curve_to(sx * hr * 1.05, 40, sx * hr * 0.9, 80, sx * hr * 1.0, 110); c.line_to(sx * hr * 1.12, 100); c.curve_to(sx * hr * 1.12, 50, sx * hr * 1.08, 10, sx * hr * 1.02, -20); c.close_path(); c.set_source_rgb(*MIA_HAIR); c.fill()
    ex = 10 * fx if face else 0; op = 1.0
    if blink and (t + phase * 1.3) % 3.9 < 0.12: op = 0.12
    for sx in (-22, 23):
        ell(c, sx + ex, 6, 7 if mood != "scared" else 9, (9 if mood != "scared" else 12) * op, INK)
        if op > 0.5: ell(c, sx + ex + 2, 3, 2.4, 2.4, WHITE)
        if not red and op > 0.5: line(c, [(sx + ex - 8, -6), (sx + ex + 9, -9)], 3, INK)
    c.set_source_rgb(*INK); c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if mood in ("worried", "scared"):
        c.move_to(-34 + ex, -14); c.line_to(-12 + ex, -20); c.move_to(36 + ex, -14); c.line_to(14 + ex, -20); c.stroke()
    my = 38
    if talk > 0.05: ell(c, 2 + ex, my, 12, 4 + 9 * talk, (0.45, 0.12, 0.12))
    elif mood == "happy": c.new_path(); c.arc(2 + ex, my - 12, 14, 0.25, math.pi - 0.25); c.stroke()
    elif mood == "scared": ell(c, 2 + ex, my, 9, 11, (0.45, 0.12, 0.12))
    elif mood == "worried": c.new_path(); c.arc(2 + ex, my + 10, 11, math.pi * 1.15, math.pi * 1.85); c.stroke()
    else: line(c, [(-8 + ex, my), (11 + ex, my)], 4, INK)
    if not red: ell(c, -36 + ex, 24, 9, 5, (1, 0.55, 0.55), 0.45); ell(c, 38 + ex, 24, 9, 5, (1, 0.55, 0.55), 0.45)
    c.restore(); c.restore()
    if alpha < 1: c.pop_group_to_source(); c.paint_with_alpha(alpha)
DOG = (0.82, 0.58, 0.3); DOG2 = (0.62, 0.4, 0.2)
def dog(c, x, y, s=1.0, face=1, t=0.0, mode="sit", bark=0.0):
    """Bolt: golden-brown medium dog. y = ground. mode: sit | stand | walk"""
    c.save(); c.translate(x, y); c.scale(s * face, s)
    wag = math.sin(t * 14) * 0.5
    run = math.sin(t * 9) if mode == "walk" else 0
    if mode == "sit":
        ell(c, -20, -70, 70, 60, DOG); rr(c, -90, -40, 60, 40, 18, DOG)
        rr(c, 20, -60, 26, 60, 12, DOG); rr(c, -6, -60, 26, 60, 12, DOG2)
        c.save(); c.translate(-85, -50); c.rotate(-0.8 + wag); rr(c, -8, -70, 16, 70, 8, DOG2); c.restore()
        hx, hy = 40, -150
        ell(c, 10, -120, 34, 40, DOG)
    else:
        rr(c, -90, -130, 170, 75, 36, DOG)
        for k, lx in enumerate((-70, -40, 30, 58)):
            a = run * 0.5 * (1 if k % 2 else -1); limb(c, lx, -70, a, 70, 20, DOG2 if k % 2 else DOG)
        c.save(); c.translate(-88, -120); c.rotate(-0.9 + wag); rr(c, -7, -60, 14, 60, 7, DOG2); c.restore()
        hx, hy = 80, -150
    ell(c, hx, hy, 46, 42, DOG); rr(c, hx + 20, hy - 6, 50, 34, 16, DOG)
    ell(c, hx + 68, hy - 2, 10, 8, INK)
    poly(c, [(hx - 30, hy - 26), (hx - 46, hy + 30), (hx - 10, hy - 6)], DOG2)
    ell(c, hx + 10, hy - 10, 6, 7, INK); ell(c, hx + 12, hy - 12, 2, 2, WHITE)
    if bark > 0.05: ell(c, hx + 52, hy + 22, 16, 5 + 10 * bark, (0.5, 0.15, 0.15))
    else: line(c, [(hx + 40, hy + 20), (hx + 62, hy + 18)], 3, INK)
    rr(c, hx - 30, hy + 30, 50, 12, 6, (0.85, 0.2, 0.2))
    c.restore()
# ------------------------------------------------------------------ UI v2 (polished)
def shadow_rr(c, x, y, w, h, r, col, a=1.0, sh=0.35, off=8):
    for k in range(6): rr(c, x - k * 2 + 2, y + off - k * 2 + 4, w + k * 4 - 4, h + k * 4 - 4, r + k * 2, (0, 0, 0), sh * a / 6)
    rr(c, x, y, w, h, r, col, a)
def icon_sun(c, x, y, r, col=(1, 0.55, 0.15)):
    for k in range(8):
        a_ = k * TAU / 8; line(c, [(x + math.cos(a_) * r * 1.25, y + math.sin(a_) * r * 1.25), (x + math.cos(a_) * r * 1.65, y + math.sin(a_) * r * 1.65)], r * 0.32, col)
    ell(c, x, y, r, r, col)
def icon_coin(c, x, y, r):
    ell(c, x, y + 3, r, r, (0.75, 0.5, 0.1)); ell(c, x, y, r, r, (1, 0.8, 0.25)); ell(c, x, y, r * 0.72, r * 0.72, (1, 0.88, 0.45)); txt(c, "$", x, y + 1, r * 1.2, (0.75, 0.5, 0.1))
def icon_bulb(c, x, y, r):
    ell(c, x, y - r * 0.2, r, r, WHITE); rr(c, x - r * 0.45, y + r * 0.6, r * 0.9, r * 0.6, r * 0.2, (0.85, 0.9, 0.95))
def ui_counters(c, days, budget=None, pulse_d=0.0, pulse_b=0.0, days_frac=1.0):
    # countdown card
    s = 1 + 0.08 * pulse_d; c.save(); c.translate(205, 305); c.scale(s, s); c.translate(-205, -305)
    shadow_rr(c, 40, 228, 330, 156, 30, (0.1, 0.1, 0.13), 0.94)
    rr(c, 40, 228, 330, 10, 5, (0.95, 0.3, 0.2))
    icon_sun(c, 84, 272, 13); txt(c, "UNTIL THE FLASH", 110, 272, 26, (0.75, 0.75, 0.8), "l")
    txt(c, f"{days}", 70, 334, 74, (1, 0.38, 0.28), "l"); w = 0
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(74); w = c.text_extents(f"{days}").x_advance
    txt(c, "DAYS", 80 + w, 344, 34, WHITE, "l")
    rr(c, 60, 366, 290, 8, 4, (0.25, 0.25, 0.3)); rr(c, 60, 366, max(8, 290 * days_frac), 8, 4, (1, 0.38, 0.28))
    c.restore()
    if budget is not None:
        s = 1 + 0.08 * pulse_b; c.save(); c.translate(875, 305); c.scale(s, s); c.translate(-875, -305)
        shadow_rr(c, 710, 228, 330, 156, 30, (0.1, 0.1, 0.13), 0.94)
        rr(c, 710, 228, 330, 10, 5, GOLD)
        icon_coin(c, 752, 272, 15); txt(c, "BUDGET", 780, 272, 26, (0.75, 0.75, 0.8), "l")
        txt(c, budget, 875, 334, 60, GOLD)
        c.restore()
def ui_pop(c, lab, sub, col, u):
    """money pop under the budget card. u: 0..1 life (in 0-0.12 slide, out after 0.85)"""
    if u <= 0 or u >= 1: return
    a = clamp(u / 0.1) * clamp((1 - u) / 0.12); dy = 30 * (1 - ease(clamp(u / 0.12)))
    c.save(); c.translate(0, -dy)
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(44); w1 = c.text_extents(lab).x_advance
    c.set_font_size(24); w2 = c.text_extents(sub).x_advance; w = max(w1, w2) + 60
    shadow_rr(c, 1040 - w, 400, w, 110, 24, col, a)
    txt(c, lab, 1040 - w / 2, 440, 44, WHITE, a=a); txt(c, sub, 1040 - w / 2, 483, 24, (1, 1, 1), a=a * 0.9)
    c.restore()
def ui_step(c, n, title, u, total=4):
    """step banner. u = seconds since shown"""
    if u < 0: return
    k = back(clamp(u / 0.35)); a = clamp(u / 0.2)
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(52); w = c.text_extents(title).x_advance + 150
    c.save(); c.translate(W / 2, 560); c.scale(k, k)
    shadow_rr(c, -w / 2, -48, w, 96, 48, WHITE, a)
    ell(c, -w / 2 + 50, 0, 34, 34, RED, a); txt(c, str(n), -w / 2 + 50, 1, 44, WHITE, a=a)
    txt(c, title, -w / 2 + 98, 0, 52, INK, "l", a=a)
    for j in range(total): ell(c, -((total - 1) * 22) / 2 + j * 22, 72, 7, 7, RED if j < n else (0.85, 0.85, 0.88), a)
    c.restore()
def wrap(c, s, size, maxw):
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    lines, cur = [], ""
    for w_ in s.split():
        t_ = (cur + " " + w_).strip()
        if c.text_extents(t_).x_advance > maxw and cur: lines.append(cur); cur = w_
        else: cur = t_
    if cur: lines.append(cur)
    return lines
def ui_fact(c, body, u, y=640, big=None):
    """REAL FACT card. u = seconds since shown"""
    if u < 0: return
    k = back(clamp(u / 0.35)); a = clamp(u / 0.2)
    ls = wrap(c, body, 46, 780); h = 120 + 60 * len(ls) + (110 if big else 0)
    c.save(); c.translate(W / 2, y); c.scale(k, k)
    shadow_rr(c, -440, 0, 880, h, 36, WHITE, a)
    rr(c, -440, 0, 880, 84, 36, (0.16, 0.62, 0.38), a); rect(c, -440, 50, 880, 34, (0.16, 0.62, 0.38), a)
    icon_bulb(c, -380, 40, 18); txt(c, "REAL FACT", -340, 42, 40, WHITE, "l", a=a)
    yy = 130
    if big: txt(c, big, 0, yy + 20, 96, (0.16, 0.62, 0.38), a=a); yy += 110
    for j, l_ in enumerate(ls): txt(c, l_, 0, yy + j * 60, 46, INK, a=a)
    c.restore()
