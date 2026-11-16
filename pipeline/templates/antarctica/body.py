# ------------------------------------------------------------------ scenes: IF ANTARCTICA MELTED
ICE = (0.88, 0.94, 0.98); ICE_D = (0.66, 0.78, 0.88); SEA = (0.16, 0.42, 0.70); SEA_L = (0.26, 0.58, 0.86)
CITYC = (0.34, 0.37, 0.46); SKY0 = (0.46, 0.64, 0.85); SKY1 = (0.78, 0.88, 0.96)


def coldsky(c, t, k=0.0):
    c.save(); c.identity_matrix()
    vgrad(c, 0, H, mix(SKY0, (0.12, 0.18, 0.3), k), mix(SKY1, (0.3, 0.42, 0.56), k))
    for q in range(4):
        x = (q * 300 + t * 11) % (W + 400) - 200
        ell(c, x, 420 + q * 80, 150, 32, WHITE, 0.14)
    c.restore()


def icecap(c, x, y, s, t, a=1.0, melt=0.0):
    c.save(); c.translate(x, y); SS(c, s)
    h = 1 - 0.72 * ease(clamp(melt))
    c.save(); c.scale(1, h)
    poly(c, [(-420, 0), (-330, -210), (-170, -140), (-40, -300), (110, -170), (260, -250), (420, 0)], ICE, a)
    poly(c, [(-420, 0), (-330, -210), (-170, -140), (-40, -300), (110, -170), (260, -250), (420, 0)], (1, 1, 1), a * 0.0)
    poly(c, [(-40, -300), (110, -170), (260, -250), (420, 0), (140, 0)], ICE_D, a * 0.55)
    c.restore()
    rr(c, -430, -8, 860, 40, 16, mix(ICE_D, SEA, 0.3), a)
    if melt > 0.08:
        R = random.Random(3)
        for k in range(10):
            ph = (t * 0.8 + R.random()) % 1
            ell(c, R.uniform(-380, 380), -20 - ph * 90 * h, 7, 11, SEA_L, a * (1 - ph) * melt)
    c.restore()


def sealevel(c, y, t, a=1.0):
    rect(c, 0, y, W, H - y, SEA, a)
    for k in range(4):
        yy = y + 14 + k * 26
        pts = [(x, yy + math.sin(x / 110 + t * 1.4 + k) * 8) for x in range(0, W + 40, 40)]
        line(c, pts, 6, SEA_L, a * 0.6)
    rect(c, 0, y, W, 7, mix(SEA_L, WHITE, 0.4), a)


def skyline(c, base, t, a=1.0, n=9, seed=5):
    R = random.Random(seed)
    for k in range(n):
        w = 70 + R.random() * 50; hh = 180 + R.random() * 520
        x = 40 + k * 112
        rr(c, x, base - hh, w, hh, 8, mix(CITYC, INK, 0.1 * (k % 3)), a)
        for r in range(int(hh / 60)):
            for q in range(int(w / 34)):
                if R.random() > 0.45:
                    rect(c, x + 10 + q * 34, base - hh + 20 + r * 60, 16, 22, (1, 0.88, 0.5), a * 0.75)


def ruler(c, x, ybase, h, s, t, a=1.0, mark=None):
    """vertical metre ruler, h px = 60 m"""
    c.save()
    rr(c, x - 26, ybase - h, 52, h, 14, (0.95, 0.95, 0.97), a)
    for k in range(7):
        yy = ybase - h * k / 6
        line(c, [(x - 26, yy), (x + 26, yy)], 4, (0.3, 0.33, 0.4), a)
        txt(c, f"{k * 10}", x + 66, yy + 10, 26, (0.2, 0.22, 0.28), a=a)
    if mark is not None:
        yy = ybase - h * (mark / 60)
        line(c, [(x - 60, yy), (x + 110, yy)], 7, RED, a)
        lab(c, x + 210, yy, f"{mark} m", WHITE, a, 30, RED)
    c.restore()


def globeice(c, x, y, r, t, a=1.0, hi=1.0):
    ell(c, x, y, r, r, SEA, a)
    ell(c, x - r * 0.35, y - r * 0.2, r * 0.4, r * 0.3, (0.3, 0.62, 0.38), a)
    ell(c, x + r * 0.3, y + r * 0.25, r * 0.36, r * 0.26, (0.3, 0.62, 0.38), a)
    c.save(); c.new_path(); c.arc(x, y, r, 0, TAU); c.clip()
    ell(c, x, y + r * 0.86, r * 0.62, r * 0.3, ICE, a)
    if hi > 0: glow(c, x, y + r * 0.86, r * 0.6, (1, 1, 1), 0.5 * hi)
    c.restore()
    ell(c, x - r * 0.3, y - r * 0.3, r * 0.25, r * 0.25, WHITE, a * 0.18)


def pie90(c, x, y, r, t, a=1.0, u=1.0):
    ell(c, x, y, r, r, (0.3, 0.34, 0.42), a)
    c.new_path(); c.move_to(x, y); c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + TAU * 0.9 * u)
    c.close_path(); c.set_source_rgba(*ICE, a); c.fill()
    txt(c, "90%", x, y + 16, 52, INK, a=a)


def peoplebar(c, x, y, t, a=1.0, lit=0):
    for k in range(10):
        xx = x + k * 92
        col = RED if k < lit else (0.55, 0.58, 0.66)
        ell(c, xx, y - 56, 22, 22, col, a)
        rr(c, xx - 20, y - 30, 40, 62, 14, col, a)


SC = [("hook", 0.0), ("ninety", T0(1) - 0.12), ("newmap", T0(2) - 0.12), ("notnumber", T0(3) - 0.12),
      ("tenpct", T0(4) - 0.12), ("first", T0(5) - 0.12), ("slow", T0(6) - 0.12), ("watching", T0(7) - 0.12), ("end", T0(8) - 0.12)]
STARTS = [s for _, s in SC]


def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k


def s_hook(c, t, lt, d):
    coldsky(c, t)
    m = ease(clamp((lt - 1.8) / 2.6))
    sealevel(c, 1480 - 120 * m, t)
    icecap(c, 540, 1480 - 120 * m, 1.25, t, melt=m)
    chip(c, "IF ANTARCTICA MELTED", INK, 560, clamp(lt / 0.3), 50)
    mt = W_(0, "meters")
    if t > mt - 0.4:
        u = back(clamp((t - mt + 0.4) / 0.35)); c.save(); c.translate(540, 900); SS(c, u)
        shadow_rr(c, -340, -110, 680, 220, 54, RED)
        txt(c, "+58 m", 0, -8, 96, WHITE); txt(c, "OF SEA LEVEL", 0, 62, 32, (1, 0.9, 0.86)); c.restore()


def s_ninety(c, t, lt, d):
    coldsky(c, t, 0.25)
    globeice(c, 540, 860, 320, t, hi=clamp((lt - 0.4) / 0.5))
    pie90(c, 540, 1520, 200, t, clamp((lt - 1.0) / 0.4), ease(clamp((lt - 1.0) / 1.0)))
    lab(c, 540, 1790, "OF ALL THE ICE ON EARTH", INK, clamp((lt - 1.6) / 0.4), 36, WHITE)
    chip(c, "NOWHERE ELSE IS CLOSE", INK, 560, clamp(lt / 0.3), 46)


def s_newmap(c, t, lt, d):
    coldsky(c, t, 0.3)
    u = ease(clamp((lt - 0.5) / 1.6))
    skyline(c, 1700, t)
    sealevel(c, 1700 - 520 * u, t, 0.9)
    ruler(c, 960, 1700, 620, 1.0, t, 0.9, mark=58 if u > 0.85 else None)
    chip(c, "NOT A FLOOD", INK, 560, clamp(lt / 0.3), 50)
    nm = W_(2, "map")
    if t > nm - 0.3: bigtxt(c, "A NEW MAP", 1860, 62, GOLD, t, nm - 0.3)


def s_notnumber(c, t, lt, d):
    coldsky(c, t, 0.45)
    k = back(clamp(lt / 0.4))
    c.save(); c.translate(540, 900); SS(c, k)
    shadow_rr(c, -330, -120, 660, 240, 56, (0.3, 0.33, 0.42))
    txt(c, "58 m", 0, 20, 110, WHITE); c.restore()
    u = clamp((lt - 1.1) / 0.4)
    if u > 0:
        line(c, [(200, 760), (880, 1040)], 16, RED, u)
        c.save(); c.translate(540, 1400); SS(c, back(u))
        shadow_rr(c, -470, -84, 940, 168, 48, RED); txt(c, "NOT THE NUMBER THAT MATTERS", 0, 20, 44, WHITE); c.restore()


def s_tenpct(c, t, lt, d):
    coldsky(c, t, 0.2)
    lit = min(1, int(clamp((lt - 0.8) / 1.2) * 1.6))
    peoplebar(c, 110, 980, t, 1.0, lit=1 if lt > 1.0 else 0)
    k = back(clamp((lt - 1.6) / 0.4))
    if k > 0:
        c.save(); c.translate(540, 1340); SS(c, k)
        shadow_rr(c, -460, -110, 920, 220, 54, RED)
        txt(c, "1 IN 10 PEOPLE", 0, -22, 60, WHITE); txt(c, "live under 10 metres", 0, 46, 36, (1, 0.9, 0.86)); c.restore()
    skyline(c, 1920, t, 0.5, 7, 9)
    sealevel(c, 1800, t, 0.85)
    chip(c, "HERE IS THE NUMBER", INK, 560, clamp(lt / 0.3), 48)


def s_first(c, t, lt, d):
    coldsky(c, t, 0.35)
    skyline(c, 1760, t)
    u = ease(clamp((lt - 0.4) / 1.8))
    sealevel(c, 1760 - 120 * u, t, 0.92)
    ruler(c, 960, 1760, 620, 1.0, t, 0.9, mark=10 if u > 0.8 else None)
    k = back(clamp((lt - 1.4) / 0.4))
    if k > 0:
        c.save(); c.translate(500, 760); SS(c, k)
        shadow_rr(c, -440, -90, 880, 180, 50, (0.75, 0.2, 0.15))
        txt(c, "IT LANDS IN THE", 0, -22, 40, WHITE); txt(c, "FIRST FEW METRES", 0, 40, 48, WHITE); c.restore()
    chip(c, "NOT WAITING AT THE END", INK, 560, clamp(lt / 0.3), 46)


def s_slow(c, t, lt, d):
    coldsky(c, t, 0.3)
    for k, (big, sub, col, at) in enumerate((("THOUSANDS", "of years for the full melt", (0.3, 0.45, 0.68), 0.3),
                                             ("THE FIRST METRE", "does not", RED, 2.0))):
        u = back(clamp((lt - at) / 0.4))
        if u <= 0: continue
        c.save(); c.translate(540, 900 + k * 330); SS(c, u)
        shadow_rr(c, -470, -110, 940, 220, 54, col)
        txt(c, big, 0, -20, 56, WHITE); txt(c, sub, 0, 46, 34, (0.95, 0.95, 0.98)); c.restore()
    icecap(c, 540, 1760, 0.6, t, 0.9, melt=ease(clamp((lt - 0.4) / 3.0)))
    chip(c, "TWO DIFFERENT CLOCKS", INK, 560, clamp(lt / 0.3), 46)


def s_watching(c, t, lt, d):
    coldsky(c, t, 0.4)
    skyline(c, 1760, t)
    sealevel(c, 1700, t, 0.92)
    ruler(c, 960, 1760, 620, 1.0, t, 0.9, mark=1)
    k = back(clamp((lt - 0.4) / 0.4))
    if k > 0:
        c.save(); c.translate(500, 860); SS(c, k)
        shadow_rr(c, -450, -120, 900, 240, 56, (0.1, 0.12, 0.18))
        txt(c, "NOBODY IS PLANNING", 0, -36, 42, (0.8, 0.84, 0.9))
        txt(c, "FOR 58", 0, 36, 62, WHITE); c.restore()
    u = back(clamp((lt - 2.0) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 1300); SS(c, u)
        shadow_rr(c, -420, -70, 840, 140, 42, RED); txt(c, "THEY WATCH THE FIRST ONE", 0, 18, 42, WHITE); c.restore()


def s_end(c, t, lt, d):
    coldsky(c, t, 0.2)
    # a hill with a little house
    poly(c, [(0, 1920), (240, 1340), (540, 1180), (840, 1360), (1080, 1920)], (0.34, 0.54, 0.32))
    rr(c, 470, 1040, 150, 120, 12, (0.86, 0.84, 0.8))
    poly(c, [(450, 1040), (545, 950), (640, 1040)], (0.72, 0.28, 0.22))
    sealevel(c, 1700, t, 0.9)
    guy(c, 760, 1500, 0.62, t, face=-1, mood="happy", armF=1.2)
    k = back(clamp(lt / 0.35))
    c.save(); c.translate(540, 700); SS(c, k)
    shadow_rr(c, -490, -140, 980, 280, 54, RED)
    txt(c, "THAT BORING HILL", 0, -46, 54, WHITE); txt(c, "IS ABOUT TO GET EXPENSIVE", 0, 34, 42, (1, 0.92, 0.88)); c.restore()
    u = back(clamp((lt - 0.7) / 0.4))
    if u > 0: chip(c, "WHAT SHOULD I EXPLAIN NEXT?", INK, 1840, u, 42)


FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"notnumber", "tenpct"}


def render(t):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    name, lt, d, k = scene_at(t)
    z = 1 + 0.05 * clamp(lt / max(d, 0.1)); c.translate(W / 2, H / 2); SS(c, z); c.translate(-W / 2, -H / 2)
    FN[name](c, t, lt, d); c.identity_matrix()
    if name in FLASH and lt < 0.14: c.set_source_rgba(1, 1, 1, 0.4 * (1 - lt / 0.14)); c.paint()
    elif lt < 0.1 and k > 0: c.set_source_rgba(0, 0, 0, 0.5 * (1 - lt / 0.1)); c.paint()
    return surf


if __name__ == "__main__":
    if sys.argv[1] == "still":
        import os; os.makedirs(B + "st", exist_ok=True)
        for a in sys.argv[2:]: render(float(a)).write_to_png(B + f"st/{float(a):06.2f}.png")
    else:
        a0, a1, out = float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))): p.stdin.write(bytes(render(i / FPS).get_data()))
        p.stdin.close(); p.wait(); print("rendered", out)
