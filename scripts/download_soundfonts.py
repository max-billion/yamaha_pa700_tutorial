#!/usr/bin/env python3
"""
Optional helper to download the four free SoundFont libraries locally into ./soundfonts/
for offline development or self-hosting (note: browser static mode streams directly from
CORS-enabled CDNs + IndexedDB without needing local files, except FreePats GM).

Libraries:
  1. GeneralUser GS      (.sf3 compact 8 MB & .sf2 full 30.8 MB) - Permissive license
  2. FluidR3 GM          (.sf3 22.6 MB & .sf2 141.5 MB)          - MIT license
  3. MuseScore General   (MS Basic.sf3 48.9 MB)                  - MIT license
  4. FreePats GM         (FreePatsGM .sf2 + Percussion .sf2)     - CC0 / GPLv3+font exception
"""

import argparse
import os
import shutil
import subprocess
import urllib.request

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF_DIR = os.path.join(ROOT_DIR, "soundfonts")

LIBRARIES = {
    "generaluser-sf3": {
        "dest": "generaluser/GeneralUserGS.sf3",
        "url": "https://raw.githubusercontent.com/spessasus/SpessaSynth/master/soundfonts/GeneralUserGS.sf3",
        "size": "8.0 MB",
    },
    "generaluser-sf2": {
        "dest": "generaluser/GeneralUser-GS.sf2",
        "url": "https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2",
        "size": "30.8 MB",
    },
    "fluidr3-sf3": {
        "dest": "fluidr3/FluidR3Mono_GM.sf3",
        "url": "https://raw.githubusercontent.com/musescore/MuseScore/main/share/sound/FluidR3Mono_GM.sf3",
        "size": "22.6 MB",
    },
    "fluidr3-sf2": {
        "dest": "fluidr3/FluidR3_GM.sf2",
        "url": "https://github.com/pianobooster/fluid-soundfont/releases/download/v3.1/FluidR3_GM.sf2",
        "size": "141.5 MB",
    },
    "musescore": {
        "dest": "musescore/MS_Basic.sf3",
        "url": "https://raw.githubusercontent.com/musescore/MuseScore/main/share/sound/MS%20Basic.sf3",
        "size": "48.9 MB",
    },
    "freepats-perc": {
        "dest": "freepats/FreePatsGM-Percussion-SF2-20200822.tar.xz",
        "url": "https://freepats.zenvoid.org/SoundSets/GM-PercussionSet/FreePatsGM-Percussion-SF2-20200822.tar.xz",
        "size": "15 MB",
        "extract": "tar",
    },
    "freepats-melodic": {
        "dest": "freepats/FreePatsGM-SF2-20221026.7z",
        "url": "https://freepats.zenvoid.org/SoundSets/FreePats-GeneralMIDI/FreePatsGM-SF2-20221026.7z",
        "size": "227 MB",
        "extract": "7z",
    },
}


def download_file(url: str, dest_path: str):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path):
        print(f"[skip] Already exists: {dest_path}")
        return
    print(f"[download] {url} -> {dest_path}")
    req = urllib.request.Request(url, headers={"User-Agent": "KorgPa700Trainer/1.0"})
    with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as out:
        shutil.copyfileobj(resp, out)


def extract_archive(path: str, kind: str):
    out_dir = os.path.dirname(path)
    if kind == "tar":
        print(f"[extract] tar -xf {path}")
        subprocess.run(["tar", "-xf", path, "-C", out_dir], check=True)
    elif kind == "7z":
        exe = shutil.which("7z") or shutil.which("7zz")
        if not exe:
            print(f"[warn] 7z binary not installed; extract manually: {path}")
            return
        print(f"[extract] {exe} x {path}")
        subprocess.run([exe, "x", "-y", f"-o{out_dir}", path], check=True)


def main():
    parser = argparse.ArgumentParser(description="Download open-source GM/GS SoundFonts for local use.")
    parser.add_argument(
        "--libs",
        nargs="+",
        choices=list(LIBRARIES.keys()) + ["compact", "all"],
        default=["compact"],
        help="Which SoundFonts to fetch (default: compact = generaluser-sf3 + fluidr3-sf3 + freepats-perc).",
    )
    args = parser.parse_args()

    selected = []
    if "compact" in args.libs:
        selected.extend(["generaluser-sf3", "fluidr3-sf3"])
    elif "all" in args.libs:
        selected.extend(LIBRARIES.keys())
    else:
        selected = args.libs

    for key in dict.fromkeys(selected):
        spec = LIBRARIES[key]
        dest_path = os.path.join(SF_DIR, spec["dest"])
        download_file(spec["url"], dest_path)
        if "extract" in spec:
            extract_archive(dest_path, spec["extract"])

    print("Done. Start a static server (`python3 -m http.server`) to test local SoundFonts.")


if __name__ == "__main__":
    main()
