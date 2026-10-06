# The data formats at a glance

What was read in session 1: headers, tables and a few samples. Nothing
here has been decoded in full yet.

## Movies: Sega FILM and Cinepak

All five `MV_` files are Sega FILM 1.08 (`FILM`, `FDSC`, `STAB` chunks)
with Cinepak video at 320×240; ffmpeg reads them as they are.

| File | Length | Sound | What (seen) |
|---|---|---|---|
| `MV_BND.BIN` | 6.6 s | 16-bit mono, 44 100 Hz | the Bandai logo (Beetle shows it 24 s after power-on) |
| `MV_OPD.BIN` | 63.0 s | 16-bit stereo, 22 254 Hz | the opening movie: a pre-rendered Dragon Ball, the Earth, a rocky plain where the cast fades in, a green horned monster, the Japanese logo |
| `MV_TDA.BIN` | 31.8 s | 16-bit stereo, 22 254 Hz | game play recorded as a movie: Goku on a battlefield |
| `MV_TDB.BIN` | 22.1 s | 16-bit stereo, 22 254 Hz | game play: the Ginyu Force |
| `MV_TDC.BIN` | 26.0 s | 16-bit stereo, 22 254 Hz | game play: a Super Saiyan, the battle gauges |

ffmpeg decodes `MV_BND` and `MV_OPD` in colour and the three `MV_TD`
files in grey. The `TD` movies are the title's attract demos: left on
the title, the game plays one in grey in a window under the logo, with
`APPUIES SUR START` over it (seen in the runtime, session 2; not yet in
Beetle).

## Sound: `SS_SND.BIN`

One 324 MB file holds all the sound but the CD-DA music and the movies'.
It starts with a table of 0x3800 bytes: its size, then the offsets of
five groups of (offset, length) pairs, all in bytes and all
sector-aligned.

| Group | Entries | Bytes | Contents |
|---|---|---|---|
| 0 | 1 | 28 672 | a 68000 program: vectors (SSP 0xA000, PC 0x1000), then the string `Ver1.33 95/08/07SATURN(S) sampleNao V0.05  06/15Kas V0.00c` — the sound driver |
| 1 | 2 | 4 096 | |
| 2 | 2 | 40 960 | |
| 3 | 61 | 737 280 | the first starts with a table of 16-bit offsets: sequences or banks (inferred) |
| 4 | 1 710 | 323 149 824 | the speech, in Japanese (heard in the battles): 8-bit signed PCM by its samples (silence reads 00, 01, FF) |

The driver is not Sega's (the other saturnkit ports run Sega's 1.27 and
1.28); its strings name its makers. 1 710 clips match the afterword's
"more than 1 500 lines spoken by the voice actors" and "about 2.5 hours
of dialogue played with the music and the effects"
(`04-curiosities.md`). Their rate is not known yet: 323 MB of 8-bit mono
over 2.5 hours would be about 36 000 bytes a second.

## Music: CD-DA

Sixteen audio tracks hold nine pieces (tracks 10 to 17 are one piece,
byte for byte). In Beetle's recording, matched by `tools/cdda_match.py`:

| When | Track | |
|---|---|---|
| the main menu (MODE) | 2 | correlation 0.97 |
| the story's opening scene (the Saiyans' arrival) | 10–17 | correlation 1.00; no speech over it (heard by the user) |
| the opening movie, the title screen | — | not CD: the movie's own sound, then silence or the driver |

The afterword's composer, Kenji Yamamoto, describes the music as
guitar house throughout, written for the 24 voices the Saturn and the
PlayStation give (the Super Famicom games had 8); "this music data and
tone data" had to be ported to the game, so some music is the driver's
own (inferred; to be heard).

## Graphics packs: `GD_*.BIN`

Each starts with a header of 0x800 bytes: the header's size, the offset
of a table, then (offset, length) pairs, the offsets sector-aligned.
`GD_TLP.BIN` (the title's, by the name) has two entries, `GD_ATB.BIN`
(7.4 MB, the battles', by the name) many. What is inside each entry
(VDP1 sprites, VDP2 cells, palettes, polygon terrain) is for the next
sessions; the afterword says the characters are sprites (more than 30
fighters, drawn by hand) on polygon terrain.

## Text

No program holds readable text: the French strings are not ASCII in the
programs. The menus' words are drawn as graphics (`HISTOIRE`, `COMBAT`
in the menu's own lettering); where the story's text lives is open
(question 5).
