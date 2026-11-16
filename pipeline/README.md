# Red Cap Survives — build pipeline backup

Restores the animation pipeline if the build container is recycled.

    git clone https://github.com/kasun511/redcap-videos /home/claude/redcap-videos
    mkdir -p /home/claude/sf /home/claude/cruise /home/claude/kb
    cp /home/claude/redcap-videos/pipeline/flat.py    /home/claude/sf/flat.py
    cp /home/claude/redcap-videos/pipeline/asr.py     /home/claude/cruise/asr.py
    cp /home/claude/redcap-videos/pipeline/wiprops.py /home/claude/kb/wiprops.py
    cp -r /home/claude/redcap-videos/pipeline/templates/* /home/claude/kb/

`templates/` holds one finished reel per format to copy and adapt:
- `jump`, `bird`, `gills` — earlier knowledge / What If reels
- `window`, `fireshadow`, `anc`, `hole`, `antarctica` — the 16 Nov batch
- `sf_p10` — Solar Flash (Arlo narrator + Mia via Kokoro, props.py/tail.py split)
- `r4b_e10` — The Rules of Room 4B (Flow images + PIL cards, single build script)

## Build order for a new reel
1. Copy a template folder, `sed` its absolute paths to the new folder, and fix
   `sys.path.insert` on line 2 of post.py — it points at the template otherwise.
2. Write nar_lines.json.
3. Voice it in AI Studio (Arlo), download, convert to 48 kHz mono `nar_raw.wav`.
4. `asr.py` over a 16 kHz copy, then fix `REPL` in assemble.py so the script
   spellings match what the ASR actually heard. Numbers are the usual mismatch.
5. `python3 assemble.py` → `bash mk.sh` → render 4 parts in parallel → `post.py`.

## Gotchas
- `rm -rf __pycache__` after editing body.py, or post.py imports the stale scenes.
- Knowledge-reel captions occupy y 235–340. Keep on-screen chips at y >= 500.
- Solar Flash captions sit near y 1500. Keep labels above ~1250 or below ~1620.
- `SS(c, k)` clamps cairo scale to >= 2e-3; `scale(0)` raises "invalid matrix".
- Delete part*.mp4 / vid.mp4 / base.mp4 after each build — disk fills fast.
