#!/usr/bin/env python3
"""THE LONG DAY POST — Final 6 delivery program, news-image-20261123.

Front page of THE LONG DAY POST for Monday 23 November 2026: forty stories
on a single sheet, twelve illustrated cards up front (the lead being the
US release of more UFO footage), a pinned world map, a UTC timeline strip,
an ALSO ON rail and the red DATE CHECK box that keeps six older items out
of the day's news.

This little program does no rendering whatsoever. The finished page lives
beside it as entry.png; all the program does is verify that file — PNG
signature, exact byte count, exact SHA-256 — and then copy it, untouched,
into MAKEFUN_OUTPUT_DIR (falling back to /output). Verification first,
copy second, so a corrupted or swapped page aborts the run instead of
quietly shipping the wrong front page. Two runs, same bytes out.
"""

import hashlib
import os
import sys

# The shipped page, pinned. Both numbers come from the verified entry.png
# that sits next to this file in the repository.
PAGE_BYTES = 280616
PAGE_SHA256 = "62f204efff0663fdd5fac35369dbc61fb2a4dafb8174c9c063621a90da1f2b39"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CEILING = 1024 * 1024  # competition cap: one mebibyte


def read_page():
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "entry.png")
    with open(path, "rb") as handle:
        return handle.read()


def verify(blob):
    """Refuse anything that is not exactly the intended page.

    Three independent checks, cheapest first: the eight-byte PNG
    signature, the byte count against both the competition ceiling and
    the pinned size, and finally the full SHA-256 digest.
    """
    if len(blob) == 0:
        sys.exit("entry.png: file is empty")
    if blob[:8] != PNG_SIGNATURE:
        sys.exit("entry.png: missing PNG signature")
    if len(blob) > CEILING:
        sys.exit("entry.png: %d bytes over the 1 MiB cap" % len(blob))
    if len(blob) != PAGE_BYTES:
        sys.exit("entry.png: got %d bytes, want %d" % (len(blob), PAGE_BYTES))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != PAGE_SHA256:
        sys.exit("entry.png: sha256 %s does not match %s" % (digest, PAGE_SHA256))
    return digest


def deliver(blob):
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    return target


def main():
    blob = read_page()
    digest = verify(blob)
    target = deliver(blob)
    sys.stderr.write("wrote %s (%d bytes, sha256 %s)\n"
                     % (target, len(blob), digest))


if __name__ == "__main__":
    main()
