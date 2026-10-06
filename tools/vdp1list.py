"""The VDP1 command list in a runtime dump, as text.

    python tools/vdp1list.py build/run/dump-N.bin [--near X,Y]

Reads the dump's VDP1 VRAM (its first 512 KiB, see saturnkit/runtime/video.cpp's
--dump) and walks the command table from address 0 as VDP1 does (jumps, calls,
returns, skips, the end bit), printing each command drawn: its address, kind,
colour mode, colour bank or table, character address and size, and vertices
(the local coordinates added). --near keeps only the commands whose vertices
or box come within 24 pixels of X,Y.
"""
import argparse
import struct

KINDS = {0: "normal sprite", 1: "scaled sprite", 2: "distorted sprite", 4: "polygon", 5: "polyline",
         6: "line", 8: "user clip", 9: "system clip", 10: "local coords"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dump")
    ap.add_argument("--near")
    ap.add_argument("--path", action="store_true", help="every command visited, drawn or not")
    a = ap.parse_args()
    vram = open(a.dump, "rb").read()[:0x80000]
    w16 = lambda o: struct.unpack_from(">H", vram, o & 0x7FFFE)[0]
    s16 = lambda o: struct.unpack_from(">h", vram, o & 0x7FFFE)[0]
    near = tuple(int(v) for v in a.near.split(",")) if a.near else None
    addr, ret, lx, ly, seen, visited = 0, None, 0, 0, 0, set()
    while seen < 4096:
        seen += 1
        if (addr, ret) in visited:
            print("%05X: a loop, the list ends here" % addr)
            break
        visited.add((addr, ret))
        ctrl = w16(addr)
        if ctrl & 0x8000:
            break
        link = w16(addr + 2) * 8
        jp, kind = ctrl >> 12 & 7, ctrl & 0xF
        nxt = addr + 0x20
        if a.path:
            print("%05X ctrl %04X link %05X" % (addr, ctrl, w16(addr + 2) * 8))
        if not ctrl & 0x4000:                     # not skipped
            pmod, colr, srca, size = w16(addr + 4), w16(addr + 6), w16(addr + 8) * 8, w16(addr + 10)
            v = [(s16(addr + 0x0C + 4 * i), s16(addr + 0x0E + 4 * i)) for i in range(4)]
            if kind == 10:
                lx, ly = v[0]
            elif kind in KINDS and kind not in (8, 9):
                pts = [(x + lx, y + ly) for x, y in v]
                if kind == 0:
                    w, h = (size >> 8 & 0x3F) * 8, size & 0xFF
                    pts = [pts[0], (pts[0][0] + w - 1, pts[0][1] + h - 1)]
                elif kind == 1:
                    pts = pts[:2] if (ctrl >> 8 & 0xF) == 0 else pts[:1]
                ok = near is None or any(abs(x - near[0]) < 24 and abs(y - near[1]) < 24 for x, y in pts) or \
                    (len(pts) == 2 and pts[0][0] - 24 <= near[0] <= pts[1][0] + 24 and pts[0][1] - 24 <= near[1] <= pts[1][1] + 24)
                if ok:
                    print("%05X %-16s mode %d colr %04X src %05X size %dx%d pmod %04X  %s" % (
                        addr, KINDS[kind], pmod >> 3 & 7, colr, srca, (size >> 8 & 0x3F) * 8, size & 0xFF, pmod,
                        " ".join("(%d,%d)" % p for p in pts)))
        j = jp & 3                                # 4-7: the same with the command skipped
        if j == 1:
            nxt = link
        elif j == 2:
            ret, nxt = addr + 0x20, link
        elif j == 3:
            nxt, ret = (ret if ret is not None else addr + 0x20), None
        addr = nxt


if __name__ == "__main__":
    main()
