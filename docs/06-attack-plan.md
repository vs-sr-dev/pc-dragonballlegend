# The plan

## What the game is, for a port

A 1996 action game in the Dragon Ball manner: up to several fighters a
side on a wide 3D battlefield (polygon terrain, hand-drawn sprites for
the characters), the player switching between them; a story mode told
in comic-strip scenes with spoken lines (1 710 clips, 2.5 hours), a
versus mode, options; music on CD (nine pieces) and from a sound driver
of its own; Cinepak movies for the logo, the opening and probably the
attract demos. Eight programs: a resident loader of 27 KB and seven
programs swapped at 0x06020000, compiled with SHC as position-independent
code, with no Sega library on the disc.

## Feasibility: static recompilation, on saturnkit

The same route as the four ports before it: every program to C++
through saturnkit's recompiler, run on saturnkit's runtime.

* **SHC**, as Virtual Hydlide, X JAPAN and Albert Odyssey; discovery
  finds 6 066 functions in the eight programs with no problem.
* **Programs started at one base and never returning**, with a resident
  below them: Virtual Hydlide's shape, which the runtime handles (a call
  to a module's base is a program start).
* **No library** to recognise: the game's own CD reader, its own movie
  player and its own sound driver. All of it is code the recompiler
  translates like the rest; nothing needs high-level emulation beyond
  what saturnkit's runtime already does for the hardware.

What saturnkit has, and what this game asks of it:

| Need | saturnkit at c5d1280 | To do |
|---|---|---|
| A single .bin for every track, the audio's first pregap not in the file (`PREGAP`) | `disc` ignores `PREGAP` (tracks 2–17 150 sectors low); the runtime marks a shared .bin with its last track's mode (the data track would read as audio) and ignores `PREGAP` | per-track modes and offsets within one file; `PREGAP` counted as silence that is not in the file, in `disc` and in the runtime's TOC and reads |
| **IP.BIN's initial program is the crt0**: the 1st read address holds a pointer table, and the game calls back into IP.BIN (0x06002E64) | the boot jumps to the 1st read address; IP.BIN's code is never run | a module for IP.BIN (the port recompiles it with seeds at its initial program and the functions the game calls); the boot enters it where the BIOS would, after the area block, and if it returns goes on to the 1st read address as the BIOS does |
| **SHC `-pic` code**: `bsrf`, `braf`, `mova; add; jsr` | the emitter resolves `bsrf`/`braf` by constants, discovery does not; `add Rm,Rn` stops constant propagation | discovery follows them (done in this port's saturnkit, to be checked on the other ports) |
| PAL: a European-only disc | 59.94 Hz for every disc, TVSTAT's PAL bit 0 | find out whether the game assumes 50 Hz (open question 2); if so a PAL raster (313 lines, 50 Hz, the PAL bit) chosen by the port, not by the disc's area (Virtual Hydlide, area E too, plays at 60 Hz on purpose) |
| Cinepak movies played by the game's own code | the CD block, DMA, VDP2 bitmaps (Virtual Hydlide's and X JAPAN's movies) | check |
| A sound driver of its own, speech streamed with music and effects | the 68000 and the SCSP in full, CD-DA into the SCSP | check against Beetle, by ear |
| The SCU DSP | Deep Fear's interpreter | check |
| The slave SH-2 | a deterministic coroutine | check |
| The battlefield's polygons and VDP2 planes | VDP1 in full in software; VDP2 NBG0–3, RBG0, windows | whatever the battles turn out to use (RBG1? the sprite window?) |
| Saves (`FICHIER 1–3`) | BUP services in a host file | check |

## What a better Dragon Ball Z on PC means

* **No waiting.** Every mode, every story chapter and every battle is a
  program and its data read from a 2x drive; read from a PC's disk they
  can be immediate once the game is known to run right.
* **The battlefield drawn sharp.** The terrain is polygons: drawn at the
  window's resolution rather than 320×224 (VDP1 on the GPU, or VDP1 in
  software at a multiple of its size) it keeps the game's geometry with
  finer edges and textures sampled finer. The fighters are hand-drawn
  sprites and stay pixel art, scaled cleanly.
* **The frame rate**: to be measured. If the battles step at 25 or 30
  fields a second, saturnkit's `--interp` (Virtual Hydlide's 60 fps)
  may draw the frames between, the terrain's polygons interpolating
  well; the sprites keep their own animation frames.
* **The speed the game was made for.** If the European release only
  runs at 50 Hz because Europe's Saturns did, the port can run its logic
  at the Japanese 60 fields a second, or keep 50: the user's choice,
  once open question 2 is answered.
* **Speech and music as on the disc**: the CD-DA straight from the
  tracks, the speech clips at their own rate, mixed on the PC.
* Later, if wanted: a wider battlefield (the field is wide by design;
  the HUD would need placing).

## Phases

1. **The survey** (session 1, done): the disc, the formats, the programs,
   discovery, the oracle to the story's first scene.
2. **saturnkit for this disc and its code**: the single .bin with its
   pregap, the boot through IP.BIN's initial program, discovery of
   `-pic` code; checked on Virtual Hydlide, Deep Fear, X JAPAN and Albert
   Odyssey.
3. **The recompiler**: IP.BIN and the eight programs as modules
   (`tools/recomp.py`), seeds, the self-test against the interpreter.
4. **The first run**: the boot, the Bandai movie, the opening, the title,
   the menu with CD-DA track 2, the story's first scene with its speech
   (`tools/run.py`, headless, pictures against Beetle's). PAL settled.
5. **The game**: the first battle (the polygon field, the SCU DSP, the
   slave), the versus mode, the options, saving and loading, the story
   to the end; against Beetle and played by the user.
6. **The PC gains**: no waiting, the field at the window's resolution,
   the frame rate, the speed.
7. **The release**: a build and a README for players (BYOA).
