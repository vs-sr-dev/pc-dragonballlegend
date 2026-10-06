"""How a program refers to an address: a literal, an address position-independent
code computes (mova + a literal nearby), or the value in its data.

    python tools/findptr.py FILE BASE ADDR      # e.g. build/extract/AP_TLP.BIN 06020000 0602315E

For a stop on "call to X, not an entry of an active module": where X comes
from, and the instructions just before it (a boundary for discovery?).
"""
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))
from saturnkit import sh2

path, base, want = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16)
d = open(path, "rb").read()
img = sh2.Image(d, base)
for a in range(base, base + len(d) - 2, 2):
    i = img.insn(a)
    if i.op == "mov.l" and i.target is not None and i.size == 4 and img.literal(i) == want:
        print("literal at %08X" % a)
    if i.op == "mova":
        for b in range(a - 16, a + 16, 2):
            j = img.insn(b)
            if j.op in ("mov.l", "mov.w") and j.target is not None and j.size:
                v = img.literal(j)
                if v is None:
                    continue
                if j.size == 2 and v & 0x8000:
                    v -= 0x10000
                if (i.target + v) & 0xFFFFFFFF == want:
                    print("mova %08X (-> %08X) + %s at %08X" % (a, i.target, j.op, b))
for k in range(0, len(d) - 3, 2):
    if int.from_bytes(d[k:k + 4], "big") == want:
        print("the value in data at %08X" % (base + k))
print("before it:", "; ".join(img.insn(want - o).text.split(";")[0].strip() for o in (6, 4, 2)))
