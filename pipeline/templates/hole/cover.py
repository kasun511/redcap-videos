import sys; sys.argv = ["x", "none"]
exec(open("/home/claude/kb/hole/scenes.py").read().split('if __name__ == "__main__":')[0])
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
t = 1.0
space(c, t)
cutaway(c, t, cx=540, cy=1080, r=520)
faller(c, 540, 820, 0.46, t, spin=0.25)
c.save(); c.identity_matrix(); rect(c, 0, 300, W, 120, (0.05, 0.05, 0.08)); c.restore()
txt(c, "RED CAP EXPLAINS", 540, 362, 66, WHITE)
c.save(); c.identity_matrix(); c.set_source_rgba(0, 0, 0, 0.55); c.rectangle(0, 1460, W, 400); c.fill(); c.restore()
txt(c, "A HOLE THROUGH", 540, 1560, 90, WHITE, stroke=14)
txt(c, "THE EARTH", 540, 1670, 118, GOLD, stroke=16)
shadow_rr(c, 170, 1750, 740, 76, 26, RED); txt(c, "42 minutes. Then it gets worse.", 540, 1798, 36, WHITE)
surf.write_to_png("/home/claude/kb/hole/cover.png")
