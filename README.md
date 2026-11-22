# Amiga OS Themes for XFCE (XFWM4)

AmigaOS-style window decorations for Xfce's window manager, xfwm4 —
originally created by lordwolfchild, updated in this fork for current
Xfce (tested with xfwm4 4.20 / Xfce 4.20).

Two styles are included, AmigaOS 1.3 and AmigaOS 3.x, each in three sizes:

| Theme                                | Scale | Use for                                    |
| ------------------------------------ | ----- | ------------------------------------------ |
| `Amiga1.3` / `Amiga3.x`              | 1×    | Standard displays (96 DPI, scale factor 1) |
| `Amiga1.3_hidpi` / `Amiga3.x_hidpi`  | 1.5×  | Larger decorations, e.g. 144 DPI setups    |
| `Amiga1.3_xhdpi` / `Amiga3.x_xhdpi`  | 2×    | HiDPI displays (scale factor 2 / 200%)     |

## Installation

Copy the theme folders into `~/.themes` (or `~/.local/share/themes`), then
open **Settings → Window Manager** and select the theme on the *Style* tab.

### HiDPI

xfwm4 does not scale custom themes automatically — only its built-in
`Default` theme is swapped for `Default-hdpi` on HiDPI screens. The title
font *is* scaled, so with the 1× themes the title text gets clipped at
scale factor 2. Select the `_xhdpi` (2×) variant manually to match a 200%
display scale, or `_hidpi` (1.5×) for in-between setups.

### Button layout

The themes set the Amiga gadget layout (`C|MH`: close on the left,
minimize and maximize/depth on the right) in `themerc`. This overrides the
button layout configured in the settings dialog — that is intentional.

## Matching the rest of the desktop

* GTK theme: the Amiga3.x GTK2 theme by untouchable89 pairs well with the
  3.x decorations: <https://www.xfce-look.org/p/127251/>
  Note that current Xfce is GTK3-based, so a GTK2 theme only styles GTK2
  applications; GTK3 apps keep their default look.
* Mouse pointers: Amiga Classic Red by xBreeze:
  <https://www.xfce-look.org/p/128152/>
* Title font: the one and only Topaz font:
  <https://github.com/rewtnull/amigafonts>
  Pick it as the title font in **Settings → Window Manager → Style**.

## Regenerating the scaled variants

`scripts/make_xhdpi.py` rebuilds the 2× `_xhdpi` themes from the base
themes: every XPM pixel is replicated into a 2×2 block (no interpolation,
so the pixel art stays crisp) and the pixel offsets in `themerc` are
doubled:

    python3 scripts/make_xhdpi.py .

`scripts/mom.sh` is the historical ImageMagick helper used for the 1.5×
`_hidpi` variants, kept for reference.
