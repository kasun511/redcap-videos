import json, re, math, subprocess, os, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
B = "/home/claude/room4b/e10/"; P5 = "/home/claude/cruise/p5/raw/"; P4 = "/home/claude/cruise/p4/raw/"; C = "/home/claude/cruise/"; P3 = C + "p3s/raw/"; W_ = B + "w/"; os.makedirs(W_ + "seg", exist_ok=True)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"; FPS = 30
TL = json.load(open(B + "timeline.json")); UN = TL["lines"]; TOTAL = TL["total"] + 0.6
IMG = {}
for k in ("window","manager","shoes","door4b","doorwide","note","lean","hotel","lobby"): IMG[k] = B + f"raw/{k}.jpg"
SHOTS = [("window","tight"),("manager","wide"),("shoes","wide"),("door4b","wide"),("truth",),("doorwide","tight"),
         ("note","tight"),("rule9",),("lean","tight"),("manager","tight"),("hotel","wide"),("lobby","wide"),("end",)]
assert len(SHOTS) == len(UN), (len(SHOTS), len(UN))
SHAKE = {2}; PUNCH = {0, 7}; GLITCH = {0, 2, 9}
MERGE = ("end", "truth", "rule9")
W, H = 1080, 1920; IMG_Y = 560; IMG_H = 720
def title(d):
    d.text((W // 2, 300), "The Rules of Room 4B", font=ImageFont.truetype(FB, 86), fill="white", anchor="mm", stroke_width=6, stroke_fill="black")
    d.text((W // 2, 405), "Part 10", font=ImageFont.truetype(FB, 80), fill=(255, 168, 64), anchor="mm", stroke_width=6, stroke_fill="black")
def load(key, box):
    im = Image.open(IMG[key]).convert("RGB")
    if box == "tight":
        w = im.width * 0.72; h = w * IMG_H / W; cx, cy = im.width / 2, im.height / 2; im = im.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)))
    s = max(W * 1.25 / im.width, IMG_H * 1.25 / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x0 = (im.width - int(W * 1.25)) // 2; y0 = (im.height - int(IMG_H * 1.25)) // 2
    return im.crop((x0, y0, x0 + int(W * 1.25), y0 + int(IMG_H * 1.25)))
def backdrop(im, out):
    bg = im.resize((int(im.width * H / im.height), H)).filter(ImageFilter.GaussianBlur(45)); bg = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H))
    bg = Image.eval(bg, lambda v: int(v * 0.5)); title(ImageDraw.Draw(bg)); bg.save(out, quality=94)
def card_frames(kind, args, n, pre, t0abs=0.0):
    paths = []; ncount = min(n, 22)
    for f in range(n):
        im = Image.new("RGB", (W, H), (6, 6, 8)); d = ImageDraw.Draw(im); title(d)
        p = min(1.0, f / max(1, ncount - 1)); p = 1 - (1 - p) ** 3
        tt = t0abs + f / FPS
        if kind == "truth":
            d.text((W // 2, 580), "HOW IT ACTUALLY WORKS", font=ImageFont.truetype(FB, 52), fill=(255, 168, 64), anchor="mm")
            if f > 4:
                d.rounded_rectangle([90, 680, 990, 900], 30, fill=(20, 60, 32))
                d.text((W // 2, 760), "WROTE THE RULES", font=ImageFont.truetype(FB, 56), fill="white", anchor="mm")
                d.text((W // 2, 840), "GOT OUT", font=ImageFont.truetype(FB, 64), fill=(120, 240, 150), anchor="mm")
            if f > 22:
                d.rounded_rectangle([90, 960, 990, 1180], 30, fill=(70, 18, 18))
                d.text((W // 2, 1040), "ONLY FOLLOWED THEM", font=ImageFont.truetype(FB, 56), fill="white", anchor="mm")
                d.text((W // 2, 1120), "WENT IN", font=ImageFont.truetype(FB, 64), fill=(255, 90, 80), anchor="mm")
        elif kind == "rule9":
            d.rounded_rectangle([70, 620, 1010, 1300], 30, fill=(238, 232, 212))
            d.text((W // 2, 700), "RULE 9", font=ImageFont.truetype(FB, 84), fill=(170, 25, 25), anchor="mm")
            if f > 6: d.text((W // 2, 880), "There is no job.", font=ImageFont.truetype(MONO, 56), fill=(45, 40, 36), anchor="mm")
            if f > 20: d.text((W // 2, 1000), "Go home.", font=ImageFont.truetype(MONO, 62), fill=(45, 40, 36), anchor="mm")
            if f > 34:
                d.line([340, 1140, 740, 1160], fill=(30, 50, 140), width=7)
                d.line([360, 1170, 700, 1130], fill=(30, 50, 140), width=6)
                d.text((W // 2, 1240), "signed", font=ImageFont.truetype(FB, 36), fill=(130, 124, 112), anchor="mm")
        elif kind == "end":
            d.text((W // 2, 680), "WHICH RULE", font=ImageFont.truetype(FB, 72), fill="white", anchor="mm")
            d.text((W // 2, 780), "WOULD YOU BREAK?", font=ImageFont.truetype(FB, 62), fill=(235, 40, 40), anchor="mm")
            if f > 8:
                d.rounded_rectangle([140, 950, 940, 1090], 36, fill=(235, 60, 50))
                d.text((W // 2, 1020), "THE FULL STORY IS UP", font=ImageFont.truetype(FB, 52), fill="white", anchor="mm")
            if f > 16:
                d.rounded_rectangle([110, 1170, 970, 1300], 30, fill=(40, 40, 46))
                d.text((W // 2, 1212), "ALL 10 PARTS", font=ImageFont.truetype(FB, 46), fill="white", anchor="mm")
                d.text((W // 2, 1265), "to my YouTube", font=ImageFont.truetype(FB, 36), fill=(255, 168, 64), anchor="mm")
        pth = f"{pre}_{f:04d}.png"
        if kind in ("truth",) or f < ncount + 14 or f == n - 1 or not paths: im.save(pth); paths.append(pth)
        else: paths.append(paths[-1])
    return paths
# ---- segments: merge consecutive units with identical shots (morse, end, etc.)
segs = []; i = 0
while i < len(UN):
    j = i + 1
    while j < len(UN) and SHOTS[j] == SHOTS[i] and SHOTS[i][0] in MERGE: j += 1
    t0 = 0.0 if i == 0 else UN[i]["t0"] - 0.08; t1 = UN[j]["t0"] - 0.08 if j < len(UN) else TOTAL
    segs.append((i, t0, t1)); i = j
lst = []; fa = 0
SKIP = os.path.exists(W_ + "base.mp4") and not os.environ.get("REBUILD")
for k, (i, t0, t1) in enumerate(segs if not SKIP else []):
    sh = SHOTS[i]; n = round(t1 * FPS) - fa; fa += n; out = W_ + f"seg/{k:02d}.mp4"; flash = k == 0 or SHOTS[segs[k - 1][0]][0] != sh[0]
    if sh[0] in ("truth", "rule9", "end"):
        fr = card_frames(sh[0], sh[1:], n, W_ + f"seg/c{k:02d}", t0)
        with open(W_ + f"seg/c{k:02d}.txt", "w") as f:
            for p in fr: f.write(f"file '{p}'\nduration {1/FPS:.6f}\n")
        vf = "fps=30,format=yuv420p" + (",fade=t=in:st=0:d=0.12:color=white" if flash else "")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", W_ + f"seg/c{k:02d}.txt", "-frames:v", str(n), "-vf", vf,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", "30", out], check=True)
    else:
        pic = load(sh[0], sh[1]); pic.save(W_ + f"seg/p{k:02d}.jpg", quality=95); backdrop(pic, W_ + f"seg/b{k:02d}.jpg")
        zin = k % 2 == 0; dx = [0, 40, -40][k % 3]
        if i in PUNCH: z = f"if(lt(on,7),1+0.14*on/7,1.14+0.03*(on-7)/{n})"
        elif zin: z = f"1+0.10*on/{n}"
        else: z = f"1.10-0.10*on/{n}"
        zp = f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)+{dx}*on/{n}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{IMG_H}:fps={FPS}"
        fx = ""
        if i in SHAKE: fx += f",crop={W-40}:{IMG_H-28}:x='20+18*sin(t*47)*exp(-t*1.6)':y='14+12*sin(t*63)*exp(-t*1.6)',scale={W}:{IMG_H}"
        if i in GLITCH: fx += ",rgbashift=rh=8:bh=-8:enable='lt(mod(t,0.9),0.09)'"
        fc = f"[1:v]scale={int(W*1.25)}:{int(IMG_H*1.25)},{zp}{fx},setsar=1[p];[0:v]scale={W}:{H},setsar=1[b];[b][p]overlay=0:{IMG_Y},format=yuv420p" + (",fade=t=in:st=0:d=0.12:color=white" if flash else "") + "[v]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", W_ + f"seg/b{k:02d}.jpg", "-loop", "1", "-framerate", "30", "-i", W_ + f"seg/p{k:02d}.jpg",
                        "-filter_complex", fc, "-map", "[v]", "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", "30", out], check=True)
    lst.append(f"file '{out}'")
if not SKIP:
    open(W_ + "seg/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", W_ + "seg/list.txt", "-c", "copy", W_ + "base.mp4"], check=True)
print("base ok", len(segs), flush=True)
# ---- captions (3-word groups; Lena pink, coast guard green, each with a speaker tag)
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
HI = {"nar": "&H0042C5F5&", "woman": "&H00F5C8A0&"}; BASE = {"nar": "&HFFFFFF&", "woman": "&HF5E8E0&"}
TAG = {"woman": ("THE VOICE", "&H00F0B070&")}
ev = []
for i, u in enumerate(UN):
    if SHOTS[i][0] in ("end",): continue
    who = u["who"]; WT = u["words"]; nxt = UN[i + 1]["t0"] - 0.02 if i + 1 < len(UN) else TOTAL
    ypos = 1360 if SHOTS[i][0] not in ("rule9", "truth") else 1640
    groups = []; cur = []
    for w, t in WT:
        if cur and (len(cur) == 3 or re.search(r"[.,?!:]$", cur[-1][0])): groups.append(cur); cur = []
        cur.append((w, t))
    if cur: groups.append(cur)
    for gi, g3 in enumerate(groups):
        for jj, (w, st) in enumerate(g3):
            st = st - 0.04
            if jj + 1 < len(g3): en = g3[jj + 1][1] - 0.04
            elif gi + 1 < len(groups): en = groups[gi + 1][0][1] - 0.04
            else: en = min(nxt, st + 1.6)
            txt = " ".join((("{\\c" + HI[who] + "}" + x.upper() + "{\\c" + BASE[who] + "}") if q == jj else x.upper()) for q, (x, _) in enumerate(g3))
            ev.append((st, en, "Cap", f"{{\\pos(540,{ypos})}}" + ("{\\fscx75\\fscy75\\t(0,100,\\fscx100\\fscy100)}" if jj == 0 else "") + "{\\c" + BASE[who] + "}" + txt))
    if who in TAG:
        lab, col = TAG[who]; ev.append((u["t0"] - 0.05, u["t1"] + 0.1, "Tag", f"{{\\pos(540,{ypos - 62})\\c{col}}}" + lab))
ev.append((UN[6]["t0"], UN[9]["t0"], "Prompt", "{\\pos(540,1560)}WOULD YOU HAVE SIGNED IT?"))
hdr = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
       "Style: Cap,Poppins,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,-1,0,0,0,100,100,0,0,1,9,5,8,50,50,0,1\n"
       "Style: Prompt,Poppins,50,&H00FFFFFF,&H00FFFFFF,&H002020C8,&H002020C8,-1,0,0,0,100,100,1,0,3,14,0,8,50,50,0,1\n"
       "Style: Tag,Poppins,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,-1,0,0,0,100,100,2,0,3,10,0,8,50,50,0,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
open(W_ + "cap.ass", "w").write(hdr + "".join(f"Dialogue: 0,{ts(a)},{ts(b)},{s},,0,0,0,,{x}\n" for a, b, s, x in ev if b > a))
# ---- sound design
src = open(C + "ep1v3/sfx3.py").read(); lib = src[:src.index("# ---------- place cues")]
g = {}; exec(lib.replace('T = json.load(open("/home/claude/cruise/ep1v3/timeline.json"))', 'T={"total":%f,"scene":{},"phr":{}}' % TOTAL), g)
SR = 48000; N = int(TOTAL * SR) + SR; L = np.zeros(N); rng = np.random.default_rng(5)
def put(x, at, gn=1.0):
    i = int(max(0, at) * SR); x = x[:max(0, N - i)] * gn; L[i:i + len(x)] += x
def tone(f, d, gn=0.4):
    n = int(d * SR); return g["norm"](np.sin(2 * np.pi * f * np.arange(n) / SR) * g["env"](n, 0.004, 0.02), gn)
def knock(big=1.0):
    n = int(0.2 * SR); t = np.arange(n) / SR
    return g["norm"](np.sin(2 * np.pi * 95 * t) * np.exp(-t * 30) + 0.5 * g["lp"](rng.standard_normal(n), 1500) * np.exp(-t * 50), 0.95 * big)
def whoosh(d=0.45):
    n = int(d * SR); x = g["bp"](rng.standard_normal(n), 300, 3000) * np.sin(np.pi * np.arange(n) / n) ** 2; return g["norm"](x, 0.35)
def static(d, gn=0.22):
    n = int(d * SR); return g["norm"](g["hp"](rng.standard_normal(n), 1500) * (0.5 + 0.5 * (rng.random(n) > 0.3)) * g["env"](n, 0.03, 0.3), gn)
def ring(d):
    n = int(d * SR); t = np.arange(n) / SR; gate = ((t % 1.2) < 0.4) | (((t % 1.2) > 0.5) & ((t % 1.2) < 0.9))
    return g["norm"]((np.sin(2 * np.pi * 1300 * t) + np.sin(2 * np.pi * 1700 * t)) * gate * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * t))), 0.35)
def growl(d=1.2, f=70):
    n = int(d * SR); t = np.arange(n) / SR
    return g["norm"](g["bp"](rng.standard_normal(n), f, f * 6) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / d) ** 1.5, 0.6)
def waves(d):
    n = int(d * SR); t = np.arange(n) / SR; return g["norm"](g["lp"](rng.standard_normal(n), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t)) ** 2 * g["env"](n, 1.0, 1.0), 0.25)
tt = np.arange(N) / SR; L += (np.sin(2 * np.pi * 48 * tt) * 0.5 + g["lp"](rng.standard_normal(N), 160) * 2) * 0.008
S = lambda i: UN[i]["t0"]; E = lambda i: UN[i]["t1"]
for k, (i, t0, t1) in enumerate(segs):
    if k and SHOTS[i][0] != SHOTS[segs[k - 1][0]][0]: put(whoosh(), t0 - 0.2, 0.45)
def brake(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR; f = 2400 + 600 * np.sin(2 * np.pi * 3 * t)
    sq = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * rng.random(n)); return g["norm"]((sq * 0.5 + g["hp"](rng.standard_normal(n), 3000) * 0.5) * g["env"](n, 0.02, 0.4), 0.5)
def winch(d=3.0):
    n = int(d * SR); t = np.arange(n) / SR; cl = (np.sin(2 * np.pi * 14 * t) > 0.92).astype(float)
    return g["norm"](g["lp"](rng.standard_normal(n), 220) * 3 + g["bp"](cl * rng.standard_normal(n), 800, 4000) * 2 + np.sin(2 * np.pi * 55 * t) * 0.6, 0.7) * g["env"](n, 0.1, 0.4)
def splash(big=1.0):
    n = int(0.9 * SR); t = np.arange(n) / SR; return g["norm"](g["bp"](rng.standard_normal(n), 300, 5000) * np.exp(-t * 5) * (1 - np.exp(-t * 80)), 0.8 * big)
def engine(d):
    n = int(d * SR); t = np.arange(n) / SR; x = sum(np.sin(2 * np.pi * 32 * h * t) / h for h in range(1, 6)) * (0.7 + 0.3 * np.sin(2 * np.pi * 8 * t))
    return g["norm"](x + g["lp"](rng.standard_normal(n), 300) * 0.5, 0.4) * g["env"](n, 0.6, 1.5)
def phone_ring(d):
    n = int(d * SR); t = np.arange(n) / SR; gate = ((t % 2.0) < 0.9) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * t)))
    return g["norm"]((np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)) * gate, 0.5)
def ding():
    n = int(1.5 * SR); t = np.arange(n) / SR; return g["norm"]((np.sin(2 * np.pi * 1318 * t) + 0.6 * np.sin(2 * np.pi * 1046 * t)) * np.exp(-t * 3), 0.4)
def rain(d):
    n = int(d * SR); return g["norm"](g["bp"](rng.standard_normal(n), 800, 6000) * g["env"](n, 0.5, 0.5), 0.15)
def sob(d):
    n = int(d * SR); return g["norm"](g["bp"](rng.standard_normal(n), 400, 2500) * g["env"](n, 0.2, 0.5), 0.12)
def hum(d):
    n = int(d * SR); t = np.arange(n) / SR; mel = [392, 440, 392, 330, 294, 330, 392, 392]
    f = np.array([mel[int(x / 0.7) % len(mel)] for x in t]); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t))
    return g["norm"](g["lp"](x, 1200) * g["env"](n, 0.8, 1.0), 0.18)
def printer(d):
    n = int(d * SR); t = np.arange(n) / SR; cl = (np.sin(2 * np.pi * 24 * t) > 0.6).astype(float)
    return g["norm"](g["bp"](rng.standard_normal(n) * cl, 600, 4000) + 0.4 * np.sin(2 * np.pi * 120 * t), 0.5) * g["env"](n, 0.05, 0.2)
def click_(): n = int(0.05 * SR); return g["norm"](rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 120), 0.7)
def breath(d):
    n = int(d * SR); t = np.arange(n) / SR; return g["norm"](g["bp"](rng.standard_normal(n), 300, 2500) * (0.5 - 0.5 * np.cos(2 * np.pi * t / 2.4)) ** 2, 0.35)
def squeak(d):
    n = int(d * SR); t = np.arange(n) / SR; f = 1800 + 400 * np.sin(2 * np.pi * 1.3 * t)
    gate = (np.sin(2 * np.pi * 1.6 * t) > 0.3).astype(float); return g["norm"](np.sin(2 * np.pi * np.cumsum(f) / SR) * gate * 0.5 + g["lp"](rng.standard_normal(n), 300) * 0.5, 0.3)
def breath(d):
    n = int(d * SR); t = np.arange(n) / SR; return g["norm"](g["bp"](rng.standard_normal(n), 300, 2500) * (0.5 - 0.5 * np.cos(2 * np.pi * t / 2.4)) ** 2, 0.35)
def squeak(d):
    n = int(d * SR); t = np.arange(n) / SR; f = 1800 + 400 * np.sin(2 * np.pi * 1.3 * t)
    gate = (np.sin(2 * np.pi * 1.6 * t) > 0.3).astype(float); return g["norm"](np.sin(2 * np.pi * np.cumsum(f) / SR) * gate * 0.5 + g["lp"](rng.standard_normal(n), 300) * 0.5, 0.3)
def stepfx(): n = int(0.18 * SR); t = np.arange(n) / SR; return g["norm"](g["lp"](rng.standard_normal(n), 700) * np.exp(-t * 30), 0.55)
def WDT(i, w):
    for x, t in UN[i]["words"]:
        if re.sub(r"[^a-z0-9]", "", x.lower()) == w: return t
    return UN[i]["t0"]
def powerdownx():
    n = int(1.4 * SR); t = np.arange(n) / SR; f = 240 * np.exp(-t * 2.2) + 28
    return g["norm"](np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.8), 0.6)
def sigh2():
    n = int(1.2 * SR); t = np.arange(n) / SR
    return g["norm"](g["bp"](rng.standard_normal(n), 250, 1600) * np.sin(np.pi * t / 1.2) ** 2, 0.35)
def knockfx(): n = int(0.35 * SR); t = np.arange(n) / SR; return g["norm"](g["lp"](rng.standard_normal(n), 500) * np.exp(-t * 18) + 0.6 * np.sin(2 * np.pi * 85 * t) * np.exp(-t * 14), 0.9)
put(g["boom"](), 0.05, 0.5); put(g["wind"](TOTAL), 0, 0.12); put(g["stinger"](), 0.2, 0.45)
put(g["heartbeat"](S(7), 88, 150), 0.4, 0.36)
put(printer(0.5), S(1) + 0.6, 0.25); put(click_(), S(1) + 2.6, 0.5)
put(g["stinger"](), S(2) + 0.2, 0.4); put(growl(2.0, 56), S(2) + 0.4, 0.35)
put(g["boom"](), S(3) + 0.1, 0.5); put(breath(2.4), S(3) + 1.4, 0.4)
put(tone(640, 0.16, 0.3), S(4) + 0.5, 0.5); put(tone(420, 0.18, 0.3), S(4) + 3.2, 0.5)
put(g["creak"](1.8), S(5) + 0.6, 0.35)
for k in range(6): put(click_(), S(6) + 0.5 + k * 0.28, 0.45)
put(g["boom"](), S(7) + 0.1, 0.55); put(static(1.0, 0.22), S(7) + 0.1, 0.5); put(ding(), S(7) + 1.6, 0.5)
for k in range(4): put(click_(), S(8) + 0.4 + k * 0.5, 0.5)
put(printer(0.6), S(8) + 2.4, 0.28)
put(breath(3.0), S(9) + 0.6, 0.45); put(g["stinger"](), WDT(9, "before") - 0.3, 0.5)
for k in range(7): put(stepfx(), S(10) + 0.6 + k * 0.5, 0.6)
put(powerdownx(), WDT(10, "dark") - 0.1, 0.8)
put(ding(), S(11) + 0.6, 0.45); put(sigh2(), S(11) + 2.6, 0.5)
put(g["boom"](), S(12), 0.5)
sf.write(W_ + "sfx.wav", np.stack([L, L], 1)[:int(TOTAL * SR)], SR)
OUT = W_ + "main.mp4"
afc = ("[0:a][1:a]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo,volume=1.5,apad,atrim=duration=%.2f,asplit[v][vs];[2:a]aformat=channel_layouts=stereo,volume=0.36[m];"
       "[3:a]aformat=channel_layouts=stereo,volume=0.75[s];[m][vs]sidechaincompress=threshold=0.02:ratio=5:attack=20:release=400[md];"
       "[md][s][v]amix=inputs=3:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=9[a]") % TOTAL
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", B + "vo_nar.wav", "-i", B + "vo_woman.wav", "-stream_loop", "-1", "-i", C + "ep1v3/bgm.wav", "-i", W_ + "sfx.wav",
                "-filter_complex", afc, "-map", "[a]", "-t", f"{TOTAL:.2f}", "-ar", "48000", W_ + "mix.wav"], check=True)
vfc = ("[0:v]vignette=PI/5,noise=alls=6:allf=t,ass=%s:fontsdir=/usr/share/fonts/truetype/google-fonts[c];[1:v]format=rgba,scale=472:88[bd];[c][bd]overlay=(W-w)/2:110[b1];"
       "[2:v]format=rgba,colorchannelmixer=aa=0.8[wm];[b1][wm]overlay=(W-w)/2:H-h-150,format=yuv420p[vo]") % (W_ + "cap.ass")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", W_ + "base.mp4", "-loop", "1", "-i", C + "brand/badge.png", "-loop", "1", "-i", C + "brand/wm.png", "-filter_complex", vfc, "-map", "[vo]",
                "-t", f"{TOTAL:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", W_ + "vid.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", W_ + "vid.mp4", "-i", W_ + "mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", OUT], check=True)
print("ok", OUT, round(TOTAL, 1))

FIN = "/mnt/user-data/outputs/RedCapSurvives_Room4B_Ep10.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT, "-filter_complex", "[0:v]setpts=PTS/1.08[v];[0:a]atempo=1.08[a]", "-map", "[v]", "-map", "[a]", "-r", "30",
                "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-maxrate", "6M", "-bufsize", "12M", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", FIN], check=True)
print("final", FIN)
