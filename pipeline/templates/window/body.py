# ------------------------------------------------------------------ scenes: WHY PLANE WINDOWS ARE ROUND
SKYB = (0.42, 0.62, 0.86); SKYB2 = (0.72, 0.84, 0.95)
ALU = (0.78, 0.81, 0.86); ALU_D = (0.5, 0.54, 0.6)
GLASS = (0.55, 0.78, 0.92)


def highsky(c, t, k=0.0):
    c.save(); c.identity_matrix()
    vgrad(c, 0, H, mix((0.08, 0.16, 0.36), DARK, k), mix(SKYB2, (0.2, 0.24, 0.34), k))
    for q in range(5):
        x = (q * 260 + t * 16) % (W + 400) - 200; y = 1180 + q * 90
        ell(c, x, y, 160, 34, (1, 1, 1, 1)[:3], 0.10)
        ell(c, x + 90, y + 14, 120, 26, WHITE, 0.08)
    c.restore()


def jet(c, x, y, s, t, a=1.0, win="round", nwin=6, crack=0.0, broken=0.0, seed=3):
    """side view airliner. win: 'round' | 'square'"""
    c.save(); c.translate(x, y); SS(c, s)
    if broken > 0.01:
        c.rotate(0.18 * broken)
    # wing behind
    poly(c, [(-40, 10), (-230, 120), (-150, 124), (30, 22)], mix(ALU, INK, 0.3), a)
    # fuselage
    c.new_path()
    c.move_to(-430, 0); c.curve_to(-470, -10, -470, -46, -400, -52)
    c.line_to(330, -52); c.curve_to(430, -48, 470, -20, 480, 0)
    c.curve_to(468, 22, 420, 52, 330, 52); c.line_to(-400, 52)
    c.curve_to(-470, 48, -470, 12, -430, 0); c.close_path()
    g = cairo.LinearGradient(0, -52, 0, 52)
    g.add_color_stop_rgba(0, *mix(ALU, WHITE, 0.5), a); g.add_color_stop_rgba(1, *mix(ALU, INK, 0.22), a)
    c.set_source(g); c.fill()
    # tail
    poly(c, [(-400, -40), (-470, -180), (-390, -180), (-300, -44)], mix(ALU, INK, 0.12), a)
    poly(c, [(-400, 4), (-520, 54), (-430, 56), (-350, 16)], mix(ALU, INK, 0.3), a)
    # nose window
    poly(c, [(430, -22), (475, -6), (448, 6), (414, -8)], (0.2, 0.24, 0.32), a)
    # engines
    for ex in (-30, 90):
        rr(c, ex - 60, 56, 120, 46, 22, mix(ALU, INK, 0.35), a)
        ell(c, ex - 56, 79, 12, 20, (0.15, 0.17, 0.22), a)
    poly(c, [(60, 20), (-110, 118), (-30, 122), (140, 30)], ALU, a)
    # windows
    for k in range(nwin):
        wx = -300 + k * 96
        if win == "square":
            rr(c, wx - 26, -26, 52, 46, 4, GLASS, a)
            rr(c, wx - 26, -26, 52, 46, 4, (0.25, 0.3, 0.4), a * 0.0)
            line(c, [(wx - 26, -26), (wx + 26, -26), (wx + 26, 20), (wx - 26, 20)], 4, mix(ALU, INK, 0.5), a)
        else:
            rr(c, wx - 24, -24, 48, 44, 20, GLASS, a)
            rr(c, wx - 24, -24, 48, 44, 20, mix(ALU, INK, 0.45), a * 0.0)
    if crack > 0.01:
        R = random.Random(seed); wx = -300 + 2 * 96
        px, py = wx + 26, -26
        pts = [(px, py)]
        for k in range(6):
            px += R.uniform(14, 34) * crack; py += R.uniform(-22, 10)
            pts.append((px, py))
        line(c, pts, 5, (0.95, 0.2, 0.15), a)
    if broken > 0.4:
        for k in range(10):
            R = random.Random(seed * 7 + k)
            an = R.uniform(0, TAU); dd = 120 + 260 * broken * R.random()
            rr(c, math.cos(an) * dd, math.sin(an) * dd * 0.5, 26, 16, 5, mix(ALU, INK, 0.2), a * (1 - broken * 0.4))
    c.restore()


def pane(c, x, y, s, square=True, t=0.0, hot=0.0, a=1.0, label=None, crack=0.0):
    """big diagram of one window, with stress flow"""
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -200, -230, 400, 460, 30, mix(ALU, WHITE, 0.25), a)
    r = 8 if square else 90
    rr(c, -150, -180, 300, 360, r, (0.1, 0.13, 0.2), a)
    rr(c, -138, -168, 276, 336, max(2, r - 10), GLASS, a)
    # stress flow lines
    n = 7
    for k in range(n):
        off = 36 + k * 26
        c.save()
        col = mix((0.25, 0.6, 1.0), (1.0, 0.25, 0.15), hot if square else 0.0)
        if square:
            pts = [(-150 - off, -180 - off), (-150 - off, 180 + off)]
            line(c, [(-150 - off, -230), (-150 - off, 230)], 5, col, a * 0.55)
            line(c, [(150 + off, -230), (150 + off, 230)], 5, col, a * 0.55)
        else:
            c.new_path()
            c.move_to(-150 - off, -230)
            c.curve_to(-150 - off, -60, -150 - off, 60, -150 - off, 230)
            c.set_source_rgba(*mix((0.25, 0.6, 1.0), (0.3, 0.8, 0.5), 0.3), a * 0.55); c.set_line_width(5); c.stroke()
            c.new_path()
            c.move_to(150 + off, -230)
            c.curve_to(150 + off, -60, 150 + off, 60, 150 + off, 230)
            c.set_source_rgba(*mix((0.25, 0.6, 1.0), (0.3, 0.8, 0.5), 0.3), a * 0.55); c.set_line_width(5); c.stroke()
        c.restore()
    if square and hot > 0.2:
        for cx, cy in ((-150, -180), (150, -180), (-150, 180), (150, 180)):
            glow(c, cx, cy, 110 * (0.6 + 0.4 * math.sin(t * 6)), (1, 0.3, 0.1), 0.55 * hot * a)
            ell(c, cx, cy, 20, 20, (1, 0.35, 0.2), a * hot)
    if crack > 0.01:
        pts = [(-150, -180)]
        R = random.Random(11); px, py = -150, -180
        for k in range(7):
            px -= R.uniform(10, 30) * crack; py -= R.uniform(0, 26) * crack
            pts.append((px, py))
        line(c, pts, 7, (0.95, 0.2, 0.15), a)
    if label: txt(c, label, 0, 290, 40, INK, a=a)
    c.restore()


def tank(c, x, y, s, t, fill=1.0, burst=0.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -340, -200, 680, 400, 24, (0.3, 0.33, 0.4), a)
    hh = 360 * clamp(fill)
    rr(c, -322, 182 - hh, 644, hh, 14, (0.2, 0.5, 0.78), a * 0.85)
    for k in range(5):
        xx = -280 + k * 140; yy = 182 - hh + 20 + 12 * math.sin(t * 2.4 + k)
        ell(c, xx, yy, 9 + 4 * math.sin(t * 3 + k), 9, WHITE, a * 0.4)
    jet(c, 0, 10, 0.44, t, a, win="square", nwin=5, crack=burst, seed=5)
    rr(c, -340, -200, 680, 400, 24, (1, 1, 1), a * 0.0)
    line(c, [(-340, -200), (340, -200), (340, 200), (-340, 200), (-340, -200)], 10, (0.42, 0.46, 0.54), a)
    c.restore()


SC = [("hook", 0.0), ("comet", T0(1) - 0.12), ("three", T0(2) - 0.12), ("balloon", T0(3) - 0.12),
      ("flow", T0(4) - 0.12), ("corner", T0(5) - 0.12), ("tank", T0(6) - 0.12), ("fixed", T0(7) - 0.12),
      ("oval", T0(8) - 0.12), ("end", T0(9) - 0.12)]
STARTS = [s for _, s in SC]


def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k


def s_hook(c, t, lt, d):
    highsky(c, t)
    u = clamp((lt - 0.4) / 0.4)
    pane(c, 300, 1150, 0.9, square=False, t=t, a=1.0, label="ROUND")
    if u > 0:
        pane(c, 780, 1150, 0.9, square=True, t=t, hot=u, a=u, label="SQUARE")
        cross(c, 780, 1150, 100, RED, 20, u)
    chip(c, "WHY ARE PLANE WINDOWS ROUND?", INK, 560, clamp(lt / 0.3), 42)
    ap = W_(0, "apart", 6.0)
    if t > ap - 0.3: bigtxt(c, "THE SQUARE ONES TORE 3 JETS APART", 1620, 50, RED, t, ap - 0.3)


def s_comet(c, t, lt, d):
    highsky(c, t)
    jet(c, 540, 980, 0.95, t, win="square", nwin=6)
    lab(c, 540, 640, "de HAVILLAND COMET", INK, clamp((lt - 0.3) / 0.3), 44, WHITE)
    lab(c, 540, 1340, "THE FIRST JET AIRLINER", INK, clamp((lt - 1.4) / 0.3), 38, GOLD)
    sq = W_(1, "windows", 8.0)
    if t > sq - 0.3:
        bigtxt(c, "BIG SQUARE WINDOWS", 1620, 56, RED, t, sq - 0.3)
        for k in range(6):
            wx = 540 + (-300 + k * 96) * 0.95
            rr(c, wx - 28, 980 - 26, 56, 50, 4, (1, 0.3, 0.2), 0.0)
            line(c, [(wx - 26, 954), (wx + 26, 954), (wx + 26, 1000), (wx - 26, 1000), (wx - 26, 954)], 5, RED, clamp((t - sq + 0.3) / 0.3))
    chip(c, "1952", GOLD, 560, clamp(lt / 0.3), 54)


def s_three(c, t, lt, d):
    highsky(c, t, 0.35)
    for k in range(3):
        at = STARTS[2] + 0.7 + k * 0.85
        u = clamp((t - at) / 0.5)
        y = 760 + k * 400
        jet(c, 540, y, 0.46, t, win="square", nwin=5, crack=min(1, u * 2), broken=u, seed=3 + k * 4)
        if u > 0.5:
            cross(c, 880, y, 56, RED, 14, clamp((u - 0.5) / 0.4))
    chip(c, "WITHIN TWO YEARS", RED, 560, clamp(lt / 0.3), 48)
    if t > STARTS[2] + 3.0: bigtxt(c, "THREE BROKE UP IN MID-AIR", 1620, 54, RED, t, STARTS[2] + 3.0)


def s_balloon(c, t, lt, d):
    highsky(c, t, 0.2)
    p = 0.5 + 0.5 * math.sin(t * 1.5)
    c.save(); c.translate(540, 1050); c.scale(1.0 + 0.055 * p, 1.0 + 0.1 * p); c.translate(-540, -1050)
    jet(c, 540, 1050, 0.9, t, win="square", nwin=6)
    c.restore()
    for k in range(10):
        an = -0.3 + k * 0.7; r0 = 300 + 60 * p
        x0 = 540 + math.cos(an) * r0 * 1.3; y0 = 1050 + math.sin(an) * r0 * 0.5
        arrow(c, x0, y0, 540 + math.cos(an) * 230 * 1.3, 1050 + math.sin(an) * 230 * 0.5, (0.25, 0.6, 1.0), 9, 0.0)
    for k in range(8):
        an = k * TAU / 8
        x1 = 540 + math.cos(an) * 330; y1 = 1050 + math.sin(an) * 150
        x0 = 540 + math.cos(an) * (150 + 60 * p); y0 = 1050 + math.sin(an) * (70 + 30 * p)
        arrow(c, x0, y0, x1, y1, (1.0, 0.7, 0.15), 9, 0.8)
    chip(c, "THE CABIN IS PUMPED UP", INK, 560, clamp(lt / 0.3), 46)
    st = W_(3, "stretches", 7.0)
    if t > st - 0.3: bigtxt(c, "EVERY FLIGHT STRETCHES THE METAL", 1620, 48, GOLD, t, st - 0.3)


def s_flow(c, t, lt, d):
    studio(c, (0.9, 0.93, 0.97), (0.74, 0.81, 0.91))
    pane(c, 310, 1120, 0.74, square=False, t=t, label="CURVE")
    pane(c, 770, 1120, 0.74, square=True, t=t, hot=clamp((lt - 1.6) / 0.6), label="CORNER")
    lab(c, 310, 1560, "STRESS FLOWS ROUND", (0.15, 0.5, 0.3), clamp((lt - 0.6) / 0.3), 32, WHITE)
    lab(c, 770, 1560, "STRESS PILES UP", (0.7, 0.15, 0.1), clamp((lt - 1.8) / 0.3), 32, WHITE)
    chip(c, "SAME PRESSURE. DIFFERENT SHAPE.", INK, 560, clamp(lt / 0.3), 42)


def s_corner(c, t, lt, d):
    studio(c, (0.95, 0.9, 0.88), (0.86, 0.74, 0.7))
    ck = clamp((lt - 2.6) / 0.8)
    pane(c, 540, 1120, 1.05, square=True, t=t, hot=1.0, crack=ck)
    th = W_(5, "higher", 4.0)
    if t > th - 0.4:
        u = back(clamp((t - th + 0.4) / 0.35)); c.save(); c.translate(540, 560); SS(c, u)
        shadow_rr(c, -260, -74, 520, 148, 40, RED); txt(c, "3x THE STRESS", 0, 16, 56, WHITE); c.restore()
    if ck > 0.3: lab(c, 540, 1700, "ONE DAY IT RAN", WHITE, clamp((ck - 0.3) / 0.4), 42, RED)


def s_tank(c, t, lt, d):
    studio(c, (0.86, 0.9, 0.95), (0.6, 0.7, 0.82))
    tank(c, 540, 1120, 1.18, t, fill=ease(clamp((lt - 0.3) / 1.2)), burst=clamp((lt - 2.4) / 0.6))
    chip(c, "SO THEY TESTED IT TO DESTRUCTION", INK, 560, clamp(lt / 0.3), 40)
    if lt > 2.6: lab(c, 540, 1680, "AND FOUND IT", WHITE, clamp((lt - 2.6) / 0.4), 44, GREEN)


def s_fixed(c, t, lt, d):
    highsky(c, t)
    jet(c, 540, 1020, 0.95, t, win="round", nwin=6)
    for k in range(6):
        wx = 540 + (-300 + k * 96) * 0.95
        u = clamp((lt - 0.5 - k * 0.14) / 0.3)
        if u > 0: check(c, wx, 920, 22, u)
    chip(c, "ROUNDED CORNERS EVER SINCE", GREEN, 560, clamp(lt / 0.3), 44)
    ag = W_(7, "again", 4.6)
    if t > ag - 0.3: bigtxt(c, "NO WINDOW HAS DONE IT AGAIN", 1620, 50, GREEN, t, ag - 0.3)


def s_oval(c, t, lt, d):
    studio(c, (0.9, 0.93, 0.97), (0.7, 0.78, 0.9))
    pane(c, 540, 1080, 1.15, square=False, t=t)
    guy(c, 190, 1840, 0.62, t, face=1, mood="happy", armF=0.5)
    chip(c, "NOT A STYLE CHOICE", INK, 560, clamp(lt / 0.3), 48)
    hs = W_(8, "history", 7.0)
    if t > hs - 0.4:
        u = back(clamp((t - hs + 0.4) / 0.35)); c.save(); c.translate(540, 1680); SS(c, u)
        shadow_rr(c, -440, -62, 880, 124, 36, GOLD); txt(c, "MOST REDESIGNED GLASS EVER", 0, 14, 42, INK); c.restore()


def s_end(c, t, lt, d):
    highsky(c, t)
    jet(c, 540, 900, 0.9, t, win="round", nwin=6)
    guy(c, 540, 1880, 1.0, t, face=1, mood="happy", armF=2.2, armB=-0.4)
    k = back(clamp(lt / 0.35))
    c.save(); c.translate(540, 1420); SS(c, k)
    shadow_rr(c, -420, -78, 840, 156, 44, RED); txt(c, "STILL THE BEST SEAT", 0, 18, 54, WHITE); c.restore()
    u = back(clamp((lt - 0.5) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 1640); SS(c, u)
        shadow_rr(c, -450, -56, 900, 112, 34, (0.12, 0.13, 0.18)); txt(c, "SEND THIS TO WHOEVER TAKES IT", 0, 14, 40, WHITE); c.restore()


FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"three", "corner", "tank"}
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
