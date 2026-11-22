#!/usr/bin/env python3
"""Generate 2x (xhdpi) variants of the Amiga xfwm4 themes.

xfwm4 does not scale custom themes on HiDPI displays (only its own
"Default" theme is swapped for "Default-hdpi"), while the title font *is*
scaled. These 2x variants keep the decorations in proportion at a window
scale factor of 2 (e.g. GDK_SCALE=2 / 200% display scaling).

Every XPM pixel is replicated into a 2x2 block (nearest-neighbour), which
preserves the pixel-art look, the exact colour map and transparency.
Pixel-based themerc offsets are doubled as well.

Usage: scripts/make_xhdpi.py [repo-root]
Creates <theme>_xhdpi/ next to each base theme (Amiga1.3, Amiga3.x).
"""

import re
import sys
from pathlib import Path

# themerc options whose values are pixel offsets and must scale with the art
SCALED_OPTIONS = {
    "button_offset",
    "button_spacing",
    "title_vertical_offset_active",
    "title_vertical_offset_inactive",
    "title_horizontal_offset",
    "maximized_offset",
    "frame_border_top",
}


def double_xpm(text: str) -> str:
    """Return the XPM with every pixel doubled in both directions."""
    strings = re.findall(r'"([^"]*)"', text)
    w, h, ncol, cpp = map(int, strings[0].split()[:4])
    colormap = strings[1 : 1 + ncol]
    rows = strings[1 + ncol : 1 + ncol + h]
    if len(rows) != h or any(len(r) != w * cpp for r in rows):
        raise ValueError("malformed XPM pixel data")

    replacement = [f"{w * 2} {h * 2} {ncol} {cpp}"] + colormap
    for row in rows:
        doubled = "".join(row[i : i + cpp] * 2 for i in range(0, w * cpp, cpp))
        replacement.extend((doubled, doubled))

    # Rebuild the file: the doubled row count differs from the original, so
    # splice a fresh string list between the C wrapper's prefix and suffix.
    first, last = text.index('"'), text.rindex('"')
    body = ",\n".join('"' + s + '"' for s in replacement)
    return text[:first] + body + text[last + 1 :]


def scale_themerc(text: str) -> str:
    out = []
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or key == "title_full_width":
            # title_full_width was never a valid xfwm4 option
            continue
        if key in SCALED_OPTIONS:
            value = str(int(value) * 2)
        out.append(f"{key}={value}")
    return "\n".join(out) + "\n"


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    for name in ("Amiga1.3", "Amiga3.x"):
        src = root / name / "xfwm4"
        dst = root / f"{name}_xhdpi" / "xfwm4"
        dst.mkdir(parents=True, exist_ok=True)
        for xpm in sorted(src.glob("*.xpm")):
            (dst / xpm.name).write_text(double_xpm(xpm.read_text()))
        (dst / "themerc").write_text(scale_themerc((src / "themerc").read_text()))
        print(f"created {dst.relative_to(root)} ({len(list(dst.glob('*.xpm')))} pixmaps)")


if __name__ == "__main__":
    main()
