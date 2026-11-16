"""Split narrator + Maya takes into lines, tighten pauses, interleave, write timeline.json + voice tracks."""
import json, re, subprocess, difflib, numpy as np, soundfile as sf
B = "/home/claude/kb/bird/"; SR = 48000
CLEAN = "highpass=f=75,equalizer=f=250:t=q:w=1.5:g=-2,equalizer=f=3500:t=q:w=1.2:g=2.5,equalizer=f=7000:t=q:w=2:g=-1.5,acompressor=threshold=-18dB:ratio=2.5:attack=10:release=150:makeup=2,alimiter=limit=0.97"
MAYA_CLEAN = "highpass=f=90,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,alimiter=limit=0.97"
RADIO = "highpass=f=450,lowpass=f=3200,acompressor=threshold=-24dB:ratio=6:makeup=6,volume=1.1,alimiter=limit=0.9"
def load(src, fx):
    out = B + "tmp_" + src.split("/")[-1]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", fx + ",aresample=48000", "-ac", "1", out], check=True)
    return sf.read(out)[0]
def silences(x):
    # frame energy based silence detection (20 ms frames)
    f = int(0.02 * SR); n = len(x) // f; e = np.array([np.sqrt(np.mean(x[i * f:(i + 1) * f] ** 2)) for i in range(n)])
    thr = max(e.max() * 0.03, 1e-4); quiet = e < thr
    return quiet, f
def edges(x, t_first, t_last):
    """refine [start, end] of a phrase given first/last word start times"""
    quiet, f = silences(x)
    i = int(t_first * SR / f)
    while i > 0 and not quiet[i - 1]: i -= 1
    j = int(t_last * SR / f) + 2
    run = 0
    while j < len(quiet):
        run = run + 1 if quiet[j] else 0
        if run >= 6: j -= 5; break
        j += 1
    return max(0, i * f / SR - 0.04), min(len(x) / SR, j * f / SR + 0.06)
def dedupe(asr):
    out = []
    for w, t in asr:
        if out and out[-1][0].lower() == w.lower() and abs(out[-1][1] - t) < 0.35: continue
        if out and t < out[-1][1] - 0.05: continue
        out.append((w, t))
    return out
norm = lambda s: re.sub(r"[^a-z0-9:'-]", "", s.lower())
def align(lines, asr, repl):
    toks = []
    for li, ln in enumerate(lines):
        s = ln
        for a, b in repl: s = s.replace(a, b)
        for w in s.split():
            if norm(w): toks.append((li, norm(w)))
    A = [t for _, t in toks]; Bw = [norm(w) for w, _ in asr]
    sm = difflib.SequenceMatcher(None, A, Bw, autojunk=False)
    m = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n): m[a + k] = b + k
    res = []
    for li in range(len(lines)):
        idx = [k for k, (l, _) in enumerate(toks) if l == li]
        hit = [m[k] for k in idx if k in m]
        if not hit: raise SystemExit(f"no match line {li}: {lines[li]}")
        res.append((asr[min(hit)][1], asr[max(hit)][1], [asr[h] for h in range(min(hit), max(hit) + 1)]))
    return res
NL = json.load(open(B + "nar_lines.json"))
REPL = [("four million","4 million"),("seventeen","17"),("thirteen","13"),("A star","A*"),("…"," ")]
nar = load(B + "nar_raw.wav", CLEAN)
NA = align(NL, dedupe(json.load(open(B + "asr_nar_raw.json"))), REPL)
TV = "highpass=f=200,lowpass=f=6000,equalizer=f=2500:t=q:w=1:g=3,acompressor=threshold=-20dB:ratio=4:makeup=3,alimiter=limit=0.9"
MIA_FX = "highpass=f=90,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,alimiter=limit=0.97"
INSP_FX = "highpass=f=100,equalizer=f=2500:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:makeup=2,alimiter=limit=0.95"
MAYA = {}
MREPL = [("one year","1 year"),("…", " ")]
maya = {}
for k, (lines, f, fx) in MAYA.items():
    x = load(B + f, fx); al = align(lines, json.load(open(B + f"asr_{MAYA[k][1][:-4]}.json")), MREPL)
    maya[k] = (x, lines, al)
INS = {}
BLOCK_END = {0, 3, 4, 6}
seq = []
for i in range(len(NL)):
    seq.append(("nar", None, i))
    seq += INS.get(i, [])
track = {k: np.zeros(int(90 * SR)) for k in ("nar",)}
tl = []; t = 0.4
for who, key, i in seq:
    if who == "nar": x = nar; t0w, t1w, ws = NA[i]; text = NL[i]
    else: x, lines, al = maya[key]; t0w, t1w, ws = al[i]; text = lines[i]
    a, b = edges(x, t0w, t1w); seg = x[int(a * SR):int(b * SR)]
    tr = track[who]; s = int(t * SR); tr[s:s + len(seg)] += seg
    tl.append({"who": who, "key": key, "i": i, "text": text, "t0": round(t, 3), "t1": round(t + len(seg) / SR, 3),
               "words": [(w, round(t + (tw - a), 3)) for w, tw in ws]})
    gap = 0.22
    if who != "nar" or (seq.index((who, key, i)) + 1 < len(seq) and seq[seq.index((who, key, i)) + 1][0] != "nar"): gap = 0.4
    if who == "nar" and i in BLOCK_END: gap = 0.5
    if who == "nar": gap += {0: 0.1, 4: 0.1}.get(i, 0)
    t += len(seg) / SR + gap
TOTAL = t + 1.5
for k in track: sf.write(B + f"vo_{k}.wav", track[k][:int(TOTAL * SR)], SR)
json.dump({"total": TOTAL, "lines": tl}, open(B + "timeline.json", "w"), indent=1)
print("total", round(TOTAL, 2))
for e in tl: print(f'{e["t0"]:7.2f} {e["t1"]:7.2f} {e["who"]:4s} {e["text"][:60]}')
