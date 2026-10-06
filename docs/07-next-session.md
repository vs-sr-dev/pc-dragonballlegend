# Next session: saturnkit for this disc, the programs as C++, the first run

Where things stand: the disc is read and extracted, the eight programs
are found and discovered (`03-executables.md`), Beetle runs the game
from the boot to the story's first chapter card (`tools/oracle.py`).
saturnkit's submodule holds one change not yet committed: discovery
following `bsrf`, `braf` and `mova; add` constants.

## 1. saturnkit, checked on every port

* **The single .bin with `PREGAP`**: in `disc.py`, a track's frames
  before INDEX 01 that are not in the file; in `runtime/cdrom.cpp`, the
  tracks of one file each with its own mode and start, the pregap as
  silent sectors that are not in the file, and the TOC from them. Check:
  `disc --info` puts track 2 at LBA 184 963 as `XX_CDA.X02` says;
  `--audio` gives the same WAV files byte for byte.
* **The boot through IP.BIN's initial program**: when a module covers
  IP.BIN's code, enter it after the area block (0x06002E00, whose
  `bra`s chain to the initial program) as the BIOS does, and go on to the
  1st read address if it returns; without such a module, the boot as now.
  The game's call into IP.BIN (0x06002E64) then reaches that module.
* **Discovery's `-pic` constants** (in the submodule now): commit.
* Every change on Virtual Hydlide, Deep Fear, X JAPAN and Albert
  Odyssey: self-tests, headless runs byte-identical in pictures and sound
  against runs made before; then bump the four.

## 2. The recompiler

`tools/recomp.py` after Albert Odyssey's: IP.BIN at 0x06002000 (seeds
0x06002E00, 0x06002E64), `0` at 0x06003000 (seeds 0x060030B6,
0x060030D2, 0x060030F6), the seven programs at 0x06020000; build with
clang (MSYS2); the self-test against `sh2emu`.

## 3. The first run

`tools/run.py`: headless from the boot, the program starts traced
(which program is which: open question 1), pictures at the Bandai logo,
the opening movie, the title and the menu against Beetle's; CD-DA track 2
under the menu. Then START, C on HISTOIRE, C on DEBUT: the first scene
and its speech. Settle PAL (open question 2) from what the game counts.

## Keep in mind

* In the menus C confirms (START only leaves the title).
* Beetle: the Bandai logo at about 24 s after power-on, the title at
  about 96 s; `100:START,110:C,124:C` reaches the story's first scene,
  its music the piece on tracks 10–17, then the chapter card at 186 s.
* The voices' language: asked of the user (Beetle's recording,
  `build/oracle4/story-intro.wav`).
* Bash heredocs feeding `python -` mangle backslashes and non-ASCII:
  use files.
