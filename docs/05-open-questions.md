# Open questions

Answered in session 2: which program is which (the boot loads `1`, then
`BND`, `TLP`, `SEL`, `INF`, seen in the runtime, and the names each
passes to the loader give the rest, `03-executables.md`); the `MV_TD`
movies (the title's attract demos, shown in grey in a window under the
logo, `11-runtime.md`).

1. **Speed: 50 or 60 fields a second.** The game steps once a field
   and never reads TVSTAT's PAL bit. At the runtime's 60 Hz it runs at
   the Japanese original's speed, 6/5 of the European release on a PAL
   Saturn (the story's first scene: about 47 s against 55 s in Beetle; at
   50 Hz it lasts as long as its music track). Was the European release
   meant to run slower, or did it only because Europe's Saturns ran at
   50 Hz? Which does the port keep: the user's choice.
2. **The voices: where, and in what language?** 1 710 clips of 8-bit
   PCM in `SS_SND.BIN`, "more than 1 500 lines" in the Japanese
   afterword; but the story's first scene speaks none: in Beetle it is
   music alone (heard by the user; the recording correlates at 1.00 with
   the CD-DA track throughout). The lines are perhaps the battles'
   (inferred). Their language, and their rate (about 36 000 bytes a
   second over 2.5 hours, if mono), are not known.
3. **Where the French text lives.** None of the programs holds ASCII
   text; the menus' words are graphics. The story's text (episode cards
   such as `LES SUPERSAIENS CONTRE LES MERCENAIRES DE L'ESPACE`) is drawn
   in a serif font: a font and strings in a `GD_` pack, or whole
   pictures?
4. **The sound driver** (`Ver1.33 95/08/07`, its makers' names): how the
   SH-2 talks to it, how the speech reaches sound RAM while a battle
   plays (streamed from the CD block?), and which music is the driver's
   rather than CD-DA.
5. **The battlefield**: polygon terrain and backgrounds (the afterword)
   drawn by VDP1 as distorted sprites, by VDP2's rotation screen, or
   both; and what the SCU DSP computes (every program but `0` loads it,
   by its ports).
6. **The slave SH-2**: every program refers to SINIT. What jobs?
7. **Saves**: the story has three files (`FICHIER 1–3`); `PROG1` writes
   a backup file `DRAGONBALLZ` (256 bytes) through the BIOS's BUP on the
   first boot. What it holds, and the story's saves.
8. **The hidden mode** the afterword hints at (「○○○○モードがあるらしいよ」).
9. **Loading times**: after START at 100 s, the runtime starts `SEL` at
   102.3 s and builds the menu from about VBlank 6750 (112.5 s), whole at
   6900 (115 s); Beetle shows it whole by 110 s (black at 104 and 106 s).
   A few seconds slower: CD reads (a 2x drive with seeks), or the time
   model?
