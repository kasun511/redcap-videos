# ------------------------------------------------------------------ gills props
PINK = (1.0, 0.45, 0.55); SEAL = (0.5, 0.54, 0.6)
def swimmer(c, x, y, s, t, rot=-1.15, gills=0.0, big=0.0, fat=0.0, a=1.0, **kw):
    """guy rotated to swim; x,y = hip-ish centre"""
    c.save(); c.translate(x, y + 12 * math.sin(t * 2.2)); c.rotate(rot); c.scale(1 + 0.75 * fat, 1)
    guy(c, 0, 150 * s, s, t, walk=kw.pop("walk", 0.55), scarf=False, jacket=HOOD, alpha=a, **kw)
    gillfx(c, 0, 150 * s, s, t, gills, big); c.restore()
def gillfx(c, x, y, s, t, gills, big=0.0):
    if gills <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    ny = -362
    if big > 0:
        for sd in (-1, 1):
            for k in range(5):
                an = (-0.9 + k * 0.42) + 0.12 * math.sin(t * 5 + k); L = (120 + 40 * (2 - abs(k - 2))) * big
                x1 = sd * (62 + math.cos(an) * L); y1 = ny + math.sin(an) * L
                line(c, [(sd * 62, ny), (x1, y1)], 16, PINK, gills)
                for j in range(1, 5): u = j / 5; px = sd * 62 + (x1 - sd * 62) * u; py = ny + (y1 - ny) * u; line(c, [(px, py - 14 * big), (px, py + 14 * big)], 6, mix(PINK, WHITE, 0.3), gills)
    for sd in (-1, 1):
        for k in range(3): line(c, [(6 + sd * (44 + k * 9), ny - 16 + k * 2), (6 + sd * (48 + k * 9), ny + 12 - k * 5)], 6, mix(PINK, RED, 0.35), gills)
    c.restore()
def stand(c, x, y, s, t, gills=0.0, big=0.0, fat=0.0, **kw):
    c.save(); c.translate(x, y + 10 * math.sin(t * 2))
    kw.setdefault("jacket", HOOD); kw.setdefault("scarf", False)
    glow(c, 0, -260 * s, 330 * s, (0.75, 0.95, 1.0), 0.22)
    guy(c, 0, 0, s, t, **kw)
    if fat > 0:
        b = back(fat); ell(c, 0, -235 * s, (70 + 95 * b) * s, (100 + 55 * b) * s, HOOD)
        for k in (-1, 0, 1): line(c, [(-(60 + 90 * b) * s, (-235 + k * 55) * s), ((60 + 90 * b) * s, (-235 + k * 55) * s)], 5 * s, HOOD2, 0.6)
        ell(c, 6 * s, -420 * s, 0, 0, WHITE)
    gillfx(c, 0, 0, s, t, gills, big); c.restore()
def breath(c, x, y, t, n=5, a=1.0):
    for k in range(n):
        ph = (t * 0.6 + k / n) % 1; r = 8 + 14 * ph
        c.new_path(); c.arc(x + 30 * math.sin(ph * 7 + k), y - 260 * ph, r, 0, TAU); c.set_line_width(4); c.set_source_rgba(1, 1, 1, 0.7 * (1 - ph) * a); c.stroke()
def nocircle(c, x, y, r, a=1.0):
    c.new_path(); c.arc(x, y, r, 0, TAU); c.set_line_width(16); c.set_source_rgba(*RED, a); c.stroke(); line(c, [(x - r * 0.7, y - r * 0.7), (x + r * 0.7, y + r * 0.7)], 16, RED, a)
def tank_icon(c, x, y, a=1.0):
    rr(c, x - 34, y - 70, 68, 150, 30, (0.95, 0.8, 0.2), a); rr(c, x - 14, y - 96, 28, 34, 8, STEEL_D, a); line(c, [(x + 10, y - 86), (x + 60, y - 60), (x + 60, y + 10)], 8, INK, a)
def mask_icon(c, x, y, a=1.0):
    rr(c, x - 70, y - 42, 140, 84, 34, INK, a); rr(c, x - 58, y - 30, 116, 60, 24, (0.6, 0.85, 1.0), a); rr(c, x + 60, y - 120, 16, 110, 8, ORANGE, a)
def jar(c, x, y, w, h, col, label, n, t, a=1.0, seed=1):
    shadow_rr(c, x - w / 2, y - h, w, h, 36, (0.95, 0.97, 1.0), a); rr(c, x - w / 2 + 12, y - h + 12, w - 24, h - 24, 26, col, a)
    R = random.Random(seed)
    for k in range(n):
        px = x - w / 2 + 50 + R.random() * (w - 100); py = y - h + 50 + R.random() * (h - 100)
        px += 8 * math.sin(t * 2 + k); py += 8 * math.cos(t * 1.7 + k * 2)
        ell(c, px, py, 17, 17, RED, a); txt(c, "O", px, py + 1, 20, WHITE, a=a)
    chip(c, label, INK, y + 60, a, 44, x)
def seal(c, x, y, s, t, face=1, a=1.0):
    c.save(); c.translate(x, y + 10 * math.sin(t * 1.8)); c.scale(s * face, s)
    poly(c, [(-190, 10), (-270, -40 + 14 * math.sin(t * 5)), (-250, 30), (-270, 70 + 14 * math.sin(t * 5))], mix(SEAL, INK, 0.2), a)
    ell(c, 0, 0, 200, 105, SEAL, a); ell(c, 20, 30, 150, 66, mix(SEAL, WHITE, 0.45), a)
    ell(c, 160, -50, 80, 72, SEAL, a); ell(c, 215, -30, 34, 26, mix(SEAL, WHITE, 0.5), a); ell(c, 240, -40, 10, 8, INK, a)
    ell(c, 175, -72, 10, 12, INK, a); ell(c, 178, -75, 3, 3, WHITE, a)
    for k in (-1, 0, 1): line(c, [(220, -24), (275, -24 + k * 14)], 3, INK, a * 0.7)
    poly(c, [(20, 70), (-10, 150 + 10 * math.sin(t * 4)), (80, 110)], mix(SEAL, INK, 0.2), a); c.restore()
def dolphin(c, x, y, s, t, face=1, a=1.0):
    c.save(); c.translate(x, y); c.scale(s * face, s); c.rotate(0.15 * math.sin(t * 3)); col = (0.45, 0.6, 0.78)
    poly(c, [(-150, 0), (-220, -45), (-200, 0), (-220, 45)], mix(col, INK, 0.2), a)
    ell(c, 0, 0, 160, 58, col, a); ell(c, 10, 22, 130, 32, mix(col, WHITE, 0.6), a)
    poly(c, [(-20, -50), (-50, -115), (30, -52)], mix(col, INK, 0.15), a); poly(c, [(140, -6), (215, 8), (140, 26)], col, a)
    ell(c, 105, -16, 8, 8, INK, a); poly(c, [(30, 40), (10, 100), (80, 48)], mix(col, INK, 0.15), a); c.restore()
def kelp(c, x, y, h, t, a=1.0, k0=0):
    pts = [(x + 26 * math.sin(t * 1.5 + j * 0.7 + k0) * (j / 8), y - h * j / 8) for j in range(9)]
    line(c, pts, 16, (0.2, 0.55, 0.3), a)
    for j in range(1, 8): px, py = pts[j]; ell(c, px + (18 if j % 2 else -18), py, 20, 9, (0.3, 0.68, 0.36), a)
def dome(c, x, y, r, t, a=1.0, lit=1.0):
    c.new_path(); c.arc(x, y, r, math.pi, TAU); c.close_path(); c.set_source_rgba(0.75, 0.92, 1.0, 0.35 * a); c.fill()
    c.new_path(); c.arc(x, y, r, math.pi, TAU); c.set_line_width(8); c.set_source_rgba(1, 1, 1, 0.8 * a); c.stroke()
    R = random.Random(int(x))
    for k in range(3):
        bw = r * 0.34; bh = r * R.uniform(0.35, 0.75); bx = x - r * 0.62 + k * r * 0.44
        rr(c, bx, y - bh, bw, bh, 8, mix(STEEL_L, BLUE, 0.2), a)
        for j in range(int(bh // 46)):
            for i in range(2): rr(c, bx + 10 + i * (bw / 2 - 4), y - bh + 12 + j * 46, bw / 2 - 16, 24, 4, mix(DARK, AMBER, lit * (0.6 + 0.4 * math.sin(t * 2 + k + j + i))), a)
    rr(c, x - r - 10, y - 10, 2 * r + 20, 26, 10, STEEL_D, a)
def seabed(c, t):
    c.save(); c.identity_matrix(); pts = [(x, 1700 + 30 * math.sin(x / 140)) for x in range(-20, 1120, 40)]
    poly(c, pts + [(1120, H), (-20, H)], (0.76, 0.68, 0.48)); c.restore()
def earth(c, x, y, r, t, a=1.0):
    ell(c, x, y, r, r, (0.2, 0.55, 0.9), a); c.save(); c.new_path(); c.arc(x, y, r, 0, TAU); c.clip()
    for k, (dx, dy, rx, ry) in enumerate([(-0.5, -0.35, 0.35, 0.28), (0.35, 0.1, 0.3, 0.4), (-0.25, 0.5, 0.25, 0.22), (0.6, -0.6, 0.22, 0.16)]):
        ox = ((dx + t * 0.12 + 1.6) % 3.2) - 1.6; ell(c, x + ox * r, y + dy * r, rx * r, ry * r, (0.35, 0.72, 0.4), a)
    c.restore(); glow(c, x - r * 0.3, y - r * 0.3, r * 0.9, WHITE, 0.18 * a)
def monster(c, t, a):
    if a <= 0: return
    c.save(); c.identity_matrix()
    for sx in (330, 750):
        glow(c, sx, 760, 220, (1, 0.9, 0.3), 0.5 * a); ell(c, sx, 760, 120, 84, (1.0, 0.92, 0.4), a); ell(c, sx + 14 * math.sin(t * 2), 772, 36, 70, INK, a)
    n = 9
    for k in range(n):
        x0 = 150 + k * 780 / (n - 1); poly(c, [(x0 - 44, 980), (x0 + 44, 980), (x0, 1130 + 20 * math.sin(k * 2))], (0.95, 0.95, 0.9), a)
        poly(c, [(x0 - 44 + 44, 1560), (x0 + 44 + 44, 1560), (x0 + 44, 1420 - 20 * math.sin(k * 2))], (0.95, 0.95, 0.9), a * 0.9)
    lx = 540 + 30 * math.sin(t * 1.3); line(c, [(540, 640), (lx, 520)], 8, (0.3, 0.3, 0.35), a); glow(c, lx, 500, 90, (0.5, 1, 0.9), 0.8 * a); ell(c, lx, 500, 22, 22, (0.7, 1, 0.95), a)
    c.restore()
# ------------------------------------------------------------------ scenes
CIT = WORD(3, "cities", d=4.5)
SC = [("hook", 0.0), ("oxy", T0(1) - 0.12), ("heat", T0(2) - 0.12), ("planet", T0(3) - 0.12), ("city", CIT - 0.15), ("dark", T0(5) - 0.12), ("end", T0(6) - 0.12)]
STARTS = [s for _, s in SC]
def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k
def s_hook(c, t, lt, d):
    sea(c, t, 520); school(c, t, 520, 4)
    fall = ease(clamp(lt / 1.1)); y = 150 + 1050 * fall
    if lt < 1.1: stand(c, 540, y, 1.0, t, mood="scared", armF=2.6, armB=-2.6)
    else:
        tk = WORD(0, "tank", d=2.6); mk = WORD(0, "mask", d=3.3); gl = WORD(0, "gills", d=4.2)
        g = clamp((t - gl + 0.1) / 0.3)
        stand(c, 540, 1300, 1.25, t, mood="happy" if g > 0 else "calm", gills=g, armF=0.5 + 0.3 * math.sin(t * 2), armB=-0.5 - 0.3 * math.sin(t * 2), walk=0.15)
        breath(c, 600, 1000, t, 5, g)
        if t > tk - 0.15 and t < gl: u = clamp((t - tk + 0.15) / 0.25); tank_icon(c, 230, 1050, u); nocircle(c, 230, 1050, 110, u)
        if t > mk - 0.15 and t < gl: u = clamp((t - mk + 0.15) / 0.25); mask_icon(c, 850, 1050, u); nocircle(c, 850, 1050, 110, u)
        if g > 0: bigtxt(c, "JUST GILLS", 1600, 120, GOLD, t, gl - 0.1)
    if lt > 0.3 and lt < 1.3: 
        for k in range(8): ell(c, 540 + 40 * math.sin(k * 2.1), 520 - 120 * clamp((lt - 0.75) / 0.4) * (1 if k % 2 else 0.6) + 0, 0, 0, WHITE)
    if 0.7 < lt < 1.5:
        u = (lt - 0.7) / 0.8
        for k in range(10): an = math.pi + k * math.pi / 9; ell(c, 540 + math.cos(an) * 220 * u, 520 + math.sin(an) * 260 * u * (1 - u) * 2, 14 * (1 - u) + 3, 14 * (1 - u) + 3, WHITE, 1 - u)
    chip(c, "WHAT IF...", RED, 470, clamp(lt / 0.3), 60)
    lab(c, 540, 575, "WE COULD BREATHE UNDERWATER?", INK, clamp((lt - 0.25) / 0.3), 40, WHITE)
def s_oxy(c, t, lt, d):
    sea(c, t, -200, cam=0.25)
    en = WORD(1, "enormous", d=6.5); th = WORD(1, "thirty", d=2.2); so = WORD(1, "so", d=5.0)
    out = ease(clamp((t - so + 0.2) / 0.4))
    chip(c, "PROBLEM 1", RED, 470, clamp(lt / 0.3), 60)
    if out < 1:
        c.save(); c.translate(0, -1600 * out)
        u1 = clamp((lt - 0.5) / 0.3); jar(c, 290, 1150, 360, 520, (0.86, 0.95, 1.0), "AIR", 30, t, u1, 3)
        u2 = clamp((t - th + 0.4) / 0.3); jar(c, 790, 1150, 360, 520, (0.3, 0.62, 0.92), "WATER", 1, t, u2, 4)
        c.restore()
        if t > th - 0.1: bigtxt(c, "30x LESS OXYGEN", 1480, 96, GOLD, t, th - 0.1, a=1 - out)
    if out > 0:
        b = back(clamp((t - en + 0.15) / 0.5)) if t > en - 0.15 else 0.0
        stand(c, 540, 1500, 1.3 * out, t, gills=out, big=b * 1.5, mood="scared" if b > 0.3 else "calm", armF=0.4 + 1.2 * clamp(b), armB=-0.4 - 1.2 * clamp(b))
        if b > 0: bigtxt(c, "ENORMOUS GILLS", 1610, 96, PINK, t, en)
def s_heat(c, t, lt, d):
    bl = WORD(2, "blubber", d=6.0); tw = WORD(2, "twenty-five", d=2.5); sl = WORD(2, "seal", d=7.5)
    if not any(x.lower().startswith("twenty") for x, _ in LINES[2]["words"]): tw = T0(2) + 2.5
    fat = ease(clamp((t - bl + 0.1) / 0.5)); cold = clamp((lt - 0.4) / 2.0) * (1 - fat)
    sea(c, t, -200, cam=0.35 + 0.2 * cold)
    chip(c, "PROBLEM 2", RED, 470, clamp(lt / 0.3), 60)
    stand(c, 400 if fat > 0 else 540, 1450, 1.2, t, gills=1, fat=fat, cold=cold, shiver=cold, mood="happy" if fat > 0.5 else "cold", armF=0.9 - 0.6 * fat, elbF=2.0 * (1 - fat), armB=-0.3)
    if fat < 0.3:
        tx, ty = 880, 1250; rr(c, tx - 26, ty - 380, 52, 420, 26, WHITE); lvl = 0.9 - 0.7 * cold
        rr(c, tx - 12, ty - 20 - 340 * lvl, 24, 340 * lvl + 30, 12, mix(RED, BLUE, cold)); ell(c, tx, ty + 40, 44, 44, mix(RED, BLUE, cold))
        if t > tw - 0.2: bigtxt(c, "25x FASTER", 1540, 100, (0.6, 0.9, 1.0), t, tw - 0.2); lab(c, 540, 1650, "HEAT LOSS", WHITE, clamp((t - tw) / 0.3), 44, BLUE)
    else:
        bigtxt(c, "BLUBBER MODE", 1610, 96, GOLD, t, bl)
        if t > sl - 0.5: u = ease(clamp((t - sl + 0.5) / 0.6)); seal(c, 1400 - 620 * u, 900, 1.0, t, face=-1)
def s_planet(c, t, lt, d):
    sea(c, t, -200, cam=0.2); school(c, t, -200, 6)
    sv = WORD(3, "seventy", d=2.5)
    k = back(clamp(lt / 0.4)); earth(c, 540, 1000, 330 * k, t)
    chip(c, "THE WHOLE OCEAN OPENS UP", GREEN, 470, clamp(lt / 0.3), 46)
    if t > sv - 0.2: bigtxt(c, "70% OF THE PLANET", 1520, 92, GOLD, t, sv - 0.2)
    swimmer(c, 540 + 430 * math.cos(t * 1.4), 1000 + 430 * math.sin(t * 1.4), 0.45, t, rot=t * 1.4 + math.pi, gills=1)
def s_city(c, t, lt, d):
    sea(c, t, -200, cam=0.3); seabed(c, t)
    kp = WORD(3, "kelp", d=6.5); dl = WORD(3, "dolphins", d=7.8); dr = T0(4)
    for k, x in enumerate((90, 190, 930, 1010)): 
        if t > kp - 0.3: kelp(c, x, 1720, (420 + 90 * (k % 2)) * ease(clamp((t - kp + 0.3) / 0.5)), t, k0=k)
    for k, (x, r) in enumerate(((300, 250), (760, 300), (540, 190))):
        u = back(clamp((lt - 0.1 - k * 0.15) / 0.4)); dome(c, x, 1700 + (60 if k == 2 else 0), r * u, t)
    if t > dl - 0.4: u = clamp((t - dl + 0.4) / 2.5); dolphin(c, -250 + 1100 * u, 760 - 120 * math.sin(u * 3.1), 1.0, t)
    if t > dl - 0.4: dolphin(c, -450 + 1100 * clamp((t - dl + 0.4) / 2.5), 900 - 100 * math.sin(clamp((t - dl + 0.4) / 2.5) * 3.1), 0.7, t + 1)
    swimmer(c, 1200 - 150 * lt, 1050, 0.75, t, rot=-1.15, gills=1, face=-1, mood="happy")
    if lt < dr - CIT + 0.15: chip(c, "CITIES ON THE SEA FLOOR", BLUE, 470, clamp(lt / 0.3), 48)
    if t > kp - 0.2 and t < dl - 0.2: lab(c, 540, 600, "KELP FARMS", WHITE, clamp((t - kp + 0.2) / 0.3), 44, GREEN)
    if t > dl - 0.2 and t < dr: lab(c, 540, 600, "DOLPHIN NEIGHBOURS", WHITE, clamp((t - dl + 0.2) / 0.3), 44, BLUE)
    if t > dr - 0.1:
        u = clamp((t - dr) / 0.3); chip(c, "NOBODY DROWNS. EVER.", GREEN, 470, u, 52)
        c.save(); c.translate(540, 640); k = back(u); c.scale(k, k); c.new_path(); c.arc(0, 0, 80, 0, TAU); c.set_line_width(44); c.set_source_rgba(1, 1, 1, 1); c.stroke()
        for q in range(4): c.new_path(); c.arc(0, 0, 80, q * math.pi / 2 - 0.3, q * math.pi / 2 + 0.3); c.set_line_width(44); c.set_source_rgba(*RED, 1); c.stroke()
        c.restore(); nocircle(c, 540, 640, 150, clamp((t - dr - 0.5) / 0.25))
def s_dark(c, t, lt, d):
    tw = WORD(5, "two", d=1.5); ns = WORD(5, "sunlight", d=4.0); dn = WORD(5, "down", d=5.5); fc = WORD(5, "food", d=8.0)
    dark = ease(clamp((lt - 0.3) / (ns - STARTS[5] + 0.3)))
    sea(c, t, -200, cam=min(1, 0.4 + dark))
    c.save(); c.identity_matrix(); c.set_source_rgba(0, 0.01, 0.04, 0.88 * dark); c.paint(); c.restore()
    monster(c, t, ease(clamp((t - fc + 0.5) / 0.6)))
    sink = 600 + 500 * dark
    stand(c, 540, sink + 250, 0.8, t, gills=1, mood="scared" if t > dn else "calm", armF=0.5, armB=-0.5, walk=0.2, shiver=clamp((t - fc) / 0.3))
    glow(c, 540, sink + 60, 200, (0.7, 0.9, 1.0), 0.25 * dark)
    depth_meter(c, 950, 700, 20 + 400 * dark, 1.0, 420)
    chip(c, "JUST ONE CATCH", RED, 470, clamp(lt / 0.3) * (1 - clamp((t - ns) / 0.3)), 56)
    if t > ns - 0.2 and t < fc - 0.5: bigtxt(c, "NO SUNLIGHT", 1560, 100, WHITE, t, ns - 0.2)
    if t > fc - 0.1: bigtxt(c, "NOT THE TOP", 1610, 96, GOLD, t, fc - 0.1); lab(c, 540, 1700, "OF THE FOOD CHAIN", WHITE, clamp((t - fc - 0.3) / 0.3), 44, RED)
def s_end(c, t, lt, d):
    sea(c, t, -200, cam=0.25); seabed(c, t); school(c, t, -200, 5)
    for k, x in enumerate((110, 980)): kelp(c, x, 1720, 480, t, k0=k)
    dome(c, 260, 1700, 230, t); dome(c, 840, 1700, 250, t)
    stand(c, 540, 1560, 1.1, t, gills=1, mood="happy", armF=2.6 + 0.3 * math.sin(t * 8), armB=-0.3); breath(c, 600, 1080, t, 4)
    k = back(clamp(lt / 0.35)); c.save(); c.translate(540, 620); c.scale(k, k)
    shadow_rr(c, -430, -95, 860, 190, 50, RED); txt(c, "WOULD YOU LIVE", 0, -32, 60, WHITE); txt(c, "UNDERWATER?", 0, 38, 60, (1, 0.9, 0.85)); c.restore()
    tb = WORD(6, "tell", d=2.0)
    if t > tb - 0.2: chip(c, "COMMENT BELOW", INK, 840, clamp((t - tb + 0.2) / 0.3), 52)
FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"oxy", "heat", "planet", "city"}
def render(t):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    name, lt, d, k = scene_at(t)
    z = 1 + 0.05 * clamp(lt / max(d, 0.1)); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    FN[name](c, t, lt, d); c.identity_matrix()
    if name in FLASH and lt < 0.14: c.set_source_rgba(1, 1, 1, 0.5 * (1 - lt / 0.14)); c.paint()
    elif lt < 0.1 and k > 0: c.set_source_rgba(0, 0, 0, 0.5 * (1 - lt / 0.1)); c.paint()
    return surf
if __name__ == "__main__":
    if sys.argv[1] == "still":
        import os; os.makedirs(B + "st", exist_ok=True)
        for a in sys.argv[2:]: render(float(a)).write_to_png(B + f"st/{float(a):06.2f}.png")
    elif sys.argv[1] == "render":
        a0, a1, out = float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))): p.stdin.write(bytes(render(i / FPS).get_data()))
        p.stdin.close(); p.wait(); print("rendered", out)
