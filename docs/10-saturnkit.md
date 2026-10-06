# What this port gave saturnkit

saturnkit (`saturnkit/`, a submodule from
https://github.com/vs-sr-dev/saturnkit) was started by Virtual Hydlide's
port and grew through Deep Fear's, X JAPAN's and Albert Odyssey's. Dragon
Ball Z is its fifth game: SHC again, but compiled as position-independent
code, with no Sega library at all, a crt0 inside IP.BIN, and a disc
dumped as one .bin. Each entry is a saturnkit commit and what this game
asked of it.

| Session | saturnkit | What |
|---|---|---|
| 1 | c5d1280 (unchanged) | the port starts at saturnkit's current head |

## Session 1: what held, and what did not

Held as it was:

* `disc --extract` and `--audio` on the single .bin: 22 files and IP.BIN,
  the 16 `XX_CDA.Xnn` records listed and left out, 16 WAV files of the
  right lengths (the file offsets come from INDEX 01, which is right).
* `sh2 --find-base`: `0` at 0x06003000, the seven programs at 0x06020000
  (each checked against its crt0).
* `recomp.discover`: 6 066 functions in eight programs, none with a
  problem.

Did not hold, for the next session (`07-next-session.md`):

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
  too. A change in this port's submodule (not committed yet) puts
  `bsrf`/`braf` among the jumps resolved by constants (target = the
  jump + 4 + the constant, as the emitter already computes it) and
  propagates constants through `add Rm,Rn`: 944 unresolved sites in the
  eight programs become 441. To be checked on the four other ports
  before it is committed.
