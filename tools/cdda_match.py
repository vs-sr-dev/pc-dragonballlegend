"""Which CD-DA track is playing in a recording, and from when.

    python tools/cdda_match.py RECORD.wav [--audio DIR] [--step S]

Cuts the recording into windows of a few seconds and finds, for each, the
CD-DA track (DIR/trackNN.wav, from `saturnkit.disc --audio`) and the
offset in it that correlate best with it, on a mono 2 kHz envelope. Prints
a line per window: the time in the recording, the track, the offset in
the track and the correlation; below 0.6 the window is marked as not on
CD (silence, the sound driver, or speech).
"""
import argparse
import glob
import os
import wave

import numpy as np

RATE = 2205   # 44 100 / 20


def load(path):
    with wave.open(path) as w:
        n, ch, r = w.getnframes(), w.getnchannels(), w.getframerate()
        a = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32)
    a = a.reshape(-1, ch).mean(axis=1)
    k = r // RATE
    a = a[: len(a) // k * k].reshape(-1, k).mean(axis=1)
    return a


def best(seg, track):
    n = len(seg)
    if len(track) < n or seg.std() < 1:
        return -1.0, 0
    # normalised cross-correlation through the FFT
    size = 1 << int(np.ceil(np.log2(len(track) + n)))
    f = np.fft.irfft(np.fft.rfft(track, size) * np.conj(np.fft.rfft(seg - seg.mean(), size)), size)[: len(track) - n + 1]
    c = np.cumsum(np.concatenate([[0], track]))
    c2 = np.cumsum(np.concatenate([[0], track * track]))
    s = c[n:] - c[:-n]
    var = (c2[n:] - c2[:-n]) - s * s / n
    corr = f / (np.sqrt(np.maximum(var, 1e-9)) * seg.std() * np.sqrt(n))
    i = int(np.argmax(corr))
    return float(corr[i]), i


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("record")
    ap.add_argument("--audio", default=os.path.join(os.path.dirname(__file__), "..", "build", "audio"))
    ap.add_argument("--step", type=float, default=6.0)
    a = ap.parse_args()
    rec = load(a.record)
    tracks = {os.path.basename(p)[5:7]: load(p) for p in sorted(glob.glob(os.path.join(a.audio, "track*.wav")))}
    win = int(4 * RATE)
    t = 0
    while t + win <= len(rec):
        seg = rec[t:t + win]
        scores = [(best(seg, tr), name) for name, tr in tracks.items()]
        (c, off), name = max(scores)
        tag = "" if c >= 0.6 else "   (not on CD)"
        print("%7.1f s  track %s at %6.1f s  corr %.2f%s" % (t / RATE, name, off / RATE, c, tag))
        t += int(a.step * RATE)


if __name__ == "__main__":
    main()
