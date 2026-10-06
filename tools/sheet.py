"""A contact sheet of pictures, labelled, for looking at a run at a glance.

    python tools/sheet.py DIR [--out FILE] [--cols N] [--width W]

Takes DIR/t*.png (the oracle's shots, by time) or DIR/shot-*.png (the
port's, by VBlank), in numeric order, and lays them out in a grid with
each one's name under it.
"""
import argparse
import glob
import os
import re

from PIL import Image, ImageDraw


def key(path):
    m = re.search(r"([\d.]+)\.png$", os.path.basename(path))
    return float(m.group(1)) if m else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dir")
    ap.add_argument("--out")
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--width", type=int, default=320)
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(a.dir, "t*.png")) + glob.glob(os.path.join(a.dir, "shot-*.png")), key=key)
    if not files:
        raise SystemExit("no pictures in %s" % a.dir)
    w = a.width
    h = w * 3 // 4
    rows = (len(files) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * w, rows * (h + 14)), (32, 32, 32))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        im.thumbnail((w, h))
        x, y = (i % a.cols) * w, (i // a.cols) * (h + 14)
        sheet.paste(im, (x, y))
        d.text((x + 2, y + h + 1), os.path.basename(f), fill=(230, 230, 230))
    out = a.out or os.path.join(a.dir, "sheet.png")
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
