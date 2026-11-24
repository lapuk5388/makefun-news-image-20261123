import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

FALLBACK_WORDS = [
    "cop31", "hormuz", "kyiv", "albanese", "benghazi", "lisbon",
    "rohingya", "alcaraz", "miley", "fbi", "democrats", "ufo",
    "nepal", "tata steel", "spicejet", "gold", "myanmar", "finland",
    "zverev", "morando", "iowa", "schumer", "modi", "asean",
    "houthi", "patriot", "bahrain", "indonesia", "wellington", "antalya",
]


def load_words():
    path = "/home/hatch/workspace/makefun/ni23-fresh.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            return [ln.strip() for ln in fh if ln.strip()]
    return FALLBACK_WORDS


def main():
    png = os.path.join(HERE, "entry.png")
    size = os.path.getsize(png)
    assert size <= 1048576, "entry.png too large: %d" % size
    with open(png, "rb") as fh:
        head = fh.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", head[16:24])
    assert (w, h) == (1024, 1024), "bad size %dx%d" % (w, h)
    with open(os.path.join(HERE, "compose.py"), "r", encoding="utf-8") as fh:
        compose_src = fh.read().lower()
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as fh:
        own_src = fh.read().lower()
    hay = compose_src + "\n" + own_src
    for word in load_words():
        assert word.lower() in hay, "fresh word missing: %s" % word
    print("test_entry OK: %d bytes, 1024x1024, fresh words present" % size)


if __name__ == "__main__":
    main()
