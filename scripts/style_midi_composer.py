#!/usr/bin/env python3
"""
Multi-Bar 8-Track Chord-Adaptive MIDI Pattern Composer for Korg Pa700 Styles.

Compiles each of the 379 individual Style Blueprints into concrete multi-bar
8-track MIDI arrangements (`Drum`, `Perc`, `Bass`, `Acc1`..`Acc5`) with:
  - Authentic time signatures: 4/4, 2/4, 3/4, 6/8, 12/8, 6/4, 9/8 (2+2+2+3)
  - Groove microtiming: straight, 16th-pocket funk/hip-hop swing, 8th-note jazz swing
  - NTT chord-adaptive pitch codes (0..25 single degrees/approaches, 50..62 voicings/strums)
  - Progressive 4-Variation density (Var 1..4 bitmasks 1|2|4|8)
  - Style-specific Intro 1 (chord progression + melody), Intro 2, Intro 3 (count-in),
    Fills 1..4, Break, and Endings 1..3.
"""

import json

# ============================================================================
# PITCH CODE CONSTANTS (Shared with pa700_audio.js)
# ============================================================================
R = 0       # Chord Root (+0)
D2 = 1      # 9th / 2nd (+2)
D3 = 2      # Chord 3rd (min=+3, maj=+4, sus4=+5, sus2=+2)
D4 = 3      # 11th / 4th (+5)
D5 = 4      # Chord 5th (dim=+6, aug=+8, else=+7)
D6 = 5      # 6th / 13th (+9)
D7 = 6      # Diatonic/Chord 7th
B7 = 7      # Dominant / Mixolydian / Blues b7 (+10)
R8 = 8      # Octave Root (+12)
L5 = 9      # Fifth BELOW Root (-5)
LR = 10     # Octave BELOW Root (-12)
U9 = 11     # Upper 9th (+14)
U3 = 12     # Upper 3rd (3rd + 12)
U5 = 13     # Upper 5th (5th + 12)
U8 = 14     # Two-Octave Root (+24)
B5 = 15     # Chromatic #4/b5 (+6)
LT = 16     # Leading tone below Root (-1)
B2 = 17     # Phrygian b2 (+1)
S5 = 18     # Raised 5th / b6 (+8) -> 007 Spy (D5-S5-D6-S5) & Tango/Cinematic
B3 = 19     # Blues minor 3rd crush (+3)
L6 = 20     # Low 6th below Root (-3)
L4 = 21     # Low 4th below Root (-7)
A5 = 22     # Half-step above 5th (5th + 1)
C5 = 23     # Chromatic below 5th (5th - 1)
U6 = 24     # Upper 6th (+21)
UB7 = 25    # Upper b7 (+22)

# Multi-note voicings & guitar articulations
CLOSE = 50       # Smooth voice-led 3-4 note close chord
OPEN = 51        # Lush spread Piano/Pad/String chord
HIGH_STAB = 52   # Upper-register Brass/Organ/Clav stab
JAZZ_SHELL = 53  # Rootless 3-7-9 Jazz/Bossa/Soul voicing
POWER5 = 54      # Rock Power Chord (Root + 5th)
POWER8 = 55      # Big Stadium Power Chord (Root + 5th + Octave)
STRUM_DN = 56    # Guitar Down-Strum (staggered low->high)
STRUM_UP = 57    # Guitar Up-Strum (staggered high->low)
CHUCK = 58       # Tight damped Guitar/Mandolin/Pompe percussive chop
MONTUNO = 59     # Cuban Octave-Shell Piano Montuno voicing
QUARTAL = 60     # Modern Quartal / House / Synth voicing (0, +5, +10)
THIRDS = 61      # Harmonized 3rds/6ths dyad (Mariachi Tpts, Norteno Acc, Bouzouki, Steel)
FOURTHS = 62     # Parallel 4ths Rock/Organ dyad (0, +5)

# Variation bitmasks
V1 = 1
V2 = 2
V3 = 4
V4 = 8
V_ALL = 15       # Var 1..4
V_234 = 14       # Var 2..4
V_34 = 12        # Var 3..4
V_4 = 8          # Var 4 only
V_12 = 3         # Var 1..2 only

# Track indices (8 Pa700 Style Accompaniment Tracks)
T_DRUM = 0
T_PERC = 1
T_BASS = 2
T_ACC1 = 3
T_ACC2 = 4
T_ACC3 = 5
T_ACC4 = 6
T_ACC5 = 7

# Meter grid definitions: (beatsPerBar, subPerBeat, beatDurScale)
METER_SPECS = {
    "4/4":  (4, 4, 1.0),   # 16 steps/bar, 32 steps/2-bar loop
    "2/4":  (2, 4, 1.0),   # 8 steps/bar,  16 steps/2-bar loop
    "3/4":  (3, 4, 1.0),   # 12 steps/bar, 24 steps/2-bar loop
    "6/8":  (6, 2, 0.5),   # 12 steps/bar (6 eighth pulses), 24 steps/2-bar loop
    "12/8": (4, 3, 1.0),   # 12 triplet steps/bar, 24 steps/2-bar loop
    "6/4":  (6, 4, 1.0),   # 24 steps/bar, 48 steps/2-bar loop
    "9/8":  (9, 2, 0.5),   # 18 steps/bar (2+2+2+3 = 4+4+4+6), 36 steps/2-bar loop
}

# Harmonic cadence progressions for Intro 1 & Ending 1 (semitone shifts per half-bar over 2 bars)
CADENCE_SHIFTS = {
    "pop_IV_V":       ([5, 5, 7, 7],   [5, 7, 0, 0]),
    "jazz_ii_V":      ([2, 2, 7, 7],   [2, 7, 0, 0]),
    "blues_V_IV":     ([7, 7, 5, 7],   [7, 5, 0, 0]),
    "flamenco_bVI_V": ([8, 8, 7, 7],   [8, 7, 0, 0]),
    "rock_bVII_IV":   ([10, 10, 5, 5], [10, 5, 0, 0]),
    "tango_V_I":      ([7, 8, 7, 0],   [7, 7, 0, 0]),
    "modal_bVII":     ([10, 10, 0, 0], [10, 0, 0, 0]),
    "cinematic_bVI":  ([8, 8, 10, 7],  [8, 10, 0, 0]),
    "march_V_I":      ([0, 7, 7, 0],   [5, 7, 0, 0]),
    "christmas_II_V": ([2, 5, 7, 7],   [5, 7, 0, 0]),
    "latin_IV_V":     ([5, 7, 5, 7],   [5, 7, 0, 0]),
    "country_IV_V":   ([5, 5, 7, 0],   [5, 7, 0, 0]),
}


def infer_gs_drum_pc(drum_kit_name: str) -> int:
    """Map Korg Pa700 Drum Kit name to GeneralUser GS / GM Drum Bank 128 program."""
    n = (drum_kit_name or "").lower()
    if "brush" in n:
        return 40
    if "jazz" in n or "cool" in n or "lounge" in n:
        return 32
    if "orch" in n or "symph" in n or "timp" in n:
        return 48
    if "hiphop" in n or "analog" in n or "jungle" in n or "808" in n:
        return 25
    if any(k in n for k in ("trance", "dance", "house", "electro", "elektro", "techno", "synth")):
        return 24
    if any(k in n for k in ("power", "rock", "gate")):
        return 16
    if any(k in n for k in ("room", "ambient", "vintage")):
        return 8
    return 0


def resolve_track_sound(sound_query: str, is_drum: bool, sounds_list: list, exact_map: dict) -> dict:
    """Resolve a track sound name or keyword to an exact PA700_DATA.sounds object."""
    q_low = sound_query.strip().lower()
    if q_low in exact_map:
        cand = exact_map[q_low]
        if bool(cand["isDrum"]) == bool(is_drum):
            return cand
    # Substring match preferring Factory > Legacy > GM/XG
    pool = [s for s in sounds_list if bool(s["isDrum"]) == bool(is_drum)]
    for tier in ("Factory", "Legacy", "GM/XG"):
        for s in pool:
            if s["type"] == tier and q_low in s["name"].lower():
                return s
    # Fallback token search
    first_tok = q_low.split()[0]
    for s in pool:
        if first_tok in s["name"].lower():
            return s
    return pool[0]


# ============================================================================
# DRUM & PERCUSSION IDIOM BUILDERS (2-BAR BASE + PER-STYLE CUSTOMIZATION)
# ============================================================================
def _add_ev(out: list, step: int, total_steps: int, trk: int, code: int, dur: int, vel: int, mask: int = V_ALL):
    if 0 <= step < total_steps:
        out.append([int(step), int(trk), int(code), max(1, int(dur)), max(18, min(127, int(vel))), int(mask)])


def build_drums_and_perc(bp: dict, bar_steps: int, sub: int) -> list:
    """Generate 2-bar Drum (trk 0) & Perc (trk 1) MIDI events with Var 1..4 build & bar-2 turnaround."""
    total = bar_steps * 2
    evs = []
    d_type = bp.get("drum_mode", "pop_8")
    kick_n = bp.get("kick_note", 36)
    snare_n = bp.get("snare_note", 38)
    rim_n = bp.get("rim_note", 37)
    hat_n = bp.get("hat_note", 42)
    open_hat = bp.get("open_hat_note", 46)
    ride_n = bp.get("ride_note", 51)
    perc_n = bp.get("perc_note", 70)
    perc2_n = bp.get("perc2_note", 54)

    custom_kicks = bp.get("kicks")      # Steps within 1 bar (auto-mirrored + bar-2 variation)
    custom_snares = bp.get("snares")
    custom_perc = bp.get("perc_steps")

    # 1. Core Idiom Templates (overridden or augmented by per-style kicks/snares/perc_steps)
    for bar in (0, 1):
        off = bar * bar_steps

        if d_type == "waltz_3_4":
            k_steps = custom_kicks if custom_kicks is not None else [0]
            s_steps = custom_snares if custom_snares is not None else [4, 8]
            for ks in k_steps:
                _add_ev(evs, off + ks, total, T_DRUM, kick_n, 2, 84, V_ALL)
            for ss in s_steps:
                _add_ev(evs, off + ss, total, T_DRUM, rim_n, 1, 56, V_12)
                _add_ev(evs, off + ss, total, T_DRUM, snare_n, 2, 68, V_34)
            for h in range(0, bar_steps, 4):
                _add_ev(evs, off + h, total, T_DRUM, hat_n, 1, 62 if h == 0 else 48, V_ALL)
            for h in (2, 6, 10):
                _add_ev(evs, off + h, total, T_DRUM, hat_n, 1, 38, V_234)
            for r in (0, 4, 8):
                _add_ev(evs, off + r, total, T_DRUM, ride_n, 2, 54, V_4)

        elif d_type == "viennese_3_4":
            _add_ev(evs, off + 0, total, T_DRUM, kick_n, 2, 82, V_ALL)
            if bar == 1:
                _add_ev(evs, off + 10, total, T_DRUM, kick_n, 1, 62, V_234)
            for ss in (custom_snares or [4, 8]):
                _add_ev(evs, off + ss, total, T_DRUM, snare_n, 1, 64, V_ALL)
            for h in (0, 3, 4, 8):
                _add_ev(evs, off + h, total, T_DRUM, ride_n if h in (0, 4, 8) else hat_n, 1, 56 if h == 0 else 44, V_234)

        elif d_type == "ballad_6_8":
            # 12 steps per bar (beats at 0, 2, 4, 6, 8, 10; backbeat on step 6 = beat 4)
            k_steps = custom_kicks if custom_kicks is not None else ([0, 10] if bar == 1 else [0])
            for ks in k_steps:
                _add_ev(evs, off + ks, total, T_DRUM, kick_n, 2, 82, V_ALL)
            _add_ev(evs, off + 6, total, T_DRUM, rim_n, 2, 62, V_12)
            _add_ev(evs, off + 6, total, T_DRUM, snare_n, 2, 78, V_34)
            for h in range(0, bar_steps, 2):
                _add_ev(evs, off + h, total, T_DRUM, hat_n, 1, 58 if h in (0, 6) else 42, V_ALL)
                _add_ev(evs, off + h, total, T_DRUM, ride_n, 2, 52, V_4)
            if bar == 1:
                _add_ev(evs, off + 11, total, T_DRUM, snare_n, 1, 50, V_34)

        elif d_type == "blues_12_8":
            # 12 triplet steps per bar (beats at 0, 3, 6, 9)
            k_steps = custom_kicks if custom_kicks is not None else ([0, 5, 6] if bar == 1 else [0, 6])
            for ks in k_steps:
                _add_ev(evs, off + ks, total, T_DRUM, kick_n, 2, 86, V_ALL)
            for ss in (custom_snares or [3, 9]):
                _add_ev(evs, off + ss, total, T_DRUM, rim_n, 1, 64, V_12)
                _add_ev(evs, off + ss, total, T_DRUM, snare_n, 2, 82, V_34)
            for h in range(bar_steps):
                _add_ev(evs, off + h, total, T_DRUM, ride_n if h % 3 == 0 else hat_n, 1, 64 if h % 3 == 0 else 44, V_ALL if h % 3 != 1 else V_234)

        elif d_type == "turkish_9_8":
            # 18 steps per bar: 2+2+2+3 eighth pulses -> Düm(0), Tek(4), Tek(8), Düm(12), Tek(14), ka(17)
            _add_ev(evs, off + 0, total, T_DRUM, 36, 2, 92, V_ALL)
            _add_ev(evs, off + 12, total, T_DRUM, 36, 2, 86, V_ALL)
            for ts in (4, 8, 14):
                _add_ev(evs, off + ts, total, T_DRUM, snare_n, 1, 76, V_ALL)
            _add_ev(evs, off + 16, total, T_DRUM, rim_n, 1, 58, V_234)
            # Authentic Darbuka on Perc track
            _add_ev(evs, off + 0, total, T_PERC, 64, 2, 94, V_ALL)
            _add_ev(evs, off + 12, total, T_PERC, 64, 2, 88, V_ALL)
            for tk in (4, 8, 14, 17 if bar == 1 else 15):
                _add_ev(evs, off + tk, total, T_PERC, 62, 1, 78, V_ALL)
            for sh in range(0, bar_steps, 2):
                _add_ev(evs, off + sh, total, T_PERC, 54, 1, 46, V_34)

        elif d_type in ("four_floor", "disco", "trance", "house", "euro_90s"):
            beats = [b for b in range(0, bar_steps, 4)]
            for b in beats:
                _add_ev(evs, off + b, total, T_DRUM, kick_n, 2, 96, V_ALL)
            if custom_kicks:
                for ks in custom_kicks:
                    if ks not in beats:
                        _add_ev(evs, off + ks, total, T_DRUM, kick_n, 1, 82, V_234)
            for ss in (custom_snares or [4, 12]):
                _add_ev(evs, off + ss, total, T_DRUM, 39 if d_type in ("disco", "house") else snare_n, 2, 84, V_234)
                if d_type != "trance":
                    _add_ev(evs, off + ss, total, T_DRUM, snare_n, 2, 78, V_34)
            for b in beats:
                _add_ev(evs, off + b + 2, total, T_DRUM, open_hat, 2, 74 if d_type != "deep_house" else 60, V_234)
                _add_ev(evs, off + b + 2, total, T_DRUM, hat_n, 1, 54, V1)
            for s16 in range(bar_steps):
                if s16 % 2 == 1:
                    _add_ev(evs, off + s16, total, T_DRUM, hat_n, 1, 42, V_34)
            if d_type == "disco":
                for c_st in (0, 3, 6, 10, 12):
                    _add_ev(evs, off + c_st, total, T_PERC, 63 if c_st in (3, 10) else 64, 1, 58, V_234)
                _add_ev(evs, off + 4, total, T_PERC, 54, 1, 62, V_34)
                _add_ev(evs, off + 12, total, T_PERC, 54, 1, 62, V_34)

        elif d_type == "reggaeton_dembow":
            # Authentic Dembow: Kick on 0, 4, 8, 12; Snare/Rim on 3, 6, 11, 14!
            for b in (0, 4, 8, 12):
                _add_ev(evs, off + b, total, T_DRUM, kick_n, 2, 96, V_ALL)
            for d_st in (custom_snares or [3, 6, 11, 14]):
                _add_ev(evs, off + d_st, total, T_DRUM, rim_n, 1, 76, V1)
                _add_ev(evs, off + d_st, total, T_DRUM, snare_n, 1, 88, V_234)
            for h in range(0, bar_steps, 2):
                _add_ev(evs, off + h, total, T_DRUM, hat_n, 1, 48, V_234)
            if bar == 1:
                _add_ev(evs, off + 15, total, T_PERC, 65, 1, 72, V_34)

        elif d_type == "trap_halftime":
            # Half-time snare on beat 3 (step 8), syncopated 808 kicks, rapid hi-hat rolls
            for ks in (custom_kicks or ([0, 7, 10] if bar == 0 else [0, 3, 10, 14])):
                _add_ev(evs, off + ks, total, T_DRUM, 36, 2, 98, V_ALL)
            _add_ev(evs, off + 8, total, T_DRUM, 39, 2, 92, V_ALL)
            _add_ev(evs, off + 8, total, T_DRUM, snare_n, 2, 86, V_234)
            for h in range(bar_steps):
                vel = 64 if h % 2 == 0 else 46
                mask = V_ALL if h % 2 == 0 else (V_234 if h in (5, 7, 13, 15) else V_34)
                _add_ev(evs, off + h, total, T_DRUM, hat_n, 1, vel, mask)
            _add_ev(evs, off + 14, total, T_DRUM, open_hat, 1, 66, V_34)

        elif d_type in ("jazz_swing", "jazz_brush", "bebop", "gypsy_pompe", "dixie"):
            # Swung 4/4 (swing8 delays subInBeat==2 to triplet pocket!)
            is_brush = d_type == "jazz_brush"
            is_pompe = d_type == "gypsy_pompe"
            if not is_pompe:
                for b in (0, 4, 8, 12):
                    _add_ev(evs, off + b, total, T_DRUM, 38 if is_brush else ride_n, 2, 62 if is_brush else 74, V_ALL)
                for sk in (2, 6, 10, 14):
                    if is_brush:
                        _add_ev(evs, off + sk, total, T_DRUM, 42, 1, 44, V_234)
                    else:
                        if sk in (6, 14) or d_type == "bebop":
                            _add_ev(evs, off + sk, total, T_DRUM, ride_n, 1, 58, V_ALL if sk in (6, 14) else V_234)
                # Hi-hat chick on 2 & 4
                _add_ev(evs, off + 4, total, T_DRUM, 44, 1, 64, V_ALL)
                _add_ev(evs, off + 12, total, T_DRUM, 44, 1, 66, V_ALL)
                # Feathering kick or Dixieland 2-beat kick
                for ks in (custom_kicks or ([0, 8] if d_type == "dixie" else [0, 4, 8, 12])):
                    _add_ev(evs, off + ks, total, T_DRUM, 35, 2, 68 if d_type == "dixie" else 42, V_234)
                if bar == 1 and d_type in ("bebop", "jazz_swing"):
                    _add_ev(evs, off + 14, total, T_DRUM, snare_n, 1, 58, V_34)
            else:
                # Gypsy Jazz: ultra-light brush hi-hat whisper on 2 & 4 only in Var 3-4
                _add_ev(evs, off + 4, total, T_DRUM, 44, 1, 38, V_34)
                _add_ev(evs, off + 12, total, T_DRUM, 44, 1, 38, V_34)

        elif d_type in ("salsa_clave", "mambo", "chacha", "bossa", "samba", "bachata", "merengue", "cumbia", "tango"):
            if d_type in ("salsa_clave", "mambo"):
                # 2-3 or 3-2 Son Clave across the 2 bars!
                clave_32 = bp.get("clave_dir", "23") == "32"
                b0_cl = [0, 3, 6, 10, 12] if clave_32 else [4, 8]
                b1_cl = [4, 8] if clave_32 else [0, 3, 6, 10, 12]
                cl_steps = b0_cl if bar == 0 else b1_cl
                for cs in cl_steps:
                    _add_ev(evs, off + cs, total, T_PERC, 75, 1, 74, V_ALL)
                # Cascara & Conga Tumbao (slap on 4, open on 6 & 14 & 12)
                for cg, note, v in ((0, 62, 52), (4, 62, 78), (6, 63, 76), (8, 62, 50), (12, 64, 80), (14, 63, 78)):
                    _add_ev(evs, off + cg, total, T_PERC, note, 1, v, V_ALL if cg in (4, 6, 14) else V_234)
                # Cowbell / Ride Bell in Var 3-4
                for cb in (0, 4, 8, 12):
                    _add_ev(evs, off + cb, total, T_DRUM, 56 if d_type == "mambo" else 53, 1, 68, V_34)
                # Anticipated Bombo Kick on 6 & 12 (authentic Salsa!)
                for ks in (custom_kicks or [6, 12]):
                    _add_ev(evs, off + ks, total, T_DRUM, 35, 2, 74, V_234)

            elif d_type == "chacha":
                for b in (0, 4, 8, 12):
                    _add_ev(evs, off + b, total, T_DRUM, 56, 1, 66, V_234)
                _add_ev(evs, off + 0, total, T_DRUM, kick_n, 2, 78, V_ALL)
                _add_ev(evs, off + 10, total, T_DRUM, kick_n, 2, 72, V_ALL)
                _add_ev(evs, off + 4, total, T_DRUM, rim_n, 1, 70, V_ALL)
                # Cha-cha-cha on 4-and-1 (steps 12, 14)
                for gs, n in ((0, 74), (4, 73), (6, 73), (8, 74), (12, 63), (14, 64)):
                    _add_ev(evs, off + gs, total, T_PERC, n, 1, 68, V_ALL)

            elif d_type == "bossa":
                # Authentic Bossa Nova cross-stick partido-alto pattern (bar1: 0, 3, 6, 10, 13; bar2: 2, 6, 9, 12)
                rims = [0, 3, 6, 10, 13] if bar == 0 else [2, 6, 9, 12]
                for rs in (custom_snares or rims):
                    _add_ev(evs, off + rs, total, T_DRUM, 37, 1, 64, V_ALL)
                # Surdo/Kick pulse on 0, 6, 8, 14
                for ks in (custom_kicks or [0, 6, 8, 14]):
                    _add_ev(evs, off + ks, total, T_DRUM, 35, 2, 72 if ks in (0, 8) else 58, V_ALL)
                for sh in range(0, bar_steps, 2):
                    _add_ev(evs, off + sh, total, T_PERC, 69, 1, 44, V_ALL if sh % 4 == 0 else V_234)

            elif d_type == "samba":
                # Surdo low on 2/4 (steps 4, 12), muted on 1/3 (steps 0, 8) + syncopated tamborim/agogo/shaker
                for ms in (0, 8):
                    _add_ev(evs, off + ms, total, T_DRUM, 86, 2, 74, V_ALL)
                    _add_ev(evs, off + ms, total, T_DRUM, 35, 2, 72, V_ALL)
                for os_ in (4, 12, 15):
                    _add_ev(evs, off + os_, total, T_DRUM, 87 if os_ != 15 else 35, 2, 86 if os_ != 15 else 64, V_ALL)
                for tb in (0, 3, 6, 7, 10, 12, 14):
                    _add_ev(evs, off + tb, total, T_PERC, 67 if tb in (0, 6, 12) else 68, 1, 64, V_234)
                for sh in range(bar_steps):
                    if sh % 2 == 0 or sh in (3, 11):
                        _add_ev(evs, off + sh, total, T_PERC, 70, 1, 46, V_ALL if sh % 4 == 0 else V_34)

            elif d_type == "bachata":
                # Dominican Bongo Martillo + Güira + Kick on 0, 6, 8, 12
                for ks in (custom_kicks or [0, 6, 8, 12]):
                    _add_ev(evs, off + ks, total, T_DRUM, 36, 2, 80, V_ALL)
                for bg in range(0, bar_steps, 2):
                    bn = 61 if bg in (6, 12, 14) else 60
                    _add_ev(evs, off + bg, total, T_PERC, bn, 1, 74 if bg == 12 else 58, V_ALL)
                if bar == 1:
                    for roll in (13, 15):
                        _add_ev(evs, off + roll, total, T_PERC, 60, 1, 68, V_234)
                for gr in range(0, bar_steps, 2):
                    _add_ev(evs, off + gr, total, T_DRUM, 42, 1, 46, V_234)

            elif d_type == "merengue":
                for b in (0, 4, 8, 12):
                    _add_ev(evs, off + b, total, T_DRUM, 36, 1, 88, V_ALL)
                for gr in range(bar_steps):
                    _add_ev(evs, off + gr, total, T_PERC, 69, 1, 62 if gr % 4 == 2 else 44, V_ALL if gr % 2 == 0 else V_234)
                for tb in (2, 6, 7, 10, 12, 14, 15):
                    _add_ev(evs, off + tb, total, T_PERC, 63 if tb in (6, 14) else 64, 1, 72, V_234)

            elif d_type == "cumbia":
                # Classic Cumbia: Kick on 0, 8 (+ pickup 14), Offbeat Guacharaca on 2, 6, 10, 14, Conga Llamador on 2, 6, 10, 14 + open 4, 12
                for ks in (custom_kicks or [0, 6, 8, 14]):
                    _add_ev(evs, off + ks, total, T_DRUM, 36, 2, 82, V_ALL)
                for ob in (2, 6, 10, 14):
                    _add_ev(evs, off + ob, total, T_PERC, 73, 1, 78, V_ALL)
                    _add_ev(evs, off + ob + 1, total, T_PERC, 70, 1, 42, V_234)
                for cg in (4, 12):
                    _add_ev(evs, off + cg, total, T_PERC, 63, 1, 72, V_ALL)
                    _add_ev(evs, off + cg, total, T_DRUM, 56, 1, 58, V_34)

            elif d_type == "tango":
                is_nuevo = bp.get("tango_332", False)
                if is_nuevo:
                    # Piazzolla 3+3+2 (steps 0, 6, 12)
                    for st_i in (0, 6, 12):
                        _add_ev(evs, off + st_i, total, T_DRUM, 36, 2, 86, V_ALL)
                        _add_ev(evs, off + st_i, total, T_DRUM, 37, 1, 70, V_234)
                    if bar == 1:
                        _add_ev(evs, off + 14, total, T_DRUM, 38, 1, 68, V_234)
                else:
                    # Argentine / Ballroom 4-to-the-bar marcato + drag pickup on step 14
                    for b in (0, 4, 8, 12):
                        _add_ev(evs, off + b, total, T_DRUM, 36, 2, 82, V_ALL)
                        _add_ev(evs, off + b, total, T_DRUM, 38, 1, 64, V_234)
                    _add_ev(evs, off + 14, total, T_DRUM, 38, 1, 76, V_ALL)

        elif d_type in ("polka_2_4", "march_2_4"):
            # Crisp Oom-Pah (steps 0..7 or 0..15)
            half = 4
            for b in range(0, bar_steps, half * 2):
                _add_ev(evs, off + b, total, T_DRUM, 36, 2, 88, V_ALL)
                if d_type == "march_2_4":
                    _add_ev(evs, off + b, total, T_DRUM, 38, 1, 70, V_234)
                    _add_ev(evs, off + b + 3, total, T_DRUM, 38, 1, 58, V_234)
                _add_ev(evs, off + b + half, total, T_DRUM, snare_n, 1, 80, V_ALL)
                _add_ev(evs, off + b + half, total, T_DRUM, 42, 1, 62, V_234)
                if d_type == "march_2_4" and bar == 1 and b + half + 2 < bar_steps:
                    _add_ev(evs, off + b + half + 2, total, T_DRUM, 38, 1, 68, V_34)
                    _add_ev(evs, off + b + half + 3, total, T_DRUM, 38, 1, 74, V_34)

        elif d_type == "reggae_onedrop":
            # Authentic One-Drop / Steppers: Rim + Kick DROP together on Beat 3 (step 8) or 2 & 4!
            drop_steps = custom_kicks if custom_kicks is not None else [8]
            for ds in drop_steps:
                _add_ev(evs, off + ds, total, T_DRUM, 36, 2, 88, V_ALL)
            for rs in (custom_snares or [8]):
                _add_ev(evs, off + rs, total, T_DRUM, 37, 1, 82, V_ALL)
            for h in range(0, bar_steps, 2):
                _add_ev(evs, off + h, total, T_DRUM, 42, 1, 58 if h % 4 == 2 else 42, V_ALL)
            if bar == 1:
                _add_ev(evs, off + 14, total, T_PERC, 65, 1, 68, V_34)

        elif d_type == "flamenco":
            # Palmas (handclaps 39) + Cajón (36 low, 38 slap) + Castanets (85)
            k_st = custom_kicks or ([0, 6, 12] if bar_steps == 16 else [0, 6])
            s_st = custom_snares or ([3, 10, 14] if bar_steps == 16 else [4, 8, 10])
            for ks in k_st:
                _add_ev(evs, off + ks, total, T_DRUM, 36, 2, 84, V_ALL)
            for ss in s_st:
                _add_ev(evs, off + ss, total, T_DRUM, 38, 1, 74, V_234)
                _add_ev(evs, off + ss, total, T_PERC, 39, 1, 78, V_ALL)
            for cs in range(2, bar_steps, 4):
                _add_ev(evs, off + cs, total, T_PERC, 85, 1, 60, V_34)

        elif d_type == "oriental_4_4":
            # Maqsum / Ciftetelli / Wahda: Düm (64/36), Tek (62/37)
            k_st = custom_kicks or [0, 6, 8]
            t_st = custom_snares or [3, 4, 12, 14]
            for ks in k_st:
                _add_ev(evs, off + ks, total, T_DRUM, 36, 2, 84, V_234)
                _add_ev(evs, off + ks, total, T_PERC, 64, 2, 90, V_ALL)
            for ts in t_st:
                _add_ev(evs, off + ts, total, T_PERC, 62, 1, 78, V_ALL)
            for sh in range(0, bar_steps, 2):
                _add_ev(evs, off + sh, total, T_PERC, 54, 1, 48, V_34)

        else:
            # Pop / Rock / Funk / Soul / Country / Ballad 4/4 & 6/4 customizable backbeat engine
            default_k = [0, 8, 10] if d_type in ("pop_8", "rock_8") else (
                [0, 6, 10] if d_type == "funk_16" else (
                    [0, 10] if d_type == "ballad_4_4" else [0, 8]
                )
            )
            k_st = custom_kicks if custom_kicks is not None else default_k
            s_st = custom_snares if custom_snares is not None else (
                [0, 4, 8, 12] if d_type == "motown_4" else ([4, 12] if bar_steps == 16 else [4, 12, 20])
            )
            for ks in k_st:
                _add_ev(evs, off + ks, total, T_DRUM, kick_n, 2, 88 if d_type != "ballad_4_4" else 72, V_ALL)
            if bar == 1 and bar_steps >= 16:
                extra_k = bp.get("bar2_kick", 14 if d_type in ("rock_8", "funk_16") else None)
                if extra_k is not None:
                    _add_ev(evs, off + extra_k, total, T_DRUM, kick_n, 1, 74, V_234)
            for ss in s_st:
                if d_type == "ballad_4_4":
                    _add_ev(evs, off + ss, total, T_DRUM, rim_n, 1, 64, V_12)
                    _add_ev(evs, off + ss, total, T_DRUM, snare_n, 2, 78, V_34)
                else:
                    _add_ev(evs, off + ss, total, T_DRUM, snare_n, 2, 86, V_ALL)
            # Funk ghost snares
            if d_type == "funk_16":
                for gh in (7, 9, 15 if bar == 1 else 11):
                    _add_ev(evs, off + gh, total, T_DRUM, snare_n, 1, 44, V_234)
            # Hi-hat / Ride grid
            hat_step = 1 if d_type in ("funk_16", "pop_16", "country_train") else 2
            for h in range(0, bar_steps, hat_step):
                vel = 66 if h % 4 == 0 else (50 if h % 2 == 0 else 36)
                mask = V_ALL if h % 2 == 0 else V_234
                _add_ev(evs, off + h, total, T_DRUM, hat_n if d_type != "country_train" else snare_n, 1, vel if d_type != "country_train" else (68 if h in (4, 12) else 34), mask)
            # Chorus Ride in Var 3-4
            for r in range(0, bar_steps, 4 if d_type == "ballad_4_4" else 2):
                _add_ev(evs, off + r, total, T_DRUM, ride_n, 2, 56, V_4 if d_type != "rock_8" else V_34)
            # Bar 1 Beat 1 subtle crash on Var 4
            if bar == 0:
                _add_ev(evs, 0, total, T_DRUM, 49, 4, 66, V_4)

        # Optional per-style Percussion overlay (Sleigh Bells, Shaker, Tambourine, Cowbell, Conga, Claps, Timpani...)
        if custom_perc:
            for p_item in custom_perc:
                if isinstance(p_item, (list, tuple)):
                    ps, pn, pv, pm = p_item[0], p_item[1], p_item[2], (p_item[3] if len(p_item) > 3 else V_234)
                else:
                    ps, pn, pv, pm = p_item, perc_n, 62, V_234
                _add_ev(evs, off + ps, total, T_PERC, pn, 1, pv, pm)
        elif d_type not in ("turkish_9_8", "salsa_clave", "mambo", "chacha", "bossa", "samba", "bachata", "merengue", "cumbia", "oriental_4_4", "flamenco"):
            # Subtle tasteful percussion on Var 3-4 matching perc_n / perc2_n
            for ps in (4, 12) if bar_steps >= 16 else [bar_steps // 2]:
                _add_ev(evs, off + ps, total, T_PERC, perc2_n, 1, 56, V_34)
            for ps in range(2, bar_steps, 4):
                _add_ev(evs, off + ps, total, T_PERC, perc_n, 1, 44, V_4)

    return evs


# ============================================================================
# BASSLINE IDIOM BUILDERS (2-BAR WITH BAR-2 TURNAROUNDS & CUSTOM CONTOURS)
# ============================================================================
BASS_PATTERNS_4_4 = {
    "root_8":        ([(0, R, 2), (2, R, 2), (4, R, 2), (6, R, 2), (8, R, 2), (10, R, 2), (12, D5, 2), (14, D5, 2)],
                      [(0, R, 2), (2, R, 2), (4, R, 2), (6, D3, 2), (8, D5, 2), (10, D5, 2), (12, B7, 2), (14, D5, 2)]),
    "pop_sync":      ([(0, R, 3), (3, R, 1), (6, D5, 2), (8, R, 4), (12, L5, 2), (14, R, 2)],
                      [(0, R, 3), (3, D3, 1), (6, D5, 2), (8, R, 3), (11, L5, 1), (12, L6, 2), (14, LT, 2)]),
    "disco_oct":     ([(0, R, 2), (2, R8, 2), (4, R, 2), (6, R8, 2), (8, R, 2), (10, R8, 2), (12, R, 2), (14, R8, 2)],
                      [(0, R, 2), (2, R8, 2), (4, R, 2), (6, R8, 2), (8, D3, 2), (10, D5, 2), (12, B7, 2), (14, R8, 2)]),
    "offbeat_edm":   ([(2, R, 2), (6, R, 2), (10, R, 2), (14, R8, 2)],
                      [(2, R, 2), (6, R, 2), (10, D5, 2), (14, B7, 2)]),
    "house_pump":    ([(0, R, 2), (3, R, 2), (6, D5, 2), (8, R, 2), (10, R8, 2), (14, B7, 2)],
                      [(0, R, 2), (3, D3, 2), (6, D5, 2), (8, R, 2), (11, B7, 1), (12, D5, 2), (14, LT, 2)]),
    "trap_808":      ([(0, R, 6), (7, R, 3), (10, R, 6)],
                      [(0, R, 3), (3, R, 5), (10, D5, 4), (14, R8, 2)]),
    "walking_jazz":  ([(0, R, 4), (4, D3, 4), (8, D5, 4), (12, D6, 4)],
                      [(0, R8, 4), (4, B7, 4), (8, D5, 4), (12, C5, 4)]),
    "walking_alt":   ([(0, R, 4), (4, D2, 4), (8, D3, 4), (12, D5, 4)],
                      [(0, D6, 4), (4, D5, 4), (8, D3, 4), (12, LT, 4)]),
    "two_feel":      ([(0, R, 7), (8, L5, 7)],
                      [(0, R, 7), (8, D5, 4), (12, LT, 4)]),
    "country_2beat": ([(0, R, 6), (8, L5, 6)],
                      [(0, R, 6), (8, L5, 3), (12, L6, 2), (14, LT, 2)]),
    "boogie_8":      ([(0, R, 2), (2, D3, 2), (4, D5, 2), (6, D6, 2), (8, B7, 2), (10, D6, 2), (12, D5, 2), (14, D3, 2)],
                      [(0, R, 2), (2, R8, 2), (4, B7, 2), (6, D6, 2), (8, D5, 2), (10, B5, 2), (12, D4, 2), (14, D3, 2)]),
    "salsa_tumbao":  ([(6, D5, 4), (12, R, 5)],
                      [(6, L5, 4), (12, R, 5)]),
    "bossa_root5":   ([(0, R, 5), (6, L5, 2), (8, L5, 5), (14, R, 2)],
                      [(0, R, 5), (6, D5, 2), (8, D5, 5), (14, LT, 2)]),
    "samba_surdo":   ([(0, R, 3), (3, L5, 1), (4, L5, 4), (8, R, 3), (11, L5, 1), (12, L5, 4)],
                      [(0, R, 3), (4, L5, 4), (8, R, 3), (12, D5, 2), (14, LT, 2)]),
    "bachata_sync":  ([(0, R, 5), (6, D5, 2), (8, R, 4), (12, D5, 4)],
                      [(0, R, 5), (6, L5, 2), (8, D3, 4), (12, D5, 2), (14, LT, 2)]),
    "cumbia_triad":  ([(0, R, 4), (6, D3, 2), (8, D5, 4), (14, D3, 2)],
                      [(0, R, 4), (6, D3, 2), (8, D5, 4), (12, R8, 2), (14, D5, 2)]),
    "reggae_drop":   ([(2, D3, 2), (4, D5, 3), (8, R, 5), (14, L5, 2)],
                      [(4, R, 3), (8, D5, 3), (12, L6, 2), (14, L5, 2)]),
    "reggaeton_sub": ([(0, R, 5), (6, R, 2), (8, R, 4), (14, L5, 2)],
                      [(0, R, 5), (6, D5, 2), (8, R, 4), (12, B7, 2), (14, D5, 2)]),
    "funk_16":       ([(0, R, 2), (3, R8, 1), (6, B7, 2), (8, R, 2), (10, D5, 2), (13, B3, 1), (14, D3, 2)],
                      [(0, R, 2), (3, R8, 1), (6, D5, 2), (9, B5, 1), (10, D5, 2), (12, B7, 2), (14, R8, 2)]),
    "slap_machine":  ([(0, R, 1), (2, R8, 1), (3, R, 1), (6, R8, 1), (8, R, 1), (10, R8, 1), (12, B7, 2), (14, D5, 2)],
                      [(0, R, 1), (2, R8, 1), (4, D3, 2), (6, D5, 1), (8, R, 1), (10, R8, 1), (12, D6, 1), (14, B7, 2)]),
    "motown_soul":   ([(0, R, 3), (3, D3, 1), (4, D5, 3), (8, D6, 3), (12, D5, 4)],
                      [(0, R, 3), (4, R, 2), (6, D3, 2), (8, D5, 2), (10, D6, 2), (12, B7, 2), (14, D6, 2)]),
    "ballad_warm":   ([(0, R, 7), (8, D5, 7)],
                      [(0, R, 7), (8, L5, 4), (12, D5, 4)]),
    "tango_marcato": ([(0, R, 2), (4, D5, 2), (8, R, 2), (12, L5, 2), (14, LT, 2)],
                      [(0, R, 2), (4, D3, 2), (8, D5, 2), (12, S5, 2), (14, D5, 2)]),
    "tango_332":     ([(0, R, 5), (6, R, 5), (12, L5, 4)],
                      [(0, R, 5), (6, D5, 5), (12, S5, 2), (14, D5, 2)]),
    "oriental_maq":  ([(0, R, 5), (6, D5, 2), (8, R, 5), (14, L5, 2)],
                      [(0, R, 5), (6, B7, 2), (8, D5, 4), (12, D4, 2), (14, D3, 2)]),
}


def build_bass_events(bp: dict, bar_steps: int) -> list:
    total = bar_steps * 2
    evs = []
    custom = bp.get("bass_pat")
    if custom:
        # Custom list of (step, deg, dur) across 1 bar or 2 bars
        max_st = max(x[0] for x in custom)
        if max_st < bar_steps:
            for bar in (0, 1):
                for idx, item in enumerate(custom):
                    st_i, deg, dur = item[0], item[1], item[2]
                    # Subtle musical bar-2 turnaround on final note if not already 2-bar
                    if bar == 1 and idx == len(custom) - 1 and deg == R:
                        deg = L5
                    _add_ev(evs, bar * bar_steps + st_i, total, T_BASS, deg, dur, 90, V_ALL)
        else:
            for item in custom:
                _add_ev(evs, item[0], total, T_BASS, item[1], item[2], 90, V_ALL)
        return evs

    b_mode = bp.get("bass_mode", "pop_sync")
    if bar_steps == 12 and bp.get("meter") == "3/4":
        b0 = [(0, R, 6), (8, L5, 4)] if b_mode != "waltz_walk" else [(0, R, 4), (4, D3, 4), (8, D5, 4)]
        b1 = [(0, R, 6), (4, D5, 4), (8, LT, 4)] if b_mode != "waltz_walk" else [(0, R8, 4), (4, D5, 4), (8, D3, 4)]
    elif bar_steps == 12 and bp.get("meter") == "6/8":
        b0 = [(0, R, 5), (6, D5, 5)]
        b1 = [(0, R, 5), (6, L5, 3), (10, LT, 2)]
    elif bar_steps == 12 and bp.get("meter") == "12/8":
        b0 = [(0, R, 3), (3, D3, 3), (6, D5, 3), (9, D6, 3)] if "walk" in b_mode or "blues" in b_mode else [(0, R, 5), (6, D5, 4), (9, R8, 3)]
        b1 = [(0, R, 5), (6, L5, 3), (9, D5, 3)]
    elif bar_steps == 8:  # 2/4
        b0 = [(0, R, 3), (4, L5, 3)]
        b1 = [(0, R, 3), (4, D5, 2), (6, LT, 2)]
    elif bar_steps == 18:  # 9/8 (0, 4, 8, 12, 14)
        b0 = [(0, R, 4), (4, D5, 4), (8, R, 4), (12, L5, 3), (15, R, 3)]
        b1 = [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, B7, 3), (15, D5, 3)]
    elif bar_steps == 24:  # 6/4
        b0 = [(0, R, 8), (8, D3, 8), (16, D5, 8)]
        b1 = [(0, R, 8), (12, L5, 8), (20, D5, 4)]
    else:
        b0, b1 = BASS_PATTERNS_4_4.get(b_mode, BASS_PATTERNS_4_4["pop_sync"])

    for st_i, deg, dur in b0:
        _add_ev(evs, st_i, total, T_BASS, deg, dur, 90, V_ALL)
    for st_i, deg, dur in b1:
        _add_ev(evs, bar_steps + st_i, total, T_BASS, deg, dur, 92, V_ALL)
    return evs


# ============================================================================
# ACCOMPANIMENT 1..5 BUILDERS (RHYTHM, INTERLOCKING ARP, PAD, HORNS, HOOK)
# ============================================================================
def build_accompaniment_events(bp: dict, bar_steps: int) -> list:
    total = bar_steps * 2
    evs = []

    # --- ACC 1: Primary Rhythm (Strum / Comp / Montuno / Power Chug / Arpeggio / Pompe) ---
    a1_mode = bp.get("acc1_mode", "pop_strum")
    a1_code = bp.get("acc1_code", CLOSE)
    a1_steps = bp.get("acc1_steps")

    for bar in (0, 1):
        off = bar * bar_steps
        if a1_steps:
            for item in a1_steps:
                s_i, cd, dur, vel = item[0], item[1], item[2], (item[3] if len(item) > 3 else 74)
                _add_ev(evs, off + s_i, total, T_ACC1, cd, dur, vel, V_ALL)
        elif a1_mode == "pop_strum":
            # Classic campfire/studio acoustic strum: D . D U . U D U (0, 4, 6, 10, 12, 14)
            for s_i, cd, dur, v in ((0, STRUM_DN, 3, 76), (4, CHUCK, 1, 64), (6, STRUM_UP, 2, 66), (10, STRUM_UP, 2, 68), (12, STRUM_DN, 2, 74), (14, STRUM_UP, 2, 62)):
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC1, cd, dur, v, V_ALL if s_i in (0, 6, 12) else V_234)
        elif a1_mode == "travis_pick":
            seq = [(0, R, 2), (2, D5, 2), (4, U3, 2), (6, D5, 2), (8, R8, 2), (10, D5, 2), (12, D3, 2), (14, D5, 2)]
            for s_i, cd, dur in seq:
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC1, cd, dur, 72, V_ALL)
        elif a1_mode == "piano_arp":
            notes = [R, D5, R8, U3, D5, R8, U3, U5]
            step_inc = 2 if bar_steps >= 12 else 1
            for idx, s_i in enumerate(range(0, bar_steps, step_inc)):
                _add_ev(evs, off + s_i, total, T_ACC1, notes[idx % len(notes)], step_inc + 1, 70 if idx % 2 == 0 else 56, V_ALL)
        elif a1_mode == "waltz_oom_pah":
            _add_ev(evs, off + 4, total, T_ACC1, a1_code, 3, 72, V_ALL)
            _add_ev(evs, off + 8, total, T_ACC1, a1_code, 3, 68, V_ALL)
        elif a1_mode == "jazz_comp":
            comp_st = [(2, JAZZ_SHELL, 2, 68), (10, JAZZ_SHELL, 3, 72)] if bar == 0 else [(0, JAZZ_SHELL, 2, 66), (6, JAZZ_SHELL, 3, 72), (14, JAZZ_SHELL, 2, 64)]
            for s_i, cd, dur, v in comp_st:
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC1, cd, dur, v, V_ALL)
        elif a1_mode == "gypsy_pompe":
            # La Pompe: every quarter beat with crisp heavy 2 & 4 crunch!
            for b in (0, 4, 8, 12):
                is_back = b in (4, 12)
                _add_ev(evs, off + b, total, T_ACC1, CHUCK if is_back else STRUM_DN, 1 if is_back else 2, 86 if is_back else 68, V_ALL)
        elif a1_mode == "stride_piano":
            for b in range(0, bar_steps, 4):
                if b + 2 < bar_steps:
                    _add_ev(evs, off + b + 2, total, T_ACC1, JAZZ_SHELL, 2, 76, V_ALL)
        elif a1_mode == "boogie_comp":
            for s_i in (0, 3, 6, 8, 12, 14):
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC1, CLOSE, 2, 76, V_ALL)
        elif a1_mode == "salsa_montuno":
            # Authentic Cuban Piano Montuno: syncopated offbeat octave-chords!
            m_seq = [(0, MONTUNO, 2, 78), (3, D3, 1, 66), (4, D5, 2, 72), (6, MONTUNO, 2, 80), (10, MONTUNO, 2, 76), (12, D3, 2, 68), (14, MONTUNO, 2, 80)] if bar == 0 else [
                (2, MONTUNO, 2, 78), (6, MONTUNO, 2, 80), (8, D3, 2, 68), (10, MONTUNO, 2, 78), (14, MONTUNO, 2, 82)
            ]
            for s_i, cd, dur, v in m_seq:
                _add_ev(evs, off + s_i, total, T_ACC1, cd, dur, v, V_ALL)
        elif a1_mode == "bossa_violao":
            v_seq = [(0, JAZZ_SHELL, 3, 70), (3, JAZZ_SHELL, 2, 66), (6, JAZZ_SHELL, 3, 68), (10, JAZZ_SHELL, 2, 66), (13, JAZZ_SHELL, 2, 62)] if bar == 0 else [
                (2, JAZZ_SHELL, 3, 68), (6, JAZZ_SHELL, 3, 70), (9, JAZZ_SHELL, 2, 64), (12, JAZZ_SHELL, 3, 68)
            ]
            for s_i, cd, dur, v in v_seq:
                _add_ev(evs, off + s_i, total, T_ACC1, cd, dur, v, V_ALL)
        elif a1_mode == "reggae_skank":
            for b in range(2, bar_steps, 4):
                _add_ev(evs, off + b, total, T_ACC1, CHUCK, 1, 82, V_ALL)
        elif a1_mode == "funk_chuck":
            for s_i in (2, 3, 6, 9, 10, 14, 15):
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC1, CHUCK if s_i not in (6, 14) else HIGH_STAB, 1, 76 if s_i in (6, 14) else 64, V_ALL if s_i in (2, 6, 10, 14) else V_234)
        elif a1_mode == "rock_power_8":
            for s_i in range(0, bar_steps, 2):
                acc = s_i in (0, 6, 8, 12)
                _add_ev(evs, off + s_i, total, T_ACC1, POWER5 if not acc else POWER8, 2, 82 if acc else 64, V_ALL if acc else V_234)
        elif a1_mode == "house_piano":
            for s_i, dur, v in ((0, 3, 84), (3, 2, 76), (6, 3, 82), (10, 2, 74), (12, 2, 80), (14, 2, 76)):
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC1, QUARTAL if bp.get("quartal") else OPEN, dur, v, V_ALL)
        elif a1_mode == "tango_332":
            for s_i in (0, 6, 12):
                _add_ev(evs, off + s_i, total, T_ACC1, CLOSE, 3, 84, V_ALL)
        elif a1_mode == "tango_staccato":
            for s_i in (0, 4, 8, 12):
                _add_ev(evs, off + s_i, total, T_ACC1, CLOSE, 1, 82, V_ALL)
            if bar == 1 and bar_steps >= 16:
                _add_ev(evs, off + 14, total, T_ACC1, HIGH_STAB, 2, 78, V_234)
        elif a1_mode == "oom_pah_off":
            half = 2 if bar_steps == 8 else 2
            for s_i in range(half, bar_steps, half * 2):
                _add_ev(evs, off + s_i, total, T_ACC1, CLOSE, 2, 78, V_ALL)
        elif a1_mode == "turkish_9_8":
            for s_i in (0, 4, 8, 12, 14):
                _add_ev(evs, off + s_i, total, T_ACC1, STRUM_DN if s_i in (0, 12) else CHUCK, 2 if s_i in (0, 12) else 1, 78, V_ALL)
        else:
            # Piano / EP rhythmic comping
            for s_i in (0, 6, 8, 14) if bar == 0 else (0, 3, 6, 12):
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC1, a1_code, 3, 74, V_ALL)

        # --- ACC 2: Secondary Interlocking Part (Banjo Roll / Clean Arp / Rhodes / Cavaquinho / Pizz) ---
        a2_mode = bp.get("acc2_mode", "arp_16")
        a2_seq = bp.get("acc2_seq")
        if a2_seq:
            for item in a2_seq:
                s_i, cd, dur = item[0], item[1], item[2]
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC2, cd, dur, 68, V_234)
        elif a2_mode == "banjo_roll":
            # Authentic 8-note Scruggs forward-backward 16th roll!
            roll = [R, D3, U5, R, D5, U3, D5, D3, R, D3, U5, R8, U3, D5, D3, R]
            for s_i in range(min(bar_steps, 16)):
                _add_ev(evs, off + s_i, total, T_ACC2, roll[s_i], 1, 70 if s_i % 4 == 0 else 56, V_234)
        elif a2_mode == "synth_seq_16":
            seq = [R, R8, D5, R8, D3, R8, D5, U3]
            for s_i in range(bar_steps):
                _add_ev(evs, off + s_i, total, T_ACC2, seq[s_i % len(seq)], 1, 66 if s_i % 4 == 0 else 50, V_234)
        elif a2_mode == "offbeat_chop":
            step_w = 4 if bar_steps >= 12 else 2
            for s_i in range(step_w // 2, bar_steps, step_w):
                _add_ev(evs, off + s_i, total, T_ACC2, CHUCK, 1, 68, V_234)
        elif a2_mode == "rhodes_color":
            for s_i in ([4, 14] if bar_steps >= 16 else [bar_steps // 2]):
                _add_ev(evs, off + s_i, total, T_ACC2, JAZZ_SHELL, 4, 64, V_234)
        else:
            arp = [D3, D5, R8, D5]
            for idx, s_i in enumerate(range(2, bar_steps, 4)):
                _add_ev(evs, off + s_i, total, T_ACC2, arp[idx % len(arp)], 2, 62, V_234)

        # --- ACC 3: Harmonic Pad / Strings / Organ Swell / Trance Gate (Var 2/3..4) ---
        a3_mode = bp.get("acc3_mode", "pad_hold")
        if a3_mode == "trance_gate":
            for s_i in (0, 2, 3, 6, 8, 10, 11, 14):
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC3, OPEN, 1, 66, V_34)
        elif a3_mode == "mandolin_chop":
            for s_i in (4, 12) if bar_steps >= 16 else [4]:
                _add_ev(evs, off + s_i, total, T_ACC3, CHUCK, 1, 76, V_ALL)
        elif a3_mode == "organ_bubble":
            for s_i in range(1, bar_steps, 2):
                _add_ev(evs, off + s_i, total, T_ACC3, CLOSE, 1, 58, V_234)
        elif a3_mode == "spiccato_8":
            for s_i in range(0, bar_steps, 2):
                _add_ev(evs, off + s_i, total, T_ACC3, CLOSE, 1, 68 if s_i % 4 == 0 else 52, V_234)
        else:
            _add_ev(evs, off + 0, total, T_ACC3, OPEN, bar_steps, 58, V_34)

        # --- ACC 4: Brass / Horn / String Section Stabs or Harmonized Thirds (Var 3..4) ---
        a4_mode = bp.get("acc4_mode", "horn_stabs")
        a4_steps = bp.get("acc4_steps")
        if a4_steps:
            for item in a4_steps:
                s_i, cd, dur = item[0], item[1], item[2]
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC4, cd, dur, 76, V_34)
        elif a4_mode == "thirds_swell":
            if bar == 1:
                _add_ev(evs, off + 0, total, T_ACC4, THIRDS, bar_steps // 2, 70, V_34)
                _add_ev(evs, off + bar_steps // 2, total, T_ACC4, HIGH_STAB, bar_steps // 2, 74, V_4)
        elif a4_mode == "Mariachi_tpts":
            if bar == 1:
                for s_i, cd, dur in ((0, THIRDS, 2), (2, THIRDS, 2), (4, HIGH_STAB, 4)):
                    if s_i < bar_steps:
                        _add_ev(evs, off + s_i, total, T_ACC4, cd, dur, 80, V_34)
        else:
            stab_st = [14] if bar == 0 else [6, 14]
            for s_i in stab_st:
                if s_i < bar_steps:
                    _add_ev(evs, off + s_i, total, T_ACC4, HIGH_STAB, 2, 76, V_34)

    # --- ACC 5: Signature Style Hook / Riff / Counter-Melody (2-Bar Span, Var 3/4 + Intro 1) ---
    hook = bp.get("hook")
    hook_mask = bp.get("hook_mask", V_4)
    if hook:
        for item in hook:
            s_i, cd, dur = item[0], item[1], item[2]
            vel = item[3] if len(item) > 3 else 78
            mk = item[4] if len(item) > 4 else hook_mask
            _add_ev(evs, s_i % total, total, T_ACC5, cd, dur, vel, mk)

    return evs


# ============================================================================
# SECTION BUILDERS: INTRO 1/2/3, FILLS 1..4, BREAK, ENDINGS 1/2/3
# ============================================================================
def build_sections(bp: dict, bar_steps: int, main_evs: list) -> dict:
    two_bars = bar_steps * 2
    fill_type = bp.get("fill_type", "pop")
    cadence_key = bp.get("cadence", "pop_IV_V")
    intro_harm, end_harm = CADENCE_SHIFTS.get(cadence_key, CADENCE_SHIFTS["pop_IV_V"])

    # 1. INTRO 1 (mask=1, melodic motif + cadence) & INTRO 2 (mask=2, chord groove)
    intro_evs = []
    for ev in main_evs:
        st_i, trk, cd, dur, vel, vmask = ev
        if vmask & V2:
            # Intro 2 uses clean verse groove + bar-2 pickup; Intro 1 adds Acc3/Acc4 + signature hook!
            intro_evs.append([st_i, trk, cd, dur, vel, 3 if trk in (T_DRUM, T_PERC, T_BASS, T_ACC1) else 1])
    hook = bp.get("hook") or [(0, R8, 4, 84), (4, U3, 4, 80), (8, U5, 6, 86)]
    for item in hook:
        s_i, cd, dur = item[0] % two_bars, item[1], item[2]
        intro_evs.append([s_i, T_ACC5, cd, dur, 86, 1])
    # Final beat pickup snare/cymbal into Measure 1
    intro_evs.append([two_bars - 2, T_DRUM, 38, 1, 84, 3])
    intro_evs.append([two_bars - 1, T_DRUM, 49, 2, 76, 1])

    # 2. INTRO 3: 1-Bar Authentic Genre Count-In + Pickup
    count_in = []
    click_note = 75 if fill_type == "latin_timbale" else (62 if fill_type == "oriental_darbuka" else (85 if fill_type == "flamenco_rasg" else 37))
    sub_step = max(2, bar_steps // max(2, METER_SPECS[bp.get("meter", "4/4")][0]))
    for s_i in range(0, bar_steps, sub_step):
        count_in.append([s_i, T_DRUM, click_note, 1, 82 if s_i == 0 else 68])
    if bar_steps >= 8:
        count_in.append([bar_steps - 2, T_DRUM, 38, 1, 78])
        count_in.append([bar_steps - 2, T_BASS, L5, 2, 82])

    # 3. FILLS 1..4 (1-Bar, graded intensity bitmasks 1|2|4|8)
    fill_evs = []
    half = bar_steps // 2
    # First half keeps pocket
    for ev in main_evs:
        if ev[0] < half and ev[1] in (T_DRUM, T_PERC, T_BASS, T_ACC1) and (ev[5] & V2):
            fill_evs.append([ev[0], ev[1], ev[2], ev[3], ev[4], V_ALL])
    # Second half genre-specific drum/percussion/bass fill!
    rem = bar_steps - half
    for idx, s_i in enumerate(range(half, bar_steps)):
        prog = idx / max(1, rem - 1)
        vel = int(68 + prog * 28)
        if fill_type == "latin_timbale":
            n = 65 if idx % 2 == 0 else (66 if idx < rem - 2 else 56)
            fill_evs.append([s_i, T_PERC, n, 1, vel, V_ALL if idx % 2 == 0 else V_34])
        elif fill_type == "oriental_darbuka":
            n = 64 if idx in (0, rem // 2) else 62
            fill_evs.append([s_i, T_PERC, n, 1, vel, V_ALL if idx % 2 == 0 else V_234])
        elif fill_type == "jazz_triplet":
            if idx % 2 == 0 or idx >= rem - 2:
                fill_evs.append([s_i, T_DRUM, 38 if idx < rem - 2 else 51, 1, vel, V_ALL])
        elif fill_type == "edm_riser":
            fill_evs.append([s_i, T_DRUM, 38 if idx < rem - 1 else 39, 1, vel, V_ALL if idx % 2 == 0 else V_34])
        elif fill_type == "flamenco_rasg":
            fill_evs.append([s_i, T_PERC, 39 if idx % 2 == 0 else 85, 1, vel, V_ALL])
            if idx in (0, rem // 2):
                fill_evs.append([s_i, T_ACC1, STRUM_DN, 2, 84, V_234])
        elif fill_type == "orchestral_timp":
            if idx % 2 == 0:
                fill_evs.append([s_i, T_DRUM, 41 if idx % 4 == 0 else 45, 2, vel, V_ALL])
        else:
            # Descending Toms (50 -> 48 -> 47 -> 45 -> 43) + Snare crack!
            toms = [50, 48, 47, 45, 43, 38]
            tn = toms[min(len(toms) - 1, int(prog * len(toms)))]
            mk = V_ALL if idx % 2 == 0 else (V_234 if idx >= rem - 3 else V_4)
            fill_evs.append([s_i, T_DRUM, tn, 1, vel, mk])
    # Bass walkup & Brass kick at end of Fill 3/4
    if bar_steps >= 8:
        fill_evs.append([bar_steps - 2, T_BASS, LT, 2, 88, V_234])
        fill_evs.append([bar_steps - 2, T_ACC4, HIGH_STAB, 2, 82, V_34])

    # 4. 1-BAR BREAK (Punch on Beat 1 + suspense silence + pickup into next bar)
    brk_evs = [
        [0, T_DRUM, 36, 2, 96],
        [0, T_DRUM, 49, 4, 82],
        [0, T_BASS, R, 3, 94],
        [0, T_ACC1, a1_hit_code(bp), 3, 88],
        [0, T_ACC4, HIGH_STAB, 2, 84],
    ]
    if bar_steps >= 6:
        brk_evs.append([bar_steps - 2, T_DRUM, 38, 1, 78])
        brk_evs.append([bar_steps - 1, T_BASS, L5, 1, 80])

    # 5. ENDINGS 1 (mask=1 cadence+melody), 2 (mask=2 groove tag), 3 (mask=4 quick rit/stop)
    end_evs = []
    # Bar 1: Ending 1 & 2 groove lead-in; Ending 3 immediate dramatic 2-hit cadence!
    for ev in main_evs:
        if ev[0] < bar_steps and ev[1] in (T_DRUM, T_PERC, T_BASS, T_ACC1) and (ev[5] & V2):
            end_evs.append([ev[0], ev[1], ev[2], ev[3], ev[4], 3])
    # Ending 1 melodic flourish in Bar 1 -> resolving to Root/3rd in Bar 2!
    end_evs.append([0, T_ACC5, U5, bar_steps // 2, 82, 1])
    end_evs.append([bar_steps // 2, T_ACC5, U3, bar_steps // 2, 80, 1])
    # Ending 3 Bar 1 punchy setup
    end_evs.append([0, T_DRUM, 36, 2, 88, 4])
    end_evs.append([0, T_BASS, L5, bar_steps // 2, 86, 4])
    end_evs.append([0, T_ACC1, OPEN, bar_steps // 2, 78, 4])
    end_evs.append([bar_steps - 2, T_DRUM, 38, 2, 84, 7])
    # Bar 2 Beat 1 (step == bar_steps): Final Tonic Resolution Hit across all Endings 1/2/3!
    fin = bar_steps
    end_evs.extend([
        [fin, T_DRUM, 36, 4, 96, 7],
        [fin, T_DRUM, 49, 8, 82, 7],
        [fin, T_BASS, R, bar_steps - 2, 96, 7],
        [fin, T_ACC1, OPEN, bar_steps - 2, 84, 7],
        [fin, T_ACC3, OPEN, bar_steps - 2, 72, 7],
        [fin, T_ACC4, HIGH_STAB, 4, 80, 3],
        [fin, T_ACC5, R8, bar_steps - 2, 86, 1],
    ])

    return {
        "steps": two_bars,
        "intro1Harm": intro_harm,
        "end1Harm": end_harm,
        "events": sorted(main_evs, key=lambda x: (x[0], x[1])),
        "intro": sorted(intro_evs, key=lambda x: (x[0], x[1])),
        "countIn": sorted(count_in, key=lambda x: (x[0], x[1])),
        "fill": sorted(fill_evs, key=lambda x: (x[0], x[1])),
        "brk": sorted(brk_evs, key=lambda x: (x[0], x[1])),
        "ending": sorted(end_evs, key=lambda x: (x[0], x[1])),
    }


def a1_hit_code(bp: dict) -> int:
    m = bp.get("acc1_mode", "")
    if "power" in m:
        return POWER8
    if "strum" in m or "pompe" in m:
        return STRUM_DN
    if "jazz" in m or "bossa" in m:
        return JAZZ_SHELL
    return HIGH_STAB


def compile_style_from_blueprint(style_id: str, name: str, category: str, bp: dict, sounds_list: list, exact_map: dict, pads_by_group: dict, matcher: dict, pick_sound_fn) -> dict:
    """Compile a full 8-track Style object + MIDI arrangement from its individual blueprint."""
    meter = bp.get("meter", "4/4")
    beats_per_bar, sub_per_beat, beat_dur_scale = METER_SPECS[meter]
    bar_steps = beats_per_bar * sub_per_beat
    tempo = max(45, min(215, int(bp["tempo"])))
    swing = round(float(bp.get("swing", 0.0)), 3)
    swing8 = bool(bp.get("swing8", False))

    # Resolve all 8 Accompaniment Tracks against real Pa700 Sounds & Drum Kits
    raw_tracks = bp["tracks"]
    assert len(raw_tracks) == 8, f"Style {style_id} must specify 8 tracks, got {len(raw_tracks)}"
    labels = ["Drum", "Perc", "Bass", "Acc1", "Acc2", "Acc3", "Acc4", "Acc5"]
    default_pans = [64, 52, 64, 42, 86, 50, 78, 36]
    default_gains = [0.95, 0.82, 0.92, 0.84, 0.74, 0.66, 0.78, 0.76]
    default_octs = [0, 0, 0, 0, 0, 0, 0, 1]
    octs = bp.get("octs", default_octs)

    style_tracks = []
    for idx in range(8):
        is_drm = idx in (0, 1)
        snd_rec = resolve_track_sound(raw_tracks[idx], is_drm, sounds_list, exact_map)
        style_tracks.append({
            "id": labels[idx].lower(),
            "label": labels[idx],
            "sound": snd_rec["name"],
            "cc00": snd_rec["cc00"],
            "cc32": snd_rec["cc32"],
            "pc": snd_rec["pc"],
            "gmProgram": snd_rec["gmProgram"],
            "isDrum": is_drm,
            "pan": default_pans[idx],
            "gain": default_gains[idx],
            "oct": octs[idx],
        })

    gs_drum_pc = infer_gs_drum_pc(style_tracks[0]["sound"])

    # Build 2-bar MIDI events + sections
    drum_evs = build_drums_and_perc(bp, bar_steps, sub_per_beat)
    bass_evs = build_bass_events(bp, bar_steps)
    acc_evs = build_accompaniment_events(bp, bar_steps)
    main_evs = drum_evs + bass_evs + acc_evs
    midi_obj = build_sections(bp, bar_steps, main_evs)

    # 4 Pads matched to blueprint or category
    pad_groups = bp.get("pad_groups") or [
        "HIT - Percussion", "SEQ - Guitar", "SEQ - Piano", "HIT - Drum"
    ]
    seed = sum((i + 1) * ord(ch) for i, ch in enumerate(style_id))
    chosen_pads = []
    for k_i in range(4):
        grp_name = pad_groups[k_i % len(pad_groups)]
        grp_list = pads_by_group.get(grp_name) or pads_by_group.get("HIT - Percussion")
        p_obj = grp_list[(seed + k_i * 11) % len(grp_list)]
        chosen_pads.append({"id": p_obj["id"], "name": p_obj["name"], "type": p_obj["type"]})

    # 4 Single Touch Settings (STS) tailored specifically to this style's lead & backing instruments!
    sts_queries = bp.get("sts") or [
        raw_tracks[3], raw_tracks[4], raw_tracks[6], raw_tracks[7]
    ]
    sts_sounds = [pick_sound_fn(matcher, [q], None) for q in sts_queries]
    low_snd = pick_sound_fn(matcher, [bp.get("low_voice", "Warm Pad"), "Real Strings 1"], ["Synth Pad", "Strings & Vocal"])
    kbd_sets = [
        {"name": f"{name[:12]} STS 1", "up1": sts_sounds[0], "up2": sts_sounds[3], "up2Muted": True,  "up3": sts_sounds[2], "up3Muted": True,  "low": low_snd},
        {"name": f"{name[:12]} STS 2", "up1": sts_sounds[1], "up2": sts_sounds[0], "up2Muted": False, "up3": sts_sounds[3], "up3Muted": True,  "low": low_snd},
        {"name": f"{name[:12]} STS 3", "up1": sts_sounds[2], "up2": sts_sounds[1], "up2Muted": False, "up3": sts_sounds[0], "up3Muted": True,  "low": low_snd},
        {"name": f"{name[:12]} Tutti", "up1": sts_sounds[3], "up2": sts_sounds[2], "up2Muted": False, "up3": sts_sounds[1], "up3Muted": False, "low": low_snd},
    ]

    return {
        "meter": meter,
        "beatsPerBar": beats_per_bar,
        "subPerBeat": sub_per_beat,
        "beatDurScale": beat_dur_scale,
        "patternBars": 2,
        "tempo": tempo,
        "swing": swing,
        "swing8": swing8,
        "groove": bp.get("groove_tag", style_id),
        "gsDrumPc": gs_drum_pc,
        "bassProgram": style_tracks[2]["gmProgram"],
        "comp1Program": style_tracks[3]["gmProgram"],
        "comp2Program": style_tracks[5]["gmProgram"],
        "drumKitPc": gs_drum_pc,
        "styleTracks": style_tracks,
        "midi": midi_obj,
        "pads": chosen_pads,
        "kbdSets": kbd_sets,
    }


def midi_pattern_fingerprint(style_obj: dict) -> str:
    """Return a canonical string fingerprint of the style's MIDI events (ignoring instrument names!)."""
    m = style_obj["midi"]
    # Fingerprint strictly the musical rhythm/pitch/meter/swing notes so uniqueness is 100% genuine MIDI pattern uniqueness!
    core = {
        "meter": style_obj["meter"],
        "swing": style_obj["swing"],
        "swing8": style_obj["swing8"],
        "events": [(e[0], e[1], e[2], e[3], e[5]) for e in m["events"]],
    }
    return json.dumps(core, separators=(",", ":"))
