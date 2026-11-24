#!/usr/bin/env python3
"""THE LONG DAY POST — entry program for news-image-20261123 (Final 6).

The Long Day Post is a one-page newspaper front page that sums up Monday
23 November 2026 in 40 stories: a 12-card illustrated main grid led by the
US release of declassified UFO footage, a dotted world map with numbered
pins, a UTC timeline, an ALSO ON column and a red DATE CHECK box that
names six older stories and keeps them out of the news.

This program is the delivery vehicle for that page. It uses only the
Python standard library (hashlib, os, sys), performs no drawing at all,
and simply copies the finished entry.png sitting next to it into the
output directory named by MAKEFUN_OUTPUT_DIR (default /output). Before
copying, it checks the PNG magic bytes, the 1 MiB competition ceiling
and the exact expected size of the shipped page, so a swapped or
truncated file fails loudly instead of submitting the wrong image.
Running it twice produces byte-identical output.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 280616
EXPECTED_SHA256 = "62f204efff0663fdd5fac35369dbc61fb2a4dafb8174c9c063621a90da1f2b39"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB competition ceiling


def load_entry():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        return fh.read()


def check_entry(data):
    if not data:
        sys.exit("entry.png is empty")
    if data[:8] != PNG_MAGIC:
        sys.exit("entry.png is not a PNG (bad magic bytes)")
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds 1 MiB: %d bytes" % len(data))
    if len(data) != EXPECTED_BYTES:
        sys.exit("entry.png size changed: %d bytes, expected %d"
                 % (len(data), EXPECTED_BYTES))


def check_digest(data):
    """Second, independent guard: the page must hash to the recorded value.

    Size alone cannot tell two different 280,616-byte files apart, so the
    SHA-256 of the shipped page is pinned as well. A mismatch means the
    entry.png on disk is not the page that won the variant duel.
    """
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 changed: %s, expected %s"
                 % (digest, EXPECTED_SHA256))
    return digest


def main():
    data = load_entry()
    check_entry(data)
    digest = check_digest(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    sys.stderr.write("entry.png: %d bytes sha256=%s\n" % (len(data), digest))


if __name__ == "__main__":
    main()
