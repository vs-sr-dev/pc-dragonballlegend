# Open questions

1. **Which program is which.** The boot loads root index 3, which by
   the directory's order is `1` (inferred); the order of the programs
   after it (`AP_BND` with the Bandai movie? `AP_TLP` the title, `AP_SEL`,
   `AP_INF`, `AP_ATB` the battles, `AP_END`) and what `1` itself does
   are inferred from the names. The runtime's trace of program starts
   will tell.
2. **PAL.** The disc is for Europe alone and no read of TVSTAT's PAL bit
   was found. Does the game count fields at 50 a second (its timers, its
   speech and subtitle timing, its game speed)? The Japanese original
   ran on a 60 Hz Saturn: was the European one slowed to 5/6, or
   retimed? saturnkit's runtime runs every disc at 59.94 Hz.
3. **The voices: where, and in what language?** 1 710 clips of 8-bit
   PCM in `SS_SND.BIN`, "more than 1 500 lines" in the Japanese
   afterword; but the story's first scene speaks none: in Beetle it is
   music alone (heard by the user; the recording correlates at 1.00 with
   the CD-DA track throughout). The lines are perhaps the battles'
   (inferred). Their language, and their rate (about 36 000 bytes a
   second over 2.5 hours, if mono), are not known.
4. **The `MV_TD` movies**: game play recorded as Cinepak, decoded grey
   by ffmpeg. Grey on the Saturn too, or a Cinepak variant ffmpeg reads
   wrong? Are they the title's attract demos (the title was left for
   only 3 s in Beetle)?
5. **Where the French text lives.** None of the programs holds ASCII
   text; the menus' words are graphics. The story's text (episode cards
   such as `LES SUPERSAIENS CONTRE LES MERCENAIRES DE L'ESPACE`) is drawn
   in a serif font: a font and strings in a `GD_` pack, or whole
   pictures?
6. **The sound driver** (`Ver1.33 95/08/07`, its makers' names): how the
   SH-2 talks to it, how the speech reaches sound RAM while a battle
   plays (streamed from the CD block?), and which music is the driver's
   rather than CD-DA.
7. **The battlefield**: polygon terrain and backgrounds (the afterword)
   drawn by VDP1 as distorted sprites, by VDP2's rotation screen, or
   both; and what the SCU DSP computes (every program but `0` loads it,
   by its ports).
8. **The slave SH-2**: every program refers to SINIT. What jobs?
9. **Saves**: the story has three files (`FICHIER 1–3`): the BIOS's
   backup RAM through BUP, or the game's own?
10. **The hidden mode** the afterword hints at (「○○○○モードがあるらしいよ」).
