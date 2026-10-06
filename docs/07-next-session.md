# Next session: what the user sees, then the first battle

Where things stand: IP.BIN's code, the loader and the seven programs are
C++ and self-tested (`09-recompiler.md`); on saturnkit's runtime the game
boots through the Bandai logo, the opening movie, the title and its
attract demo, the menu with its CD-DA music, and the story's first
comic-strip scene to its chapter card, at Beetle's rhythm
(`11-runtime.md`). `python tools/recomp.py --build --test`, then
`python tools/run.py` (headless, to the card), `--play` for the window.

## First: the user plays the first battle

Done in session 2 already: the user played to the first battle
(`tools/scripts/to-the-first-battle.txt`), and the stop there is fixed.
Next, `python tools/run.py --play` into the battle itself: the pictures,
the music, the speech (if any), the controls, and whether the speed
feels right (the runtime runs at the Japanese 60 fields a second; open
question 1). Each game is recorded to `build/run/play-*.txt` and can be
given back headless with `--input @FILE`.

## Then

1. Past the chapter card: what follows in the story (`INF`), and the
   first battle (`AP_ATB`): the polygon field, the SCU DSP (open question
   5), the slave SH-2 (6), the speech clips (2) and the driver (4).
   Against Beetle: a pad script for the oracle that reaches the same
   battle.
2. COMBAT (the versus mode) and OPTION (the office-floor wallpaper).
3. Saves: `FICHIER 1–3` and `DRAGONBALLZ` in the runtime's backup file.
4. The speed: settle with the user whether the port keeps 60 or offers
   50 (a PAL raster in saturnkit, chosen by the port).
5. Loading times (open question 9).

## Keep in mind

* In the menus A or C confirms; START leaves the title and skips the
  opening movie and the story's scenes.
* Beetle (PAL, wall-clock): the Bandai logo at about 24 s, the title at
  about 96 s; `100:START,110:C,124:C` reaches the story's first scene.
  The runtime (60 Hz, VBlanks): `6000:START,6006:,7300:C,7306:,7900:C,7906:`.
* The task list's handlers are reached only through computed addresses:
  a stop on "call to X, not an entry" is most likely one more pattern of
  `-pic` code for discovery (`tools/findptr.py` shows how a
  program computes X).
* Every saturnkit change: Virtual Hydlide, Deep Fear, X JAPAN and Albert
  Odyssey (self-tests, headless runs byte-identical or the difference
  explained against Beetle), then bump all four. X JAPAN's pad script
  depends on its frame pacing.
* Bash heredocs feeding `python -` mangle backslashes and non-ASCII:
  use files.
