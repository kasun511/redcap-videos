def SS(c, k):
    k = max(abs(k), 2e-3); c.scale(k, k)
# ================================================================== Ep 7 "Not Enough Power"
WATERC = (0.25, 0.6, 0.95); LEDP = (0.75, 0.3, 0.95); LETT = (0.45, 0.82, 0.3)
AMB = (1.0, 0.72, 0.2); DIESEL = (0.85, 0.45, 0.12); BATG = (0.2, 0.78, 0.45)
def cross(c, x, y, r, col=RED, w=14, a=1.0): line(c, [(x - r, y - r), (x + r, y + r)], w, col, a); line(c, [(x + r, y - r), (x - r, y + r)], w, col, a)
def check(c, x, y, r, a=1.0): ell(c, x, y, r, r, GREEN, a); line(c, [(x - r * 0.45, y), (x - r * 0.1, y + r * 0.35), (x + r * 0.5, y - r * 0.35)], r * 0.24, WHITE, a)
def lab(c, x, y, s, col=INK, a=1.0, size=34, bg=WHITE):
    if a <= 0: return
    c.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size); w = c.text_extents(s).x_advance + 40
    k = back(a); c.save(); c.translate(x, y); SS(c, k); shadow_rr(c, -w / 2, -size * 0.85, w, size * 1.7, size * 0.55, bg, min(1, a * 2)); txt(c, s, 0, 0, size, col, a=min(1, a * 2)); c.restore()
def bigtxt_(c, s, y, size, col, t, at, x=540):
    if t < at: return
    k = back(clamp((t - at) / 0.3)); c.save(); c.translate(x, y); SS(c, k); txt(c, s, 0, 0, size, col, stroke=10); c.restore()
def torchbeam(c, x, y, ang, L=900, a=0.25):
    c.new_path(); c.move_to(x, y); c.line_to(x + math.cos(ang - 0.26) * L, y + math.sin(ang - 0.26) * L); c.line_to(x + math.cos(ang + 0.26) * L, y + math.sin(ang + 0.26) * L)
    c.close_path(); c.set_source_rgba(1, 0.95, 0.75, a); c.fill()
def emerg(c, t, a=1.0):
    """red emergency strip lighting"""
    for x in (120, 540, 960):
        glow(c, x, 700, 240, (1, 0.2, 0.15), 0.18 * a * (0.7 + 0.3 * math.sin(t * 3 + x)))
        rr(c, x - 50, 690, 100, 16, 8, (1, 0.35, 0.3), a)
# ---- appliance icons -------------------------------------------------------
def ap_dehum(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s); rr(c, -52, -78, 104, 156, 18, (0.9, 0.92, 0.95), a); rr(c, -36, -58, 72, 54, 10, (0.6, 0.82, 1.0), a)
    for k in range(3): line(c, [(-32, 24 + k * 18), (32, 24 + k * 18)], 7, (0.72, 0.75, 0.8), a)
    c.restore()
def ap_fan(c, x, y, t, s=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s); c.new_path(); c.arc(0, 0, 72, 0, TAU); c.set_line_width(12); c.set_source_rgba(0.72, 0.75, 0.8, a); c.stroke()
    c.rotate(t * 7)
    for k in range(3): c.save(); c.rotate(k * TAU / 3); poly(c, [(0, 0), (58, -26), (58, 20)], (0.55, 0.6, 0.68), a); c.restore()
    c.restore(); ell(c, x, y, 12 * s, 12 * s, (0.4, 0.44, 0.5), a)
def ap_pump(c, x, y, t, s=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s); rr(c, -60, -40, 120, 80, 20, (0.2, 0.45, 0.9), a); ell(c, 0, 0, 30, 30, (0.75, 0.85, 0.95), a)
    rect(c, 52, -16, 40, 32, (0.5, 0.55, 0.62), a); rect(c, -92, -16, 40, 32, (0.5, 0.55, 0.62), a)
    c.restore()
def ap_light(c, x, y, s=1.0, a=1.0, on=1.0):
    rect(c, x - 90 * s, y - 10 * s, 180 * s, 18 * s, mix((0.35, 0.35, 0.4), LEDP, on), a)
    if on > 0: glow(c, x, y + 60 * s, 180 * s, LEDP, 0.35 * on * a)
def ap_fridge(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s); rr(c, -54, -86, 108, 172, 16, (0.88, 0.9, 0.93), a); line(c, [(-54, -10), (54, -10)], 5, (0.7, 0.72, 0.76), a)
    rr(c, 30, -70, 12, 40, 6, (0.6, 0.63, 0.7), a); rr(c, 30, 10, 12, 40, 6, (0.6, 0.63, 0.7), a); c.restore()
APS = {"DEHUMIDIFIER": lambda c, x, y, t, a: ap_dehum(c, x, y, 0.72, a),
       "AIR FANS": lambda c, x, y, t, a: ap_fan(c, x, y, t, 0.72, a),
       "WATER PUMP": lambda c, x, y, t, a: ap_pump(c, x, y, t, 0.72, a),
       "GROW LIGHTS": lambda c, x, y, t, a: ap_light(c, x, y, 0.8, a),
       "LIGHTS + MORE": lambda c, x, y, t, a: ap_fridge(c, x, y, 0.62, a)}
def loadrow(c, y, name, watts, t, at, maxw=600.0, run=None):
    """one appliance row: icon, name, animated watt bar + number"""
    u = clamp((t - at) / 0.35)
    if u <= 0: return
    k = back(u); c.save(); c.translate(100, y); SS(c, 1)
    c.save(); c.translate(0, 0); SS(c, k); shadow_rr(c, -70, -62, 920, 124, 30, (0.14, 0.15, 0.2), 0.96); c.restore()
    c.restore()
    APS[name](c, 150, y, t, u)
    txt(c, name, 250, y - 18, 34, WHITE, anchor="l", a=u)
    bw = 420 * (watts / maxw) * ease(clamp((t - at) / 0.6))
    rect(c, 250, y + 8, bw, 26, mix(AMB, RED, watts / maxw), u)
    txt(c, f"{watts} W", 960, y, 40, GOLD, anchor="r", a=u)
def totbar(c, t, val, maxv, y=1300, col=RED, labl="TOTAL"):
    w = 880 * clamp(val / maxv)
    rr(c, 100, y, 880, 70, 35, (0.16, 0.17, 0.22));
    if w > 8: rr(c, 100, y, max(w, 70), 70, 35, col)
    txt(c, labl, 540, y - 50, 36, WHITE, stroke=6)
# ---- solar / battery / generator -------------------------------------------
def panel(c, x, y, s=1.0, a=1.0, burn=0.0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt); SS(c, s)
    rr(c, -140, -90, 280, 180, 10, mix((0.14, 0.2, 0.42), (0.25, 0.1, 0.05), burn), a)
    for i in range(3):
        for j in range(2): rr(c, -128 + i * 88, -78 + j * 86, 76, 74, 6, mix((0.2, 0.32, 0.65), (0.3, 0.12, 0.06), burn), a)
    rr(c, -146, -96, 292, 192, 12, (0.7, 0.73, 0.8), 0)
    c.new_path(); c.rectangle(-146, -96, 292, 192); c.set_line_width(10); c.set_source_rgba(0.7, 0.73, 0.8, a); c.stroke()
    c.restore()
def crate(c, x, y, s=1.0, a=1.0, open_=0.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -200, -130, 400, 260, 16, (0.55, 0.4, 0.24), a)
    for k in (-1, 1): line(c, [(k * 170, -120), (k * 170, 120)], 16, (0.44, 0.31, 0.18), a)
    line(c, [(-190, -40), (190, -40)], 14, (0.44, 0.31, 0.18), a)
    c.save(); c.translate(0, -130); c.rotate(-0.5 * open_); rr(c, -205, -28, 410, 30, 10, (0.62, 0.46, 0.28), a); c.restore()
    txt(c, "SOLAR PANELS", 0, 50, 38, (0.3, 0.2, 0.1), a=a); txt(c, "OPEN AFTER THE FLASH", 0, 100, 24, (0.35, 0.24, 0.12), a=a)
    c.restore()
def battbank(c, x, y, t, s=1.0, a=1.0, lvl=1.0, n=6):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -250, -230, 500, 470, 18, (0.2, 0.22, 0.28), a)
    for i in range(3):
        for j in range(2):
            bx = -170 + i * 170; by = -140 + j * 200
            rr(c, bx - 72, by - 82, 144, 164, 14, (0.12, 0.14, 0.18), a); rr(c, bx - 60, by - 70, 120, 140, 10, (0.17, 0.2, 0.26), a)
            f = clamp(lvl * 6 - (i + j * 3)) if n else 1
            for k in range(4):
                on = f > (3 - k) / 4
                rr(c, bx - 46, by - 54 + k * 34, 92, 24, 8, mix((0.2, 0.22, 0.28), BATG if lvl > 0.25 else RED, 1 if on else 0.08), a)
    txt(c, "30 kWh", 0, 300, 44, GOLD, stroke=7, a=a); c.restore()
def genset(c, x, y, t, s=1.0, a=1.0, run=0.0):
    c.save(); c.translate(x, y); SS(c, s)
    if run > 0: c.translate(2.5 * math.sin(t * 61) * run, 2 * math.cos(t * 53) * run)
    rr(c, -190, -110, 380, 220, 20, mix((0.78, 0.4, 0.1), DIESEL, 0.5), a); rr(c, -160, -86, 150, 90, 12, (0.25, 0.27, 0.32), a)
    for k in range(4): line(c, [(30 + k * 32, -80), (30 + k * 32, 20)], 12, (0.3, 0.32, 0.38), a)
    rr(c, -205, 86, 410, 40, 14, (0.3, 0.32, 0.38), a)
    rect(c, 150, -210, 34, 110, (0.35, 0.37, 0.42), a)
    if run > 0:
        for k in range(5):
            ph = (t * 0.8 + k / 5) % 1; ell(c, 167 + 40 * ph * math.sin(k), -210 - 170 * ph, 22 + 46 * ph, 20 + 40 * ph, (0.45, 0.45, 0.48), 0.5 * (1 - ph) * a * run)
    c.restore()
def fueltank(c, x, y, s=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -80, -150, 160, 300, 26, (0.85, 0.5, 0.15), a); rr(c, -58, -120, 116, 60, 12, (0.95, 0.72, 0.4), a)
    txt(c, "DIESEL", 0, -86, 26, (0.5, 0.26, 0.06), a=a); rect(c, -30, 150, 60, 24, (0.45, 0.47, 0.52), a); c.restore()
def bucketfill(c, x, y, t, s=1.0, a=1.0, fill=0.5, pour=0.0):
    c.save(); c.translate(x, y); SS(c, s)
    poly(c, [(-130, -150), (130, -150), (100, 150), (-100, 150)], (0.75, 0.78, 0.84), a)
    f = clamp(fill)
    if f > 0.02:
        yt = 150 - 300 * f; wt = 100 + 30 * f
        poly(c, [(-wt, yt), (wt, yt), (100, 150), (-100, 150)], BATG, a)
    rr(c, -140, -164, 280, 28, 14, (0.6, 0.63, 0.7), a)
    if pour > 0:
        for k in range(6):
            ph = (t * 1.6 + k / 6) % 1; ell(c, 6 * math.sin(t * 5 + k), -420 + 260 * ph, 13, 20, BATG, (1 - ph * 0.5) * pour * a)
    c.restore()
# ---- electrolysis ----------------------------------------------------------
def electro(c, x, y, t, s=1.0, a=1.0):
    c.save(); c.translate(x, y); SS(c, s)
    rr(c, -150, -170, 300, 340, 24, (0.8, 0.9, 1.0), 0.45 * a)
    rect(c, -134, -60, 268, 216, WATERC, 0.75 * a); rr(c, -134, 120, 268, 36, 10, WATERC, 0.75 * a)
    for sd in (-1, 1):
        rect(c, sd * 70 - 12, -100, 24, 200, (0.6, 0.63, 0.7), a)
        for k in range(4):
            ph = (t * 1.1 + k / 4 + (0.3 if sd > 0 else 0)) % 1; ell(c, sd * 70 + 16 * math.sin(ph * 6 + k), 90 - 160 * ph, 10 + 7 * ph, 10 + 7 * ph, WHITE, 0.75 * (1 - ph) * a)
    txt(c, "H2", -70, -200, 34, WHITE, stroke=6, a=a); txt(c, "O2", 70, -200, 34, GOLD, stroke=6, a=a)
    c.restore()
def boltzap(c, x, y, s, col=GOLD, a=1.0): poly(c, [(x + 10 * s, y - 46 * s), (x - 26 * s, y + 6 * s), (x - 2 * s, y + 6 * s), (x - 14 * s, y + 46 * s), (x + 28 * s, y - 8 * s), (x + 4 * s, y - 8 * s)], col, a)
def fixcard(c, t, at, what):
    u = clamp((t - at) / 0.3); k = back(u)
    c.save(); c.translate(540, 600); SS(c, k); c.translate(-540, -600); chip(c, "FIX: " + what, GREEN, 600, 1.0, 44); c.restore()
def dark_room(c, t, k=1.0):
    vgrad(c, 0, H, mix((0.16, 0.17, 0.22), (0.03, 0.03, 0.05), k), mix((0.1, 0.11, 0.15), (0.01, 0.01, 0.02), k))
    rect(c, 0, 1560, W, H - 1560, mix((0.2, 0.2, 0.24), (0.04, 0.04, 0.06), k))
def arrow(c, x0, y0, x1, y1, col, w=12, a=1.0):
    if a <= 0: return
    an = math.atan2(y1 - y0, x1 - x0); hl = w * 2.6
    line(c, [(x0, y0), (x1 - math.cos(an) * hl * 0.6, y1 - math.sin(an) * hl * 0.6)], w, col, a)
    poly(c, [(x1, y1), (x1 - math.cos(an - 0.5) * hl, y1 - math.sin(an - 0.5) * hl), (x1 - math.cos(an + 0.5) * hl, y1 - math.sin(an + 0.5) * hl)], col, a)
