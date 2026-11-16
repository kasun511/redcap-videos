# ------------------------------------------------------------------ scenes: EVERYONE JUMPS
GRASS = (0.42, 0.66, 0.34)
def field(c, t, k=0.0):
    c.save(); c.identity_matrix(); vgrad(c, 0, H, mix(DAY0, SKYD, k), mix(DAY1, SKYD2, k))
    if k > 0.25: starfield(c, t, (k - 0.25) / 0.75)
    rect(c, 0, 1560, W, H - 1560, mix(GRASS, (0.2, 0.24, 0.2), k)); rect(c, 0, 1560, W, 16, mix((0.33, 0.55, 0.26), (0.16, 0.2, 0.16), k))
    c.restore()
SC = [("hook", 0.0), ("gather", T0(1) - 0.12), ("maths", T0(2) - 0.12), ("shove", T0(3) - 0.12),
      ("atom", T0(4) - 0.12), ("land", T0(5) - 0.12), ("quake", T0(6) - 0.12), ("home", T0(7) - 0.12), ("end", T0(8) - 0.12)]
STARTS = [s for _, s in SC]
def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k
def s_hook(c, t, lt, d):
    field(c, t)
    jp = clamp((lt - 0.5) / 0.3)
    crowdrow(c, 1560, 11, t, 0.62, jump=jp, seed=2)
    crowdrow(c, 1700, 9, t + 0.4, 0.78, jump=jp, seed=5)
    guy(c, 540, 1880 - 70 * abs(math.sin(t * 2.2)) * jp, 1.0, t, face=1, jacket=HOOD, scarf=False, mood="happy", armF=2.4, armB=-2.4)
    chip(c, "WHAT IF...", RED, 520, clamp(lt / 0.3), 58)
    lab(c, 540, 650, "8 BILLION PEOPLE JUMP AT ONCE?", INK, clamp((lt - 0.25) / 0.3), 38, WHITE)
    mv = W_(0, "move", 4.6)
    if t > mv - 0.3: bigtxt(c, "WOULD EARTH MOVE?", 900, 72, GOLD, t, mv - 0.3)
def s_gather(c, t, lt, d):
    field(c, t)
    u = ease(clamp((lt - 0.3) / 1.6))
    earthball(c, 540, 820, 230, t)
    for k in range(5):
        an = -2.3 + k * 0.45; r0 = 420 - 240 * u
        ell(c, 540 + math.cos(an) * r0, 820 + math.sin(an) * r0 * 0.7, 16, 16, RED, 0.9)
    crowdrow(c, 1680, 13, t, 0.52, jump=0.0, seed=9)
    crowdrow(c, 1830, 11, t + 0.3, 0.66, jump=0.0, seed=4)
    cd = W_(1, "down", 3.6)
    if t > cd - 0.3:
        n = max(1, 3 - int((t - cd + 0.3) / 0.5)); clockface(c, 540, 1240, 120, str(n), clamp((t - cd + 0.3) / 0.25), GOLD)
    chip(c, "EVERYONE IN ONE PLACE", INK, 520, clamp(lt / 0.3), 48)
def s_maths(c, t, lt, d):
    space(c, t)
    hu = W_(2, "500", 3.0); ew = W_(2, "6,", 6.0)
    if t > hu - 0.4:
        u = back(clamp((t - hu + 0.4) / 0.35)); c.save(); c.translate(300, 1020); SS(c, u)
        shadow_rr(c, -240, -150, 480, 300, 34, (0.14, 0.15, 0.2)); txt(c, "ALL HUMANS", 0, -90, 34, (0.8, 0.82, 0.88))
        txt(c, "5 x 10", 0, 0, 64, WHITE); txt(c, "11", 118, -30, 38, GOLD); txt(c, "kg", 0, 70, 36, (0.8, 0.82, 0.88)); c.restore()
    if t > ew - 0.4:
        u = back(clamp((t - ew + 0.4) / 0.35)); c.save(); c.translate(790, 1020); SS(c, u)
        shadow_rr(c, -240, -150, 480, 300, 34, (0.14, 0.15, 0.2)); txt(c, "THE EARTH", 0, -90, 34, (0.8, 0.82, 0.88))
        txt(c, "6 x 10", 0, 0, 64, WHITE); txt(c, "24", 118, -30, 38, GOLD); txt(c, "kg", 0, 70, 36, (0.8, 0.82, 0.88)); c.restore()
    crowdrow(c, 1560, 9, t, 0.52, seed=3)
    earthball(c, 540, 1800, 240, t)
    chip(c, "LET'S DO THE MATHS", INK, 520, clamp(lt / 0.3), 48)
def s_shove(c, t, lt, d):
    space(c, t)
    earthball(c, 720, 1000, 320, t)
    u = ease(clamp((lt - 0.4) / 1.4))
    crowdrow(c, 1560, 9, t, 0.56, seed=7)
    arrowline(c, 170, 1000, 330 + 60 * u, 1000, GOLD, 16, clamp(lt / 0.4))
    tr = W_(3, "trillion", 2.2)
    if t > tr - 0.3: bigtxt(c, "10 TRILLION x HEAVIER", 700, 76, RED, t, tr - 0.3)
    if lt > 1.6: lab(c, 540, 1300, "GOOD LUCK", WHITE, clamp((lt - 1.6) / 0.3), 42, INK)
def s_atom(c, t, lt, d):
    space(c, t)
    off = 26 * math.sin(clamp((lt - 0.8) / 2.4) * 3.1)
    earthball(c, 540 + off, 1060, 320, t)
    at = W_(4, "atom", 3.4)
    if t > at - 0.4:
        u = clamp((t - at + 0.4) / 0.3)
        lab(c, 540, 1480, "ONE ATOM WIDE", WHITE, u, 40, GOLD)
    bk = W_(4, "back", 5.6)
    if t > bk - 0.3: bigtxt(c, "AND STRAIGHT BACK", 1700, 68, WHITE, t, bk - 0.3)
    chip(c, "IT DOES MOVE...", INK, 520, clamp(lt / 0.3), 50)
def s_land(c, t, lt, d):
    field(c, t, 0.08)
    crowdrow(c, 1560, 11, t, 0.62, jump=clamp(1 - lt / 0.8), seed=2)
    crowdrow(c, 1700, 9, t + 0.4, 0.78, jump=clamp(1 - lt / 0.8), seed=5)
    nt = W_(5, "not", 2.2)
    bigtxt(c, "THE JUMP: BORING", 700, 74, (0.7, 0.72, 0.8), t, STARTS[5] + 0.1)
    if t > nt - 0.3: bigtxt(c, "THE LANDING: NOT", 860, 80, RED, t, nt - 0.3)
def s_quake(c, t, lt, d):
    sh = clamp((lt - 0.6) / 0.3) * (1 - clamp((lt - 2.6) / 0.6))
    field(c, t, 0.12)
    c.save()
    if sh > 0: c.translate(12 * sh * math.sin(t * 40), 9 * sh * math.cos(t * 37))
    crowdrow(c, 1620, 13, t, 0.56, seed=2); crowdrow(c, 1790, 11, t + 0.4, 0.7, seed=5)
    quakeicon(c, 540, 1420, 1.0, t, sh)
    c.restore()
    seismo(c, 540, 980, 820, 280, t, sh)
    mg = W_(6, "magnitude", 3.2)
    if t > mg - 0.3: bigtxt(c, "MAGNITUDE 4", 680, 92, RED, t, mg - 0.3)
    bd = W_(6, "bad", 6.4)
    if t > bd - 0.3: lab(c, 540, 1300, "A VERY BAD DAY", WHITE, clamp((t - bd + 0.3) / 0.3), 44, RED)
def s_home(c, t, lt, d):
    field(c, t, 0.05)
    crowdrow(c, 1480, 15, t, 0.44, seed=2); crowdrow(c, 1620, 13, t + 0.3, 0.56, seed=5)
    crowdrow(c, 1780, 11, t + 0.6, 0.7, seed=8); crowdrow(c, 1900, 9, t + 0.9, 0.86, seed=11)
    chip(c, "THE REAL DISASTER", RED, 520, clamp(lt / 0.3), 52)
    hm = W_(7, "home", 5.6)
    if t > hm - 0.4: bigtxt(c, "NOW GET HOME", 880, 92, GOLD, t, hm - 0.4)
    if t > hm + 0.3: lab(c, 540, 1030, "8 BILLION PEOPLE. ONE COUNTRY.", WHITE, clamp((t - hm - 0.3) / 0.3), 36, INK)
def s_end(c, t, lt, d):
    field(c, t, 0.15); crowdrow(c, 1760, 11, t, 0.66, jump=0.5, seed=5)
    earthball(c, 540, 980, 200, t)
    k = back(clamp(lt / 0.35)); c.save(); c.translate(540, 560); SS(c, k)
    shadow_rr(c, -430, -95, 860, 190, 50, RED); txt(c, "WHAT SHOULD I", 0, -32, 60, WHITE); txt(c, "EXPLAIN NEXT?", 0, 38, 60, (1, 0.9, 0.85)); c.restore()
    tb = W_(8, "tell", 1.6)
    if t > tb - 0.2: chip(c, "COMMENT BELOW", INK, 1320, clamp((t - tb + 0.2) / 0.3), 52)
FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"maths", "shove", "atom", "quake"}
def render(t):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    name, lt, d, k = scene_at(t)
    z = 1 + 0.05 * clamp(lt / max(d, 0.1)); c.translate(W / 2, H / 2); SS(c, z); c.translate(-W / 2, -H / 2)
    FN[name](c, t, lt, d); c.identity_matrix()
    if name in FLASH and lt < 0.14: c.set_source_rgba(1, 1, 1, 0.45 * (1 - lt / 0.14)); c.paint()
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
