# Sessions

## Session 1 (2026-10-06): the disc, the code, the plan

* **The disc** (`01-disc-layout.md`): the European release, Bandai,
  T-13301H V1.000 (1996-11-08), area E alone, the title in IP.BIN
  `DRAGON BALL Z LA GRANDE LEGENDE DES BOULES DE CRISTAL`; the dump is
  of the Spanish pressing (T-13301H-06), whose text is French. An
  official release, not a fan translation. One .bin for 17 tracks: a
  Mode 1 data track and 16 CD-DA tracks holding nine pieces (tracks
  10–17 are one piece eight times). 22 files: a resident loader `0`,
  seven programs, seven graphics packs, five Cinepak movies, and one
  324 MB sound file.
* **The code** (`03-executables.md`): IP.BIN's initial program is the
  game's crt0 and jumps through a pointer table at the 1st read address;
  `0` (0x06003000) is a resident loader with its own ISO 9660 reader,
  which loads programs to 0x06020000 and starts them there: first the
  root's fourth record, `1` (by the directory's order), and by name
  `AP_TLP.BIN`; the seven programs each have their own crt0. No Sega library anywhere; SHC's
  position-independent code (`bsrf`, `braf`, `mova; add; jsr`). The
  programs use the SCU DSP, the slave SH-2, VDP1 and VDP2. Discovery:
  6 066 functions, none with a problem.
* **The formats** (`02-data-formats.md`): Sega FILM/Cinepak movies (the
  Bandai logo, the opening, three game-play movies); `SS_SND.BIN`: a
  68000 sound driver of its own (`Ver1.33 95/08/07`), banks, and 1 710
  speech clips in 8-bit PCM; graphics packs with offset tables.
* **The oracle** (`tools/oracle.py`, PAL): Beetle Saturn from the boot
  through the Bandai logo, the opening movie, the French title
  (`APPUIES SUR START`), the menu (`HISTOIRE`, `COMBAT`, `OPTION`, CD-DA
  track 2) and the story's first scene (the Saiyans' arrival, the piece
  on tracks 10–17, music alone: no speech, as the user heard) to its
  chapter card, `EPISODE 1 / LES SUPERSAIENS CONTRE LES MERCENAIRES DE
  L'ESPACE`. C confirms in the menus.
* **Curiosities** (`04-curiosities.md`): the Japanese team's afterword,
  a Shift-JIS file still on the European disc (the main programmer's
  year, the PlayStation team's vanished programmer, the characters cut
  for time, the office floor in the option screen's wallpaper, a hidden
  mode).
* **saturnkit** (`10-saturnkit.md`): `disc`, `sh2` and discovery held;
  three needs found: the single .bin's `PREGAP`, the boot through
  IP.BIN's initial program, and discovery of `-pic` code (changed in the
  submodule, to be checked on the other ports).
* **The plan** (`06-attack-plan.md`).

## Session 2 (2026-10-06): saturnkit for this disc, the programs as C++, the run to the story

* **saturnkit** (`10-saturnkit.md`): one .bin for every track with a
  `PREGAP` (b65cc58); the boot through IP.BIN's initial program when a
  build has IP.BIN as a module (6de2d31); discovery of SHC's `-pic` code,
  `bsrf`/`braf` and `mova`-computed addresses (1bc2e75); landings, the
  task list's longjmp unwound to its scheduler (c20d3c2); VDP1's frame
  change at the HBlank after VBlank-OUT, as Mednafen (bd3fd6c). Checked
  on Virtual Hydlide, Deep Fear, X JAPAN and Albert Odyssey; all four
  moved to bd3fd6c (X JAPAN's pad script 290 VBlanks earlier, its SEGA
  logo now as short as in Beetle).
* **The recompiler** (`09-recompiler.md`, `tools/recomp.py`): IP.BIN's
  code, the loader and the seven programs as nine modules, 6 426
  functions; self-test 30 261 of 30 261 vectors.
* **The first run** (`11-runtime.md`, `tools/run.py`): from the boot
  through `PROG1`, the Bandai logo, the opening movie, the French title
  (the same picture as Beetle's) and its attract demo (the `MV_TD`
  movies in grey under the logo), START, the menu with CD-DA track 2, C
  on HISTOIRE and DEBUT, the story's first comic-strip scene with the
  piece on tracks 10–17 (correlation 1.00), to the chapter card. The
  program chain seen and read: `PROG1` → `BND` → `TLP` → `SEL` →
  `INF`/`ATB` → `END`.
* **The frame rate**: the scene first ran at half speed: the game's
  VBlank-OUT handler waits for VDP1's draw end before it asks for a
  frame change, and the runtime changed frames before the handler ran.
  With Mednafen's order the game changes frame every field, as Beetle's
  recording shows (49.7 pictures a second), in time with its music.
* **Speed**: the game counts fields and never reads the PAL bit: at the
  runtime's 60 Hz it runs at the Japanese speed, 6/5 of the PAL release
  (open question 1, for the user).
* **Tools**: `tools/run.py` (to the chapter card), `tools/findptr.py`
  (where a program gets an address), `tools/vdp1list.py`.
* **Played by the user** to the first battle (`tools/scripts/to-the-first-battle.txt`):
  the loading picture says `Chergemant...`; the run stopped on an SCU
  DMA from backup RAM's mirror at 0x001F0010, which saturnkit now maps
  as Mednafen does (97047f9, the four other ports byte-identical); the battle's first screen follows.
