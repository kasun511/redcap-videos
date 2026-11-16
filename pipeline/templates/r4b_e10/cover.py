from PIL import Image, ImageDraw, ImageFont
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
W, H = 1080, 1920
im = Image.open("raw/hotel.jpg").convert("RGB")
s = max(W / im.width, H / im.height) * 1.25
im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
x0 = int((im.width - W) * 0.52); y0 = max(0, int((im.height - H) / 2) - 60)
im = im.crop((x0, y0, x0 + W, y0 + H))
d = ImageDraw.Draw(im, "RGBA")
d.rectangle([0, 0, W, 330], fill=(0, 0, 0, 170)); d.rectangle([0, 1250, W, H], fill=(0, 0, 0, 130))
d.rectangle([0, 240, W, 400], fill=(10, 10, 12, 235))
d.text((W // 2, 320), "THE RULES OF ROOM 4B", font=ImageFont.truetype(FB, 72), fill="white", anchor="mm")
d.rounded_rectangle([420, 430, 660, 512], 40, fill=(228, 45, 40))
d.text((W // 2, 472), "PART 10", font=ImageFont.truetype(FB, 46), fill="white", anchor="mm")
for ln, yy in (("RULE", 1390), ("NINE", 1540)):
    for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-5, -5), (5, 5), (-5, 5), (5, -5)):
        d.text((W // 2 + ox, yy + oy), ln, font=ImageFont.truetype(FB, 142), fill=(0, 0, 0), anchor="mm")
    d.text((W // 2, yy), ln, font=ImageFont.truetype(FB, 142), fill=(255, 205, 40), anchor="mm")
d.rounded_rectangle([150, 1640, 930, 1736], 26, fill=(12, 12, 14, 240))
d.text((W // 2, 1688), "The only way out of 4B", font=ImageFont.truetype(FB, 48), fill=(240, 235, 228), anchor="mm")
d.rounded_rectangle([330, 1770, 750, 1860], 26, fill=(200, 30, 28))
d.text((W // 2, 1816), "SERIES FINALE", font=ImageFont.truetype(FB, 44), fill="white", anchor="mm")
im.save("cover.png")
im.resize((300, 533)).save("/tmp/claude-0/-home-claude/1f0ee3e5-19dd-58f1-9528-636514cc0c08/scratchpad/e10cov.png")
