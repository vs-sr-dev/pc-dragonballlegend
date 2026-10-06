# What this port gave saturnkit

saturnkit (`saturnkit/`, a submodule from
https://github.com/vs-sr-dev/saturnkit) was started by Virtual Hydlide's
port and grew through Deep Fear's, X JAPAN's and Albert Odyssey's. Dragon
Ball Z is its fifth game: SHC again, but compiled as position-independent
code, with no Sega library at all, a crt0 inside IP.BIN, a task list that
leaves its tasks by longjmp, and a disc dumped as one .bin. Each entry is
a saturnkit commit and what this game asked of it.

| Session | saturnkit | What |
|---|---|---|
| 1 | c5d1280 (unchanged) | the port starts at saturnkit's current head |
| 2 | b65cc58 | `disc` and the runtime: one .bin for every track, each track with its own mode, a `PREGAP` the file does not hold counted on the disc and read as silence |
| 2 | 6de2d31 | runtime: when a build has IP.BIN as a module, the boot runs its area block and initial program (here the game's crt0), and the 1st read address only if that returns |
| 2 | 1bc2e75 | `recomp.discover`: SHC's position-independent code: `bsrf`/`braf` by constants, constants through `add Rm,Rn`, addresses computed with `mova` and `add` taken as entries at a boundary |
| 2 | c20d3c2 | landings: `mov.l #X,rn; lds rn,pr; rts` makes X an address returned to without a call (the task list's longjmp); the recompiler makes it a label its calls unwind to, the runtime throws `SH2Unwind` for a return there |
| 2 | db53060 | README |
| 2 | bd3fd6c | runtime: VDP1 takes the VBlank's end at the next HBlank, as Mednafen: a VBlank-OUT handler's frame change comes in the same blanking |
| 2 | 97047f9 | runtime: backup RAM answers over 0x00180000-0x001FFFFF (64 KiB repeated), as Mednafen: the first battle's sprite loading reads one SCU DMA source there |

## Session 1: what held, and what did not

Held as it was:

* `disc --extract` and `--audio` on the single .bin: 22 files and IP.BIN,
  the 16 `XX_CDA.Xnn` records listed and left out, 16 WAV files of the
  right lengths (the file offsets come from INDEX 01, which is right).
* `sh2 --find-base`: `0` at 0x06003000, the seven programs at 0x06020000
  (each checked against its crt0).
* `recomp.discover`: 6 066 functions in eight programs, none with a
  problem.

Did not hold, and was done in session 2:

* **`disc --info` and the runtime's TOC ignore `PREGAP`.** Track 2's
  two-second pregap is not in the .bin; every audio track is listed 150
  sectors below where the disc's own `XX_CDA.Xnn` records put it. The
  runtime also gives a .bin shared by several tracks the last track's
  mode, so this disc's data track would read as audio.
* **The boot jumps to the 1st read address.** Here it holds a table of
  pointers; IP.BIN's initial program is the crt0 and jumps through it,
  and the game later calls a function inside IP.BIN.
* **Discovery and SHC's `-pic` code.** `bsrf` and `braf` (outside
  switches) were left unresolved, and constant propagation stopped at
  `add Rm,Rn`, so `mova LABEL,r0; add r0,rn; jsr @rn` was unresolved
  too. Discovery now puts `bsrf`/`braf` among the jumps resolved by constants (target = the
  jump + 4 + the constant, as the emitter already computes it) and
  propagates constants through `add Rm,Rn`: 944 unresolved sites in the
  eight programs become 441 (1bc2e75, with the computed entries the run
  asked for, `09-recompiler.md`).

## Session 2: the checks on the other ports

Each change was applied to the four other ports' submodules, which were
regenerated, rebuilt, self-tested and run headless against a run made
just before with c5d1280 (pictures at three VBlanks and the whole run's
sound compared byte for byte), by a script kept in the session's
scratchpad.

* **b65cc58 to db53060** (the single .bin, the boot through IP.BIN,
  `-pic` discovery, landings): Virtual Hydlide (51 542 vectors), Deep
  Fear (16 527), X JAPAN (11 632) and Albert Odyssey (15 532) pass their
  self-tests with the same vectors (their discovery unchanged, no
  landings in them); all four runs byte-identical. All four moved to
  db53060.
* **bd3fd6c** (VDP1's frame change): Virtual Hydlide byte-identical.
  Deep Fear: 963 VDP1 frame changes in 3 000 VBlanks against 964, its
  "presents" title a frame apart at VBlank 2000, the sound and its first
  room identical. Albert Odyssey: the sound identical, 5 566 frame
  changes against 5 565; its title's forest, a VDP1 object drawn every
  other field before as after, shows in the other fields (the picture at
  VBlank 2040 lacks it); the user's recorded game still reaches the
  harpies' village. X JAPAN: its handler asks for a change every field,
  so its SEGA logo is shorter and everything after it comes 4.84 s
  earlier, the opening at the same speed; against a Beetle recording the
  opening now starts 3.56 s after the logo appears (Beetle 3.15 s, before
  6.4 s): closer. Its pad script was moved from VBlank 7500 to 7210 and
  still reaches the corridor. All four moved to bd3fd6c, X JAPAN with its
  script and a note in its `docs/11-runtime.md`.
* **97047f9** (backup RAM's mirror): an access there was fatal before;
  all four byte-identical against runs made at bd3fd6c (X JAPAN with its
  new script). All four moved to 97047f9.

## What this game will ask next

* The battles (`AP_ATB`): the polygon field, the SCU DSP, the slave SH-2,
  the speech clips through the game's own 68000 driver.
* A choice of speed: the game counts fields; the runtime's raster is
  60 Hz only (a PAL raster, chosen by the port, if the user wants the
  European speed).
