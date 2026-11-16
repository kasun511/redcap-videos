# ================================================================== Ep 10 "Eleven Days" — scenes
WATER = (0.22, 0.58, 0.92); CLAY = (0.62, 0.52, 0.36)
AUR = (0.3, 0.95, 0.55); AUR2 = (0.1, 0.65, 0.45)
START_BUDGET = 1_552_000
EV = [(W_(2, "900", 7.0), -900, "-$900", "TRANSFER SWITCH"),
      (W_(4, "1,400", 8.4), -1_400, "-$1,400", "SURGE ARRESTORS")]
DAYCHG = [(0, 11), (T0(2) + 2.2, 9), (T0(3) + 2.2, 7), (T0(4) + 2.2, 5), (T0(5) + 2.2, 3), (T0(6) + 2.0, 1), (T0(7) + 1.0, 0)]


def pylon(c, x, y, s, t, a=1.0, zap=0.0):
    c.save(); c.translate(x, y); SS(c, s)
    line(c, [(-70, 0), (-26, -420)], 14, (0.42, 0.44, 0.5), a); line(c, [(70, 0), (26, -420)], 14, (0.42, 0.44, 0.5), a)
    for k in range(5):
        yy = -70 - k * 70; w = 62 - k * 8
        line(c, [(-w, yy), (w, yy)], 9, (0.42, 0.44, 0.5), a)
        line(c, [(-w, yy), (w, yy - 70)], 6, (0.42, 0.44, 0.5), a * 0.8)
    line(c, [(-130, -430), (130, -430)], 14, (0.42, 0.44, 0.5), a)
    if zap > 0:
        for k in range(3):
            boltzap(c, -90 + k * 90, -470 + 14 * math.sin(t * 20 + k), 1.3, (0.6, 1.0, 0.8), a * zap * (0.5 + 0.5 * math.sin(t * 26 + k)))
    c.restore()


def wirespan(c, y, t, a=1.0, surge=0.0):
    for k in range(3):
        yy = y + k * 34
        line(c, [(0, yy), (W, yy + 26 * math.sin(k))], 7, (0.2, 0.2, 0.25), a)
        if surge > 0:
            ph = (t * 1.6 + k / 3) % 1
            ell(c, W * ph, yy + 26 * math.sin(k) * ph, 20, 20, (0.6, 1.0, 0.8), a * surge)
            glow(c, W * ph, yy, 90, (0.4, 1.0, 0.7), 0.5 * a * surge)


def transferswitch(c, x, y, s, t, thrown=0.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -170, -220, 340, 440, 30, (0.55, 0.58, 0.64), a); rr(c, -140, -190, 280, 300, 22, (0.2, 0.21, 0.26), a)
    for k, (nm, on) in enumerate([("GRID", 1 - thrown), ("SOLAR", thrown)]):
        yy = -130 + k * 110
        ell(c, -90, yy, 26, 26, mix((0.3, 0.3, 0.34), GREEN if k else RED, on), a)
        txt(c, nm, -40, yy + 10, 34, WHITE, a=a, anchor="l")
    ang = -0.7 + 1.4 * ease(clamp(thrown))
    c.save(); c.translate(0, 60); c.rotate(ang); rr(c, -16, -110, 32, 120, 14, (0.9, 0.35, 0.15), a); ell(c, 0, -110, 26, 26, (0.95, 0.6, 0.2), a); c.restore()
    txt(c, "TRANSFER SWITCH", 0, 190, 30, (0.75, 0.78, 0.84), a=a)
    c.restore()


def faraday(c, x, y, s, t, lid=0.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -210, -180, 420, 360, 26, (0.58, 0.61, 0.67), a)
    rr(c, -182, -150, 364, 300, 18, (0.74, 0.62, 0.42), a)   # cardboard liner
    items = [("RADIO", (0.25, 0.27, 0.32), -110), ("LAPTOP", (0.3, 0.32, 0.38), 0), ("CTRL", (0.2, 0.45, 0.8), 110)]
    for nm, col, xx in items:
        rr(c, xx - 48, -40, 96, 110, 14, col, a); txt(c, nm, xx, 100, 20, WHITE, a=a)
    c.save(); c.translate(0, -180); c.rotate(-1.0 * (1 - ease(clamp(lid))))
    rr(c, -220, -46, 440, 46, 18, (0.5, 0.53, 0.59), a)
    rr(c, -220, -14, 440, 14, 7, (0.85, 0.55, 0.2), a)       # copper tape
    c.restore()
    txt(c, "COPPER TAPE SEAL", 0, 240, 28, (0.85, 0.6, 0.3), a=a)
    c.restore()


def arrestor(c, x, y, s, t, on=0.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -54, -100, 108, 200, 20, (0.2, 0.55, 0.3) if on > 0.5 else (0.4, 0.42, 0.48), a)
    for k in range(3): line(c, [(-40, -60 + k * 60), (40, -60 + k * 60)], 8, (0.1, 0.12, 0.15), a)
    line(c, [(0, -100), (0, -160)], 10, (0.5, 0.53, 0.6), a); line(c, [(0, 100), (0, 170)], 10, (0.5, 0.53, 0.6), a)
    if on > 0.5: boltzap(c, 0, 0, 1.0, GOLD, a * (0.5 + 0.5 * math.sin(t * 9)))
    c.restore()


def jerrycan(c, x, y, s, a=1.0, full=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -50, -70, 100, 140, 16, (0.75, 0.35, 0.15), a)
    hh = 110 * clamp(full); rr(c, -36, 56 - hh, 72, hh, 10, WATER, a)
    rr(c, -22, -92, 44, 26, 10, (0.6, 0.28, 0.12), a)
    c.restore()


def shelfrow(c, y, t, stock=0.0, a=1.0):
    rect(c, 90, y - 230, 26, 246, (0.3, 0.32, 0.36), a); rect(c, 964, y - 230, 26, 246, (0.3, 0.32, 0.36), a)
    rect(c, 90, y, 900, 18, (0.42, 0.44, 0.48), a)
    rect(c, 116, y - 230, 848, 230, (0.17, 0.17, 0.2), a * 0.8)
    n = int(10 * clamp(stock))
    for k in range(n):
        rr(c, 130 + k * 84, y - 96, 62, 96, 10, [(0.8, 0.5, 0.2), (0.3, 0.55, 0.8), (0.5, 0.6, 0.3)][k % 3], a)


def auroras(c, t, k=1.0):
    vgrad(c, 0, 1100, (0.02, 0.05, 0.09), mix((0.05, 0.1, 0.16), AUR2, 0.3 * k))
    for b in range(6):
        c.save()
        for q in range(26):
            xx = q * 44; ph = math.sin(t * 0.9 + b * 1.3 + q * 0.3)
            h = (220 + 150 * ph) * k
            c.set_source_rgba(AUR[0], AUR[1], AUR[2], 0.055 * k)
            c.rectangle(xx, 120 + b * 40 + 60 * ph, 44, h); c.fill()
        c.restore()


def valley(c, t, lit=1.0, ours=1.0):
    rect(c, 0, 1100, W, H - 1100, (0.08, 0.12, 0.1))
    for k in range(7):
        x = 60 + k * 150; y = 1420 + 90 * math.sin(k * 1.9)
        rr(c, x - 54, y - 70, 108, 90, 10, (0.14, 0.15, 0.18))
        poly(c, [(x - 66, y - 70), (x, y - 126), (x + 66, y - 70)], (0.1, 0.11, 0.14))
        if lit > 0:
            rr(c, x - 24, y - 50, 48, 40, 6, mix((0.12, 0.12, 0.14), (1.0, 0.85, 0.45), lit))
            glow(c, x, y - 30, 120, (1, 0.85, 0.5), 0.3 * lit)
    x, y = 540, 1780
    rr(c, x - 110, y - 130, 220, 150, 14, (0.18, 0.2, 0.24))
    poly(c, [(x - 130, y - 130), (x, y - 230), (x + 130, y - 130)], (0.13, 0.14, 0.18))
    rr(c, x - 44, y - 100, 88, 70, 8, mix((0.12, 0.12, 0.14), (1.0, 0.88, 0.5), ours))
    if ours > 0: glow(c, x, y - 64, 240, (1, 0.85, 0.5), 0.4 * ours)


def transformer_blow(c, x, y, t, at, a=1.0):
    u = clamp((t - at) / 0.9)
    rr(c, x - 50, y - 70, 100, 140, 18, (0.42, 0.44, 0.5), a)
    if t < at: return
    r = 90 + 420 * ease(u)
    glow(c, x, y, r, (1, 0.8, 0.35), (1 - u) * 0.9)
    R = random.Random(7)
    for k in range(14):
        an = R.uniform(0, TAU); dd = r * R.uniform(0.3, 1.0)
        ell(c, x + math.cos(an) * dd, y + math.sin(an) * dd, 14 * (1 - u) + 4, 14 * (1 - u) + 4, (1, 0.6 + 0.3 * R.random(), 0.2), (1 - u))


# ================================================================== scenes
SC = [("clock", 0.0), ("grid", T0(1) - 0.12), ("switch", T0(2) - 0.12), ("cage", T0(3) - 0.12),
      ("mia0", MIA[0] - 0.12), ("surge", T0(4) - 0.12), ("fill", T0(5) - 0.12), ("mia1", MIA[1] - 0.12),
      ("town", T0(6) - 0.12), ("sky", T0(7) - 0.12), ("mia2", MIA[2] - 0.12), ("dark", T0(8) - 0.12),
      ("alive", T0(9) - 0.12), ("mia3", MIA[3] - 0.12), ("tally", T0(10) - 0.12), ("end", T0(11) - 0.3)]
STARTS = [s for _, s in SC]


def s_clock(c, t, lt, d):
    rect(c, 0, 0, W, H, (0.07, 0.07, 0.1)); glow(c, 540, 1150, 700, (1, 0.45, 0.2), 0.2)
    shadow_rr(c, 410, 300, 260, 76, 38, RED); txt(c, "PART 10", 540, 338, 46, WHITE)
    chip(c, "THE FINALE", GOLD, 520, clamp(lt / 0.3), 48)
    u = clamp((lt - 0.5) / 0.4)
    txt(c, "300 DAYS", 540, 1060, 86, (0.5, 0.5, 0.56), stroke=10)
    if u > 0: line(c, [(230, 1040), (850, 1040)], 12, RED, u)
    el = W_(0, "days", 1.1)
    if t > el - 0.3:
        k = back(clamp((t - el + 0.3) / 0.35)); c.save(); c.translate(540, 1300); SS(c, k)
        txt(c, "11 DAYS", 0, 0, 160, RED, stroke=18); c.restore()
    person(c, 300, 1880, 0.8, "red", face=1, t=t, mood="scared")
    person(c, 790, 1880, 0.78, "mia", face=-1, t=t, mood="scared")
    hud(c, t, feats=False)


def s_grid(c, t, lt, d):
    vgrad(c, 0, 1200, (0.1, 0.13, 0.2), (0.3, 0.2, 0.22))
    rect(c, 0, 1200, W, H - 1200, (0.2, 0.3, 0.16))
    su = clamp((lt - 1.8) / 0.5)
    wirespan(c, 760, t, 1.0, su)
    pylon(c, 250, 1200, 0.85, t, 1.0, su); pylon(c, 870, 1200, 0.85, t, 1.0, su)
    if t > W_(1, "antenna", 4.2) - 0.3: bigtxt_(c, "EVERY LINE IS AN ANTENNA", 1180, 62, (0.5, 1.0, 0.7), t, W_(1, "antenna", 4.2) - 0.3)
    ck = W_(1, "cooked", 6.6)
    if t > ck - 0.2:
        u = back(clamp((t - ck + 0.2) / 0.3)); c.save(); c.translate(540, 1420); SS(c, u)
        shadow_rr(c, -330, -58, 660, 116, 34, (0.6, 0.15, 0.13)); txt(c, "PLUGGED IN = COOKED", 0, 6, 46, WHITE); c.restore()
    chip(c, "PROBLEM 1 · THE GRID", RED, 520, clamp(lt / 0.3), 46)
    hud(c, t, feats=False)


def s_switch(c, t, lt, d):
    interior(c, t, 0.75)
    th = ease(clamp((lt - 1.6) / 0.8))
    transferswitch(c, 560, 1180, 1.0, t, th)
    if th > 0.6: person(c, 230, 1800, 0.76, "red", face=-1, t=t, mood="calm")
    fixcard(c, t, STARTS[2] + 0.1, "CUT OFF THE GRID")
    pn = W_(2, "panels", 9.6)
    if t > pn - 0.3: lab(c, 540, 1760, "OUR PANELS, OR NOTHING", WHITE, clamp((t - pn + 0.3) / 0.3), 34, GREEN)
    hud(c, t)


def s_cage(c, t, lt, d):
    dark_room(c, t, 0.85)
    faraday(c, 540, 1200, 0.95, t, clamp((lt - 2.8) / 0.8))
    fixcard(c, t, STARTS[3] + 0.1, "FARADAY CAGE")
    chip(c, "A STEEL BIN. THAT IS IT.", INK, 520, clamp((lt - 0.4) / 0.3), 42)
    hud(c, t)


def s_mia0(c, t, lt, d):
    dark_room(c, t, 0.85); faraday(c, 760, 1180, 0.6, t, 0.4)
    person(c, 330, 1800, 1.0, "mia", face=1, t=t, mood="calm", talk=mtalk(t))
    hud(c, t)


def s_surge(c, t, lt, d):
    vgrad(c, 0, 1100, (0.12, 0.16, 0.26), (0.25, 0.3, 0.38)); rect(c, 0, 1100, W, H - 1100, (0.2, 0.3, 0.16))
    panel(c, 300, 820, 1.0, 1.0, 0.0, 0.25); panel(c, 760, 820, 1.0, 1.0, 0.0, 0.25)
    on = clamp((lt - 1.8) / 0.4)
    wirespan(c, 1120, t, 0.8, 0.4 * (1 - on))
    arrestor(c, 250, 1420, 0.9, t, on); arrestor(c, 830, 1420, 0.9, t, on)
    if on > 0.5:
        check(c, 250, 1250, 46, clamp((lt - 2.2) / 0.3)); check(c, 830, 1250, 46, clamp((lt - 2.4) / 0.3))
    fixcard(c, t, STARTS[5] + 0.1, "SURGE ARRESTORS")
    chip(c, "THE WIRES PICK UP THE SURGE", INK, 520, clamp(lt / 0.3), 42)
    hud(c, t)


def s_fill(c, t, lt, d):
    interior(c, t, 0.7)
    u = ease(clamp((lt - 0.6) / 2.4))
    n = int(12 * u)
    for k in range(n):
        jerrycan(c, 190 + (k % 6) * 140, 1200 + (k // 6) * 220, 0.78, 1.0, 1.0)
    cnt = f"{min(40, int(40 * u))} JERRY CANS"
    lab(c, 540, 1760, cnt, WHITE, clamp(lt / 0.4), 40, (0.2, 0.45, 0.8))
    fixcard(c, t, STARTS[6] + 0.1, "FILL EVERYTHING")
    hud(c, t)


def s_mia1(c, t, lt, d):
    interior(c, t, 0.7)
    for k in range(6): jerrycan(c, 760 + (k % 3) * 130, 1300 + (k // 3) * 190, 0.62)
    person(c, 300, 1800, 1.0, "mia", face=1, t=t, mood="worried", talk=mtalk(t))
    hud(c, t)


def s_town(c, t, lt, d):
    rect(c, 0, 0, W, 1150, (0.14, 0.15, 0.2)); rect(c, 0, 1150, W, H - 1150, (0.22, 0.22, 0.26))
    for k in range(3): shelfrow(c, 1000 + k * 300, t, max(0.0, 0.15 - 0.15 * clamp(lt / 1.2)))
    chip(c, "DAY 10 · THE SHELVES ARE GONE", RED, 520, clamp(lt / 0.3), 44)
    person(c, 540, 1900, 0.8, "red", face=1, t=t, mood="worried")
    hb = W_(6, "home", 7.6)
    if t > hb - 0.3: bigtxt_(c, "WE BUY NOTHING", 1700, 72, GOLD, t, hb - 0.3)
    hud(c, t)


def s_sky(c, t, lt, d):
    k = clamp((lt - 0.8) / 1.6)
    auroras(c, t, 0.25 + 0.75 * k)
    rect(c, 0, 1500, W, H - 1500, (0.06, 0.1, 0.09))
    for q in range(6):
        x = 70 + q * 180; rr(c, x - 50, 1560, 100, 90, 10, (0.1, 0.11, 0.14))
    person(c, 380, 1880, 0.8, "red", face=1, t=t, mood="scared")
    person(c, 700, 1880, 0.78, "mia", face=-1, t=t, mood="scared")
    chip(c, "DAY 11 · 4:12 AM", INK, 520, clamp(lt / 0.3), 50)
    gr = W_(7, "green", 4.2)
    if t > gr - 0.3: bigtxt_(c, "THE SKY TURNS GREEN", 1180, 72, AUR, t, gr - 0.3)
    hud(c, t, feats=False)


def s_mia2(c, t, lt, d):
    auroras(c, t, 1.0); rect(c, 0, 1500, W, H - 1500, (0.06, 0.1, 0.09))
    person(c, 540, 1900, 1.0, "mia", face=1, t=t, mood="scared", talk=mtalk(t))
    hud(c, t, feats=False)


def s_dark(c, t, lt, d):
    auroras(c, t, 0.9)
    at = STARTS[11] + 0.9
    valley(c, t, lit=1.0 - clamp((t - at - 0.5) / 0.3), ours=1.0 - clamp((t - at - 0.5) / 0.3))
    transformer_blow(c, 880, 1240, t, at)
    c.save(); c.identity_matrix()
    fl = clamp((t - at) / 0.1) * (1 - clamp((t - at) / 0.5))
    c.set_source_rgba(1, 0.9, 0.6, 0.7 * fl); c.paint(); c.restore()
    if t > at + 0.9: bigtxt_(c, "THE WHOLE VALLEY", 760, 72, (0.7, 0.72, 0.8), t, at + 0.9)
    chip(c, "THE TRANSFORMER WENT", RED, 520, clamp(lt / 0.3), 46)
    hud(c, t, feats=False)


def s_alive(c, t, lt, d):
    auroras(c, t, 0.55)
    valley(c, t, lit=0.0, ours=clamp((lt - 0.4) / 0.6))
    on = clamp((lt - 0.4) / 0.6)
    items = [("FRIDGE", W_(9, "hummed", 3.2)), ("TAP", W_(9, "ran", 4.4)), ("RADIO", W_(9, "worked", 7.0))]
    for k, (nm, at) in enumerate(items):
        v = back(clamp((t - at + 0.2) / 0.3))
        if v <= 0: continue
        c.save(); c.translate(250 + k * 290, 760); SS(c, v)
        shadow_rr(c, -130, -52, 260, 104, 30, GREEN); txt(c, nm, 0, 6, 38, WHITE); c.restore()
    if on > 0.6: bigtxt_(c, "OURS DID NOT", 1120, 92, GOLD, t, STARTS[12] + 0.6)
    hud(c, t)


def s_mia3(c, t, lt, d):
    auroras(c, t, 0.45); valley(c, t, lit=0.0, ours=1.0)
    person(c, 540, 1900, 1.0, "mia", face=1, t=t, mood="happy", talk=mtalk(t))
    hud(c, t)


def s_tally(c, t, lt, d):
    rect(c, 0, 0, W, H, (0.05, 0.05, 0.08)); glow(c, 540, 1000, 700, (1, 0.6, 0.2), 0.18)
    rows = [("$1.6 MILLION", "SPENT", GOLD, W_(10, "million", 1.4)),
            ("220 DAYS", "OF BUILDING", (0.4, 0.7, 1.0), W_(10, "days", 3.6)),
            ("10 EPISODES", "OF BEING CALLED PARANOID", GREEN, W_(10, "episodes", 5.0))]
    for k, (big, sub, col, at) in enumerate(rows):
        v = back(clamp((t - at + 0.25) / 0.35))
        if v <= 0: continue
        y = 760 + k * 300
        c.save(); c.translate(540, y); SS(c, v)
        shadow_rr(c, -450, -110, 900, 220, 44, (0.12, 0.13, 0.18))
        txt(c, big, 0, -14, 82, col); txt(c, sub, 0, 62, 32, (0.75, 0.76, 0.82)); c.restore()


def s_end(c, t, lt, d):
    rect(c, 0, 0, W, H, (0.03, 0.03, 0.05)); glow(c, 540, 900, 620, (1, 0.6, 0.2), 0.24)
    k = back(clamp(lt / 0.35)); a = clamp(lt / 0.2)
    c.save(); c.translate(540, 820); SS(c, k)
    shadow_rr(c, -430, -150, 860, 300, 60, RED, a)
    txt(c, "SERIES", 0, -54, 96, WHITE, a=a); txt(c, "COMPLETE", 0, 62, 96, WHITE, a=a)
    c.restore()
    u = back(clamp((lt - 0.5) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 1280); SS(c, u)
        shadow_rr(c, -470, -90, 940, 180, 44, (0.12, 0.13, 0.18), a)
        txt(c, "WHICH BUILD WOULD YOU", 0, -22, 44, WHITE, a=a); txt(c, "HAVE DONE FIRST?", 0, 44, 44, GOLD, a=a); c.restore()


FN = {n: globals()["s_" + n] for n, _ in SC}
CUT_FLASH = {"grid", "switch", "cage", "surge", "town", "sky", "dark", "alive"}
