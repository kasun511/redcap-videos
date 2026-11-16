# ------------------------------------------------------------------ power line props
SKY0 = (0.45, 0.72, 0.98); SKY1 = (0.85, 0.94, 1.0); WIRE = (0.15, 0.15, 0.18); POLE = (0.5, 0.33, 0.18); ELEC = (1.0, 0.85, 0.2)
def sky(c, t, dusk=0.0):
    c.save(); c.identity_matrix(); vgrad(c, 0, H, mix(SKY0, (0.3, 0.3, 0.5), dusk), mix(SKY1, (0.9, 0.7, 0.6), dusk))
    for k in range(4): x = (k * 360 + t * 14) % 1500 - 200; ell(c, x, 360 + k * 110, 130, 42, WHITE, 0.85); ell(c, x + 80, 335 + k * 110, 90, 44, WHITE, 0.85)
    rect(c, 0, 1650, W, 270, (0.45, 0.7, 0.35)); rect(c, 0, 1650, W, 18, (0.35, 0.58, 0.28)); c.restore()
def wirey(x, x0, x1, y, sag): u = (x - x0) / (x1 - x0); return y + sag * 4 * u * (1 - u)
def wire(c, x0, x1, y, sag, t, w=10, flow=1.0, a=1.0, glowc=None):
    pts = [(x0 + (x1 - x0) * k / 30, wirey(x0 + (x1 - x0) * k / 30, x0, x1, y, sag)) for k in range(31)]
    if glowc: line(c, pts, w + 22, glowc, 0.35 * a)
    line(c, pts, w, WIRE, a)
    if flow > 0:
        for k in range(14):
            u = ((k / 14) + t * 0.35 * flow) % 1; x = x0 + (x1 - x0) * u; ell(c, x, wirey(x, x0, x1, y, sag), w * 0.55, w * 0.55, ELEC, a * 0.95)
def pole(c, x, top, s=1.0):
    rect(c, x - 22 * s, top, 44 * s, 1700 - top, POLE); rect(c, x - 200 * s, top + 40 * s, 400 * s, 34 * s, mix(POLE, INK, 0.2))
    for k in (-160, 0, 160): rr(c, x + k * s - 12 * s, top + 10 * s, 24 * s, 34 * s, 8 * s, (0.75, 0.85, 0.9))
def bird(c, x, y, s, t, flap=0.0, col=(0.35, 0.45, 0.75), face=1, mood="calm", wing=0.0, a=1.0, singe=0.0):
    c.save(); c.translate(x, y); c.scale(s * face, s)
    col = mix(col, (0.2, 0.18, 0.18), singe)
    line(c, [(-10, 0), (-14, -40)], 6, ORANGE, a); line(c, [(14, 0), (10, -40)], 6, ORANGE, a)
    poly(c, [(-70, -70), (-120, -50), (-110, -90)], mix(col, INK, 0.2), a)
    ell(c, 0, -80, 75, 55, col, a); ell(c, 10, -62, 48, 30, mix(col, WHITE, 0.6), a)
    ell(c, 52, -135, 38, 36, col, a); poly(c, [(84, -138), (118, -128), (84, -120)], ORANGE, a)
    if mood == "dizzy":
        for k in range(2): c.new_path(); c.arc(62, -142, 8 + k * 6, t * 8 + k, t * 8 + k + 4); c.set_line_width(3); c.set_source_rgba(*INK, a); c.stroke()
    else: ell(c, 62, -142, 9, 9, WHITE, a); ell(c, 64, -142, 5, 5, INK, a)
    if wing > 0:
        poly(c, [(-20, -100), (-20 - 260 * wing, -60 - 220 * wing), (-20 - 200 * wing, -40 - 160 * wing), (20, -70)], mix(col, INK, 0.25), a)
    else:
        f = math.sin(t * 30) * flap
        poly(c, [(-40, -100), (-60, -100 - 110 * f), (40, -100 - 60 * f), (30, -80)], mix(col, INK, 0.2), a)
    if singe > 0.3:
        for k in range(4): ph = (t * 0.8 + k / 4) % 1; ell(c, -20 + k * 20, -150 - 140 * ph, 18 + 20 * ph, 18 + 20 * ph, (0.5, 0.5, 0.5), 0.5 * (1 - ph) * a)
        for k in range(6): an = k * 1.05; line(c, [(math.cos(an) * 80, -80 + math.sin(an) * 60), (math.cos(an) * 105, -80 + math.sin(an) * 78)], 6, mix(col, INK, 0.3), a)
    c.restore()
def eagle(c, x, y, s, t, a=1.0, glowc=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if glowc > 0: glow(c, 0, -60, 420, (1, 0.25, 0.2), 0.5 * glowc)
    for sd in (-1, 1):
        poly(c, [(0, -80), (sd * 420, -150), (sd * 470, -110), (sd * 380, -80), (sd * 420, -60), (sd * 300, -40), (0, -30)], (0.4, 0.25, 0.12), a)
    ell(c, 0, -60, 70, 90, (0.45, 0.28, 0.14), a); ell(c, 0, -170, 46, 44, WHITE, a); poly(c, [(30, -170), (72, -158), (34, -146)], GOLD, a)
    ell(c, 16, -180, 7, 7, INK, a); poly(c, [(-40, 20), (0, 60), (40, 20)], WHITE, a); c.restore()
def zapbolt(c, x0, y0, x1, y1, t, w=10, a=1.0):
    rnd = random.Random(int(t * 30)); pts = [(x0, y0)]
    for k in range(1, 8): u = k / 8; pts.append((x0 + (x1 - x0) * u + rnd.uniform(-30, 30), y0 + (y1 - y0) * u + rnd.uniform(-30, 30)))
    pts.append((x1, y1)); line(c, pts, w + 14, (0.6, 0.85, 1.0), 0.4 * a); line(c, pts, w, WHITE, a)
def tank(c, x, y, w, h, lvl, label, col, a=1.0):
    rr(c, x - w / 2, y - h, w, h, 20, (0.88, 0.92, 0.96), a); rr(c, x - w / 2 + 10, y - h * lvl + 10 - 20, w - 20, h * lvl - 10, 14, (0.25, 0.6, 0.95), a)
    chip(c, label, col, y + 70, a, 40, x)
def vtag(c, x, y, s, col=GOLD, a=1.0):
    shadow_rr(c, x - 130, y - 40, 260, 80, 30, INK, a); txt(c, s, x, y + 2, 38, col, a=a)
def bigtxt(c, s, y, size, col, t, at, a=1.0, x=540):
    if t < at: return
    k = back(clamp((t - at) / 0.3)); c.save(); c.translate(x, y); c.scale(k, k); txt(c, s, 0, 0, size, col, stroke=10, a=a); c.restore()
# ------------------------------------------------------------------ scenes
SC = [("hook", 0.0), ("secret", T0(1) - 0.12), ("water", T0(2) - 0.12), ("feet", T0(3) - 0.12), ("zap", T0(4) - 0.12), ("eagle", T0(5) - 0.12), ("ground", T0(6) - 0.12), ("end", T0(7) - 0.12)]
STARTS = [s for _, s in SC]
def scene_at(t):
    k = max(j for j in range(len(SC)) if STARTS[j] <= t)
    t1 = STARTS[k + 1] if k + 1 < len(SC) else TOTAL
    return SC[k][0], t - STARTS[k], t1 - STARTS[k], k
WY = 1000
def s_hook(c, t, lt, d):
    sky(c, t); pole(c, -40, 820); pole(c, 1120, 820)
    for k, y in enumerate((880, 1000, 1120)): wire(c, -40, 1120, y, 120, t, 10)
    land = ease(clamp(lt / 1.3)); bx = 1250 - 700 * land; by = 500 + (wirey(550, -40, 1120, 1000, 120) - 500) * land
    bird(c, bx, by, 1.1, t, flap=1 - clamp((lt - 1.2) / 0.2), face=-1)
    if lt > 1.3:
        for k in range(3): sparks(c, 200 + k * 330, wirey(200 + k * 330, -40, 1120, 880, 120), t, 4, 30, 2)
    vo = WORD(0, "volts", d=4.0)
    if t > vo - 0.6: chip(c, "THOUSANDS OF VOLTS", RED, 640, clamp((t - vo + 0.6) / 0.3), 52)
    bigtxt(c, "WHY NO ZAP?", 1460, 110, GOLD, t, WORD(0, "fried", d=2.0))
    chip(c, "BIRDS ON POWER LINES", INK, 470, clamp(lt / 0.3), 50)
def s_secret(c, t, lt, d):
    sky(c, t); wire(c, -40, 1120, 1000, 80, t, 16, flow=1.6, glowc=ELEC)
    bird(c, 540, wirey(540, -40, 1120, 1000, 80), 1.3, t)
    sg = WORD(1, "somewhere", d=2.5)
    if t > sg - 0.3:
        u = ease(clamp((t - sg + 0.3) / 0.6)); arrow(c, 300, 1220, 300 + 480 * u, 1220, GREEN, 16, 1.0)
        chip(c, "IT NEEDS A PATH", GREEN, 1400, clamp((t - sg + 0.3) / 0.3), 56)
    chip(c, "THE SECRET", INK, 470, clamp(lt / 0.3), 52)
def s_water(c, t, lt, d):
    sky(c, t)
    u = ease(clamp((lt - 0.6) / 3.0))
    tank(c, 280, 900, 260, 380, 0.9 - 0.4 * u, "HIGH VOLTAGE", RED); tank(c, 800, 1460, 260, 380, 0.15 + 0.4 * u, "LOW VOLTAGE", BLUE)
    line(c, [(410, 860), (540, 860), (540, 1300), (670, 1300)], 30, (0.6, 0.62, 0.66))
    for k in range(6):
        ph = (t * 1.2 + k / 6) % 1; pts = [(410, 860), (540, 860), (540, 1300), (670, 1300)]
        L = [130, 440, 130]; s_ = ph * 700; acc = 0
        for j in range(3):
            if s_ <= acc + L[j]:
                f = (s_ - acc) / L[j]; x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f; y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f; ell(c, x, y, 10, 10, (0.25, 0.6, 0.95)); break
            acc += L[j]
    dh = WORD(2, "downhill", d=3.5)
    if t > dh - 0.3: chip(c, "LIKE WATER FLOWING DOWNHILL", BLUE, 1640, clamp((t - dh + 0.3) / 0.3), 44)
def s_feet(c, t, lt, d):
    sky(c, t)
    c.save(); c.translate(540, 1000); c.scale(1.6, 1.6); c.translate(-540, -1000)
    wire(c, -100, 1180, 1000, 30, t, 14, flow=1.2); bird(c, 540, wirey(540, -100, 1180, 1000, 30), 1.1, t)
    c.restore()
    sv = WORD(3, "same", d=1.5)
    if t > WORD(3, "voltage", d=3.0) - 0.3:
        u = clamp((t - WORD(3, "voltage", d=3.0) + 0.3) / 0.3); vtag(c, 330, 1160, "11,000 V", GOLD, u); vtag(c, 750, 1160, "11,000 V", GOLD, u)
    nd = WORD(3, "downhill", d=4.5)
    if t > nd - 0.3: chip(c, "DIFFERENCE: 0 V", GREEN, 1400, clamp((t - nd + 0.3) / 0.3), 60)
    nc = WORD(3, "current", d=5.5)
    if t > nc - 0.2: check(c, 540, 1580, 60, clamp((t - nc) / 0.3)); lab(c, 540, 620, "NO CURRENT THROUGH THE BIRD", WHITE, clamp((t - nc) / 0.3), 38, INK)
def s_zap(c, t, lt, d):
    zp = WORD(4, "zap", d=3.0)
    sky(c, t, 0.0); pole(c, 900, 760)
    wire(c, -100, 900, 820, 60, t, 10); wire(c, -100, 900, 1040, 60, t, 10)
    hit = t > zp - 0.05
    bx = 420; by = wirey(bx, -100, 900, 1040, 60)
    bird(c, bx, by, 1.0, t, wing=0.6 * ease(clamp((lt - 0.6) / 0.6)) if not hit else 0.6, face=-1, mood="dizzy" if t > zp + 0.6 else "calm", singe=clamp((t - zp) / 0.3))
    tw = WORD(4, "two", d=1.0)
    if t > tw - 0.2: lab(c, 540, 600, "TWO WIRES", WHITE, clamp((t - tw + 0.2) / 0.3), 40, RED)
    if hit and t < zp + 0.7:
        zapbolt(c, 520, wirey(520, -100, 900, 820, 60), 420, by - 80, t, 12)
        if t < zp + 0.15: c.save(); c.identity_matrix(); c.set_source_rgba(1, 1, 1, 0.7); c.paint(); c.restore()
    if hit: bigtxt(c, "ZAP!", 1400, 160, GOLD, t, zp)
    pt = WORD(4, "path", d=4.0)
    if t > pt - 0.2: chip(c, "NOW THERE'S A PATH", RED, 1600, clamp((t - pt + 0.2) / 0.3), 52)
def s_eagle(c, t, lt, d):
    sky(c, t); pole(c, 540, 900, 1.6)
    wire(c, -100, 540 - 320, 965, 40, t, 10); wire(c, 540 + 320, 1180, 965, 40, t, 10)
    dg = WORD(5, "danger", d=2.0)
    eagle(c, 540, 860 + 10 * math.sin(t * 3), 1.0, t, glowc=clamp((t - dg + 0.3) / 0.3) * (0.6 + 0.4 * math.sin(t * 10)))
    if t > dg - 0.3: chip(c, "BIG BIRDS IN DANGER", RED, 520, clamp((t - dg + 0.3) / 0.3), 52)
    wd = WORD(5, "wide", d=4.0)
    if t > wd - 0.3: arrow(c, 120, 1260, 960, 1260, WHITE, 10, 1.0); arrow(c, 960, 1260, 120, 1260, WHITE, 10, 1.0); lab(c, 540, 1340, "WINGSPAN UP TO 2 M", WHITE, clamp((t - wd + 0.3) / 0.3), 38, INK)
def s_ground(c, t, lt, d):
    sky(c, t, 0.2); pole(c, 900, 800)
    pts = [(900 - 30, 840)] + [(900 - 30 - 40 * k, 840 + 60 * k + 20 * math.sin(k)) for k in range(1, 13)] + [(200, 1660)]
    line(c, pts, 10, WIRE)
    sparks(c, 230, 1650, t, 10, 70, 4); glow(c, 230, 1650, 160, ELEC, 0.4 + 0.2 * math.sin(t * 20))
    nv = WORD(6, "never", d=1.5); gr = WORD(6, "ground", d=4.0); bp = WORD(6, "path", d=6.0)
    back_ = ease(clamp((t - nv) / 1.0))
    guy(c, 640 - 160 * (1 - back_) + 0, 1800, 0.9, t, face=-1, mood="scared", jacket=HOOD, scarf=False, armF=1.6, elbF=-0.3, armB=1.2)
    if t > nv - 0.2: chip(c, "NEVER GO NEAR IT", RED, 500, clamp((t - nv + 0.2) / 0.3), 52)
    if t > gr - 0.2:
        for k in range(5): ph = (t * 1.2 + k / 5) % 1; ell(c, 230 + 380 * ph, 1700 + 20 * math.sin(ph * 6), 10, 6, ELEC, 1 - ph)
    if t > bp - 0.3: lab(c, 640, 1360, "YOU BECOME THE PATH", WHITE, clamp((t - bp + 0.3) / 0.3), 40, RED)
    if t > bp + 0.6: chip(c, "STAY AWAY. CALL FOR HELP.", INK, 650, clamp((t - bp - 0.6) / 0.3), 44)
def s_end(c, t, lt, d):
    sky(c, t); pole(c, 1000, 760)
    wire(c, -100, 1000, 800, 140, t, 12)
    fr = WORD(7, "friend", d=1.2); th = WORD(7, "them", d=4.0); tb = WORD(7, "tell", d=5.0)
    reach = ease(clamp((lt - 0.4) / 2.2)) * (1 - ease(clamp((t - th) / 0.4)) * 0.0)
    if t > tb: reach = reach * (1 - ease(clamp((t - tb) / 0.5)))
    wob = 0.08 * math.sin(t * 9) if t < th else 0
    for sx in (-70, 70): line(c, [(430 + sx, 1665), (430 + sx * 0.75, 1335)], 14, (0.85, 0.6, 0.2))
    for k in range(5): yy = 1640 - k * 70; w_ = 70 - k * 4; line(c, [(430 - w_, yy), (430 + w_, yy)], 10, (0.85, 0.6, 0.2))
    guy(c, 430, 1365, 1.0, t, face=1, jacket=(0.2, 0.62, 0.3), cap=False, hair=(0.2, 0.14, 0.1), scarf=False, mood="happy", armF=0.3 + 1.8 * reach + wob, elbF=0.7 * reach, armB=-0.3)
    pull = ease(clamp((t - fr) / 0.4))
    guy(c, 860, 1660, 1.0, t, face=-1, jacket=HOOD, scarf=False, mood="scared", armF=0.4 + 1.3 * pull, armB=0.2 + 0.6 * pull, lean=0.15 * pull, shiver=pull)
    if reach > 0.8: sparks(c, 525, 945, t, 6, 45, 3, a=0.8)
    if t > fr - 0.2: chip(c, "SEND THIS TO THAT FRIEND", RED, 520, clamp((t - fr + 0.2) / 0.3), 52)
    if t > th - 0.3 and t < tb:
        u = clamp((t - th + 0.3) / 0.3)
        c.save(); c.identity_matrix(); g_ = cairo.RadialGradient(430, 1100, 260, 430, 1100, 760); g_.add_color_stop_rgba(0, 0, 0, 0, 0); g_.add_color_stop_rgba(1, 0, 0, 0, 0.45 * u); c.set_source(g_); c.paint(); c.restore()
        arrow(c, 170, 1120, 340, 1170, GOLD, 14, u); lab(c, 190, 1060, "YES. THEM.", INK, u, 46, GOLD)
    if t > tb - 0.2:
        k = back(clamp((t - tb + 0.2) / 0.35)); c.save(); c.translate(540, 680); c.scale(k, k)
        shadow_rr(c, -430, -95, 860, 190, 50, INK); txt(c, "WHAT SHOULD I", 0, -32, 60, WHITE); txt(c, "EXPLAIN NEXT?", 0, 38, 60, GOLD); c.restore()
FN = {n: globals()["s_" + n] for n, _ in SC}
FLASH = {"secret", "water", "feet", "eagle"}
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
    else:
        a0, a1, out = float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))): p.stdin.write(bytes(render(i / FPS).get_data()))
        p.stdin.close(); p.wait(); print("rendered", out)
