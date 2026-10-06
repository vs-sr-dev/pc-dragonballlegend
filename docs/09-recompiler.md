# The programs as C++

`python tools/recomp.py [--build] [--test]` turns IP.BIN's code, the
resident loader and the seven programs into C++ through saturnkit's
recompiler, builds them with clang from MSYS2 and checks them against
saturnkit's interpreter.

## The modules

| Module | File | Base | Functions | Instructions | Seeds |
|---|---|---|---|---|---|
| IP | `IP.BIN` | 0x06002000 | 21 | 827 | 0x06002E00 (the area block, whose `bra` leads to the initial program), 0x06002E64 (called by the game) |
| LOADER | `0` | 0x06003000 | 285 | 13 828 | 0x060030B6, 0x060030D2, 0x060030F6 (the table's three entries) |
| PROG1 | `1` | 0x06020000 | 663 | 50 575 | |
| BND | `AP_BND.BIN` | 0x06020000 | 827 | 55 788 | |
| TLP | `AP_TLP.BIN` | 0x06020000 | 864 | 57 836 | |
| SEL | `AP_SEL.BIN` | 0x06020000 | 941 | 68 319 | |
| INF | `AP_INF.BIN` | 0x06020000 | 945 | 66 890 | |
| ATB | `AP_ATB.BIN` | 0x06020000 | 1 173 | 141 352 | |
| END | `AP_END.BIN` | 0x06020000 | 707 | 52 865 | |

6 426 functions of the game and 510 410 instructions with saturnkit's
instruction test (775 functions), in 79 files; generated in about 15 s,
built in about 30 s (a full build a few minutes).

The base is always a seed too (saturnkit's recompiler adds it), so IP
and LOADER each have one function with a problem: the IP.BIN header and
the loader's table, which are never called. The seven programs are
ordinary programs started at their base (a crt0 that never returns);
IP and LOADER stay active below them.

## Discovery and SHC's `-pic` code

The first runs stopped on calls to addresses discovery had not found,
all of them handlers of the game's task list, which position-independent
code reaches only through addresses it computes:
`mov.l #k,rn; mova T,r0; add r0,rn`, then the address handed to the
task-creation function in a register. Discovery learned (saturnkit,
`10-saturnkit.md`):

1. `bsrf` and `braf` resolved by constants (target = the jump + 4 + the
   register), as the emitter already resolved them;
2. constants carried through `add Rm,Rn`, so `mova; add; jsr @rn`
   resolves;
3. addresses computed that way and never called directly are entries
   when they start at a boundary (after a terminator, a `braf` that is
   not a switch, or a literal pool) and descend cleanly into code that
   meets no known data; the `mova` may be up to 16 instructions before
   the `add`.

Each step was found by a stop in the run: BND at 0x0602C95E (a thunk
after an `rts`), 0x060224EA (after a tail `braf`); TLP at 0x0602315E
(computed in code reached only in the same pass), 0x06022BA4 (after an
unreached function's pool), 0x0602280A (the `mova` six instructions
before the `add`).

## Landings: the task list's longjmp

The task scheduler (0x060201D6 in every program but `AP_ATB`) saves r15,
calls each task's handler, and two routines let a handler leave at once:
0x060201BE restores the scheduler's stack and returns to 0x0602020E (the
next task), 0x060201CA returns to 0x06020226 (the scheduler's end), by
`mov.l #X,r1; lds r1,pr; rts`. A C++ call cannot return elsewhere, so
saturnkit learned landings: discovery lists such X, the recompiler
makes them labels and wraps the calls of the function holding them in a
`try`, and the runtime throws when a return goes to a landing instead of
its call's address, unwinding to that function. `AP_ATB` has its own
pair, 0x0604DAFA and 0x0604DB12.

## The self-test

Every function that runs alone (on its stack, or with pointer arguments)
is run in saturnkit's interpreter and in the C++, with IP and LOADER
loaded beside each program: 2 094 functions (775 of the instruction
test), 30 261 vectors, 0 differences in registers or memory.
