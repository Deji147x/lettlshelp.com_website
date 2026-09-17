#!/usr/bin/env python3
"""Prepare web assets from the owner's source folders.

    python tools/process_assets.py

Reads logos and sample photos from ~/Downloads, writes to wireframes/<site>/assets/:
  logo.png, logo-mark.png        transparent crops of the official JPEG logos
  favicon.ico/-16/-32, apple-touch-icon.png, icon-192/-512.png
  og-image.jpg                   1200x630 social sharing image
  img/<name>-1600.jpg, -800.jpg  resized, EXIF-stripped photos + manifest.json
Also copies the original logo and palette files into brand/<site>/ for reference.
"""
import json
import shutil
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"
PHOTOS = DL / "Imagery for Websites" / "Imagery for Websites"
LOGOS = DL / "Logos" / "Logos"
PALETTES = DL / "Color Pallets" / "Color Pallets"

# Photos excluded on purpose (see docs/consistency-review.md): unknown source/licence
# (134f…, 7512…, 978b…, Board-768x509), visible distress (a-darmel-6643024,
# liza-summer-6382681), and children rather than young adults (cottonbro-*).
SITES = {
    "life-solutions": {
        "logo": "Transformative Life Solutions Logo_2026.jpeg",
        "palette": "Transformative Life Solutions Color Palette 2026.jpg",
        "og_bg": (244, 247, 248),
        "photos": {
            "hero-facilitated-conversation": "pexels-shkrabaanthony-7579320.jpg",
            "mediation-session": "pexels-rdne-9064741.jpg",
            "calm-conversation": "pexels-divinetechygirl-1181717.jpg",
            "supportive-talk": "pexels-divinetechygirl-1181505.jpg",
            "young-adults-group": "pexels-divinetechygirl-1181626.jpg",
            "couple-reviewing-agreement": "pexels-ron-lach-9870138.jpg",
            "elders-community": "pexels-priscilla-cezar-2157245929-36883131.jpg",
            "group-review": "pexels-mikhail-nilov-8730966.jpg",
        },
    },
    "leadership-systems": {
        "logo": "Transformative Leadership Systems Logo_2026.jpeg",
        "palette": "Transformative Leadership Systems Color Palette 2026.jpg",
        "og_bg": (248, 248, 248),
        "photos": {
            "hero-women-led-meeting": "pexels-divinetechygirl-1181418.jpg",
            "leader-dialogue": "pexels-divinetechygirl-1181426.jpg",
            "conference-room-team": "pexels-divinetechygirl-1181396.jpg",
            "facilitated-negotiation": "pexels-karola-g-7875947.jpg",
            "leaders-in-conversation": "pexels-tima-miroshnichenko-5717504.jpg",
            "small-group-panel": "pexels-prolificpeople-31968534.jpg",
            "business-meeting": "pexels-a-darmel-8133997.jpg",
            "signing-agreement": "pexels-energepic-com-27411-175045.jpg",
        },
    },
}


def knockout(img, tol=14, soft=40):
    """Make the logo's off-white background transparent, keeping soft edges.

    The background isn't flat (the Leadership file has a faint gradient), so it is
    estimated per row by interpolating between the left and right edge colours.
    """
    img = img.convert("RGB")
    w, h = img.size
    src = img.load()

    def edge(y, xs):
        px = [src[x, y] for x in xs]
        return [sum(p[i] for p in px) / len(px) for i in range(3)]

    out = Image.new("RGBA", img.size)
    dst = out.load()
    for y in range(h):
        left, right = edge(y, range(1, 6)), edge(y, range(w - 6, w - 1))
        for x in range(w):
            t = x / (w - 1)
            bg = [left[i] + (right[i] - left[i]) * t for i in range(3)]
            r, g, b = src[x, y]
            d = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
            dst[x, y] = (r, g, b, 0 if d <= tol else min(255, int((d - tol) * 255 / soft)))
    return out


def bands(rgba, min_alpha=80, min_height=8):
    """Vertical runs of rows containing logo pixels: [mark, wordmark line 1, line 2, ...]."""
    alpha = rgba.getchannel("A").load()
    w, h = rgba.size
    rows = [any(alpha[x, y] > min_alpha for x in range(w)) for y in range(h)]
    runs, start = [], None
    for y, on in enumerate(rows + [False]):
        if on and start is None:
            start = y
        elif not on and start is not None:
            if y - start >= min_height:
                runs.append((start, y))
            start = None
    return runs


def solid_bbox(rgba, box, min_alpha=80):
    mask = rgba.getchannel("A").point(lambda v: 255 if v > min_alpha else 0)
    x0, y0, x1, y1 = mask.crop(box).getbbox()
    return (box[0] + x0, box[1] + y0, box[0] + x1, box[1] + y1)


def square(img, pad=0.1):
    side = int(max(img.size) * (1 + pad))
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2), img)
    return canvas


def on_color(img, color):
    bg = Image.new("RGBA", img.size, color + (255,))
    bg.alpha_composite(img)
    return bg.convert("RGB")


def save_png(img, path, colors=128):
    """Flat brand art (logo, icons) compresses far smaller as a palette PNG, with alpha kept."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.quantize(colors=colors, method=Image.FASTOCTREE).save(path, optimize=True)


def build_site(slug, cfg):
    out = ROOT / "wireframes" / slug / "assets"
    (out / "img").mkdir(parents=True, exist_ok=True)
    brand = ROOT / "brand" / slug
    brand.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LOGOS / cfg["logo"], brand / ("logo-original" + Path(cfg["logo"]).suffix.lower()))
    shutil.copy2(PALETTES / cfg["palette"], brand / "color-palette.jpg")

    logo = knockout(Image.open(LOGOS / cfg["logo"]))
    runs = bands(logo)
    w = logo.width
    mark_box = solid_bbox(logo, (0, runs[0][0], w, runs[0][1]))
    full_box = solid_bbox(logo, (0, runs[0][0], w, runs[-1][1]))
    mark = logo.crop(mark_box)
    full = logo.crop(full_box)
    print(f"{slug}: bands={runs} mark={mark_box} full={full_box}")

    save_png(full, out / "logo.png", colors=192)
    icon = square(mark, pad=0.08)
    save_png(icon.resize((96, 96), Image.LANCZOS), out / "logo-mark.png")
    for size in (16, 32):
        save_png(icon.resize((size, size), Image.LANCZOS), out / f"favicon-{size}.png", colors=64)
    icon.resize((256, 256), Image.LANCZOS).save(out / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    for size in (192, 512):
        save_png(icon.resize((size, size), Image.LANCZOS), out / f"icon-{size}.png")
    # iOS renders transparency as black, so the touch icon gets a white tile
    on_color(square(mark, pad=0.3).resize((180, 180), Image.LANCZOS), (255, 255, 255)).save(out / "apple-touch-icon.png")

    og = Image.new("RGBA", (1200, 630), cfg["og_bg"] + (255,))
    scale = 440 / full.height
    logo_og = full.resize((int(full.width * scale), 440), Image.LANCZOS)
    og.alpha_composite(logo_og, ((1200 - logo_og.width) // 2, (630 - logo_og.height) // 2))
    og.convert("RGB").save(out / "og-image.jpg", quality=82, optimize=True, progressive=True)

    manifest = {"_logo": list(full.size)}
    for name, filename in cfg["photos"].items():
        photo = ImageOps.exif_transpose(Image.open(PHOTOS / filename)).convert("RGB")
        manifest[name] = {}
        for bound in (1600, 800):
            copy = photo.copy()
            copy.thumbnail((bound, bound), Image.LANCZOS)
            # AVIF first (smallest, Safari 16+/Chrome/Firefox/Edge), WebP next, JPEG as the fallback.
            copy.save(out / "img" / f"{name}-{bound}.avif", quality=52, speed=4)
            copy.save(out / "img" / f"{name}-{bound}.webp", quality=72, method=6)
            copy.save(out / "img" / f"{name}-{bound}.jpg", quality=74, optimize=True, progressive=True)
            manifest[name][str(bound)] = list(copy.size)
        print(f"  {name}: {manifest[name]}")
    (out / "img" / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    for site_slug, site_cfg in SITES.items():
        build_site(site_slug, site_cfg)
