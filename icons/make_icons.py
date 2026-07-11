#!/usr/bin/env python3
"""
make_icons.py — turn the Nyxite logo into a full-bleed, square app icon and
export every size the four Nyxite surfaces need (web/PWA, Android, desktop,
GitHub).

The white background and purple glow are removed, then the slab is cropped to
the largest solid square so the artwork fills the whole frame with NO
transparent space. All outputs are opaque.

Usage:
    python make_icons.py SOURCE.png [-o OUTDIR] [--dark 90]

Dependencies:  pip install Pillow numpy scipy scikit-image
"""
import argparse, os, json
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.morphology import convex_hull_image


def slab_mask(rgb, dark_l=90.0):
    """Boolean mask of the tile slab. Found from its dark stone body (the glow
    is always brighter and lies outside the slab); the convex hull gives a
    clean boundary the glow cannot cross."""
    lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    dark = ndimage.binary_opening(lum < dark_l, iterations=2)
    lbl, n = ndimage.label(dark)
    sizes = ndimage.sum(np.ones_like(lbl), lbl, range(1, n + 1))
    dark = lbl == int(np.argmax(sizes)) + 1
    return convex_hull_image(dark)


def fullbleed_master(path, dark_l=90.0, size=1024):
    """Opaque RGB square that the slab fills edge to edge (no transparency)."""
    rgb = np.asarray(Image.open(path).convert("RGB"))
    mask = slab_mask(rgb.astype(np.float32), dark_l)

    ys, xs = np.where(mask)
    cy, cx = int(round(ys.mean())), int(round(xs.mean()))
    integ = np.zeros((mask.shape[0] + 1, mask.shape[1] + 1), np.int64)
    integ[1:, 1:] = np.cumsum(np.cumsum(mask.astype(np.int64), 0), 1)

    def solid(x0, y0, x1, y1):
        s = integ[y1, x1] - integ[y0, x1] - integ[y1, x0] + integ[y0, x0]
        return s == (x1 - x0) * (y1 - y0)

    lo, hi = 0, min(cx, cy, mask.shape[1] - cx, mask.shape[0] - cy)
    while lo < hi:                                   # largest centered solid square
        m = (lo + hi + 1) // 2
        if solid(cx - m, cy - m, cx + m, cy + m):
            lo = m
        else:
            hi = m - 1
    crop = Image.fromarray(rgb[cy - lo:cy + lo, cx - lo:cx + lo])
    return crop.resize((size, size), Image.LANCZOS).convert("RGB")


def main():
    ap = argparse.ArgumentParser(description="Make full-bleed Nyxite app icons.")
    ap.add_argument("source")
    ap.add_argument("-o", "--out", default="icons")
    ap.add_argument("--dark", type=float, default=90.0,
                    help="luminance cutoff for the slab body (lower = stricter)")
    ap.add_argument("--inset", type=int, default=0,
                    help="trim N px off every edge (in 1024 master space) then "
                         "re-square; clears thin bevel/shadow strips")
    args = ap.parse_args()

    out = args.out
    for d in ("master", "web", "android", "android/mipmap-mdpi",
              "android/mipmap-hdpi", "android/mipmap-xhdpi",
              "android/mipmap-xxhdpi", "android/mipmap-xxxhdpi",
              "desktop", "desktop/linux", "github"):
        os.makedirs(os.path.join(out, d), exist_ok=True)

    master = fullbleed_master(args.source, args.dark)
    if args.inset:
        w, h = master.size
        n = args.inset
        master = master.crop((n, n, w - n, h - n)).resize((w, h), Image.LANCZOS)
    master.save(os.path.join(out, "master", "nyxite-icon.png"))

    saved = []
    def res(size):  # high-quality opaque resize from the master
        return master.resize((size, size), Image.LANCZOS)
    def save(size, *parts):
        p = os.path.join(out, *parts)
        res(size).save(p)
        saved.append(os.path.relpath(p, out))

    # WEB / PWA -- full bleed, opaque (valid for "any" and "maskable")
    for s in (16, 32, 48):
        save(s, "web", f"favicon-{s}x{s}.png")
    res(256).save(os.path.join(out, "web", "favicon.ico"),
                  sizes=[(16, 16), (32, 32), (48, 48)])
    saved.append("web/favicon.ico")
    save(192, "web", "icon-192.png")
    save(512, "web", "icon-512.png")
    save(180, "web", "apple-touch-icon.png")
    save(192, "web", "maskable-192.png")
    save(512, "web", "maskable-512.png")
    with open(os.path.join(out, "web", "manifest-icons.json"), "w") as f:
        json.dump({"icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png",
             "purpose": "any maskable"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "any maskable"},
        ]}, f, indent=2)
    saved.append("web/manifest-icons.json")

    # ANDROID
    for dens, s in (("mdpi", 48), ("hdpi", 72), ("xhdpi", 96),
                    ("xxhdpi", 144), ("xxxhdpi", 192)):
        save(s, "android", f"mipmap-{dens}", "ic_launcher.png")
    save(432, "android", "ic_launcher_foreground.png")   # adaptive, full bleed
    save(512, "android", "ic_launcher-playstore.png")

    # DESKTOP
    res(256).save(os.path.join(out, "desktop", "nyxite.ico"),
                  sizes=[(16, 16), (32, 32), (48, 48), (64, 64),
                         (128, 128), (256, 256)])
    saved.append("desktop/nyxite.ico")
    for s in (16, 24, 32, 48, 64, 128, 256, 512):
        save(s, "desktop", "linux", f"nyxite-{s}.png")

    # GITHUB
    save(512, "github", "org-avatar-512.png")

    print(f"Wrote {len(saved) + 1} files to {out}/ (full-bleed, opaque)\n")
    for s in sorted(saved):
        print("  ", s)


if __name__ == "__main__":
    main()
