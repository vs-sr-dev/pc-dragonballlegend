"""Tally the literal-pool words of a program that point at the hardware.

    python tools/hwlits.py FILE@BASE [FILE@BASE ...]

Reads every `mov.l @(disp,PC)` literal and counts those that fall in one
of the Saturn's hardware areas (cache-through and cached addresses of
the A-bus and B-bus devices alike), with the distinct values. Literals in
data areas count too: a first look, not proof.
"""
import collections
import struct
import sys

AREAS = [
    (0x20100000, 0x20100080, 'SMPC'), (0x25890000, 0x258A0000, 'CD block'),
    (0x25A00000, 0x25B00000, 'sound RAM'), (0x25B00000, 0x25B01000, 'SCSP regs'),
    (0x25C00000, 0x25CC0000, 'VDP1 VRAM'), (0x25C80000, 0x25CC0000, 'VDP1 FB'),
    (0x25D00000, 0x25D00020, 'VDP1 regs'), (0x25E00000, 0x25E80000, 'VDP2 VRAM'),
    (0x25F00000, 0x25F01000, 'VDP2 CRAM'), (0x25F80000, 0x25F80120, 'VDP2 regs'),
    (0x25FE0000, 0x25FE00D0, 'SCU regs'), (0x21000000, 0x21800000, 'SINIT/MINIT'),
    (0xFFFFFE00, 0x100000000, 'on-chip'), (0x00200000, 0x00300000, 'WRAM-L'),
    (0x22000000, 0x24000000, 'A-bus cart'), (0x22400000, 0x22800000, 'A-bus CS1'),
    (0x05800000, 0x05900000, 'CD (cached?)'),
]

def scan(path, base):
    d = open(path, 'rb').read()
    tally = collections.Counter(); vals = collections.defaultdict(set)
    for i in range(0, len(d) - 1, 2):
        w = (d[i] << 8) | d[i + 1]
        if w >> 12 != 0xD: continue
        a = (base + i + 4 + (w & 0xFF) * 4) & ~3
        o = a - base
        if o < 0 or o + 4 > len(d): continue
        v = struct.unpack('>I', d[o:o + 4])[0]
        for lo, hi, name in AREAS:
            vv = v | 0x20000000 if (v >> 24) in (0x05,) else v
            if lo <= vv < hi:
                tally[name] += 1; vals[name].add(v); break
    return tally, vals

for spec in sys.argv[1:]:
    path, base = spec.rsplit('@', 1)
    t, v = scan(path, int(base, 16))
    print('==', path.split('\\')[-1].split('/')[-1])
    for k, n in t.most_common():
        s = sorted(v[k]); print('  %-12s %4d  %s%s' % (k, n, ' '.join('%08X' % x for x in s[:10]), ' ...' if len(s) > 10 else ''))
