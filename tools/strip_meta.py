#!/usr/bin/env python3
"""Remove EXIF, GPS, XMP, IPTC, and comments from JPEG and PNG files, without re-encoding the picture.

Phone photos carry the place they were taken, and screenshots and exports carry their own notes.
Run this on every JPEG and PNG before it is committed:

    python3 tools/strip_meta.py assets/img/*.jpg
    python3 tools/strip_meta.py --check assets/img/*.jpg     # report only, change nothing

The colour profile (ICC) and the image data are kept, so the photo looks the same.
WebP files made by tools/to_webp.py are already clean.
"""
import pathlib
import struct
import sys

DROP = {0xE1: "EXIF/XMP", 0xED: "IPTC", 0xFE: "comment"}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_DROP = {b"eXIf": "EXIF", b"iTXt": "text/XMP", b"tEXt": "text", b"zTXt": "text", b"tIME": "timestamp", b"iDOT": "Apple data"}


def segments(data):
    """Yield (marker, start, end) for each header segment, then ('scan', start, len(data))."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG")
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            raise ValueError("bad marker at %d" % i)
        marker = data[i + 1]
        if marker == 0xDA:  # start of scan: the rest is image data
            yield "scan", i, len(data)
            return
        size = struct.unpack(">H", data[i + 2:i + 4])[0]
        yield marker, i, i + 2 + size
        i += 2 + size


def has_gps(segment):
    """True if an EXIF segment points at a GPS block."""
    if segment[4:10] != b"Exif\x00\x00":
        return False
    tiff = segment[10:]
    order = "<" if tiff[:2] == b"II" else ">"
    offset = struct.unpack(order + "I", tiff[4:8])[0]
    count = struct.unpack(order + "H", tiff[offset:offset + 2])[0]
    for n in range(count):
        entry = tiff[offset + 2 + n * 12: offset + 14 + n * 12]
        if len(entry) == 12 and struct.unpack(order + "H", entry[:2])[0] == 0x8825:
            return True
    return False


def png_chunks(data):
    """Yield (type, start, end) for each PNG chunk."""
    i = len(PNG_SIGNATURE)
    while i < len(data):
        size, kind = struct.unpack(">I4s", data[i:i + 8])
        yield kind, i, i + 12 + size
        i += 12 + size


def clean(data):
    """Return (cleaned bytes, list of what was removed)."""
    found = []
    if data.startswith(PNG_SIGNATURE):
        out = [PNG_SIGNATURE]
        for kind, start, end in png_chunks(data):
            if kind in PNG_DROP:
                found.append(PNG_DROP[kind])
                continue
            out.append(data[start:end])
        return b"".join(out), found
    out = [b"\xff\xd8"]
    for marker, start, end in segments(data):
        chunk = data[start:end]
        if marker in DROP:
            found.append(DROP[marker] + (" with GPS" if marker == 0xE1 and has_gps(chunk) else ""))
            continue
        out.append(chunk)
    return b"".join(out), found


def main():
    args = sys.argv[1:]
    check = "--check" in args
    files = [a for a in args if a != "--check"]
    if not files:
        sys.exit(__doc__)
    dirty = 0
    for name in files:
        path = pathlib.Path(name)
        data = path.read_bytes()
        out, found = clean(data)
        if found:
            dirty += 1
            if not check:
                path.write_bytes(out)
        print("%-44s %s" % (path.name, ("found: " if check else "removed: ") + ", ".join(found) if found else "clean"))
    if check and dirty:
        sys.exit(1)


if __name__ == "__main__":
    main()
