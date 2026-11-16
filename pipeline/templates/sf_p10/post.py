import json, re, subprocess, numpy as np, soundfile as sf, math, sys
sys.path.insert(0, "/home/claude/sf/p10")
B = "/home/claude/sf/p10/"; C = "/home/claude/cruise/"; SR = 48000
TL = json.load(open(B + "timeline.json")); LINES = TL["lines"]; TOTAL = TL["total"] + 0.4
T0 = lambda i: LINES[i]["t0"]; T1 = lambda i: LINES[i]["t1"]; WT = lambda i, k=0: LINES[i]["words"][k][1]
# ---------------- captions
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
GOLD = "&H0033CCFF&"; CY = "&H00FFE36F&"; ev = []
for li, e in enumerate(LINES):
    ws = e["words"]; groups = []; cur = []
    for w, t in ws:
        if cur and (len(cur) == 3 or re.search(r"[.,?!:]$", cur[-1][0])): groups.append(cur); cur = []
        cur.append((w, t))
    if cur: groups.append(cur)
    hi = {"nar": GOLD, "news": "&H004040FF&", "mia": "&H0080E0FF&", "out": GOLD, "insp": GOLD}[e["who"]]; base = {"nar": "&HFFFFFF&", "news": "&HFFFFFF&", "mia": "&HFFFFFF&", "out": "&HFFFFFF&", "insp": "&HFFFFFF&"}[e["who"]]
    for gi, g in enumerate(groups):
        nxt = groups[gi + 1][0][1] - 0.03 if gi + 1 < len(groups) else e["t1"] + 0.15
        for j, (w, t) in enumerate(g):
            en = g[j + 1][1] - 0.03 if j + 1 < len(g) else nxt
            txt = " ".join((("{\\c" + hi + "}" + x.upper() + "{\\c" + base + "}") if k == j else x.upper()) for k, (x, _) in enumerate(g))
            pre = "{\\fscx80\\fscy80\\t(0,90,\\fscx100\\fscy100)}" if j == 0 else ""
            ev.append((t - 0.03, en, "Cap" if e["who"] == "nar" else "Maya", pre + "{\\c" + base + "}" + txt))
hdr = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
       "Style: Cap,Poppins,100,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,-1,0,0,0,100,100,1,0,1,10,4,2,50,50,330,1\n"
       "Style: Maya,Poppins,100,&H00FFFFFF,&H00FFFFFF,&H00300060,&H99000000,-1,0,0,0,100,100,1,0,1,10,4,2,50,50,330,1\n\n"
       "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
NI = {e["i"]: k for k, e in enumerate(LINES) if e["who"] == "nar"}
hdr = hdr.replace("\n\n[Events]", "\nStyle: Prompt,Poppins,56,&H00FFFFFF,&H00FFFFFF,&H002020C8,&H002020C8,-1,0,0,0,100,100,1,0,3,14,0,5,60,60,0,1\n\n[Events]")
open(B + "cap.ass", "w").write(hdr + "".join(f"Dialogue: 0,{ts(a)},{ts(b)},{s},,0,0,0,,{x}\n" for a, b, s, x in ev if b > a))
# ---------------- sound design
src_ = open(C + "ep1v3/sfx3.py").read(); lib = src_[:src_.index("# ---------- place cues")]
g = {}; exec(lib.replace('T = json.load(open("/home/claude/cruise/ep1v3/timeline.json"))', 'T={"total":%f,"scene":{},"phr":{}}' % TOTAL), g)
norm, lp, hp, bp, env = g["norm"], g["lp"], g["hp"], g["bp"], g["env"]
N = int(TOTAL * SR) + SR; Lt = np.zeros(N); rng = np.random.default_rng(11)
def put(x, at, gn=1.0):
    i = int(max(0, at) * SR); x = x[:max(0, N - i)] * gn; Lt[i:i + len(x)] += x
def tone(f, d, typ="sine"):
    tt = np.arange(int(d * SR)) / SR; ph = 2 * np.pi * f * tt
    return np.sign(np.sin(ph)) * 0.5 if typ == "sq" else np.sin(ph)
def beep_alarm(d):
    n = int(d * SR); tt = np.arange(n) / SR; gate = ((tt % 0.5) < 0.1) | (((tt % 0.5) > 0.16) & ((tt % 0.5) < 0.26))
    return norm(lp(np.sign(np.sin(2 * np.pi * 1950 * tt)) * gate, 4000), 0.5)
def step(soft=False):
    n = int(0.11 * SR); tt = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * 80 * tt) * np.exp(-tt * 45) + 0.5 * bp(rng.standard_normal(n), 300, 3000) * np.exp(-tt * 70), 0.5 if soft else 0.8)
def steps(t0, t1, rate, gn, soft=False):
    t = t0
    while t < t1: put(step(soft), t, gn * (0.8 + 0.4 * rng.random())); t += rate
def click(): n = int(0.04 * SR); return norm(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 150), 0.6)
def static(d, gn=0.3): n = int(d * SR); return norm(hp(rng.standard_normal(n), 1800) * (0.6 + 0.4 * (rng.random(n) > 0.3)) * env(n, 0.03, 0.15), gn)
def squelch(): n = int(0.18 * SR); return norm(bp(rng.standard_normal(n), 1000, 5000) * env(n, 0.005, 0.1), 0.5)
def idle(d):
    n = int(d * SR); tt = np.arange(n) / SR; x = np.sin(2 * np.pi * 32 * tt) + 0.5 * np.sign(np.sin(2 * np.pi * 16 * tt)) + 0.5 * lp(rng.standard_normal(n), 200)
    return norm(lp(x, 400) * env(n, 0.4, 0.6), 0.5)
def whine():
    n = int(0.7 * SR); tt = np.arange(n) / SR; f = np.linspace(1100, 700, n) + 40 * np.sin(2 * np.pi * 7 * tt)
    return norm(np.sin(np.cumsum(2 * np.pi * f / SR)) * np.sin(np.pi * tt / 0.7) ** 2, 0.4)
def coo():
    n = int(0.5 * SR); tt = np.arange(n) / SR; f = 420 + 60 * np.sin(2 * np.pi * 5 * tt)
    return norm(np.sin(np.cumsum(2 * np.pi * f / SR)) * np.sin(np.pi * tt / 0.5) * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * tt)), 0.25)
def chirp():
    n = int(0.12 * SR); tt = np.arange(n) / SR; f = np.linspace(3800, 5200, n)
    return norm(np.sin(np.cumsum(2 * np.pi * f / SR)) * np.sin(np.pi * tt / 0.12), 0.2)
def hum(d, f=50):
    n = int(d * SR); tt = np.arange(n) / SR; return norm(sum(np.sin(2 * np.pi * f * k * tt) / k for k in (1, 2, 3, 5)) * env(n, 0.3, 0.8), 0.3)
def zap():
    n = int(0.25 * SR); return norm(bp(rng.standard_normal(n), 2000, 9000) * (rng.random(n) > 0.6) * env(n, 0.002, 0.2), 0.5)
def siren(d):
    n = int(d * SR); tt = np.arange(n) / SR; f = 750 + 350 * np.sin(2 * np.pi * 0.3 * tt)
    return norm(lp(np.sin(np.cumsum(2 * np.pi * f / SR)) + 0.3 * np.sin(np.cumsum(4 * np.pi * f / SR)), 2500) * env(n, 1.0, 1.0), 0.35)
def bell(d):
    n = int(d * SR); tt = np.arange(n) / SR; x = (np.sin(2 * np.pi * 3100 * tt) + 0.6 * np.sin(2 * np.pi * 4300 * tt)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * tt)))
    return norm(x * env(n, 0.02, 0.2), 0.3)
def tick(): n = int(0.03 * SR); return norm(np.sin(2 * np.pi * 2400 * np.arange(n) / SR) * np.exp(-np.arange(n) / SR * 160), 0.4)
def clink(): n = int(0.5 * SR); tt = np.arange(n) / SR; return norm((np.sin(2 * np.pi * 2600 * tt) + 0.5 * np.sin(2 * np.pi * 4100 * tt)) * np.exp(-tt * 9), 0.4)
def creak(d=1.2): return g["creak"](d)
def pad(d, f=110):
    n = int(d * SR); tt = np.arange(n) / SR; return norm(sum(np.sin(2 * np.pi * f * m * tt + m) for m in (1, 1.5, 2, 3)) * env(n, 0.8, 1.0), 0.25)
def rev_whoosh(d=1.2): x = g["whoosh"](d); return x[::-1]
tt = np.arange(N) / SR
Lt += lp(rng.standard_normal(N), 400) * 0.03
def gravel():
    n = int(0.28 * SR); return norm(bp(rng.standard_normal(n), 800, 6000) * (rng.random(n) > 0.5) * env(n, 0.02, 0.2) + 0.4 * lp(rng.standard_normal(n), 300) * env(n, 0.01, 0.15), 0.6)
def scrape(d=1.2): n = int(d * SR); return norm(bp(rng.standard_normal(n), 1500, 7000) * env(n, 0.05, 0.3) * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * np.arange(n) / SR)), 0.45)
def crackle(d):
    n = int(d * SR); x = hp(rng.standard_normal(n), 3000) * 0.08; idx = rng.integers(0, n, int(d * 40)); x[idx] += rng.standard_normal(len(idx)) * 1.2; return norm(x, 0.25)
def birds(d):
    out = np.zeros(int(d * SR))
    for k in range(int(d * 2)):
        c = chirp(); i = int(rng.random() * (len(out) - len(c))); out[i:i + len(c)] += c
    return out
import scenes as S1
ST = {n: t for n, t in S1.SC}; WD = S1.WORD; T0 = S1.T0; T1 = S1.T1
def vib(d=0.42, f=175):
    n = int(d * SR); tt = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * f * tt)) * 0.6 + np.sin(2 * np.pi * 2 * f * tt) * 0.3
    x = bp(x * (0.75 + 0.25 * np.sin(2 * np.pi * 23 * tt)), 90, 1800)
    rattle = bp(rng.standard_normal(n), 800, 3500) * 0.15 * (np.sin(2 * np.pi * f * tt) > 0.7)
    return norm((x + rattle) * env(n, 0.015, 0.05), 0.45)
def alert_tone(d=2.4):
    n = int(d * SR); tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * 853 * tt) + np.sin(2 * np.pi * 960 * tt)
    gate = ((tt % 0.6) < 0.45).astype(float); gate = lp(gate, 60)
    return norm(lp(x * gate, 5000) * env(n, 0.01, 0.15), 0.32)
def chaching():
    n = int(0.9 * SR); tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 1568 * tt) + np.sin(2 * np.pi * 2093 * tt) * (tt > 0.08)) * np.exp(-tt * 5); x[:int(0.06 * SR)] += bp(rng.standard_normal(int(0.06 * SR)), 2000, 8000) * 0.6
    return norm(x, 0.5)
def thud(): n = int(0.5 * SR); tt = np.arange(n) / SR; return norm(np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 14) + 0.3 * lp(rng.standard_normal(n), 400) * np.exp(-tt * 25), 0.7)
def clank(): n = int(0.9 * SR); tt = np.arange(n) / SR; return norm((np.sin(2 * np.pi * 410 * tt) + 0.7 * np.sin(2 * np.pi * 1130 * tt) + 0.5 * np.sin(2 * np.pi * 2210 * tt)) * np.exp(-tt * 6) + 0.4 * bp(rng.standard_normal(n), 1000, 6000) * np.exp(-tt * 30), 0.7)
def engine(d, f=38):
    n = int(d * SR); tt = np.arange(n) / SR; x = sum(np.sin(2 * np.pi * f * h * tt) / h for h in range(1, 7)) * (0.7 + 0.3 * np.sin(2 * np.pi * 6 * tt))
    return norm(lp(x + 0.4 * lp(rng.standard_normal(n), 300), 900) * env(n, 0.5, 0.8), 0.5)
def beep_rev(d):
    n = int(d * SR); tt = np.arange(n) / SR; return norm(np.sin(2 * np.pi * 1200 * tt) * ((tt % 1.0) < 0.5), 0.15)
def rainfx(d): n = int(d * SR); return norm(hp(rng.standard_normal(n), 900) * env(n, 1.5, 0.5) * (0.7 + 0.3 * lp(rng.standard_normal(n), 3)), 0.5)
def water_rush(d): n = int(d * SR); return norm(bp(rng.standard_normal(n), 200, 2500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * np.arange(n) / SR)) * env(n, 0.4, 0.5), 0.6)
def bark(): n = int(0.28 * SR); tt = np.arange(n) / SR; f = 520 - 300 * tt / 0.28; return norm(np.sign(np.sin(np.cumsum(2 * np.pi * f / SR))) * np.exp(-tt * 9) * (1 - np.exp(-tt * 200)), 0.5)
def typing(d):
    out = np.zeros(int(d * SR)); t_ = 0
    while t_ < d - 0.05: c = click(); i = int(t_ * SR); out[i:i + len(c)] += c * (0.5 + 0.5 * rng.random()); t_ += 0.08 + 0.12 * rng.random()
    return out * 0.6
def rumble(d): n = int(d * SR); return norm(lp(rng.standard_normal(n), 90) * env(n, 0.8, 0.3) * np.linspace(0.3, 1, n), 0.8)
def rustle_(d): return g["rustle"](d)
def suck(d): n = int(d * SR); tt = np.arange(n) / SR; return norm(bp(rng.standard_normal(n), 300, 1500) * (0.7 + 0.3 * np.sin(2 * np.pi * 3 * tt)) * env(n, 0.5, 0.5), 0.5)
def pull_start(): n = int(0.6 * SR); tt = np.arange(n) / SR; f = 200 + 600 * tt; return norm(bp(rng.standard_normal(n), 400, 3000) * np.exp(-tt * 4) + 0.3 * np.sin(np.cumsum(2 * np.pi * f / SR)) * np.exp(-tt * 5), 0.5)
def co_alarm(d):
    n = int(d * SR); tt = np.arange(n) / SR; gate = ((tt % 0.5) < 0.12) | (((tt % 0.5) > 0.2) & ((tt % 0.5) < 0.32))
    return norm(np.sin(2 * np.pi * 3100 * tt) * gate, 0.35)
def spray_fx(d): n = int(d * SR); return norm(hp(rng.standard_normal(n), 2500) * env(n, 0.2, 0.3), 0.35)
def drip(): n = int(0.25 * SR); tt = np.arange(n) / SR; return norm(np.sin(2 * np.pi * (900 + 1500 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 25), 0.3)
def fanfx(d, on=True): n = int(d * SR); tt = np.arange(n) / SR; return norm(lp(rng.standard_normal(n), 600) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * tt)) * env(n, 0.3, 0.3), 0.3)
def drill(d): n = int(d * SR); tt = np.arange(n) / SR; return norm(lp(np.sign(np.sin(2 * np.pi * 60 * tt)) + 0.5 * rng.standard_normal(n), 1500) * (0.7 + 0.3 * np.sin(2 * np.pi * 4 * tt)) * env(n, 0.3, 0.4), 0.5)
def ding(): n = int(0.8 * SR); tt = np.arange(n) / SR; return norm((np.sin(2 * np.pi * 1318 * tt) + 0.6 * np.sin(2 * np.pi * 1976 * tt)) * np.exp(-tt * 5), 0.35)
def powerdown(): n = int(1.2 * SR); tt = np.arange(n) / SR; f = 220 * np.exp(-tt * 2.5) + 30; return norm(np.sin(np.cumsum(2 * np.pi * f / SR)) * np.exp(-tt * 2), 0.6)
E = lambda n: ST[n]
def hiss_(d): n = int(d * SR); return norm(hp(rng.standard_normal(n), 3000) * env(n, 0.1, 0.4), 0.25)
def cough(): n = int(0.35 * SR); tt = np.arange(n) / SR; return norm(bp(rng.standard_normal(n), 200, 2000) * np.exp(-tt * 10) * (1 - np.exp(-tt * 200)), 0.6)
def winch(d): n = int(d * SR); tt = np.arange(n) / SR; return norm(np.sign(np.sin(2 * np.pi * (14 + 4 * np.sin(tt)) * tt)) * lp(rng.standard_normal(n), 900) * 0.4 + 0.3 * np.sin(2 * np.pi * 90 * tt), 0.35)
def squeak_(d): n = int(d * SR); tt = np.arange(n) / SR; return norm(np.sin(2 * np.pi * (900 + 300 * np.sin(2 * np.pi * 2.5 * tt)) * tt) * (np.sin(2 * np.pi * 2.5 * tt) > 0.2) * env(n, 0.05, 0.2), 0.25)
def sigh(): n = int(0.9 * SR); tt = np.arange(n) / SR; return norm(bp(rng.standard_normal(n), 250, 1600) * np.sin(np.pi * tt / 0.9) ** 2, 0.4)
put(hum(TOTAL, 50), 0, 0.10)
put(alert_tone(1.2), 0.4, 0.3); put(thud(), S1.W_(0, "days", 1.1) - 0.1, 0.9)
put(vib(0.5), E("grid") + 0.4, 0.3); put(zap(), S1.W_(1, "antenna", 4.2) - 0.1, 0.45); put(g["boom"](), S1.W_(1, "cooked", 6.6) - 0.1, 0.55)
put(ding(), E("switch") + 0.15, 0.6); put(clank(), E("switch") + 1.7, 0.6); put(powerdown(), E("switch") + 1.8, 0.4); put(chaching(), S1.W_(2, "900", 7.0) - 0.2, 0.35)
put(ding(), E("cage") + 0.15, 0.6)
for k in range(3): put(clank(), E("cage") + 1.2 + k * 0.7, 0.4)
put(thud(), E("cage") + 3.0, 0.7)
put(ding(), E("surge") + 0.15, 0.6); put(zap(), E("surge") + 2.0, 0.4); put(chaching(), S1.W_(4, "1,400", 8.4) - 0.2, 0.35)
put(ding(), E("fill") + 0.15, 0.6); put(water_rush(3.6), E("fill") + 0.7, 0.35)
for k in range(5): put(clank(), E("fill") + 1.0 + k * 0.55, 0.22)
put(squeak_(1.2), E("town") + 0.6, 0.35); put(sigh(), E("town") + 2.4, 0.4)
put(rumble(E("dark") - E("sky")), E("sky") + 0.3, 0.45); put(hiss_(2.0), S1.W_(7, "green", 4.2) - 0.2, 0.3)
put(g["boom"](), E("dark") + 0.9, 0.95); put(rumble(3.0), E("dark") + 0.9, 0.6); put(powerdown(), E("dark") + 1.3, 0.7)
for k, w in enumerate(("hummed", "ran", "worked")):
    put(ding(), S1.W_(9, w, 3.2 + k * 1.9) - 0.1, 0.55)
put(fanfx(3.0), E("alive") + 0.6, 0.25); put(water_rush(1.6), S1.W_(9, "ran", 4.4) + 0.1, 0.25)
for k, w in enumerate(("million", "days", "episodes")):
    put(thud(), S1.W_(10, w, 1.4 + k * 1.8) - 0.1, 0.7); put(ding(), S1.W_(10, w, 1.4 + k * 1.8) - 0.05, 0.4)
put(g["boom"](), E("end"), 0.5); put(ding(), E("end") + 0.9, 0.6)
for n_, t_ in ST.items():
    if t_ > 0.5: put(g["whoosh"](0.4), t_ - 0.18, 0.22)
sf.write(B + "sfx.wav", np.stack([Lt, Lt], 1)[:int(TOTAL * SR)], SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", B + "vo_nar.wav", "-i", B + "vo_mia.wav", "-stream_loop", "-1", "-i", C + "ep1v3/bgm.wav", "-i", B + "sfx.wav", "-filter_complex",
                ("[0:a][1:a]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo,volume=1.5,apad,atrim=duration=%.2f,asplit[v][vs];[2:a]aformat=channel_layouts=stereo,volume=0.26[m];[3:a]aformat=channel_layouts=stereo,volume=0.8[s];"
                 "[m][vs]sidechaincompress=threshold=0.02:ratio=5:attack=20:release=400[md];[md][s][v]amix=inputs=3:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=9[a]") % TOTAL,
                "-map", "[a]", "-t", f"{TOTAL:.2f}", "-ar", "48000", B + "mix.wav"], check=True)
print("audio ok")
if len(sys.argv) > 1 and sys.argv[1] == "audio": sys.exit()
open(B + "parts.txt", "w").write("".join(f"file '{B}part{k}.mp4'\n" for k in range(4)))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "parts.txt", "-c", "copy", B + "base.mp4"], check=True)
vfc = (f"[0:v]noise=alls=4:allf=t,ass={B}cap.ass:fontsdir=/usr/share/fonts/truetype/google-fonts[v3];[1:v]format=rgba,scale=420:-1[bd];[v3][bd]overlay=(W-w)/2:60[v4];"
       f"[2:v]format=rgba,colorchannelmixer=aa=0.8[wm];[v4][wm]overlay=(W-w)/2:H-h-130,format=yuv420p[vo]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", B + "base.mp4", "-loop", "1", "-i", C + "brand/badge.png", "-loop", "1", "-i", C + "brand/wm.png",
                "-filter_complex", vfc, "-map", "[vo]", "-t", f"{TOTAL:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "19", B + "vid.mp4"], check=True)
OUT = B + "final_raw.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", B + "vid.mp4", "-i", B + "mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], check=True)
print("ok", OUT)
FIN = "/mnt/user-data/outputs/RedCapSurvives_SolarFlash_Ep10.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT, "-filter_complex", "[0:v]setpts=PTS/1.08[v];[0:a]atempo=1.08[a]", "-map", "[v]", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-maxrate", "6M", "-bufsize", "12M", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", FIN], check=True)
print("final", FIN)
