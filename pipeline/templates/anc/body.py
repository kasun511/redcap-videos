# ------------------------------------------------------------------ scenes: NOISE CANCELLING HEADPHONES
CUP = (0.22, 0.24, 0.30); CUP_L = (0.34, 0.37, 0.45); PAD = (0.14, 0.15, 0.19)
NOISEC = (1.0, 0.42, 0.22); ANTIC = (0.26, 0.68, 1.0); OKC = (0.18, 0.76, 0.48)


def studio2(c, k=0.0):
    c.save(); c.identity_matrix()
    vgrad(c, 0, H, mix((0.09, 0.11, 0.18), (0.05, 0.06, 0.10), k), mix((0.16, 0.19, 0.28), (0.07, 0.08, 0.13), k))
    glow(c, 540, 1000, 820, (0.3, 0.5, 0.9), 0.16)
    c.restore()


def wave(c, x0, x1, y, amp, freq, t, col, a=1.0, w=8, phase=0.0, n=170, damp=None):
    pts = []
    for k in range(n):
        f = k / (n - 1); x = x0 + (x1 - x0) * f
        e = 1.0 if damp is None else damp(f)
        pts.append((x, y - math.sin(f * freq * TAU + t * 5 + phase) * amp * e))
    line(c, pts, w, col, a)


def headphone(c, x, y, s, t, a=1.0, on=0.0, mic=0.0):
    c.save(); c.translate(x, y); SS(c, s)
    # band
    c.new_path(); c.move_to(-180, -40)
    c.curve_to(-180, -230, 180, -230, 180, -40)
    c.set_source_rgba(*CUP_L, a); c.set_line_width(34); c.stroke()
    for sd in (-1, 1):
        rr(c, sd * 180 - 72, -70, 144, 230, 46, CUP, a)
        rr(c, sd * 180 - 54, -46, 108, 182, 38, PAD, a)
        if on > 0:
            ell(c, sd * 180, 44, 34, 34, mix(PAD, OKC, on), a)
            glow(c, sd * 180, 44, 120, OKC, 0.35 * on * a)
    if mic > 0:
        ell(c, -186, -92, 15, 15, (0.95, 0.8, 0.25), a * mic)
        glow(c, -186, -92, 70, (1, 0.85, 0.3), 0.5 * mic * a)
        lab(c, -300, -170, "MIC", INK, mic, 26, (1, 0.85, 0.3))
    c.restore()


def head(c, x, y, s, t, a=1.0, wear=1.0, calm=0.0):
    c.save(); c.translate(x, y); SS(c, s)
    ell(c, 0, 0, 120, 132, SKIN, a)
    ell(c, -42, -18, 13, 17, INK, a); ell(c, 42, -18, 13, 17, INK, a)
    if calm > 0.5:
        line(c, [(-52, 44), (0, 62), (52, 44)], 9, INK, a)
    else:
        line(c, [(-40, 52), (40, 52)], 9, INK, a)
    c.restore()
    if wear > 0: headphone(c, x, y - 26 * s, s * 0.68, t, a, on=calm, mic=0.0)


def chipbox(c, x, y, s, t, a=1.0, busy=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -110, -80, 220, 160, 22, (0.16, 0.18, 0.24), a)
    rr(c, -82, -54, 164, 108, 14, (0.22, 0.26, 0.36), a)
    for k in range(5):
        line(c, [(-110, -54 + k * 28), (-150, -54 + k * 28)], 8, (0.5, 0.54, 0.62), a)
        line(c, [(110, -54 + k * 28), (150, -54 + k * 28)], 8, (0.5, 0.54, 0.62), a)
    for k in range(9):
        on = (int(t * 9) + k) % 3 == 0
        ell(c, -62 + k * 16, 0, 5, 5, ANTIC if on else (0.3, 0.34, 0.42), a * busy)
    txt(c, "DSP", 0, 42, 26, (0.72, 0.78, 0.9), a=a)
    c.restore()


def planeicon(c, x, y, s, a=1.0, col=(0.8, 0.84, 0.9)):
    c.save(); c.translate(x, y); SS(c, s)
    poly(c, [(-120, 0), (90, -16), (130, 0), (90, 16)], col, a)
    poly(c, [(-10, -8), (-70, -70), (-30, -72), (40, -10)], mix(col, INK, 0.2), a)
    poly(c, [(-10, 8), (-70, 70), (-30, 72), (40, 10)], mix(col, INK, 0.3), a)
    c.restore()


def babyicon(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    ell(c, 0, 0, 72, 78, SKIN, a)
    ell(c, -26, -12, 9, 12, INK, a); ell(c, 26, -12, 9, 12, INK, a)
    ell(c, 0, 36, 24, 18 + 6 * math.sin(t * 9), (0.7, 0.2, 0.2), a)
    line(c, [(-14, -74), (0, -98)], 7, (0.3, 0.24, 0.2), a)
    for k in range(3):
        ph = (t * 1.6 + k / 3) % 1
        c.new_path(); c.arc(0, 0, 90 + ph * 90, -0.9, 0.9)
        c.set_source_rgba(*NOISEC, a * (1 - ph) * 0.7); c.set_line_width(7); c.stroke()
    c.restore()


SC = [("hook", 0.0), ("wavey", T0(1) - 0.12), ("mic", T0(2) - 0.12), ("opposite", T0(3) - 0.12),
      ("cancel", T0(4) - 0.12), ("fast", T0(5) - 0.12), ("vs", T0(6) - 0.12), ("why", T0(7) - 0.12), ("end", T0(8) - 0.12)]
STARTS = [s for _, s in SC]


def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k


def s_hook(c, t, lt, d):
    studio2(c)
    headphone(c, 540, 1100, 1.5, t, on=clamp((lt - 1.2) / 0.5))
    chip(c, "THEY DON'T BLOCK SOUND", INK, 560, clamp(lt / 0.3), 48)
    ms = W_(0, "sound", 2)
    if t > ms - 0.3:
        u = back(clamp((t - ms + 0.3) / 0.35)); c.save(); c.translate(540, 1620); SS(c, u)
        shadow_rr(c, -400, -80, 800, 160, 46, RED); txt(c, "THEY MAKE MORE", 0, 20, 58, WHITE); c.restore()


def s_wavey(c, t, lt, d):
    studio2(c)
    wave(c, 70, 1010, 1060, 180, 2.4, t, NOISEC, clamp(lt / 0.3), 11)
    u = clamp((lt - 1.0) / 0.6)
    if u > 0:
        for k, (nm, xx, col) in enumerate((("SQUEEZE", 300, NOISEC), ("STRETCH", 760, ANTIC))):
            lab(c, xx, 1390, nm, WHITE, u, 34, col)
            arrowline(c, xx, 1330, xx, 1150, col, 9, u)
    chip(c, "SOUND IS A WAVE", INK, 560, clamp(lt / 0.3), 50)
    lab(c, 540, 1700, "SQUEEZE, STRETCH, OVER AND OVER", WHITE, clamp((lt - 2.0) / 0.4), 36, (0.2, 0.3, 0.5))


def s_mic(c, t, lt, d):
    studio2(c)
    headphone(c, 620, 1120, 1.35, t, on=0.2, mic=clamp((lt - 0.8) / 0.4))
    wave(c, 40, 380, 1120, 90, 2.2, t, NOISEC, clamp((lt - 0.3) / 0.4), 9)
    arrowline(c, 170, 1300, 400, 1230, NOISEC, 10, clamp((lt - 0.6) / 0.4))
    chip(c, "A MIC ON THE OUTSIDE", INK, 560, clamp(lt / 0.3), 48)
    bf = W_(2, "do", 1)
    if t > bf - 0.3: bigtxt(c, "IT HEARS THE NOISE BEFORE YOU DO", 1700, 42, GOLD, t, bf - 0.3)


def s_opposite(c, t, lt, d):
    studio2(c)
    chipbox(c, 540, 700, 1.0, t)
    wave(c, 70, 1010, 1130, 150, 2.4, t, NOISEC, 1.0, 10)
    u = clamp((lt - 1.4) / 0.6)
    if u > 0:
        wave(c, 70, 1010, 1130, 150, 2.4, t, ANTIC, u, 10, phase=math.pi)
        lab(c, 300, 1430, "NOISE", WHITE, u, 32, NOISEC)
        lab(c, 760, 1430, "THE OPPOSITE", WHITE, u, 32, ANTIC)
    chip(c, "THE CHIP BUILDS THE MIRROR", INK, 560, clamp(lt / 0.3), 44)
    sq = W_(3, "squeezes")
    if t > sq - 0.3: bigtxt(c, "SQUEEZE WHERE IT STRETCHES", 1700, 42, ANTIC, t, sq - 0.3)


def s_cancel(c, t, lt, d):
    studio2(c, 0.2)
    k = clamp((lt - 0.8) / 1.0)
    amp = 160 * (1 - k)
    wave(c, 70, 1010, 1060, amp, 2.4, t, NOISEC, 1.0, 10)
    wave(c, 70, 1010, 1060, amp, 2.4, t, ANTIC, 1.0, 10, phase=math.pi)
    if k > 0.75:
        line(c, [(70, 1060), (1010, 1060)], 10, OKC, clamp((k - 0.75) / 0.25))
        lab(c, 540, 1230, "SILENCE", WHITE, clamp((k - 0.8) / 0.2), 44, OKC)
    nt = W_(4, "nothing")
    if t > nt - 0.3:
        u = back(clamp((t - nt + 0.3) / 0.35)); c.save(); c.translate(540, 1560); SS(c, u)
        shadow_rr(c, -440, -80, 880, 160, 46, OKC); txt(c, "PEAK + TROUGH = NOTHING", 0, 20, 50, WHITE); c.restore()
    chip(c, "THE TWO CANCEL", OKC, 560, clamp(lt / 0.3), 50)


def s_fast(c, t, lt, d):
    studio2(c)
    chipbox(c, 540, 980, 1.4, t)
    k = back(clamp((lt - 0.6) / 0.4))
    if k > 0:
        c.save(); c.translate(540, 1420); SS(c, k)
        shadow_rr(c, -340, -90, 680, 180, 50, GOLD); txt(c, "UNDER 1 ms", 0, 22, 66, INK); c.restore()
    pr = W_(5, "predict")
    if t > pr - 0.3: bigtxt(c, "SO IT ONLY WORKS ON SOUND IT CAN PREDICT", 1700, 36, GOLD, t, pr - 0.3)
    chip(c, "AND IT HAS TO BE FAST", INK, 560, clamp(lt / 0.3), 48)


def s_vs(c, t, lt, d):
    studio2(c)
    ue = clamp((lt - 0.3) / 0.4); ub = clamp((lt - 2.4) / 0.4)
    planeicon(c, 540, 820, 1.25, ue)
    wave(c, 120, 960, 1010, 46, 7.0, t, NOISEC, ue * 0.8, 7)
    if ue > 0.5: check(c, 880, 1010, 44, clamp((ue - 0.5) / 0.4)); lab(c, 300, 1120, "STEADY DRONE  ·  EASY", WHITE, ue, 32, OKC)
    if ub > 0:
        babyicon(c, 540, 1450, 1.15, t, ub)
        cross(c, 880, 1560, 46, RED, 13, ub)
        lab(c, 300, 1700, "RANDOM  ·  HOPELESS", WHITE, ub, 32, (0.75, 0.2, 0.15))
    chip(c, "WHAT IT CAN AND CANNOT DO", INK, 560, clamp(lt / 0.3), 44)


def s_why(c, t, lt, d):
    studio2(c, 0.15)
    head(c, 540, 980, 1.25, t, calm=1.0)
    planeicon(c, 190, 1420, 0.8, 1.0, (0.4, 0.45, 0.55))
    lab(c, 190, 1570, "GONE", WHITE, clamp((lt - 0.6) / 0.3), 32, OKC)
    babyicon(c, 880, 1420, 0.9, t, 1.0)
    lab(c, 880, 1570, "STILL THERE", WHITE, clamp((lt - 1.6) / 0.3), 30, (0.75, 0.2, 0.15))
    chip(c, "ROW 14 IS NOT GOING ANYWHERE", INK, 560, clamp(lt / 0.3), 42)


def s_end(c, t, lt, d):
    studio2(c)
    headphone(c, 540, 900, 1.3, t, on=1.0)
    guy(c, 540, 1920, 0.74, t, face=1, mood="happy", armF=1.6, armB=-0.3)
    k = back(clamp(lt / 0.35))
    c.save(); c.translate(540, 1270); SS(c, k)
    shadow_rr(c, -480, -140, 960, 280, 54, RED)
    txt(c, "$200 TO BE LOUDER", 0, -46, 54, WHITE); txt(c, "AND QUIETER AT ONCE", 0, 32, 54, (1, 0.92, 0.88)); c.restore()
    u = back(clamp((lt - 0.6) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 1560); SS(c, u)
        shadow_rr(c, -470, -56, 940, 112, 34, (0.12, 0.13, 0.18)); txt(c, "TAG WHOEVER WEARS THEIRS SILENT", 0, 14, 36, GOLD); c.restore()


FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"cancel", "fast"}


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
