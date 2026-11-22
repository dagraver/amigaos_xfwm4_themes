#!/bin/sh
# Historical helper used when the _hidpi themes were created: resizes every
# XPM in the current directory to 75% (ImageMagick). Kept for reference;
# use scripts/make_xhdpi.py to (re)generate the scaled theme variants.
#
# ImageMagick 7 renamed "convert" to "magick"; fall back for IM6.
if command -v magick >/dev/null 2>&1; then
    IM=magick
else
    IM=convert
fi

for f in *.xpm; do
    "$IM" "$f" -resize 75% "$f"
done
