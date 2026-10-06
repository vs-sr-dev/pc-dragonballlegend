# pc-dragonballlegend

Toward a native PC port of **Dragon Ball Z: La Grande Légende des Boules
de Cristal** (Sega Saturn, Bandai; 1996 in Japan as *Dragon Ball Z:
Idainaru Dragon Ball Densetsu*, then in Europe in French), an action game
in which up to several fighters a side battle on a wide 3D field, the
player switching between them, through the story of Dragon Ball Z from
the Saiyans' arrival on: polygon terrain, hand-drawn sprites, comic-strip
story scenes with about 1 500 spoken lines, and house music on CD. It
came out on the Saturn and the PlayStation and was never re-released.
The goal is the game running natively on PC: without the CD's waits, its
battlefield drawn sharp at the window's resolution, at the speed it was
made for, with its speech and music as they are on the disc.

This repository documents the disc, its formats and its code, and grows
the tooling for the port. It is the fifth port built on **saturnkit**,
the game-agnostic toolkit for Saturn reverse engineering that grew out
of [pc-virtualhydlide](https://github.com/vs-sr-dev/pc-virtualhydlide).
Dragon Ball Z is where saturnkit meets position-independent SHC code, a
game with no Sega library at all, a crt0 inside IP.BIN, a task list that
leaves its tasks by longjmp, and a disc kept as a single .bin. saturnkit is a submodule here: clone with
`--recursive`, or run `git submodule update --init`.

## BYOA: Bring Your Own Assets

This repository contains **documentation and tools only**. No game data,
no executables, no assets. You need your own original disc. The work is
done on the European release, T-13301H V1.000 (1996-11-08), one disc in
French, as a .cue with a single .bin for its 17 tracks in `iso/` (CRC32
of the .bin: 8950B64B).

## Layout

    docs/            disc, format and code analysis, and the plan
    tools/           Dragon Ball Z-specific tools: recomp.py, run.py, oracle.py, sheet.py,
                     cdda_match.py, hwlits.py, findptr.py, vdp1list.py
    saturnkit/       game-agnostic Saturn toolkit (submodule)
    iso/, build/     your disc and everything derived from it (ignored by git)

## Tools

The Python tools need only Python 3.8+; `sheet.py` needs PIL and
`cdda_match.py` numpy. Building the recompiled C++ needs CMake, Ninja,
clang and SDL3 (MSYS2's mingw64, found at `C:\msys64\mingw64\bin`). The
oracle needs RetroArch with the Beetle Saturn
core and the US/European BIOS (`mpr-17933.bin`), and ffmpeg for its
recordings. Run everything from the repository root.

```sh
C=iso/dw-dbzl.cue

# the disc: IP.BIN, the volume, the 17 tracks; the files; the CD-DA tracks as WAV
python -m saturnkit.disc "$C" --info
python -m saturnkit.disc "$C" --list
python -m saturnkit.disc "$C" --extract build/extract
python -m saturnkit.disc "$C" --audio build/audio

# the code: IP.BIN's initial program, the resident loader, a program
python -m saturnkit.sh2 build/extract/IP.BIN --base 06002000 --at 06002E20 --count 40
python -m saturnkit.sh2 build/extract/0 --base 06003000 --at 060030B6 --count 40
python -m saturnkit.recomp.discover build/extract/0 --base 06003000 --report
python -m saturnkit.recomp.discover build/extract/AP_TLP.BIN --base 06020000 --report
python tools/hwlits.py build/extract/0@06003000 build/extract/1@06020000

# the programs to C++, built with clang (MSYS2) and checked against the interpreter
python tools/recomp.py --build --test

# run it on saturnkit's runtime: headless to the story's first chapter card, pictures at chosen VBlanks
python tools/run.py -- --shot 5400,6900,10500
python tools/run.py --play                 # a window, the keyboard or a gamepad
python tools/findptr.py build/extract/AP_TLP.BIN 06020000 0602315E   # where a program gets an address

# the oracle: Beetle Saturn in RetroArch, pressed and photographed from here
python tools/oracle.py --at 100:START,110:C,124:C --every 3 --quit 200 --record
python tools/sheet.py build/oracle                                  # the shots on one sheet
python tools/cdda_match.py build/oracle/record.wav                  # which CD-DA track plays when
```

## Status

Session 1: the survey. One disc, a data track and 16 CD-DA tracks (nine
pieces of music). IP.BIN's initial program is the game's crt0; a
resident loader, `0`, at 0x06003000, with its own ISO 9660 reader, starts
seven programs in turn at 0x06020000. No Sega library; SHC compiled as
position-independent code, which saturnkit's discovery learned to
follow (`bsrf`, `braf`, `mova`-relative calls): 6 066 functions, none with a
problem. Cinepak movies, a 68000 sound driver of the game's own and
1 710 speech clips in one 324 MB file. Beetle Saturn driven from the boot
through the Bandai logo, the opening movie, the French title and menu,
to the story's first scene and chapter card. The disc also carries the
Japanese team's development afterword (`docs/04-curiosities.md`).

Session 2: IP.BIN's code, the loader and the seven programs as C++
(6 426 functions in nine modules; self-test 30 261 of 30 261 vectors) on
saturnkit's runtime, from the boot through the Bandai logo, the opening
movie, the French title and its attract demo, the menu with its CD-DA
music and the story's first comic-strip scene to its chapter card, at
Beetle's rhythm. saturnkit learned a single .bin with a `PREGAP`, the
boot through IP.BIN's initial program, SHC's position-independent code,
landings (the game's task list leaves its tasks by longjmp) and VDP1's
frame change after the VBlank-OUT handler, as Mednafen
(`docs/10-saturnkit.md`, `docs/11-runtime.md`).

## Playing it

The game runs as far as it has been played: through the title, the
menu and the story's first scene into the first battle's opening screen
(the user's game, `tools/scripts/to-the-first-battle.txt`). The battle
itself has not been played yet.

```sh
python tools/run.py --play            # the game in a window
```

Keys (in `saturnkit/runtime/host.cpp`): the arrows, Enter for START,
Z X C for A B C (A or C confirms in the menus), A S D for X Y Z, Q W for L R;
F11 fullscreen, F12 a picture. A gamepad works too. Each game is
recorded to `build/run/play-DATE-TIME.txt`; `python tools/run.py
--input @that-file` plays it again, headless. The runtime runs at 60
fields a second, the Japanese original's speed, 6/5 of the European
release on a PAL Saturn.

## Documentation

* [00-sessions.md](docs/00-sessions.md): what each session did
* [01-disc-layout.md](docs/01-disc-layout.md): IP.BIN, tracks, the files; is it the official release
* [02-data-formats.md](docs/02-data-formats.md): movies, sound, music, graphics packs at a glance
* [03-executables.md](docs/03-executables.md): IP.BIN's start, the loader, the programs, the compiler, discovery
* [04-curiosities.md](docs/04-curiosities.md): things found on the way
* [05-open-questions.md](docs/05-open-questions.md): what is not known yet
* [06-attack-plan.md](docs/06-attack-plan.md): feasibility, what saturnkit has and lacks, the phases, what a better Dragon Ball Z means
* [07-next-session.md](docs/07-next-session.md): the next session's list
* [09-recompiler.md](docs/09-recompiler.md): the programs as C++, discovery and `-pic` code, landings, the self-test
* [10-saturnkit.md](docs/10-saturnkit.md): what this port gives saturnkit
* [11-runtime.md](docs/11-runtime.md): the game on saturnkit's Saturn, how far it runs, the frame rate, the speed

## Licence

MIT: see [LICENSE](LICENSE). Dragon Ball Z: La Grande Légende des Boules
de Cristal is © Bird Studio / Shueisha, Toei Animation, Bandai 1996 (as
its title screen gives it); this project contains none of it.
