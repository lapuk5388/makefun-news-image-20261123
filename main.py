"""THE DAY'S DISPATCH — NI23 G4 entry for Final 6.

Stdlib-only, copy-only: copies the bundled entry.png to the
output directory named by MAKEFUN_OUTPUT_DIR (default ./out).
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not os.path.isabs(out):
        out = os.path.join(os.getcwd(), out)
    os.makedirs(out, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out, "entry.png")
    shutil.copyfile(src, dst)
    sys.exit(0)


if __name__ == "__main__":
    main()
