#!/usr/bin/env python3
"""
Extract all Factory Musical Resources from Pa700_User_Manual_v15_E.pdf (Appendix pages 954-1028)
and generate a comprehensive, musically enriched pa700_data.js for the Korg Pa700 Trainer.

Parsed manual totals (verified against Pa700 User Manual v1.5 E):
  - Styles:        379 across 12 Categories
  - Keyboard Sets: 298 across 9 Library Categories
  - Sounds:      1,727 melodic Sounds across Factory / Legacy / GM-XG (45 sub-groups)
  - Drum Kits:     118 Drum & SFX Kits across Factory / Legacy / GM-XG (total 1,845 Sound entries)
  - DNC Sounds:    All DNC / DN1 / DN2 control mappings (Legato, SC1, SC2, Y+, Y-, AfterTouch)
  - Factory Pads:  415 across 20 Groups (10 HIT banks = 193 Hits + 10 SEQ banks = 222 Sequences)
"""

import json
import os
import re
import subprocess
import sys
import zlib
from collections import OrderedDict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from style_catalog_379 import get_style_blueprint, STYLE_BLUEPRINTS_379
from style_midi_composer import compile_style_from_blueprint, midi_pattern_fingerprint

ROOT_DIR = os.path.dirname(SCRIPT_DIR)
PDF_PATH = os.path.join(ROOT_DIR, "Pa700_User_Manual_v15_E.pdf")
OUTPUT_JS = os.path.join(ROOT_DIR, "pa700_data.js")

ROW_RE = re.compile(r"^(.+?)\s+(\d+)\s+(\d+(?:-\d+)?)\s+(\d+(?:-\d+)?)$")
PAD_RE = re.compile(r"^(\d+)\s+(.+)$")
HEADER_PAGE_RE = re.compile(r"(^\d+\|\s*Appendix$|^Musical Resources\s*\|\d+$)")

# Stable slug ID aliases referenced by Set List entries, Drills, and default boot state.
STYLE_ALIASES = {
    "Standard 8 Beat": "8beat_standard",
    "Capital Soul": "16beat_soul",
    "Classic Rock": "classic_rock",
    "Big Band Swing": "big_band_swing",
    "Brush Ballad": "brush_ballad",
    "Bossa Nova": "bossa_nova",
    "70’s Disco": "disco_fever",
    "French Waltz": "french_waltz",
}

STYLE_CATEGORY_LIST = [
    "Pop", "Ballad", "Ballroom", "Dance", "Rock", "Country",
    "Latin", "Latin Dance", "Jazz", "Movie & Show", "Funk & Blues", "World",
]

KBD_LIBRARY_CATEGORIES = [
    {"id": "piano", "buttonNumber": 1, "label": "Piano & EP", "manualName": "Piano & EP", "icon": "Pn"},
    {"id": "organ", "buttonNumber": 2, "label": "Organ", "manualName": "Organ", "icon": "Org"},
    {"id": "guitar", "buttonNumber": 3, "label": "Guitar", "manualName": "Guitar", "icon": "Gtr"},
    {"id": "strings", "buttonNumber": 4, "label": "Strings", "manualName": "Strings", "icon": "Str"},
    {"id": "brass", "buttonNumber": 5, "label": "Brass", "manualName": "Brass", "icon": "Brs"},
    {"id": "trumpet", "buttonNumber": 6, "label": "Trumpet", "manualName": "Trumpet", "icon": "Tpt"},
    {"id": "sax", "buttonNumber": 7, "label": "Sax & W.Wind", "manualName": "Sax & Woodwinds", "icon": "Sax"},
    {"id": "synth", "buttonNumber": 8, "label": "Synth", "manualName": "Synth", "icon": "Syn"},
    {"id": "ethnic", "buttonNumber": 9, "label": "Ethnic", "manualName": "Ethnic", "icon": "Eth"},
]
KBD_CAT_BY_MANUAL = {c["manualName"]: c["id"] for c in KBD_LIBRARY_CATEGORIES}


def slugify(text: str) -> str:
    s = text.lower().replace("’", "'").replace("–", "-")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "item"


def unique_slug(base: str, used: set) -> str:
    candidate = base
    n = 2
    while candidate in used:
        candidate = f"{base}_{n}"
        n += 1
    used.add(candidate)
    return candidate


def stable_hash(text: str) -> int:
    return zlib.crc32(text.encode("utf-8")) & 0xFFFFFFFF


def run_pdftotext() -> str:
    cmd = ["pdftotext", "-layout", "-f", "954", "-l", "1028", PDF_PATH, "-"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return res.stdout


def split_page_columns(page_text: str, header_token: str, min_cols: int = 2) -> list:
    lines = page_text.splitlines()
    hdr_idx = None
    starts = None
    for idx, line in enumerate(lines):
        if header_token == "#":
            matches = [m.start() for m in re.finditer(r"#\s+Pad\b", line)]
        else:
            matches = [m.start() for m in re.finditer(rf"\b{re.escape(header_token)}\b", line)]
        if len(matches) >= min_cols:
            hdr_idx = idx
            starts = matches
            break
    if hdr_idx is None:
        return []
    cuts = [0] + [max(0, pos - 1) for pos in starts[1:]] + [None]
    cols = [[] for _ in starts]
    for line in lines[hdr_idx + 1:]:
        if not line.strip():
            continue
        for c_idx in range(len(starts)):
            chunk = line[cuts[c_idx]:cuts[c_idx + 1]] if cuts[c_idx + 1] is not None else line[cuts[c_idx]:]
            chunk = chunk.strip()
            if chunk:
                cols[c_idx].append(chunk)
    return [item for col in cols for item in col]


# ---------------------------------------------------------------------------
# DNC Controls Parser (Appendix pages idx 38..40)
# ---------------------------------------------------------------------------
def parse_dnc_controls(pages: list) -> dict:
    """Parse DNC, DN1, and DN2 expression controls from Appendix pages 38-40."""
    entries = {}
    row_start_re = re.compile(r"^(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s*(.*)$")
    for p_idx in range(38, 41):
        lines = pages[p_idx].splitlines()
        subhdr_idx = None
        col_bounds = {}
        for idx, line in enumerate(lines):
            if "Sound Name" in line and "Legato" in line:
                # Next lines contain '00 32 In Out Note On Note Off ...' and Y+/Y-/AfterTouch
                subhdr_idx = idx
                hdr1 = line
                hdr2 = lines[idx + 2] if idx + 2 < len(lines) and "Note On" in lines[idx + 2] else (
                    lines[idx + 1] if idx + 1 < len(lines) and "Note On" in lines[idx + 1] else ""
                )
                in_pos = hdr2.find("In")
                out_pos = hdr2.find("Out")
                no1 = hdr2.find("Note On")
                noff1 = hdr2.find("Note Off")
                no2 = hdr2.find("Note On", no1 + 1) if no1 >= 0 else -1
                noff2 = hdr2.find("Note Off", noff1 + 1) if noff1 >= 0 else -1
                yp = hdr1.find("Y+")
                ym = hdr1.find("Y") if "Y–" in hdr1 else hdr1.find("Y-")
                if "Y–" in hdr1:
                    ym = hdr1.find("Y–")
                at = hdr1.find("After")
                raw_cols = [
                    ("legatoIn", in_pos),
                    ("legatoOut", out_pos),
                    ("sc1On", no1),
                    ("sc1Off", noff1),
                    ("sc2On", no2),
                    ("sc2Off", noff2),
                    ("yPlus", yp),
                    ("yMinus", ym),
                    ("afterTouch", at),
                ]
                valid = [
                    (k, max(0, v - (4 if k in ("sc1Off", "sc2Off", "yPlus", "yMinus", "afterTouch") else 3)))
                    for k, v in raw_cols if v >= 0
                ]
                col_bounds = {}
                for k_i, (k_name, start_pos) in enumerate(valid):
                    end_pos = valid[k_i + 1][1] if k_i + 1 < len(valid) else None
                    col_bounds[k_name] = (start_pos, end_pos)
                subhdr_idx = idx + (3 if hdr2 and lines[idx + 2] == hdr2 else 2)
                break
        if subhdr_idx is None:
            continue

        cur_entry = None
        for line in lines[subhdr_idx:]:
            s = line.strip()
            if not s or s.startswith("Factory/") or s.startswith("The following table") or s.startswith("DNC Control"):
                if s.startswith("The following table") or s.startswith("SC1 Note On"):
                    break
                continue
            m = row_start_re.match(line)
            if m and not s.startswith(">") and not s.startswith("<"):
                name = m.group(1).strip()
                cc00, cc32, pc = int(m.group(2)), int(m.group(3)), int(m.group(4))
                cur_entry = {
                    "name": name,
                    "cc00": cc00,
                    "cc32": cc32,
                    "pc": pc,
                    "legatoIn": "",
                    "legatoOut": "",
                    "sc1On": "",
                    "sc1Off": "",
                    "sc2On": "",
                    "sc2Off": "",
                    "yPlus": "",
                    "yMinus": "",
                    "afterTouch": "",
                }
                for field, (a, b) in col_bounds.items():
                    # Adjust cut boundaries to nearest whitespace so multi-word tokens never split mid-word
                    sa = a
                    while 0 < sa < len(line) and line[sa - 1] != " " and line[sa] != " ":
                        sa -= 1
                    sb = b
                    if sb is not None and sb < len(line):
                        while sb > sa and line[sb - 1] != " " and line[sb] != " ":
                            sb -= 1
                    part = line[sa:sb].strip() if sb is not None else line[sa:].strip()
                    cur_entry[field] = part
                entries[(cc00, cc32, pc)] = cur_entry
            elif cur_entry is not None:
                # Multi-line wrapped name suffix (e.g. HardTrombone / DN1) or wrapped cell
                left_name = line[:32].strip()
                if left_name in ("DN1", "DN2", "DNC") and not cur_entry["name"].endswith(left_name):
                    cur_entry["name"] = f"{cur_entry['name']} {left_name}".strip()
                for field, (a, b) in col_bounds.items():
                    part = line[a:b].strip() if b is not None else line[a:].strip()
                    if part:
                        cur_entry[field] = f"{cur_entry[field]} {part}".strip()
    return entries


# ---------------------------------------------------------------------------
# Sounds & Drum Kits Parser (idx 11..37, 41..42)
# ---------------------------------------------------------------------------
SOUND_NAME_CAT_MAP = {
    "Piano": "Piano",
    "E. piano": "E. Piano",
    "E. Piano": "E. Piano",
    "Mallet & Bell": "Mallet & Bell",
    "Accordion": "Accordion",
    "Organ": "Organ",
    "Guitar": "Guitar",
    "Strings & Vocal": "Strings & Vocal",
    "Trumpet & Trbn.": "Trumpet & Trbn.",
    "Brass": "Brass",
    "Sax": "Sax",
    "Woodwind": "Woodwind",
    "Synth Pad": "Synth Pad",
    "Synth Lead": "Synth Lead",
    "Ethnic": "Ethnic",
    "Bass": "Bass",
    "Chrom. Perc.": "Mallet & Bell",
    "Strings": "Strings & Vocal",
    "Ensemble": "Strings & Vocal",
    "Reed": "Sax",
    "Pipe": "Woodwind",
    "Syn Lead": "Synth Lead",
    "Syn Pad": "Synth Pad",
    "Synth SFX": "SFX",
    "Percussive": "Drum & SFX",
    "SFX": "SFX",
    "Drum & SFX": "Drum & SFX",
    "Drum": "Drum & SFX",
}


def compute_sound_profile(name: str, category: str, is_drum: bool, pc: int, cc32: int) -> dict:
    """Derive realistic audio synthesis & DSP sculpting metadata for each manual Sound."""
    n = name.lower()
    brightness = 1.0
    detune = 4.0 + (cc32 % 5) * 1.4
    attack_scale = 1.0
    release_scale = 1.0
    chorus_mix = 0.08
    vibrato = 0.0
    overdrive = 0.0
    rotary = False

    if "bright" in n or "brilli" in n or "rock" in n or "honky" in n or "pick" in n or "slap" in n or "punch" in n:
        brightness = 1.28
        detune += 3.0
    elif "warm" in n or "mellow" in n or "dark" in n or "soft" in n or "velvet" in n or "ballad" in n or "nylon" in n:
        brightness = 0.78
        release_scale *= 1.15
    if "slow" in n or "pad" in n or "sweep" in n or "swell" in n or "choir" in n or "bow" in n or "legato" in n:
        attack_scale = 1.65
        release_scale = 1.35
    if "stacc" in n or "pizz" in n or "mute" in n or "pluck" in n or "spicc" in n:
        release_scale = 0.48
        attack_scale = 0.6
    if "chorus" in n or "detune" in n or "ensemble" in n or "ens." in n or "12str" in n or "12-str" in n or "stereo" in n or "super" in n or "unison" in n:
        chorus_mix = 0.28
        detune += 7.5
    if "rotary" in n or "bx3" in n or "cx3" in n or "b3" in n or "drawbar" in n or "hammond" in n or "gospel" in n or "leslie" in n or "perc.org" in n:
        rotary = True
        chorus_mix = 0.24
    if "overdrive" in n or "dist" in n or "fuzz" in n or "crunch" in n or "drive" in n or "metal" in n or "power" in n:
        overdrive = 0.42 if "overdrive" in n or "crunch" in n else 0.65
        brightness = 1.25
    if "vib" in n or "tremolo" in n or "mandolin" in n or "musette" in n or "accordion" in n or "dnc" in n or "dn1" in n or "dn2" in n:
        vibrato = 0.16 if "tremolo" in n or "mandolin" in n else 0.08
    if "dyno" in n or "bell" in n or "tine" in n or "crystal" in n or "celesta" in n or "glock" in n or "chime" in n:
        brightness = max(brightness, 1.32)

    return {
        "gmProgram": pc if not is_drum else 0,
        "brightness": round(brightness, 2),
        "detuneCents": round(detune, 1),
        "attackScale": round(attack_scale, 2),
        "releaseScale": round(release_scale, 2),
        "chorusMix": round(chorus_mix, 2),
        "vibrato": round(vibrato, 2),
        "overdrive": round(overdrive, 2),
        "rotary": rotary,
    }


def refine_gm_program(name: str, pc: int, is_drum: bool) -> int:
    """Korg Pa700 PC aligns directly with GM Program 0..127 for nearly all melodic Sounds;
    ensure out-of-range or ambiguous names stay valid 0..127."""
    if is_drum:
        return 0
    if 0 <= pc <= 127:
        return pc
    return 0


def parse_sounds_and_drums(pages: list, dnc_map: dict) -> tuple:
    used_ids = set()
    sounds = []
    # Melodic Sounds idx 11..37
    cur_type = "Factory"
    cur_group = "Piano"
    for p_idx in range(11, 38):
        for token in split_page_columns(pages[p_idx], "Sound", min_cols=2):
            m = ROW_RE.match(token)
            if m:
                if "-" in m.group(3) or "-" in m.group(4):
                    continue
                name = m.group(1).strip()
                cc00, cc32, pc = int(m.group(2)), int(m.group(3)), int(m.group(4))
                group_name = cur_group
                if cur_type == "GM/XG" and cur_group == "Syn Lead Syn Pad":
                    group_name = "Syn Lead" if pc <= 87 else "Syn Pad"
                canon_cat = SOUND_NAME_CAT_MAP.get(group_name, group_name)
                if group_name == "E. piano":
                    group_name = "E. Piano"
                dnc = dnc_map.get((cc00, cc32, pc))
                sid = unique_slug(slugify(f"{cur_type}_{name}_{cc32}_{pc}"), used_ids)
                sounds.append({
                    "id": sid,
                    "name": name,
                    "type": cur_type,
                    "group": group_name,
                    "category": canon_cat,
                    "isDrum": False,
                    "cc00": cc00,
                    "cc32": cc32,
                    "pc": pc,
                    "gmProgram": refine_gm_program(name, pc, False),
                    "dnc": dnc,
                    "profile": compute_sound_profile(name, canon_cat, False, pc, cc32),
                })
            else:
                if token in ("Legacy", "GM/XG", "Factory"):
                    cur_type = token
                elif "/" in token:
                    t_part, g_part = token.rsplit("/", 1)
                    cur_type = t_part.strip()
                    cur_group = g_part.strip()

    # Drum Kits idx 41..42
    cur_type = "Factory"
    cur_group = "Drum & SFX"
    for p_idx in range(41, 43):
        for token in split_page_columns(pages[p_idx], "Drum Kit", min_cols=2):
            m = ROW_RE.match(token)
            if m:
                if "-" in m.group(3) or "-" in m.group(4):
                    continue
                name = m.group(1).strip()
                cc00, cc32, pc = int(m.group(2)), int(m.group(3)), int(m.group(4))
                sid = unique_slug(slugify(f"drm_{cur_type}_{name}_{cc32}_{pc}"), used_ids)
                sounds.append({
                    "id": sid,
                    "name": name,
                    "type": cur_type,
                    "group": cur_group,
                    "category": "Drum & SFX",
                    "isDrum": True,
                    "cc00": cc00,
                    "cc32": cc32,
                    "pc": pc,
                    "gmProgram": pc if 0 <= pc <= 127 else 0,
                    "dnc": None,
                    "profile": compute_sound_profile(name, "Drum & SFX", True, pc, cc32),
                })
            else:
                if "/" in token:
                    t_part, g_part = token.rsplit("/", 1)
                    cur_type = t_part.strip()
                    cur_group = g_part.strip()

    return sounds, used_ids


# ---------------------------------------------------------------------------
# Factory Pads Parser (idx 69..73)
# ---------------------------------------------------------------------------
def classify_pad(name: str, group: str, bank_type: str) -> dict:
    n = name.lower()
    g = group.lower()
    pad_type = "OneShot" if bank_type == "HIT" else "Loop"

    # Determine GM drum note for HIT drum/percussion/world hits or GM melodic program
    drum_note = None
    gm_program = 0
    phrase = "arp_up"

    if bank_type == "HIT":
        if "cowbell" in n:
            drum_note = 56
        elif "crash" in n or "splash" in n:
            drum_note = 49 if "1" in n or "88" in n else 57
        elif "china" in n:
            drum_note = 52
        elif "ride bell" in n:
            drum_note = 53
        elif "ride" in n:
            drum_note = 51 if "1" in n else 59
        elif "rev" in n and "cymb" in n:
            drum_note = 55
        elif "stick" in n or "rim" in n or "kup" in n or "rek" in n:
            drum_note = 37
        elif "tom" in n:
            drum_note = 50 if "hi" in n else (45 if "low" in n else 47)
        elif "agogo" in n:
            drum_note = 67 if "1" in n else 68
        elif "castanet" in n or "block" in n or "wood" in n or "clave" in n:
            drum_note = 76 if "1" in n else 75
        elif "conga" in n or "darbuka" in n or "baya" in n or "ramazan" in n or "davul" in n:
            drum_note = 62 if "mute" in n else (63 if "hi" in n or "1" in n or "slap" in n else 64)
        elif "cuica" in n:
            drum_note = 78 if "1" in n else 79
        elif "jingle" in n or "bell" in n or "triangle" in n or "windchime" in n:
            drum_note = 81 if "triangle" in n else (83 if "jingle" in n else 80)
        elif "guiro" in n or "rain" in n or "whistle" in n:
            drum_note = 73 if "short" in n else (74 if "guiro" in n else 71)
        elif "tamb" in n:
            drum_note = 54
        elif "timbale" in n:
            drum_note = 65 if "hi" in n else 66
        elif "vibra" in n:
            drum_note = 58
        elif "gong" in n:
            drum_note = 52
        elif "orch" in g or "orch" in n or "timp" in n or "brass" in n or "stabs" in n or "hit" in n:
            gm_program = 55 if ("hit" in n or "brass" in n) else (47 if "timp" in n else 48)
        elif "voice" in g or "vox" in n or "hey" in n or "yeah" in n or "ah" in n or "ooh" in n:
            gm_program = 54
        elif "synth" in g or "pad" in g or "sweep" in n or "laser" in n or "zap" in n:
            gm_program = 81 if "lead" in n or "zap" in n else 95
        elif "sfx" in g or "misc" in g or "thunder" in n or "applause" in n or "bird" in n or "phone" in n:
            gm_program = 122 if "wave" in n or "rain" in n else (126 if "applause" in n else 124)
        else:
            drum_note = 38
    else:
        # SEQ Loop Pads
        if "drum" in g or "perc" in g or "groove" in g:
            gm_program = 0
            phrase = "perc_latin" if ("perc" in g or "conga" in n or "bongo" in n or "shaker" in n or "latin" in n) else "drum_groove"
        elif "bass" in g or "bass" in n:
            gm_program = 33 if "finger" in n or "ac" not in n else 32
            if "synth" in n or "acid" in n or "dance" in n or " house" in n:
                gm_program = 38
            phrase = "bass_pulse"
        elif "piano" in g or "piano" in n or "ep" in n or "clav" in n:
            gm_program = 4 if ("ep" in n or "rhodes" in n or "tine" in n or "wurl" in n) else (7 if "clav" in n else 0)
            phrase = "montuno" if ("montuno" in n or "latin" in n or "salsa" in n) else "piano_arp"
        elif "guitar" in g or "gtr" in n:
            gm_program = 24 if ("nylon" in n or "bossa" in n or "flamenco" in n) else (27 if "funk" in n or "clean" in n else 25)
            phrase = "guitar_strum"
        elif "orch" in g or "string" in n or "harp" in n or "brass" in n:
            gm_program = 46 if "harp" in n else (61 if "brass" in n else 48)
            phrase = "harp_arp" if "harp" in n else "ostinato"
        elif "solo" in g or "sax" in n or "flute" in n or "trump" in n:
            gm_program = 66 if "sax" in n else (73 if "flute" in n else 56)
            phrase = "riff_solo"
        elif "synth" in g or "pad" in g:
            gm_program = 81 if ("seq" in n or "arp" in n or "lead" in n) else 89
            phrase = "synth_gate"
        else:
            gm_program = 98 if ("precount" in n or "metronome" in n) else 99
            phrase = "fx_seq"

    return {
        "padType": pad_type,
        "drumNote": drum_note,
        "gmProgram": gm_program,
        "phrase": phrase,
    }


def parse_pads(pages: list) -> tuple:
    pads = []
    pad_groups = OrderedDict()
    used_ids = set()
    cur_group = "HIT - Drum"
    for p_idx in range(69, 74):
        for token in split_page_columns(pages[p_idx], "#", min_cols=3):
            m = PAD_RE.match(token)
            if m:
                slot = int(m.group(1))
                name = m.group(2).strip()
                bank_type = "HIT" if cur_group.lower().startswith("hit") else "SEQ"
                meta = classify_pad(name, cur_group, bank_type)
                pid = unique_slug(slugify(f"{cur_group}_{slot}_{name}"), used_ids)
                entry = {
                    "id": pid,
                    "slot": slot,
                    "name": name,
                    "group": cur_group,
                    "bankType": bank_type,
                    "type": meta["padType"],
                    "drumNote": meta["drumNote"],
                    "gmProgram": meta["gmProgram"],
                    "phrase": meta["phrase"],
                }
                pads.append(entry)
                pad_groups.setdefault(cur_group, []).append(pid)
            else:
                # Normalize e.g. 'Hit - World 2' -> 'HIT - World 2'
                norm = re.sub(r"^Hit\s*-", "HIT -", token)
                cur_group = norm
    return pads, [{"name": g, "bankType": ("HIT" if g.startswith("HIT") else "SEQ"), "padIds": ids} for g, ids in pad_groups.items()]


# ---------------------------------------------------------------------------
# Keyboard Sets Parser (idx 6..10) + Sound Matching
# ---------------------------------------------------------------------------
def build_sound_matcher(sounds: list) -> dict:
    exact = {}
    melodic = [s for s in sounds if not s["isDrum"]]
    for s in melodic:
        exact.setdefault(s["name"].lower(), s["name"])
    return {"exact": exact, "melodic": melodic}


def pick_sound_for_keywords(matcher: dict, keywords: list, prefer_cat: list = None, fallback: str = "Concert Grand") -> str:
    for kw in keywords:
        low = kw.lower()
        if low in matcher["exact"]:
            return matcher["exact"][low]
    # Substring search weighted by Factory > Legacy > GM/XG
    candidates = matcher["melodic"]
    if prefer_cat:
        pref = [s for s in candidates if s["category"] in prefer_cat]
        if pref:
            candidates = pref
    for kw in keywords:
        low = kw.lower()
        for t in ("Factory", "Legacy", "GM/XG"):
            for s in candidates:
                if s["type"] == t and low in s["name"].lower():
                    return s["name"]
    if prefer_cat:
        for t in ("Factory", "Legacy", "GM/XG"):
            for s in matcher["melodic"]:
                if s["type"] == t and s["category"] in prefer_cat:
                    return s["name"]
    return fallback if fallback in matcher["exact"].values() else "Concert Grand"


def voice_set_for_kbd_name(name: str, cat_id: str, matcher: dict) -> dict:
    """Create authentic Upper1 / Upper2 / Upper3 / Lower layers using real manual Sounds."""
    n = name.lower()
    str_layer = pick_sound_for_keywords(matcher, ["Real Strings", "Warm Strings", "Movie Strings", "Strings"], ["Strings & Vocal"], "Ensemble Strings")
    pad_layer = pick_sound_for_keywords(matcher, ["Warm Pad", "Dark Pad", "Soft Pad", "Analog Pad"], ["Synth Pad"], "Warm Pad GM")
    low_strings = pick_sound_for_keywords(matcher, ["Cellos & Contrabass", "Legato Strings", "Warm Strings", "Strings"], ["Strings & Vocal"])

    if cat_id == "piano":
        if "wurly" in n:
            u1 = pick_sound_for_keywords(matcher, ["Wurly Logic", "Wurly", "Classic Wurly"], ["E. Piano"])
        elif "tine" in n or "dyno" in n or "suitcase" in n or "rhodes" in n or "fm" in n or "e.p" in n or "ep" in n:
            u1 = pick_sound_for_keywords(matcher, ["Tine EP Dyno", "Bell Tine EP", "Suit Case88 EP1", "E.Piano"], ["E. Piano"])
        elif "clav" in n or "harpsi" in n:
            u1 = pick_sound_for_keywords(matcher, ["ClassicClav DNC", "Clavi", "Harpsi"], ["Piano", "E. Piano"])
        elif "honky" in n:
            u1 = pick_sound_for_keywords(matcher, ["Honky", "Ragtime"], ["Piano"])
        elif "jazz" in n:
            u1 = pick_sound_for_keywords(matcher, ["Jazz Piano", "Mellow"], ["Piano"])
        elif "m1" in n:
            u1 = pick_sound_for_keywords(matcher, ["M1 Piano"], ["Piano"])
        elif "rock" in n or "bright" in n:
            u1 = pick_sound_for_keywords(matcher, ["Rock Piano", "Bright Piano"], ["Piano"])
        elif "classic" in n:
            u1 = pick_sound_for_keywords(matcher, ["Classic Piano"], ["Piano"])
        else:
            u1 = pick_sound_for_keywords(matcher, ["Concert Grand", "Pop Grand", "Live Piano"], ["Piano"])
        u2 = str_layer if ("string" in n or "pad" in n or "ballad" in n or "symph" in n) else pad_layer
        u2_muted = not any(w in n for w in ("&", "string", "pad", "choir", "brass", "layer", "symph", "dual"))
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": u2, "muted": u2_muted, "octave": 0},
            "up3": {"sound": pick_sound_for_keywords(matcher, ["Choir", "Bell", "Celesta"], ["Strings & Vocal", "Mallet & Bell"]), "muted": True, "octave": 0},
            "low": {"sound": pad_layer if "ep" in n or "wurly" in n or "tine" in n else low_strings, "muted": False, "octave": 0},
        }
    elif cat_id == "organ":
        u1 = pick_sound_for_keywords(matcher, ["Jazz Organ", "BX3", "CX3", "Rock Organ", "Church", "Pipe Organ", "Gospel", "Organ"] if "church" not in n and "pipe" not in n else ["Pipe Organ", "Church", "Chapel", "Cathedral"], ["Organ"])
        u2 = pick_sound_for_keywords(matcher, ["Organ", "Rot", "Drawbar"], ["Organ"])
        low = pick_sound_for_keywords(matcher, ["Organ Bass", "Pedal", "Sub", "Warm Pad"], ["Organ", "Bass", "Synth Pad"])
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": u2, "muted": "duo" not in n and "full" not in n and "gospel" not in n, "octave": 0},
            "up3": {"sound": pad_layer, "muted": True, "octave": 0},
            "low": {"sound": low, "muted": False, "octave": 0},
        }
    elif cat_id == "guitar":
        if "nylon" in n or "classic" in n or "flamenco" in n or "spanish" in n:
            u1 = pick_sound_for_keywords(matcher, ["Nylon", "Concert Guitar", "Spanish"], ["Guitar"])
        elif "12" in n:
            u1 = pick_sound_for_keywords(matcher, ["12Str", "12 Str"], ["Guitar"])
        elif "jazz" in n:
            u1 = pick_sound_for_keywords(matcher, ["Jazz Gtr"], ["Guitar"])
        elif "dist" in n or "overdr" in n or "rock" in n or "metal" in n or "lead" in n:
            u1 = pick_sound_for_keywords(matcher, ["Dist. Gtr", "Overdrive", "Crunch Gtr", "Rock"], ["Guitar"])
        elif "clean" in n or "strat" in n or "tele" in n or "funk" in n:
            u1 = pick_sound_for_keywords(matcher, ["Strat", "Clean", "Funk"], ["Guitar"])
        else:
            u1 = pick_sound_for_keywords(matcher, ["SteelGtr", "RealFolk Gtr", "Acoustic", "Folk"], ["Guitar"])
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": pad_layer, "muted": "pad" not in n and "string" not in n, "octave": 0},
            "up3": {"sound": pick_sound_for_keywords(matcher, ["Harmonic", "Guitar"], ["Guitar"]), "muted": True, "octave": 1},
            "low": {"sound": pick_sound_for_keywords(matcher, ["Acoustic Bass", "Finger Bass"], ["Bass"]), "muted": False, "octave": 0},
        }
    elif cat_id == "strings":
        if "violin" in n or "solo" in n:
            u1 = pick_sound_for_keywords(matcher, ["Violin", "Fiddle"], ["Strings & Vocal"])
        elif "cello" in n:
            u1 = pick_sound_for_keywords(matcher, ["Cello"], ["Strings & Vocal"])
        elif "choir" in n or "vocal" in n or "vox" in n:
            u1 = pick_sound_for_keywords(matcher, ["Choir", "SopranoVox", "Vocal"], ["Strings & Vocal"])
        else:
            u1 = str_layer
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": str_layer if u1 != str_layer else pad_layer, "muted": False if ("orch" in n or "symph" in n or "choir" in n) else True, "octave": 0},
            "up3": {"sound": pick_sound_for_keywords(matcher, ["Harp", "Celesta", "Flute"], ["Strings & Vocal", "Mallet & Bell"]), "muted": True, "octave": 1},
            "low": {"sound": low_strings, "muted": False, "octave": 0},
        }
    elif cat_id in ("brass", "trumpet"):
        if cat_id == "trumpet":
            u1 = pick_sound_for_keywords(matcher, ["Jazz Trumpet", "Trumpet", "Cornet", "Flugel"] if "flugel" not in n else ["Flugel"], ["Trumpet & Trbn."])
            u2 = pick_sound_for_keywords(matcher, ["Trombone", "Trb.", "Brass"], ["Trumpet & Trbn.", "Brass"])
        else:
            u1 = pick_sound_for_keywords(matcher, ["Brass", "Horn", "Big Band", "Fanfare"], ["Brass", "Trumpet & Trbn."])
            u2 = pick_sound_for_keywords(matcher, ["Trombone", "Tenor Sax", "Horn"], ["Trumpet & Trbn.", "Sax", "Brass"])
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": u2, "muted": "solo" in n, "octave": 0},
            "up3": {"sound": pick_sound_for_keywords(matcher, ["Tuba", "Brass"], ["Brass", "Trumpet & Trbn."]), "muted": True, "octave": -1},
            "low": {"sound": pick_sound_for_keywords(matcher, ["Tuba", "Finger Bass", "Acoustic Bass"], ["Brass", "Bass"]), "muted": False, "octave": 0},
        }
    elif cat_id == "sax":
        if "accordion" in n or "musette" in n or "tango" in n:
            u1 = pick_sound_for_keywords(matcher, ["Accordion", "Musette", "Bandoneon"], ["Accordion"])
        elif "harmonica" in n:
            u1 = pick_sound_for_keywords(matcher, ["Harmonica"], ["Accordion"])
        elif "flute" in n or "pan" in n or "whistle" in n:
            u1 = pick_sound_for_keywords(matcher, ["Flute", "Pan Flute", "Whistle"], ["Woodwind"])
        elif "clarinet" in n or "oboe" in n:
            u1 = pick_sound_for_keywords(matcher, ["Clarinet", "Oboe"], ["Woodwind"])
        elif "alto" in n:
            u1 = pick_sound_for_keywords(matcher, ["Alto Sax", "Jazz Sax"], ["Sax"])
        elif "soprano" in n:
            u1 = pick_sound_for_keywords(matcher, ["Soprano Sax"], ["Sax"])
        elif "bari" in n:
            u1 = pick_sound_for_keywords(matcher, ["Baritone Sax", "Bari"], ["Sax"])
        else:
            u1 = pick_sound_for_keywords(matcher, ["Tenor Sax", "Tenor Growl", "Sax"], ["Sax"])
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": pad_layer, "muted": "section" not in n and "duo" not in n, "octave": 0},
            "up3": {"sound": str_layer, "muted": True, "octave": 0},
            "low": {"sound": pick_sound_for_keywords(matcher, ["Acoustic Bass", "Warm Pad"], ["Bass", "Synth Pad"]), "muted": False, "octave": 0},
        }
    elif cat_id == "synth":
        u1 = pick_sound_for_keywords(matcher, ["Lead", "Saw", "Pad", "Sweep", "Poly", "Brass", "Vocoder", "Square"], ["Synth Lead", "Synth Pad"])
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": pad_layer, "muted": "lead" in n, "octave": 0},
            "up3": {"sound": pick_sound_for_keywords(matcher, ["Bell", "Square", "Pluck"], ["Mallet & Bell", "Synth Lead"]), "muted": True, "octave": 1},
            "low": {"sound": pick_sound_for_keywords(matcher, ["Synth Bass", "Bass", "Warm Pad"], ["Bass", "Synth Pad"]), "muted": False, "octave": -1},
        }
    else:  # ethnic
        u1 = pick_sound_for_keywords(matcher, [name.split()[0], "Mandolin", "Sitar", "Oud", "Bouzouki", "Kanun", "Koto", "Shamisen", "Bagpipe", "Banjo"], ["Ethnic", "Guitar"])
        return {
            "up1": {"sound": u1, "muted": False, "octave": 0},
            "up2": {"sound": pad_layer, "muted": True, "octave": 0},
            "up3": {"sound": str_layer, "muted": True, "octave": 0},
            "low": {"sound": pick_sound_for_keywords(matcher, ["Oud", "Cello", "Acoustic Bass"], ["Ethnic", "Strings & Vocal", "Bass"]), "muted": False, "octave": 0},
        }


def parse_kbd_sets(pages: list, matcher: dict) -> tuple:
    kbd_by_cat = OrderedDict((c["id"], []) for c in KBD_LIBRARY_CATEGORIES)
    all_sets = []
    used_ids = set()
    cur_cat_id = "piano"
    cur_cat_manual = "Piano & EP"

    for p_idx in range(6, 11):
        for token in split_page_columns(pages[p_idx], "Keyboard Set", min_cols=2):
            m = ROW_RE.match(token)
            if m:
                if "-" in m.group(3) or "-" in m.group(4):
                    continue
                name = m.group(1).strip()
                cc00, cc32, pc = int(m.group(2)), int(m.group(3)), int(m.group(4))
                kid = unique_slug(slugify(f"{cur_cat_id}_{name}"), used_ids)
                voices = voice_set_for_kbd_name(name, cur_cat_id, matcher)
                entry = {
                    "id": kid,
                    "name": name,
                    "category": cur_cat_manual,
                    "categoryId": cur_cat_id,
                    "cc00": cc00,
                    "cc32": cc32,
                    "pc": pc,
                    **voices,
                }
                kbd_by_cat[cur_cat_id].append(entry)
                all_sets.append(entry)
            else:
                if token in KBD_CAT_BY_MANUAL:
                    cur_cat_manual = token
                    cur_cat_id = KBD_CAT_BY_MANUAL[token]
    return kbd_by_cat, all_sets


# ---------------------------------------------------------------------------
# Styles Parser (idx 0..5) + 379 Individual Blueprint & 8-Track MIDI Compiler
# ---------------------------------------------------------------------------
def parse_styles(pages: list, pads: list, sounds: list, matcher: dict) -> list:
    pads_by_group_norm = {}
    for p in pads:
        pads_by_group_norm.setdefault(p["group"], []).append(p)

    exact_sound_map = {}
    for s in sounds:
        low = s["name"].lower()
        if low not in exact_sound_map or s["type"] == "Factory":
            exact_sound_map[low] = s

    styles = []
    used_ids = set(STYLE_ALIASES.values())
    cur_cat = "Pop"

    for p_idx in range(0, 6):
        for token in split_page_columns(pages[p_idx], "Style", min_cols=2):
            m = ROW_RE.match(token)
            if m:
                if "-" in m.group(3) or "-" in m.group(4):
                    continue
                name = m.group(1).strip()
                cc00, cc32, pc = int(m.group(2)), int(m.group(3)), int(m.group(4))
                alias = STYLE_ALIASES.get(name)
                if alias:
                    sid = alias
                else:
                    sid = unique_slug(slugify(name), used_ids)
                bp = get_style_blueprint(sid, cur_cat)
                compiled = compile_style_from_blueprint(
                    sid, name, cur_cat, bp, sounds, exact_sound_map,
                    pads_by_group_norm, matcher, pick_sound_for_keywords
                )
                styles.append({
                    "id": sid,
                    "name": name,
                    "category": cur_cat,
                    "bank": f"Fty-{cur_cat}",
                    "cc00": cc00,
                    "cc32": cc32,
                    "pc": pc,
                    **compiled,
                })
            else:
                if token in STYLE_CATEGORY_LIST:
                    cur_cat = token
    return styles


def main():
    raw_txt = run_pdftotext()
    pages = raw_txt.split("\f")
    assert len(pages) >= 74, f"Expected >=74 appendix pages, got {len(pages)}"

    dnc_map = parse_dnc_controls(pages)
    sounds, _ = parse_sounds_and_drums(pages, dnc_map)
    melodic_count = sum(1 for s in sounds if not s["isDrum"])
    drum_count = sum(1 for s in sounds if s["isDrum"])
    matcher = build_sound_matcher(sounds)

    pads, pad_groups = parse_pads(pages)
    kbd_by_cat, all_kbd_sets = parse_kbd_sets(pages, matcher)
    styles = parse_styles(pages, pads, sounds, matcher)

    # Hard verification assertions matching Korg Pa700 User Manual v1.5
    assert len(styles) == 379, f"Expected 379 Styles, got {len(styles)}"
    assert len(STYLE_BLUEPRINTS_379) == 379, f"Expected 379 Style Blueprints, got {len(STYLE_BLUEPRINTS_379)}"
    assert len(all_kbd_sets) == 298, f"Expected 298 Keyboard Sets, got {len(all_kbd_sets)}"
    assert melodic_count == 1727, f"Expected 1727 Melodic Sounds, got {melodic_count}"
    assert drum_count == 118, f"Expected 118 Drum Kits, got {drum_count}"
    assert len(pads) == 415, f"Expected 415 Factory Pads, got {len(pads)}"

    # Verify all Style ID aliases, 8-track Sound refs, STS refs, and 379/379 MIDI Pattern Uniqueness!
    style_ids = {s["id"] for s in styles}
    for alias in STYLE_ALIASES.values():
        assert alias in style_ids, f"Missing required alias styleId: {alias}"
    sound_names = {s["name"] for s in sounds}
    for ks in all_kbd_sets:
        for trk in ("up1", "up2", "up3", "low"):
            assert ks[trk]["sound"] in sound_names, f"Dangling KbdSet sound: {ks[trk]['sound']}"

    seen_midi_fps = {}
    seen_band_lineups = set()
    for st in styles:
        assert len(st["styleTracks"]) == 8, f"Style {st['id']} missing 8 styleTracks"
        for trk_obj in st["styleTracks"]:
            assert trk_obj["sound"] in sound_names, f"Dangling Style Track sound in {st['id']}: {trk_obj['sound']}"
        band_tuple = tuple(t["sound"] for t in st["styleTracks"])
        seen_band_lineups.add(band_tuple)
        fp = midi_pattern_fingerprint(st)
        if fp in seen_midi_fps:
            raise AssertionError(
                f"Duplicate MIDI pattern detected between {st['id']!r} and {seen_midi_fps[fp]!r}!"
            )
        seen_midi_fps[fp] = st["id"]
        for sts in st["kbdSets"]:
            for trk in ("up1", "up2", "up3", "low"):
                assert sts[trk] in sound_names, f"Dangling Style STS sound: {sts[trk]}"

    print(f"Verified 379/379 unique MIDI patterns and {len(seen_band_lineups)}/379 unique 8-track instrument lineups!")

    # Organize Sound Type -> Ordered Group -> Sound IDs for fast O(1) TouchView rendering
    sound_groups_by_type = OrderedDict([("Factory", OrderedDict()), ("Legacy", OrderedDict()), ("GM/XG", OrderedDict())])
    for s in sounds:
        sound_groups_by_type[s["type"]].setdefault(s["category"], []).append(s["id"])

    style_ids_by_cat = OrderedDict((cat, []) for cat in STYLE_CATEGORY_LIST)
    for st in styles:
        style_ids_by_cat[st["category"]].append(st["id"])

    # SetList entries (all mapped cleanly to real manual Styles)
    set_list_entries = [
        {"slot": 1, "title": "(Wanna come) Home", "type": "STY", "styleId": "8beat_standard", "kbdSetIndex": 0, "tempo": 108, "subType": "Style"},
        {"slot": 2, "title": "1/2 minute", "type": "STY", "styleId": "16beat_soul", "kbdSetIndex": 1, "tempo": 100, "subType": "Style"},
        {"slot": 3, "title": "A believer", "type": "STY", "styleId": "classic_rock", "kbdSetIndex": 0, "tempo": 122, "subType": "Style"},
        {"slot": 4, "title": "A gigolo'", "type": "STY", "styleId": "big_band_swing", "kbdSetIndex": 3, "tempo": 136, "subType": "Style"},
        {"slot": 5, "title": "A hard day/night", "type": "STY", "styleId": "classic_rock", "kbdSetIndex": 2, "tempo": 128, "subType": "Style"},
        {"slot": 6, "title": "A walk on wild", "type": "STY", "styleId": "brush_ballad", "kbdSetIndex": 0, "tempo": 73, "subType": "Style"},
        {"slot": 7, "title": "Apache song", "type": "STY", "styleId": "8beat_standard", "kbdSetIndex": 2, "tempo": 116, "subType": "Style"},
        {"slot": 8, "title": "As song", "type": "STY", "styleId": "16beat_soul", "kbdSetIndex": 0, "tempo": 98, "subType": "Style"},
        {"slot": 9, "title": "Baker road", "type": "STY", "styleId": "pop_chart", "kbdSetIndex": 3, "tempo": 118, "subType": "Style"},
    ]
    # fallback if pop_chart isn't a manual style slug
    for e in set_list_entries:
        if e["styleId"] not in style_ids:
            e["styleId"] = "standard_16_beat" if "standard_16_beat" in style_ids else "8beat_standard"

    payload = {
        "manualMeta": {
            "source": "Korg Pa700 User Manual v1.5 E (Appendix pp. 954-1028)",
            "stylesCount": len(styles),
            "kbdSetsCount": len(all_kbd_sets),
            "melodicSoundsCount": melodic_count,
            "drumKitsCount": drum_count,
            "totalSoundsCount": len(sounds),
            "dncCount": len(dnc_map),
            "padsCount": len(pads),
        },
        "mySetting": {
            "name": "Concert Grand + Pad",
            "styleId": "brush_ballad",
            "tempo": 73,
            "kbdSet": {
                "name": "Concert Grand",
                "up1": {"sound": "Concert Grand", "muted": False, "octave": 0, "volume": 115},
                "up2": {"sound": "Real Strings 1", "muted": True, "octave": 0, "volume": 88},
                "up3": {"sound": "Warm Pad GM", "muted": True, "octave": 0, "volume": 72},
                "low": {"sound": "Cellos & Contrabass" if "Cellos & Contrabass" in sound_names else "Warm Strings", "muted": False, "octave": 0, "volume": 84},
            },
        },
        "libraryCategories": KBD_LIBRARY_CATEGORIES,
        "keyboardSetLibrary": kbd_by_cat,
        "allKbdSets": all_kbd_sets,
        "styleCategories": STYLE_CATEGORY_LIST,
        "styleIdsByCategory": style_ids_by_cat,
        "styles": styles,
        "soundTypes": ["Factory", "Legacy", "GM/XG"],
        "soundGroupsByType": sound_groups_by_type,
        "sounds": sounds,
        "soundsCatalog": [s["name"] for s in sounds if not s["isDrum"]],
        "pads": pads,
        "padGroups": pad_groups,
        "setListEntries": set_list_entries,
        "playerSongs": [
            {"id": "song_01", "title": "01_Pa700_Demo_Pop.mid", "tempo": 118, "length": "03:42"},
            {"id": "song_02", "title": "02_Bossa_Evening.mid", "tempo": 124, "length": "04:10"},
            {"id": "song_03", "title": "03_Autumn_Ballad.mp3", "tempo": 74, "length": "03:55"},
        ],
        "subScalePresets": [
            {"name": "Equal", "offsets": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
            {"name": "Bayati (D)", "offsets": [0, 0, 0, 0, -50, 0, 0, 0, 0, 0, 0, -50]},
            {"name": "Rast (C)", "offsets": [0, 0, 0, 0, -50, 0, 0, 0, 0, 0, 0, -50]},
            {"name": "Hijaz (D)", "offsets": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
            {"name": "Saba (D)", "offsets": [0, 0, 0, 0, -50, 0, 0, 0, 0, 0, 0, 0]},
            {"name": "User", "offsets": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
        ],
        "drills": [
            {
                "id": "voices",
                "title": "Drill 1: Changing Voices Fast (4 Ways + Set List Trap)",
                "steps": [
                    {
                        "prompt": "1. Notice SET LIST (bottom-right) is OFF. Click 'ORGAN' (button 2 in KEYBOARD SET LIBRARY) to load a Jazz Organ voice set (press repeatedly to cycle all 40 manual Organ sets!).",
                        "targetBtn": "ksl_2",
                    },
                    {
                        "prompt": "2. Click note G4 (right side of the keyboard) to play a G Major triad (G4-B4-D5) with your new Organ voice!",
                        "targetKey": 67,
                    },
                    {
                        "prompt": "3. Now test Style-matched voices: click KEYBOARD SET '3' right under the TouchView screen to switch to the Style's 3rd voice.",
                        "targetBtn": "kbd_set_3",
                    },
                    {
                        "prompt": "4. Watch out for the #1 gig trap: click 'SET LIST' (left of PIANO & EP). When its red LED is ON, buttons 1-9 switch SongBook songs instead of instrument families! Click 'SET LIST' again to return to Voice Library mode.",
                        "targetBtn": "set_list",
                    },
                    {
                        "prompt": "5. Emergency Home Voice: click 'MY SETTING' (white label, bottom-right of center) to instantly restore your favorite Concert Grand piano setup!",
                        "targetBtn": "my_setting",
                    },
                ],
            },
            {
                "id": "arranger",
                "title": "Drill 2: Running Auto-Arranger (Intro -> Variations -> Fill -> Ending)",
                "steps": [
                    {
                        "prompt": "1. Make sure SPLIT, ACCOMP., MEMORY, and AUTO FILL are ON. Click 'SYNCHRO START' (round button left of red START/STOP) so the band waits for your left hand!",
                        "targetBtn": "synchro_start",
                    },
                    {
                        "prompt": "2. Book your song's opening: click 'VARIATION 1' (sparse verse), then click 'INTRO 2' (intro using your chord). Notice VARIATION 1 starts blinking (booked after Intro)!",
                        "targetBtn": "intro_2",
                    },
                    {
                        "prompt": "3. Trigger the band! Click note G2 (left of C4 split point) to feed a G Major triad (G2-B2-D3) to the Arranger.",
                        "targetKey": 43,
                    },
                    {
                        "prompt": "4. Build energy into the Chorus! Click 'VARIATION 3'. Because AUTO FILL is lit, Pa700 plays a drum fill first, then drops into Variation 3!",
                        "targetBtn": "var_3",
                    },
                    {
                        "prompt": "5. Wrap up the song right now by clicking 'ENDING 3' (immediate 2-bar ending + auto-stop)!",
                        "targetBtn": "ending_3",
                    },
                ],
            },
            {
                "id": "split",
                "title": "Drill 3: Changing the Split Point & Full-Piano Mode",
                "steps": [
                    {
                        "prompt": "1. Press and HOLD the 'SPLIT' button (right panel, above Strings/Brass) for ~0.6s until the green 'Split Point' popup opens on screen!",
                        "targetBtn": "split",
                    },
                    {
                        "prompt": "2. Click key F3 on the 61-key keyboard to move the Split Point lower to F3 (giving your right hand more room)!",
                        "targetKey": 53,
                    },
                    {
                        "prompt": "3. Want solo full-range piano with NO split? Click 'SPLIT' briefly to turn its LED OFF—now your Upper voice spans all 61 keys!",
                        "targetBtn": "split",
                    },
                ],
            },
        ],
    }

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("// Auto-generated from Pa700_User_Manual_v15_E.pdf by scripts/extract_manual_resources.py\n")
        f.write("// Exact Factory Resources: 379 Styles, 298 Keyboard Sets, 1,727 Sounds, 118 Drum Kits, 415 Pads.\n")
        f.write("window.PA700_DATA = ")
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    size_kb = os.path.getsize(OUTPUT_JS) / 1024
    print(f"Generated {OUTPUT_JS} ({size_kb:.1f} KB)")
    print("Meta:", json.dumps(payload["manualMeta"]))


if __name__ == "__main__":
    main()
