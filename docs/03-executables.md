# The executables

Eight programs: a small resident loader, `0`, and seven programs that
take turns at 0x06020000. The addresses below were read in the code with
`saturnkit.sh2`; what is inferred says so.

## The start: IP.BIN, then `0`

The BIOS runs IP.BIN's initial program (0x06002E20, after the area
block), which is the game's own crt0 for `0` (`01-disc-layout.md`):
interrupts masked, VBR 0x06000000, stack 0x06002000, the work RAM
zeroed from 0x06009C8D up, then `jmp @(0x06003000)`.

IP.BIN also keeps code the game calls later: `0`'s start calls
0x06002E64 (`mov #0,r0; or #240,r0; rts; ldc r0,sr`, the interrupts
masked) with a `bsrf` at 0x060030BA (offset 0xFFFFFDA6 from 0x060030BE).

## `0`: the resident loader (0x06003000, 27 788 bytes)

It begins with a table, not code:

| Address | Value | |
|---|---|---|
| 0x06003000 | 0x060030B6 | the start: init, load the program, jump to it |
| 0x06003004 | 0x060030D2 | load the program `r4` names and jump to it (inferred: the programs' way to chain) |
| 0x06003008 | 0x060030F6 | load `AP_TLP.BIN` by name (the string at 0x06009C10) and jump to it |
| 0x0600300C | 0x06020000 | where programs load and start |

All three entries end in `jmp @(0x0600300C)`. The start calls the loader
at 0x06004514 with r4 = 3, r5 = 0, r6 = 0x06020000, r7 = −1; the
by-name entries first look the name up (0x06004090) and pass the index
it returns. Index 3 is the root directory's fourth record (`.`, `..`,
`0`, `1`): the boot loads `1`, as the runtime shows (session 2).

The programs chain by name: each ends with `jmp @(0x06003004)` and r4
pointing at the next program's name in its own data. The names each one
holds: `1` → `AP_BND`; `AP_BND` → `AP_TLP`; `AP_TLP` → `AP_SEL`;
`AP_SEL` → `AP_INF`, `AP_ATB`; `AP_INF` → `AP_ATB`, `AP_END`, `AP_TLP`;
`AP_ATB` → `AP_INF`, `AP_SEL`; `AP_END` → `AP_BND`. Of the data, `1`
names `GD_WAR`, `AP_BND` `MV_BND`, `AP_TLP` `GD_TLP`, `MV_OPD` and the
three `MV_TD` movies, `AP_ATB` `GD_ATB` and `GD_ORV`, the others the
`GD_` pack of their name, and all of them `SS_SND`.

`0` reads the disc itself: its own ISO 9660 reader (`CD001`, `.`, `..`
among its data) over the CD block's registers (0x25890008–0x25890020,
the data port 0x25898000). There is no GFS and no other library string
anywhere on the disc. It also refers to the SCU's registers, low work
RAM (0x00200000, 0x00240000) and sound RAM (0x05A00000), and calls the
BIOS through SYS_SETUINT, SYS_SETSINT, SYS_GETUINT, SYS_GETSINT,
SYS_CHGSCUIM and 0x0600026C.

## The programs at 0x06020000

| File | Size | Ends at | `main` | Role (seen in the runtime where it says so; the rest from the names) |
|---|---|---|---|---|
| `1` | 114 246 | 0x0603BE46 | 0x06020254 | the first program: writes the backup file `DRAGONBALLZ`, names `GD_WAR`, then `AP_BND` (seen: 3 s of black) |
| `AP_TLP.BIN` | 132 248 | 0x06040498 | 0x06020254 | the opening movie, the title and its attract demos (seen) |
| `AP_SEL.BIN` | 179 962 | 0x0604BEFA | 0x06020254 | the menus: MODE, HISTOIRE's CHOIX (seen) |
| `AP_INF.BIN` | 195 658 | 0x0604FC4A | 0x06020254 | the story's scenes (seen: the first one and its chapter card) |
| `AP_ATB.BIN` | 564 492 | 0x060A9D0C | 0x06020058 | the battles |
| `AP_BND.BIN` | 126 160 | 0x0603ECD0 | 0x06020254 | the Bandai logo's movie, `MV_BND` (seen) |
| `AP_END.BIN` | 135 422 | 0x060410FE | 0x06020254 | the ending |

Each starts with the same crt0 (the first 0x4D bytes are identical in
all seven): interrupts masked, VBR 0x06000000, the registers cleared,
the stack at 0x06002000, its own BSS zeroed from its end to 0x06100000,
then `jmp` to its `main` (0x06020254 in six of them, laid out alike; 0x06020058 in `AP_ATB`, laid out otherwise). So a program is started at its base and never
returns, like Virtual Hydlide's programs; the resident `0` below
0x06020000 survives every start. Their main loops call a fixed set of
functions forever through registers (in `AP_INF`: four, r11 to r14,
computed before the loop), and run a task list whose entries hold
function pointers (0x060201D6: `jsr @r5` with r5 from the task record).

### The compiler: SHC with position-independent code

Every program is compiled to run wherever it is put: calls go through
`mov.l #offset,rn; bsrf rn` (offset from the call + 4) or
`mov.l #offset,rn; mova LABEL,r0; add r0,rn; jsr @rn`, and far branches
through `braf`. This is the code of Hitachi SHC's `-pic` option
(inferred from the patterns; there is no compiler string). In `1`, 768
`bsrf` and 26 `braf` against 1 147 `jsr` and 812 `bsr`.

### Hardware they use

`tools/hwlits.py` over the literal pools (a first look): every program
but `0` refers to the SMPC, the SCU's registers including the DSP's
program and data ports (0x25FE0080–0x25FE008C), VDP1's registers and
VRAM, VDP2's registers, VRAM and colour RAM, sound RAM, the SCSP, SINIT
(the slave SH-2), the CD block and the SH-2's on-chip registers.
`AP_ATB` writes many places in VDP2's VRAM and low work RAM.

TVSTAT (0x25F80004) is read for its VBLANK bit around writes to TVMD
(0x06020066, 0x06020080 in `1`: display on and off) and once with a mask
(0x0602ABF6). No read of its PAL bit was found: a European game that
assumes PAL (open question 2).

## Discovery

`saturnkit.recomp.discover --report` on each program, at its base:

| Program | Functions | With problems | Switch tables | Unresolved indirect (c5d1280 → with bsrf/braf and `add` constants) | Calls through pointers |
|---|---|---|---|---|---|
| `0` | 301 | 1 (the table at 0x06003000, which is not code) | 1 | 30 → 18 | 30 |
| `1` | 659 | 0 | 4 | 110 → 42 | 49 |
| `AP_ATB` | 1 173 | 0 | 28 | 52 → 52 | 40 |
| `AP_BND` | 821 | 0 | 4 | 72 → 61 | 57 |
| `AP_END` | 690 | 0 | 4 | 128 → 48 | 49 |
| `AP_INF` | 807 | 0 | 4 | 254 → 88 | 51 |
| `AP_SEL` | 775 | 0 | 4 | 209 → 68 | 47 |
| `AP_TLP` | 840 | 0 | 4 | 89 → 64 | 57 |

6 066 functions in all, none with a problem. saturnkit as it was left
every `bsrf` and every `braf` that is not a switch unresolved, and could
not follow `mova LABEL,r0; add r0,rn` to a constant; with both (a change
in this port's saturnkit, `10-saturnkit.md`) 503 of the 944 unresolved
sites resolve. The rest, read in `AP_INF`, are calls through function
pointers: the task list, the main loop's registers loaded from memory.
The recompiler's emitter already resolved `bsrf` and `braf` by constants;
only discovery missed them, and so missed the functions they reach.

`0`'s seeds must be its three entries (0x060030B6, 0x060030D2,
0x060030F6), not its base. IP.BIN's initial program and the function the
game calls in it (0x06002E64) need a module of their own, or the
runtime has to do what they do.
