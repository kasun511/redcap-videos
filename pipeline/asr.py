import sherpa_onnx, soundfile as sf, librosa, numpy as np, json, sys
M="/tmp/claude-0/-home-claude/1f0ee3e5-19dd-58f1-9528-636514cc0c08/scratchpad/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8/"
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=M+"encoder.int8.onnx",decoder=M+"decoder.int8.onnx",joiner=M+"joiner.int8.onnx",tokens=M+"tokens.txt",model_type="nemo_transducer",num_threads=2)
y,_=librosa.load(sys.argv[1],sr=16000); out=[]; CH=30*16000
for s0 in range(0,len(y),CH-2*16000):   # 30 s windows, 2 s overlap
    seg=y[s0:s0+CH]; st=rec.create_stream(); st.accept_waveform(16000,seg); rec.decode_stream(st); r=st.result
    # merge tokens into words
    w=None
    for tok,t in zip(r.tokens,r.timestamps):
        t=t+s0/16000
        if tok.startswith(" ") or w is None:
            if w: out.append(w)
            w=[tok.strip(),t]
        else: w[0]+=tok
    if w: out.append(w)
    if s0+CH>=len(y): break
# dedupe overlap: keep words in time order, drop ones earlier than last kept
res=[];last=-1
for w,t in out:
    if t>last+0.05: res.append((w,round(t,2))); last=t
json.dump(res,open(sys.argv[2],"w"))
print(" ".join(f"{w}@{t}" for w,t in res))
