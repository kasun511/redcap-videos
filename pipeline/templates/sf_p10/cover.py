import sys; sys.argv = ["x", "none"]
exec(open("/home/claude/sf/p10/scenes.py").read().split('if __name__ == "__main__":')[0])
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
t = 2.2
auroras(c, t, 1.0)
valley(c, t, lit=0.0, ours=1.0)
c.save(); c.identity_matrix(); rect(c, 0, 280, W, 130, (0.05, 0.05, 0.07)); c.restore()
txt(c, "THE SOLAR FLASH", 540, 350, 72, WHITE)
shadow_rr(c, 410, 440, 260, 76, 38, RED); txt(c, "PART 10", 540, 480, 46, WHITE)
txt(c, "ELEVEN", 540, 690, 150, GOLD, stroke=16)
txt(c, "DAYS", 540, 830, 150, GOLD, stroke=16)
shadow_rr(c, 150, 880, 780, 80, 26, (0.12, 0.13, 0.17)); txt(c, "The night the grid died.", 540, 922, 40, WHITE)
shadow_rr(c, 330, 1000, 420, 66, 22, (0.6, 0.15, 0.13)); txt(c, "SERIES FINALE", 540, 1038, 36, WHITE)
surf.write_to_png("/home/claude/sf/p10/cover.png")
