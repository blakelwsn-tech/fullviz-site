#!/usr/bin/env python3
"""Convert images to WebP with headless Chrome.

This Mac has no cwebp, and sips can read WebP but not write it, so Chrome's own
encoder does the work. If cwebp is ever installed, it does the same job.

Usage:
    python3 tools/to_webp.py assets/img/photo-480.jpg assets/img/photo-960.jpg
    python3 tools/to_webp.py --quality 0.9 assets/img/photo-480.png

Writes a .webp next to each input, at the same pixel size.
"""
import base64
import mimetypes
import pathlib
import re
import subprocess
import sys
import tempfile
import threading

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PAGE = """<!doctype html><meta charset="utf-8"><title>working</title>%s<script>
addEventListener("load", () => {
  for (const img of [...document.images]) {
    const c = document.createElement("canvas");
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    c.getContext("2d").drawImage(img, 0, 0);
    const pre = document.createElement("pre");
    pre.dataset.name = img.dataset.name;
    pre.textContent = c.toDataURL("image/webp", %s);
    document.body.appendChild(pre);
    img.remove();
  }
});
</script>"""


def main():
    args = sys.argv[1:]
    quality = "0.82"
    if "--quality" in args:
        i = args.index("--quality")
        quality = str(float(args[i + 1]))
        del args[i:i + 2]
    if not args:
        sys.exit(__doc__)
    if not pathlib.Path(CHROME).exists():
        sys.exit("Google Chrome not found at %s" % CHROME)

    sources = {}
    tags = []
    for n, arg in enumerate(args):
        path = pathlib.Path(arg)
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        sources["img%d" % n] = path
        tags.append('<img data-name="img%d" src="data:%s;base64,%s">' % (n, mime, base64.b64encode(path.read_bytes()).decode()))

    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "page.html"
        page.write_text(PAGE % ("".join(tags), quality), encoding="utf-8")
        proc = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
             "--user-data-dir=%s/profile" % tmp, "--virtual-time-budget=15000", "--dump-dom", page.as_uri()],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        # Chrome prints the DOM and then tends to linger, so stop it once the DOM has arrived.
        timer = threading.Timer(90, proc.kill)
        timer.start()
        chunks = []
        for line in proc.stdout:
            chunks.append(line)
            if "</html>" in line:
                break
        timer.cancel()
        proc.kill()
        proc.wait()

    found = re.findall(r'<pre data-name="(img\d+)">data:image/webp;base64,([^<]+)</pre>', "".join(chunks))
    if len(found) != len(sources):
        sys.exit("expected %d image(s) back from Chrome, got %d" % (len(sources), len(found)))
    for name, data in found:
        out = sources[name].with_suffix(".webp")
        out.write_bytes(base64.b64decode(data))
        print("%s  %d bytes" % (out, out.stat().st_size))


if __name__ == "__main__":
    main()
