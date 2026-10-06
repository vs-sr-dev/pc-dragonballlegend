"""Recompile Dragon Ball Z's programs to C++ and check them.

    python tools/recomp.py [--build] [--test] [--no-vectors]

1. `python -m saturnkit.recomp`: IP.BIN's code (its initial program is
   the game's crt0, and the game calls back into it) as module IP, the
   resident loader `0` as LOADER, and the seven programs that take turns
   at 0x06020000 as one module each, with saturnkit's instruction test,
   into build/recomp; report.txt there has the counts.
2. `python -m saturnkit.recomp.selftest`: the vectors of every function of
   each module that runs alone (on its stack, or on what its pointer
   arguments point at), with IP and LOADER loaded beside each program,
   into build/recomp/selftest.
3. --build: CMake, Ninja and clang from MSYS2 into build/recomp-build.
4. --test: the self-test executable on every vectors file.

Run from the repository root, after the disc has been extracted
(build/extract).
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
EXTRACT = os.path.join(ROOT, "build", "extract")
OUT = os.path.join(ROOT, "build", "recomp")
BUILD = os.path.join(ROOT, "build", "recomp-build")
MSYS = r"C:\msys64\mingw64\bin"

IP_BASE = 0x06002000
# the area block (its `bra` leads to the initial program) and the function
# the game calls in IP.BIN (interrupts masked)
IP_SEEDS = [0x06002E00, 0x06002E64]
LOADER_BASE = 0x06003000
# the three entries of the table at 0x06003000 (the base itself is the table)
LOADER_SEEDS = [0x060030B6, 0x060030D2, 0x060030F6]
PROGRAM_BASE = 0x06020000
PROGRAMS = [("PROG1", "1"), ("BND", "AP_BND.BIN"), ("TLP", "AP_TLP.BIN"), ("SEL", "AP_SEL.BIN"),
            ("INF", "AP_INF.BIN"), ("ATB", "AP_ATB.BIN"), ("END", "AP_END.BIN")]


def hexes(seeds):
    return ",".join("%08X" % s for s in seeds)


def specs():
    yield "IP=%s@%08X+%s" % (os.path.join(EXTRACT, "IP.BIN"), IP_BASE, hexes(IP_SEEDS))
    yield "LOADER=%s@%08X+%s" % (os.path.join(EXTRACT, "0"), LOADER_BASE, hexes(LOADER_SEEDS))
    for name, f in PROGRAMS:
        yield "%s=%s@%08X" % (name, os.path.join(EXTRACT, f), PROGRAM_BASE)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--no-vectors", action="store_true")
    a = ap.parse_args()
    from saturnkit.recomp.__main__ import generate, parse_spec
    from saturnkit.recomp import selftest
    t0 = time.time()
    all_specs = list(specs())
    generate([parse_spec(s) for s in all_specs], OUT, optest=True)
    if not a.no_vectors:
        os.makedirs(os.path.join(OUT, "selftest"), exist_ok=True)
        resident = all_specs[:2]
        for s in all_specs:
            name = s.split("=", 1)[0]
            images = resident if s in resident else resident + [s]
            argv = ["--out", os.path.join(OUT, "selftest", name.lower() + ".txt"), "--test", name, "--auto"]
            for img in images:
                argv += ["--image", img]
            selftest.main(argv)
    print("generated in %.0f s" % (time.time() - t0))
    env = dict(os.environ, PATH=MSYS + os.pathsep + os.environ["PATH"])
    tool = lambda x: shutil.which(x, path=env["PATH"])      # CreateProcess searches the parent's PATH
    if a.build:
        t = time.time()
        subprocess.run([tool("cmake"), "-S", OUT, "-B", BUILD, "-G", "Ninja", "-DCMAKE_CXX_COMPILER=clang++",
                        "-DCMAKE_C_COMPILER=clang"], env=env, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([tool("ninja"), "-C", BUILD], env=env, check=True)
        print("built in %.0f s" % (time.time() - t))
    if a.test:
        names = ["optest"] + [s.split("=", 1)[0].lower() for s in all_specs]
        files = [os.path.join(OUT, "selftest", n + ".txt") for n in names]
        r = subprocess.run([os.path.join(BUILD, "selftest.exe")] + [f for f in files if os.path.exists(f)], env=env)
        sys.exit(r.returncode)


if __name__ == "__main__":
    main()
