#!/usr/bin/env python3
"""
Builds self-contained pa700_standalone.html by inlining CSS assets (base64 PNGs),
styles.css, pa700_data.js, pa700_audio.js, and app.js into index.html.
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def inline_css_assets(css_text: str) -> str:
    pattern = re.compile(r'url\((["\']?)(assets/[^"\')]+)\1\)')

    def repl(match: re.Match) -> str:
        rel_path = match.group(2)
        asset_file = ROOT / rel_path
        if not asset_file.exists():
            raise FileNotFoundError(f"Missing CSS asset: {asset_file}")
        ext = asset_file.suffix.lower().lstrip(".")
        mime = "image/png" if ext == "png" else f"image/{ext}"
        b64 = base64.b64encode(asset_file.read_bytes()).decode("ascii")
        return f'url("data:{mime};base64,{b64}")'

    return pattern.sub(repl, css_text)


def safe_inline_script(js_text: str) -> str:
    return js_text.replace("</script>", "<\\/script>")


def build() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = inline_css_assets((ROOT / "styles.css").read_text(encoding="utf-8"))
    data_js = safe_inline_script((ROOT / "pa700_data.js").read_text(encoding="utf-8"))
    audio_js = safe_inline_script((ROOT / "pa700_audio.js").read_text(encoding="utf-8"))
    app_js = safe_inline_script((ROOT / "app.js").read_text(encoding="utf-8"))

    # Replace stylesheet link
    html = html.replace(
        '<link rel="stylesheet" href="styles.css" />',
        f"<style>\n{css}\n  </style>",
        1,
    )

    # Remove relative ES module script in single-file mode so file:// stays clean
    html = html.replace(
        '<script type="module" src="./vendor/spessasynth/spessasynth_bridge.js"></script>\n',
        '<script>window.PA700_STANDALONE = true;</script>\n',
        1,
    )

    # Inline script files
    html = html.replace('<script src="pa700_data.js"></script>', f"<script>\n{data_js}\n  </script>", 1)
    html = html.replace('<script src="pa700_audio.js"></script>', f"<script>\n{audio_js}\n  </script>", 1)
    html = html.replace('<script src="app.js"></script>', f"<script>\n{app_js}\n  </script>", 1)

    out_path = ROOT / "pa700_standalone.html"
    out_path.write_text(html, encoding="utf-8")
    kb = out_path.stat().st_size / 1024.0
    print(f"Wrote {out_path} ({kb:.1f} KB)")


if __name__ == "__main__":
    build()
