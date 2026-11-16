def render(t):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    name, lt, d, k = scene_at(t)
    z = 1 + 0.035 * clamp(lt / max(d, 0.1)); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    FN[name](c, t, lt, d)
    c.identity_matrix()
    if name in CUT_FLASH and lt < 0.14: c.set_source_rgba(1, 1, 1, 0.5 * (1 - lt / 0.14)); c.paint()
    elif lt < 0.1 and k > 0: c.set_source_rgba(0, 0, 0, 0.6 * (1 - lt / 0.1)); c.paint()
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
