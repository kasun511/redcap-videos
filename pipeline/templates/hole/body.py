# ------------------------------------------------------------------ scenes: A HOLE THROUGH THE EARTH
CRUST = (0.38, 0.52, 0.30); MANTLE = (0.78, 0.36, 0.16); OUTER = (0.96, 0.60, 0.16); CORE = (1.0, 0.86, 0.35)
TUBE = (0.08, 0.09, 0.13)
RE = 620  # earth radius on screen
CX, CY = 540, 1120


def cutaway(c, t, a=1.0, cx=CX, cy=CY, r=RE, tube=1.0, spin=0.0):
    ell(c, cx, cy, r, r, CRUST, a)
    ell(c, cx, cy, r * 0.94, r * 0.94, MANTLE, a)
    ell(c, cx, cy, r * 0.56, r * 0.56, OUTER, a)
    ell(c, cx, cy, r * 0.26, r * 0.26, CORE, a)
    glow(c, cx, cy, r * 0.5, (1, 0.8, 0.3), 0.3 * a)
    if tube > 0:
        rect(c, cx - 46, cy - r - 10, 92, (2 * r + 20) * clamp(tube), TUBE, a)
        line(c, [(cx - 46, cy - r), (cx - 46, cy + r)], 5, (0.3, 0.33, 0.4), a * tube)
        line(c, [(cx + 46, cy - r), (cx + 46, cy + r)], 5, (0.3, 0.33, 0.4), a * tube)


def faller(c, x, y, s, t, a=1.0, spin=0.0, still=0.0):
    c.save(); c.translate(x, y); c.rotate(spin); SS(c, s)
    guy(c, 0, 0, 1.0, t, face=1, mood="scared" if still < 0.5 else "happy",
        armF=2.5 - 1.6 * still, armB=-2.5 + 1.6 * still, alpha=a)
    c.restore()


def speedo(c, x, y, s, v, t, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    shadow_rr(c, -200, -70, 400, 140, 40, (0.1, 0.11, 0.16), a)
    txt(c, f"{int(v):,}", 0, -2, 56, GOLD, a=a)
    txt(c, "km/h", 0, 46, 26, (0.8, 0.82, 0.9), a=a)
    c.restore()


def pullarrows(c, cx, cy, r, t, a=1.0, n=12, inward=True):
    for k in range(n):
        an = k * TAU / n
        x0 = cx + math.cos(an) * r; y0 = cy + math.sin(an) * r
        x1 = cx + math.cos(an) * (r * 0.42); y1 = cy + math.sin(an) * (r * 0.42)
        if inward: arrowline(c, x0, y0, x1, y1, (0.3, 0.7, 1.0), 9, a)
        else: arrowline(c, x1, y1, x0, y0, (1, 0.6, 0.2), 9, a)


def pendulum(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    an = math.sin(t * 1.9) * 0.6
    line(c, [(-220, 0), (220, 0)], 10, (0.4, 0.44, 0.52), a)
    px, py = math.sin(an) * 260, math.cos(an) * 260
    line(c, [(0, 0), (px, py)], 6, (0.55, 0.58, 0.66), a)
    ell(c, px, py, 42, 42, GOLD, a)
    c.restore()


def orbitdiag(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    ell(c, 0, 0, 150, 150, (0.25, 0.5, 0.85), a)
    ell(c, -40, -46, 44, 34, (0.3, 0.68, 0.4), a); ell(c, 50, 30, 54, 38, (0.3, 0.68, 0.4), a)
    c.new_path(); c.arc(0, 0, 230, 0, TAU)
    c.set_source_rgba(1, 1, 1, 0.35 * a); c.set_line_width(5); c.set_dash([16, 14]); c.stroke(); c.set_dash([])
    an = t * 1.6
    rr(c, math.cos(an) * 230 - 22, math.sin(an) * 230 - 12, 44, 24, 8, (0.85, 0.88, 0.94), a)
    c.restore()


SC = [("hook", 0.0), ("ignore", T0(1) - 0.12), ("fall", T0(2) - 0.12), ("centre", T0(3) - 0.12),
      ("slow", T0(4) - 0.12), ("arrive", T0(5) - 0.12), ("forever", T0(6) - 0.12), ("air", T0(7) - 0.12),
      ("orbit", T0(8) - 0.12), ("end", T0(9) - 0.12)]
STARTS = [s for _, s in SC]


def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k


def s_hook(c, t, lt, d):
    space(c, t)
    cutaway(c, t, tube=ease(clamp((lt - 0.4) / 0.9)))
    u = clamp((lt - 1.3) / 0.4)
    if u > 0: faller(c, CX, CY - RE - 40, 0.42, t, u, spin=0.2)
    chip(c, "A HOLE THROUGH THE EARTH", INK, 560, clamp(lt / 0.3), 44)
    al = W_(0, "Almost")
    if t > al - 0.3: bigtxt(c, "YOU DON'T COME OUT. ALMOST.", 1870, 46, GOLD, t, al - 0.3)


def s_ignore(c, t, lt, d):
    space(c, t)
    cutaway(c, t)
    for k, (nm, at) in enumerate((("THE HEAT", 0.3), ("THE AIR", 1.0))):
        u = back(clamp((lt - at) / 0.35))
        if u <= 0: continue
        c.save(); c.translate(300 + k * 480, 780); SS(c, u)
        shadow_rr(c, -190, -56, 380, 112, 34, (0.4, 0.42, 0.5)); txt(c, nm, 0, 14, 42, WHITE)
        cross(c, 0, 0, 56, RED, 14, clamp((lt - at - 0.5) / 0.3)); c.restore()
    g_ = W_(1, "gravity")
    if t > g_ - 0.3:
        u = back(clamp((t - g_ + 0.3) / 0.35)); c.save(); c.translate(540, 1780); SS(c, u)
        shadow_rr(c, -260, -62, 520, 124, 38, GOLD); txt(c, "JUST GRAVITY", 0, 18, 50, INK); c.restore()
    chip(c, "FORGET TWO THINGS", INK, 560, clamp(lt / 0.3), 48)


def s_fall(c, t, lt, d):
    space(c, t)
    cutaway(c, t)
    u = ease(clamp((lt - 0.2) / 2.6))
    fy = CY - RE + (RE) * u
    faller(c, CX, fy, 0.42, t, spin=0.35 * math.sin(t * 2))
    for k in range(7):
        yy = CY - RE + ((u * RE) - k * 70) % (RE + 60)
        line(c, [(CX - 28, yy), (CX - 28, yy - 44)], 5, WHITE, 0.3 * u)
        line(c, [(CX + 28, yy), (CX + 28, yy - 44)], 5, WHITE, 0.3 * u)
    speedo(c, 540, 480, 0.92, 29000 * u, t, clamp((lt - 0.4) / 0.4))
    chip(c, "YOU KEEP SPEEDING UP", INK, 1830, clamp(lt / 0.3), 44)


def s_centre(c, t, lt, d):
    space(c, t)
    cutaway(c, t)
    faller(c, CX, CY, 0.42, t, spin=0.5 * math.sin(t * 3))
    u = clamp((lt - 0.8) / 0.6)
    pullarrows(c, CX, CY, 440, t, u)
    if u > 0.6:
        c.save(); c.translate(540, 480); SS(c, back(clamp((u - 0.6) / 0.4)))
        shadow_rr(c, -400, -70, 800, 140, 40, (0.1, 0.11, 0.16)); txt(c, "PULLED EVERY WAY AT ONCE", 0, 18, 42, WHITE); c.restore()
    up = W_(3, "up")
    if t > up - 0.3: bigtxt(c, "IT STOPS SPEEDING YOU UP", 1830, 46, GOLD, t, up - 0.3)


def s_slow(c, t, lt, d):
    space(c, t)
    cutaway(c, t)
    u = ease(clamp((lt - 0.2) / 2.4))
    fy = CY + RE * u
    faller(c, CX, fy, 0.42, t, spin=0.2)
    speedo(c, 540, 480, 0.92, 29000 * (1 - u), t)
    arrowline(c, CX + 150, CY + 380, CX + 150, CY + 180, (0.3, 0.7, 1.0), 10, clamp((lt - 0.6) / 0.4))
    lab(c, CX + 290, CY + 280, "SLOWING", WHITE, clamp((lt - 0.8) / 0.3), 30, (0.2, 0.45, 0.8))
    chip(c, "NOW IT SLOWS YOU DOWN", INK, 1830, clamp(lt / 0.3), 44)


def s_arrive(c, t, lt, d):
    space(c, t)
    cutaway(c, t)
    faller(c, CX, CY + RE + 20, 0.42, t, still=clamp((lt - 0.8) / 0.5))
    u = back(clamp((lt - 0.9) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 480); SS(c, u)
        shadow_rr(c, -330, -90, 660, 180, 50, GREEN); txt(c, "SPEED: ZERO", 0, 22, 62, WHITE); c.restore()
    eg = W_(5, "edge")
    if t > eg - 0.3: bigtxt(c, "LONG ENOUGH TO GRAB THE EDGE", 1870, 42, GOLD, t, eg - 0.3)
    chip(c, "YOU ARRIVE WITH NOTHING LEFT", INK, 1830, clamp(lt / 0.3), 40)


def s_forever(c, t, lt, d):
    space(c, t)
    cutaway(c, t)
    ph = (t * 0.55) % 2
    u = ph if ph < 1 else 2 - ph
    fy = CY - RE + 2 * RE * u
    faller(c, CX, fy, 0.42, t, spin=0.3 * math.sin(t * 2))
    for k, (yy, nm) in enumerate(((CY - RE - 70, "START"), (CY + RE + 70, "OTHER SIDE"))):
        lab(c, CX + 330, yy, nm, WHITE, 0.9, 28, (0.3, 0.34, 0.44))
    k = back(clamp((lt - 0.8) / 0.4))
    if k > 0:
        c.save(); c.translate(540, 480); SS(c, k)
        shadow_rr(c, -380, -94, 760, 188, 50, RED)
        txt(c, "42 MINUTES", 0, -18, 62, WHITE); txt(c, "EACH WAY, FOREVER", 0, 48, 36, (1, 0.9, 0.86)); c.restore()


def s_air(c, t, lt, d):
    space(c, t)
    cutaway(c, t)
    amp = max(0.08, 1 - ease(clamp((lt - 0.4) / 2.4)))
    ph = (t * 0.9) % 2; u = ph if ph < 1 else 2 - ph
    fy = CY + (u - 0.5) * 2 * RE * amp
    faller(c, CX, fy, 0.42, t, spin=0.1)
    for k in range(10):
        yy = CY - RE + k * (2 * RE / 10)
        ell(c, CX + 70 + 20 * math.sin(t * 2 + k), yy, 7, 7, (0.6, 0.75, 1.0), 0.45)
    if amp < 0.4:
        lab(c, 540, 1810, "FLOATING AT THE CENTRE", WHITE, clamp((0.4 - amp) / 0.2), 40, GOLD)
    chip(c, "PUT THE AIR BACK IN", INK, 480, clamp(lt / 0.3), 48)


def s_orbit(c, t, lt, d):
    space(c, t)
    orbitdiag(c, 540, 860, 1.0, t)
    pendulum(c, 540, 1420, 0.72, t, clamp((lt - 1.8) / 0.5))
    k = back(clamp((lt - 0.5) / 0.4))
    if k > 0:
        c.save(); c.translate(540, 1780); SS(c, k)
        shadow_rr(c, -470, -66, 940, 132, 40, (0.12, 0.13, 0.18)); txt(c, "ORBITING IS JUST FALLING AND MISSING", 0, 16, 36, GOLD); c.restore()
    chip(c, "SAME 42 MINUTES. SAME MATHS.", INK, 480, clamp(lt / 0.3), 42)


def s_end(c, t, lt, d):
    space(c, t)
    cutaway(c, t, cx=540, cy=1300, r=460)
    guy(c, 540, 820, 0.78, t, face=1, mood="happy", armF=2.0, armB=-0.4)
    k = back(clamp(lt / 0.35))
    c.save(); c.translate(540, 1240); SS(c, k)
    shadow_rr(c, -480, -140, 960, 280, 54, RED)
    txt(c, "42 MINUTES TO AUSTRALIA", 0, -46, 46, WHITE); txt(c, "NO BAGGAGE FEE", 0, 32, 56, (1, 0.92, 0.88)); c.restore()
    u = back(clamp((lt - 0.6) / 0.4))
    if u > 0:
        c.save(); c.translate(540, 1620); SS(c, u)
        shadow_rr(c, -470, -70, 940, 140, 40, (0.12, 0.13, 0.18))
        txt(c, "THE 5,000° IRON IS THE CATCH", 0, -6, 38, WHITE); txt(c, "who are you taking?", 0, 42, 32, GOLD); c.restore()


FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"centre", "arrive", "forever"}


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
