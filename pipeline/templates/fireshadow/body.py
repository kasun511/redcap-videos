# ------------------------------------------------------------------ scenes: FIRE HAS NO SHADOW
WALLC = (0.90, 0.87, 0.80); WALLD = (0.72, 0.68, 0.60)
WAX = (0.95, 0.93, 0.86); FLAME1 = (1.0, 0.82, 0.25); FLAME2 = (1.0, 0.45, 0.12)
LAMPC = (0.42, 0.45, 0.52)


def room(c, t, dim=0.0):
    c.save(); c.identity_matrix()
    vgrad(c, 0, H, mix(WALLC, (0.10, 0.11, 0.16), dim), mix(WALLD, (0.06, 0.07, 0.11), dim))
    rect(c, 0, 1760, W, H - 1760, mix((0.46, 0.36, 0.26), (0.10, 0.09, 0.12), dim))
    rect(c, 0, 1760, W, 14, mix((0.34, 0.26, 0.18), (0.08, 0.07, 0.1), dim))
    c.restore()


def lamp(c, x, y, s, t, on=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -70, 120, 140, 26, 12, LAMPC, a)
    rr(c, -14, -70, 28, 196, 12, LAMPC, a)
    poly(c, [(-110, -70), (110, -70), (70, -175), (-70, -175)], mix(LAMPC, INK, 0.2), a)
    if on > 0:
        ell(c, 0, -74, 96, 30, mix((1, 0.96, 0.8), WHITE, 0.4), a * on)
        glow(c, 0, -74, 340, (1, 0.95, 0.72), 0.5 * on * a)
    c.restore()


def beam(c, x0, y0, x1, half, a=0.22, col=(1, 0.96, 0.78)):
    """cone of light going right from (x0,y0) to plane x1, half-height 'half'"""
    poly(c, [(x0, y0 - 16), (x1, y0 - half), (x1, y0 + half), (x0, y0 + 16)], col, a)


def rays(c, x0, y0, x1, n, t, a=0.5, col=(1, 0.93, 0.6), through=None, w=5):
    """straight rays left->right. through = (cx, cy, r) a region they pass through"""
    for k in range(n):
        f = (k / max(1, n - 1)) - 0.5
        yy = y0 + f * 460
        ph = (t * 1.6 + k * 0.17) % 1
        line(c, [(x0, y0 + f * 60), (x1, yy)], w, col, a)
        px = x0 + (x1 - x0) * ph; py = (y0 + f * 60) + (yy - (y0 + f * 60)) * ph
        ell(c, px, py, 7, 7, WHITE, a * 0.8)


def candle(c, x, y, s, t, a=1.0, flame=1.0, lit=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -46, -220, 92, 220, 14, WAX, a)
    ell(c, 0, -220, 46, 14, mix(WAX, INK, 0.12), a)
    line(c, [(0, -228), (0, -252)], 7, (0.25, 0.22, 0.2), a)
    if flame > 0.01:
        fl = 1 + 0.08 * math.sin(t * 7.3); sway = math.sin(t * 2.7) * 5
        c.save(); c.translate(sway, -252); c.scale(1, fl)
        c.new_path(); c.move_to(0, -118)
        c.curve_to(36, -64, 32, -12, 0, 0); c.curve_to(-32, -12, -36, -64, 0, -118); c.close_path()
        c.set_source_rgba(*FLAME2, a * flame); c.fill()
        c.new_path(); c.move_to(0, -80)
        c.curve_to(20, -44, 18, -8, 0, 0); c.curve_to(-18, -8, -20, -44, 0, -80); c.close_path()
        c.set_source_rgba(*FLAME1, a * flame); c.fill()
        ell(c, 0, -16, 9, 18, (0.55, 0.72, 1.0), a * flame * 0.8)
        c.restore()
        glow(c, sway, -300, 230 * lit, (1, 0.72, 0.3), 0.55 * a * flame * lit)
    c.restore()


def shimmer(c, x, y, h, t, a=0.5):
    for k in range(7):
        yy = y - k * (h / 7); off = math.sin(t * 3.4 + k * 1.1) * (10 + k * 4)
        c.new_path()
        c.move_to(x - 40 + off, yy)
        c.curve_to(x - 10 + off, yy - 22, x + 10 - off, yy - 22, x + 40 - off, yy)
        c.set_source_rgba(1, 1, 1, a * 0.22); c.set_line_width(5); c.stroke()


def sootspecks(c, x, y, t, a=1.0, n=22, seed=4):
    R = random.Random(seed)
    for k in range(n):
        ph = (t * 0.45 + R.random()) % 1
        xx = x + R.uniform(-60, 60) + math.sin(t * 2 + k) * 16
        yy = y - ph * 420
        ell(c, xx, yy, 5 + R.random() * 5, 5 + R.random() * 5, (0.18, 0.17, 0.18), a * (1 - ph) * 0.8)


def ball(c, x, y, r, a=1.0, col=(0.25, 0.4, 0.75)):
    ell(c, x, y, r, r, col, a); ell(c, x - r * 0.3, y - r * 0.3, r * 0.3, r * 0.3, WHITE, a * 0.3)


def wallpanel(c, x, w, a=1.0):
    rect(c, x, 480, w, 1280, mix(WALLC, WHITE, 0.25), a)
    line(c, [(x, 480), (x, 1760)], 8, mix(WALLD, INK, 0.2), a)


SC = [("hook", 0.0), ("gap", T0(1) - 0.12), ("through", T0(2) - 0.12), ("adds", T0(3) - 0.12),
      ("isthelight", T0(4) - 0.12), ("faint", T0(5) - 0.12), ("soot", T0(6) - 0.12), ("end", T0(7) - 0.12)]
STARTS = [s for _, s in SC]


def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k


def s_hook(c, t, lt, d):
    room(c, t, 0.55)
    wallpanel(c, 760, 320)
    lamp(c, 180, 1560, 0.85, t)
    beam(c, 230, 1380, 760, 430, 0.18)
    candle(c, 520, 1560, 1.0, t)
    nu = clamp((lt - 2.2) / 0.5)
    if nu > 0:
        c.save(); c.translate(905, 1200); SS(c, back(nu))
        shadow_rr(c, -120, -56, 240, 112, 34, GREEN); txt(c, "NO", 0, -4, 54, WHITE); txt(c, "SHADOW", 0, 34, 26, WHITE); c.restore()
    chip(c, "FIRE HAS NO SHADOW", RED, 560, clamp(lt / 0.3), 52)
    sh = W_(0, "shadow", 9.0)
    if t > sh - 0.3: bigtxt(c, "TRY IT. NOTHING SHOWS UP.", 1700, 44, GOLD, t, sh - 0.3)


def s_gap(c, t, lt, d):
    room(c, t, 0.5)
    wallpanel(c, 760, 320)
    lamp(c, 180, 1560, 0.85, t)
    beam(c, 230, 1380, 760, 430, 0.2)
    u = ease(clamp((lt - 0.5) / 0.8))
    ball(c, 520, 1380, 110 * u)
    if u > 0.5:
        rect(c, 760, 1110, 320, 560, (0.18, 0.16, 0.2), 0.55 * clamp((u - 0.5) / 0.4))
        lab(c, 920, 1390, "SHADOW", WHITE, clamp((u - 0.6) / 0.3), 30, (0.2, 0.2, 0.26))
    chip(c, "A SHADOW IS A GAP", INK, 560, clamp(lt / 0.3), 50)
    wy = W_(1, "way", 8.0)
    if t > wy - 0.3: bigtxt(c, "YOU HAVE TO BE IN THE WAY", 1700, 46, GOLD, t, wy - 0.3)


def s_through(c, t, lt, d):
    room(c, t, 0.62)
    wallpanel(c, 760, 320)
    lamp(c, 180, 1560, 0.85, t)
    rays(c, 250, 1380, 1070, 9, t, 0.5)
    candle(c, 520, 1560, 1.0, t, lit=0.7)
    chip(c, "LIGHT GOES STRAIGHT THROUGH", INK, 560, clamp(lt / 0.3), 42)
    gs = W_(2, "gas", 4.2)
    if t > gs - 0.3: bigtxt(c, "A FLAME IS THIN HOT GAS", 1700, 46, GOLD, t, gs - 0.3)


def s_adds(c, t, lt, d):
    room(c, t, 0.78)
    wallpanel(c, 760, 320)
    lamp(c, 180, 1560, 0.85, t, on=0.35)
    candle(c, 520, 1560, 1.15, t, lit=1.0)
    u = clamp((lt - 0.8) / 0.8)
    for k in range(12):
        an = k * TAU / 12
        arrowline(c, 520 + math.cos(an) * 190, 1250 + math.sin(an) * 190,
                  520 + math.cos(an) * (300 + 40 * math.sin(t * 3 + k)), 1250 + math.sin(an) * (300 + 40 * math.sin(t * 3 + k)), (1, 0.75, 0.25), 9, u * 0.9)
    chip(c, "IT DOES THE OPPOSITE", GOLD, 560, clamp(lt / 0.3), 48)
    tp = W_(3, "top", 3.8)
    if t > tp - 0.3: bigtxt(c, "IT ADDS ITS OWN LIGHT", 1700, 48, GOLD, t, tp - 0.3)


def s_isthelight(c, t, lt, d):
    room(c, t, 0.92)
    candle(c, 540, 1620, 1.5, t, lit=1.3)
    k = back(clamp((lt - 0.4) / 0.4))
    if k > 0:
        c.save(); c.translate(540, 760); SS(c, k)
        shadow_rr(c, -440, -150, 880, 300, 54, (0.1, 0.1, 0.14))
        txt(c, "FIRE IS NOT IN", 0, -58, 56, (0.8, 0.82, 0.88))
        txt(c, "THE LIGHT", 0, 14, 72, WHITE)
        c.restore()
    u = back(clamp((lt - 2.6) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 1120); SS(c, u)
        shadow_rr(c, -400, -80, 800, 160, 46, RED); txt(c, "FIRE IS THE LIGHT", 0, 20, 58, WHITE); c.restore()


def s_faint(c, t, lt, d):
    room(c, t, 0.6)
    wallpanel(c, 760, 320)
    lamp(c, 180, 1560, 0.85, t)
    beam(c, 230, 1380, 760, 430, 0.2)
    candle(c, 520, 1560, 1.0, t)
    u = clamp((lt - 1.4) / 0.8)
    if u > 0:
        rect(c, 850, 1250, 140, 320, (0.3, 0.28, 0.3), 0.18 * u)
        shimmer(c, 905, 1560, 300, t, 0.5 * u)
    nf = W_(5, "flame", 5.0)
    if t > nf - 0.3:
        c.save(); c.translate(905, 1060); SS(c, back(clamp((t - nf + 0.3) / 0.35)))
        shadow_rr(c, -170, -52, 340, 104, 32, RED); txt(c, "NOT THE FLAME", 0, 14, 34, WHITE); c.restore()
    chip(c, "YOU MIGHT SEE SOMETHING FAINT", INK, 560, clamp(lt / 0.3), 40)


def s_soot(c, t, lt, d):
    room(c, t, 0.72)
    candle(c, 380, 1640, 1.1, t)
    sootspecks(c, 380, 1300, t, clamp((lt - 0.3) / 0.5))
    shimmer(c, 380, 1300, 420, t, 0.8 * clamp((lt - 1.6) / 0.5))
    for k, (nm, sub, at, col) in enumerate((("SOOT", "solid, so it blocks", 0.4, (0.25, 0.25, 0.3)),
                                            ("HOT AIR", "bends the light", 2.0, (0.2, 0.5, 0.8)))):
        u = back(clamp((lt - at) / 0.4))
        if u <= 0: continue
        c.save(); c.translate(760, 1040 + k * 250); SS(c, u)
        shadow_rr(c, -260, -84, 520, 168, 44, col)
        txt(c, nm, 0, -14, 50, WHITE); txt(c, sub, 0, 44, 28, (0.85, 0.87, 0.92)); c.restore()
    chip(c, "THAT IS NOT A SHADOW EITHER", INK, 560, clamp(lt / 0.3), 42)


def s_end(c, t, lt, d):
    room(c, t, 0.85)
    candle(c, 540, 1700, 1.3, t, lit=1.2)
    guy(c, 230, 1760, 0.68, t, face=1, mood="happy", armF=0.5)
    k = back(clamp(lt / 0.35))
    c.save(); c.translate(540, 800); SS(c, k)
    shadow_rr(c, -470, -140, 940, 280, 54, RED)
    txt(c, "THE ONE THING", 0, -48, 56, WHITE); txt(c, "THAT NEVER FOLLOWS YOU", 0, 30, 46, (1, 0.92, 0.88)); c.restore()
    u = back(clamp((lt - 0.6) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 1140); SS(c, u)
        shadow_rr(c, -400, -58, 800, 116, 36, (0.12, 0.13, 0.18)); txt(c, "LIGHT ONE AND CHECK", 0, 16, 42, GOLD); c.restore()


FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"isthelight", "adds"}


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
