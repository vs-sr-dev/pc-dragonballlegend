# The disc

The European release, one disc, as a single .bin with a .cue for its 17
tracks in `iso/` (a 2007 dump made with CDRWIN from the original CD; the
.bin's CRC32 is 8950B64B, as its notes give it). The notes name it the
Spanish pressing, catalogue T-13301H-06, and say its language is French.
Everything here is from `python -m saturnkit.disc … --info`, `--list`
and `--extract`, with the files read where it says so.

## Is it the official release?

Yes. The disc is Bandai's own master for Europe: IP.BIN names Bandai's
licensee code, the area E alone and a French title, dated 1996-11-08,
five months after the Japanese master (the developers' notes on the disc
are dated March 1996, `04-curiosities.md`). The game's text is French
from the menus to the story (`MODE`, `HISTOIRE`, `COMBAT`, `OPTION`,
`APPUIES SUR START`, `EPISODE 1 / LES SUPERSAIENS CONTRE LES MERCENAIRES
DE L'ESPACE`, seen in Beetle). Nothing on it is a fan translation: no
patched Japanese IP.BIN, the volume and file dates are the European
master's. The opening movie keeps the Japanese logo
(偉大なるドラゴンボール伝説), and so do the title screen's small katakana.

## IP.BIN

| Field | Value |
|---|---|
| Maker | `SEGA TP T-133` (Bandai's licensee code) |
| Product | T-13301H |
| Version | V1.000 |
| Date | 1996-11-08 |
| Device | `CD-1/1` |
| Areas | E (Europe only); the area block at 0x0E04 reads `For EUROPE.` |
| Peripherals | J (control pad) |
| Title | `DRAGON BALL Z LA GRANDE LEGENDE DES BOULES DE CRISTAL` |
| IP size | 0x1000 |
| Stacks | master 0x06002000, slave 0x06001000 |
| 1st read | 0x06003000, the whole file: `/0` (27 788 bytes) |

IP.BIN's initial program, right after the area block (0x06002E20),
is the game's start, not the BIOS's: it masks the interrupts (SR 0xF0),
sets VBR to 0x06000000 and the stack to 0x06002000, zeroes the work RAM
from 0x06009C8D to 0x06100000 (everything above `0`'s end) and jumps
through the first word of `0`, to 0x060030B6. The 1st read address
itself holds a table of pointers, not code (`03-executables.md`).

The ISO 9660 volume is `DRAGONBALLZ`, 264 139 sectors, created
1996-11-08, publisher and preparer `BANDAI`. It names `DB_CPY.TXT`,
`DB_ABS.TXT` and `DB_BIB.TXT` as its copyright, abstract and
bibliography files, but none of the three is on the disc.

## Tracks

| Track | Mode | LBA | Length | |
|---|---|---|---|---|
| 1 | MODE1/2352 | 0 | 184 813 sectors (41:04) | IP.BIN, the file system, every file |
| 2–17 | AUDIO | 184 963 – 260 013 | 16 tracks, 9.6 s to 2:22 each | the music (CD-DA) |

Every audio track has a 2-second pregap. Track 2's is not in the .bin:
the .cue gives it as `PREGAP 00:02:00`, so the drive's LBAs from track 2
on are 150 sectors above the .bin's offsets. The disc agrees: its
root directory holds a record for each audio track, `XX_CDA.X02` to
`XX_CDA.X17`, and `XX_CDA.X02` starts at LBA 184 963 = 184 813 + 150.
saturnkit at c5d1280 does not count a `PREGAP` line (its `--info` lists
track 2 at 184 813 and every later one 150 too low), and its runtime
marks a .bin shared by several tracks with the last track's mode, so the
data track of this single .bin would read as audio: `10-saturnkit.md`.

Tracks 10 to 17 are byte-identical: one 55-second piece eight times.
The disc holds nine different pieces on CD (`02-data-formats.md`).

## Files

22 files and 16 CD-DA records, all in the root directory.

| File | Size | |
|---|---|---|
| `0` | 27 788 | the 1st read file: a resident loader at 0x06003000 (`03-executables.md`) |
| `1` | 114 246 | the first program, at 0x06020000 |
| `AP_ATB.BIN`, `AP_BND.BIN`, `AP_END.BIN`, `AP_INF.BIN`, `AP_SEL.BIN`, `AP_TLP.BIN` | 126 160 – 564 492 | six more programs, all at 0x06020000 |
| `GD_ATB.BIN`, `GD_END.BIN`, `GD_INF.BIN`, `GD_ORV.BIN`, `GD_SEL.BIN`, `GD_TLP.BIN`, `GD_WAR.BIN` | 0.1 – 7.4 MB | data packs (graphics, by the name), sector-aligned, with a table of offsets |
| `MV_BND.BIN`, `MV_OPD.BIN`, `MV_TDA.BIN`, `MV_TDB.BIN`, `MV_TDC.BIN` | 1.0 – 17.5 MB | movies: Sega FILM 1.08, Cinepak |
| `SS_SND.BIN` | 323 975 168 | all the sound: the 68000 driver, its banks, and 1 710 speech clips |
| `TF_DBZ.DOC` | 21 116 | the Japanese team's afterword, Shift-JIS text (`04-curiosities.md`) |

The prefixes read as AP = application (program), GD = graphic data,
MV = movie, SS = sound (inferred from the contents). The second half of
each name pairs a program with its data: `ATB`, `END`, `INF`, `SEL`,
`TLP` have both an `AP_` and a `GD_` file; `BND` has a program and a
movie; `ORV` and `WAR` have data alone.
