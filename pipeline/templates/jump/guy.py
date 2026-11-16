JACK = (0.16, 0.36, 0.55); PANT = (0.22, 0.24, 0.32); BOOT = (0.25, 0.2, 0.18); SCARF = (0.86, 0.16, 0.16)
# ------------------------------------------------------------------ the guy (full pose control)
def seg(c, x0, y0, ang, L, w, col):
    x1, y1 = x0 + math.sin(ang) * L, y0 + math.cos(ang) * L; line(c, [(x0, y0), (x1, y1)], w, col); return x1, y1
def guy(c, x, y, s, t, face=1, walk=0.0, armF=0.2, armB=-0.2, elbF=0.0, elbB=0.0, lean=0.0, sit=0.0, mood="calm", shiver=0.0, cold=0.0, holdF=None, mouth=0.0, alpha=1.0, phase=0.0, jacket=None, scarf=True, cap=True, hair=None, pants=None):
    """y = feet. angles in rad from straight down, + = towards facing direction. sit 0..1"""
    if alpha < 1: c.push_group()
    c.save(); c.translate(x + (math.sin(t * 50) * 3 * shiver), y); c.scale(s * face, s)
    ph = t * 6.5 + phase; sw = math.sin(ph) * walk; bob = -abs(math.sin(ph)) * 10 * walk
    hipy = -150 + 80 * sit + bob
    J0 = jacket or JACK; jack = mix(J0, (0.55, 0.65, 0.85), cold * 0.5); jack2 = mix(mix(J0, INK, 0.25), (0.4, 0.5, 0.75), cold * 0.5); PANT_ = pants or PANT; skin = mix(SKIN, (0.75, 0.85, 1.0), cold * 0.6)
    # legs (back then front)
    for k, sd in enumerate((-1, 1)):
        if sit > 0.5:
            kx, ky = seg(c, 0, hipy, 1.45, 80, 44, PANT_); fx_, fy_ = seg(c, kx, ky, 0.15, 70, 40, PANT_)
        else:
            th = sd * 0.5 * sw; kx, ky = seg(c, 0, hipy, th, 75, 44, mix(PANT_, INK, 0.15 if k == 0 else 0)); fx_, fy_ = seg(c, kx, ky, th - max(0, sd * sw) * 0.6 * walk, 75, 40, mix(PANT_, INK, 0.15 if k == 0 else 0))
        rr(c, fx_ - 22, fy_ - 12, 58, 28, 12, BOOT)
    c.save(); c.translate(0, hipy); c.rotate(lean)
    by = math.sin(t * 2.2 + phase) * 3
    # back arm
    def arm(ang, elb, col, hold=None):
        ex, ey = seg(c, 0, -165 + by, ang, 80, 38, col); hx, hy = seg(c, ex, ey, ang + elb, 72, 34, col)
        ell(c, hx, hy, 20, 20, (0.25, 0.25, 0.3))  # glove
        if hold: hold(c, hx, hy)
        return hx, hy
    arm(armB + 0.15 * sw, elbB, jack2)
    # torso (puffy jacket)
    rr(c, -66, -195 + by, 132, 205, 50, jack); for_k = None
    for k in range(3): line(c, [(-56, -150 + k * 55 + by), (56, -150 + k * 55 + by)], 5, jack2, 0.6)
    line(c, [(8, -190 + by), (8, 5 + by)], 5, jack2)
    # scarf + tail flapping
    if scarf: rr(c, -55, -205 + by, 110, 34, 16, SCARF)
    fl = [(-30, -190 + by)] + [(-30 - 22 * j, -185 + by + 10 * j + 12 * math.sin(t * 9 - j)) for j in range(1, 5)]
    if scarf: line(c, fl, 22, SCARF)
    hx, hy = arm(armF - 0.15 * sw, elbF, jack, holdF)
    # head
    c.save(); c.translate(6, -270 + by)
    ell(c, 0, 0, 72, 76, skin)
    if cap:
        c.new_path(); c.arc(0, -10, 74, math.pi * 1.0, math.pi * 2.0); c.close_path(); c.set_source_rgb(*CAP); c.fill()
        rr(c, -76, -24, 152, 22, 11, CAP2); rr(c, 40, -26, 70, 18, 9, CAP2)
    else:
        c.new_path(); c.arc(0, -6, 76, math.pi * 1.0, math.pi * 2.0); c.close_path(); c.set_source_rgb(*(hair or HAIR)); c.fill(); ell(c, -50, -10, 30, 34, hair or HAIR)
    ex = 14
    blink = (t + phase) % 3.3 < 0.12
    for sx in (-20, 26):
        if mood == "happy": c.new_path(); c.arc(sx + ex, 14, 9, math.pi, TAU); c.set_line_width(5); c.set_source_rgba(*INK, 1); c.stroke()
        else: ell(c, sx + ex, 12, 8 if mood != "scared" else 10, 1.5 if blink else (11 if mood != "scared" else 14), INK)
    if mood in ("worried", "scared", "cold"):
        line(c, [(-34 + ex, -8), (-8 + ex, -14)], 5, INK); line(c, [(40 + ex, -8), (14 + ex, -14)], 5, INK)
    my = 46
    if mouth > 0.05: ell(c, 6 + ex, my, 14, 4 + 12 * mouth, (0.45, 0.12, 0.12))
    elif mood == "happy": c.new_path(); c.arc(6 + ex, my - 14, 16, 0.2, math.pi - 0.2); c.set_line_width(5); c.set_source_rgba(*INK, 1); c.stroke()
    elif mood == "cold": line(c, [(-8 + ex + 6 * k, my + (4 if k % 2 else -4)) for k in range(5)], 4, INK)
    elif mood == "scared": ell(c, 6 + ex, my, 10, 13, (0.45, 0.12, 0.12))
    else: line(c, [(-6 + ex, my), (18 + ex, my)], 5, INK)
    ell(c, -30 + ex, 32, 12, 7, (1, 0.45, 0.45), 0.55 + 0.3 * (1 - cold)); ell(c, 40 + ex, 32, 10, 7, (1, 0.45, 0.45), 0.55)
    ell(c, 62, 18, 9, 7, mix((1, 0.6, 0.55), (0.6, 0.75, 1), cold))  # nose
    c.restore(); c.restore(); c.restore()
    if alpha < 1: c.pop_group_to_source(); c.paint_with_alpha(alpha)
    return x + (6 + 62) * s * face, y + (hipy - 270 + 18) * s  # nose position
