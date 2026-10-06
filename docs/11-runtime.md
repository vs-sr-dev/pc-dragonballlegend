# The game on saturnkit's Saturn

`python tools/run.py` runs the recompiled programs (`tools/recomp.py
--build`) on saturnkit's runtime, headless and in virtual time (the same
run every time); `--play` opens the window. Pad scripts count VBlanks at
the runtime's 60 Hz.

## How far it runs

From the boot, through IP.BIN's initial program, `PROG1` (which writes
the save file `DRAGONBALLZ` to the backup RAM on the first run), `BND`
(the Bandai movie, from 5 s), `TLP` (from 15.7 s: the opening movie, the
title from about VBlank 5400 with `APPUIES SUR START` blinking, the
attract demos), and with the pad, `SEL` (the menu, CD-DA track 2) and
`INF` (the story's first scene with the piece on tracks 10–17, then the
chapter card):

    python tools/run.py --vblanks 13200 --input "6000:START,6006:,7300:C,7306:,7900:C,7906:"

| VBlank | |
|---|---|
| 300–600 | `PROG1`, then the Bandai logo (`BND`, `MV_BND`) |
| 1500–4800 | the opening movie (`MV_OPD`), to the Japanese logo |
| 5400 | the title, the same picture as Beetle's |
| 8700–10200 | the attract demo: `MV_TDA` in grey in a window under the logo, then the opening again |
| 6000 START | `SEL` starts at 102.3 s; the menu (MODE: HISTOIRE, COMBAT, OPTION) builds from about 6750 and is whole at 6900, CD-DA track 2 (correlation 1.00 with the disc's) |
| 7300 C | HISTOIRE: CHOIX (DEBUT, FICHIER 1–3) |
| 7900 C | DEBUT: `INF` starts at 135.7 s; CD-DA track 10 at 142.9 s; the comic-strip scene (the Saiyan pods, the city, Gohan, Nappa, Vegeta), the chapter card at about VBlank 11400 |

The order of the programs, read from the names each passes to the loader
(`03-executables.md`), is now seen: `PROG1` → `BND` → `TLP` → `SEL` →
`INF`.

## The frame rate, and VDP1's frame change

The game's VBlank-OUT handler drives VDP1's frame changes in manual
mode: when the program has asked for a frame (0x0604F430) and the last
draw has ended (EDSR's CEF), it writes FBCR to change frames; if the draw
has not ended it waits a field (0x0604F434), and the program waits with
it. In Beetle the scene changes picture every field (49.7 distinct
frames a second in its recording); the runtime first gave one frame
every two fields and took the scene at half speed. The runtime changed
VDP1's frame at line 0, before the VBlank-OUT interrupt was taken, so the
handler always found the new draw just started (CEF 0) and asked for its
change a field late. Mednafen's VDP1 takes the end of the VBlank at the
next HBlank, after the SCU has raised VBlank-OUT: saturnkit now does the
same (`10-saturnkit.md`), and the game changes frame every field, the
scene's pictures keeping time with its music as in Beetle.

## Speed: 60 fields a second

The game steps once a field and never reads TVSTAT's PAL bit. At the
runtime's 60 Hz it runs at the Japanese original's speed, 6/5 of a
European Saturn's: the story's first scene lasts about 47 s from the
music's start against about 55 s in Beetle (PAL). At 50 Hz that scene
lasts as long as its music track (55.0 s); at 60 Hz the chapter card
comes with 8 s of the track left. Which speed the port keeps (the
Japanese 60, or the European 50) is the user's choice (open question 2).

## Discovery's stops

The runs stopped on calls to task handlers discovery had not found, and
on the task list's longjmp; both are now saturnkit's
(`09-recompiler.md`). From the boot to the chapter card no call to a
non-entry and no wrong return.

## Played by the user: to the first battle

The user played in the window (`--play`): START skips the opening movie
and the story's scene, A confirms as C does; from the menu into the
story, past the chapter card, and through the loading picture
(`Chergemant...`, `04-curiosities.md`) into `ATB`, the first battle
(58 s into the game). Kept as `tools/scripts/to-the-first-battle.txt`
(`python tools/run.py --input @tools/scripts/to-the-first-battle.txt
--vblanks 6000`).

At 77 s the run stopped: `ATB` loads its fighters' sprites by SCU DMA,
a command and a picture each, from a list; one more transfer reads its
source at 0x001F0010, past the list's end. On the Saturn that is backup
RAM, which answers anywhere in 0x00180000-0x001FFFFF (64 KiB repeated);
the runtime knew only the first 64 KiB. saturnkit now repeats it as
Mednafen does (`10-saturnkit.md`); the 32 bytes land in a VDP1 command
slot that nothing draws, and the battle's first screen comes: Goku,
Gohan, Piccolo and Krillin on the field, their portraits (`OVER`) and
the POWER BALANCE gauge.
