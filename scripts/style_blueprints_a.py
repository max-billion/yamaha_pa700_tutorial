#!/usr/bin/env python3
"""
Individually Curated Musical Blueprints for Korg Pa700 Styles — Part A (183 Styles):
  1. Pop (37)
  2. Ballad (32)
  3. Ballroom (24)
  4. Dance (32)
  5. Rock (34)
  6. Country (24)

Every style is crafted specifically for its Pa700 title, song/artist tribute,
meter, groove feel, 8-track instrumentation, bassline, rhythm voicings, and melodic hook.
"""

from style_midi_composer import (
    R, D2, D3, D4, D5, D6, D7, B7, R8, L5, LR, U9, U3, U5, U8,
    B5, LT, B2, S5, B3, L6, L4, A5, C5, U6, UB7,
    CLOSE, OPEN, HIGH_STAB, JAZZ_SHELL, POWER5, POWER8,
    STRUM_DN, STRUM_UP, CHUCK, MONTUNO, QUARTAL, THIRDS, FOURTHS,
    V1, V2, V3, V4, V_ALL, V_234, V_34, V_4,
)

BLUEPRINTS_A = {
    # =========================================================================
    # 1. POP (37 Styles)
    # =========================================================================
    # Marvin Gaye ("Sexual Healing" / "What's Going On"): 808 analog rim/conga pocket, Rhodes, mellow synth/finger bass
    "marvin_g_pop": {
        "meter": "4/4", "tempo": 95, "swing": 0.16,
        "tracks": ["Analog Kit", "Latin Perc.Kit 1", "Synth Bass Warm", "Suit Case88 EP1", "Strat N Cln Mute", "Warm Pad", "Soft Horns 1", "Tenor Sax DN1"],
        "drum_mode": "pop_16", "kick_note": 36, "snare_note": 37,
        "kicks": [0, 3, 8, 10], "snares": [4, 12],
        "perc_steps": [(2, 63, 66), (6, 64, 72), (11, 62, 60), (14, 63, 70), (15, 64, 62)],
        "bass_pat": [(0, R, 3), (3, D3, 2), (6, D5, 2), (8, R, 4), (14, B7, 2)],
        "acc1_mode": "jazz_comp", "acc2_mode": "offbeat_chop", "acc3_mode": "pad_hold",
        "hook": [(2, D5, 2), (4, D6, 2), (6, R8, 4), (18, U3, 2), (20, D6, 2), (22, D5, 4)],
        "cadence": "jazz_ii_V", "fill_type": "funk_sync",
    },
    # John Legend ("All of Me"): Intimate rolling 8th/16th grand piano ballad-pop pulse (3+3+2 chord accent!)
    "all_begins_pop": {
        "meter": "4/4", "tempo": 66, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "Finger Bass DN1", "Concert Grand", "RealFolk Gtr DNC", "Real Strings 1", "Cello", "Warm Pad"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6, 12], "snares": [12],
        "bass_pat": [(0, R, 6), (6, R, 6), (12, L5, 4)],
        "acc1_steps": [(0, OPEN, 5, 78), (6, OPEN, 5, 76), (12, CLOSE, 4, 74)],
        "acc2_seq": [(2, D5, 2), (4, R8, 2), (8, U3, 2), (10, D5, 2), (14, R8, 2)],
        "acc3_mode": "pad_hold",
        "hook": [(0, U3, 6), (6, R8, 6), (12, D5, 4), (16, U5, 6), (22, U3, 6), (28, R8, 4)],
        "cadence": "pop_IV_V", "fill_type": "pop",
    },
    # The Weeknd ("Can't Feel My Face"): 108 BPM disco-funk octave bass, Nile Rodgers 16th Strat, crisp clap/snare
    "can_t_feel_pop": {
        "meter": "4/4", "tempo": 108, "swing": 0.08,
        "tracks": ["Dance Kit", "Standard PercKit", "JB Slap Bass", "Strat N Cln Mute", "Pop Grand", "Analog Pad 1", "Tight Brass 1", "Octo Lead"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "perc_steps": [(4, 39, 82), (12, 39, 84)],
        "bass_pat": [(0, R, 2), (2, R8, 1), (3, B7, 1), (6, D5, 2), (8, R, 2), (10, R8, 2), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "funk_chuck", "acc2_seq": [(0, CLOSE, 3), (6, CLOSE, 3), (12, HIGH_STAB, 3)],
        "hook": [(0, R8, 2), (3, B7, 2), (6, D5, 3), (12, D3, 2), (14, D5, 2), (16, R8, 4)],
        "cadence": "modal_bVII", "fill_type": "funk_sync",
    },
    # Upbeat acoustic/electric strummed pop ("Wake Me Up" / Katy-style fast guitar pop)
    "fast_guitar_pop": {
        "meter": "4/4", "tempo": 126, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "SteelGtrPro DNC", "Strat N Cln DNC", "Pop Grand", "Warm Pad", "Bright Piano"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "perc_steps": [(2, 54, 58), (6, 54, 62), (10, 54, 58), (14, 54, 64)],
        "bass_mode": "root_8",
        "acc1_steps": [(0, STRUM_DN, 2, 80), (2, STRUM_DN, 2, 68), (4, CHUCK, 1, 74), (6, STRUM_UP, 2, 74), (8, STRUM_DN, 2, 78), (10, STRUM_UP, 2, 70), (12, CHUCK, 1, 74), (14, STRUM_UP, 2, 72)],
        "acc2_seq": [(0, R8, 2), (4, U3, 2), (8, U5, 2), (12, U3, 2)],
        "hook": [(0, U5, 3), (3, U3, 3), (6, R8, 2), (16, U3, 3), (19, D5, 3), (22, R8, 4)],
    },
    # Dramatic Pop Farewell ("Time to Say Goodbye" / Sam Smith): sweeping piano triplets/arpeggios + lush strings
    "goodbye_pop": {
        "meter": "4/4", "tempo": 92, "swing": 0.0,
        "tracks": ["Studio Kit", "Standard PercKit", "Finger Bass DN1", "Pop Grand", "Nylon GuitarDNC", "Movie Str.1 DNC", "French Section", "Oboe 1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 7, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (7, L5, 1), (8, D5, 4), (12, L6, 4)],
        "acc1_mode": "piano_arp", "acc2_mode": "travis_pick", "acc4_mode": "thirds_swell",
        "hook": [(0, R8, 4), (4, U3, 4), (8, U5, 6), (14, U6, 2), (16, U5, 8), (24, U3, 8)],
        "cadence": "pop_IV_V", "fill_type": "orchestral_timp",
    },
    # 1970s California Soft-Rock Guitar Pop (Bread / America / Fleetwood Mac): warm 12-string, Wurly, flatwound bass
    "70_s_guitar_pop": {
        "meter": "4/4", "tempo": 98, "swing": 0.06,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Strum 12Str. DNC", "Wurly Logic", "Warm Strings", "Harmonica 1 DN1", "RealFolk Gtr DNC"],
        "drum_mode": "pop_8", "kicks": [0, 8, 11], "snares": [4, 12],
        "perc_steps": [(0, 70, 50), (4, 54, 62), (8, 70, 50), (12, 54, 64)],
        "bass_pat": [(0, R, 5), (6, D3, 2), (8, D5, 5), (14, D6, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "rhodes_color",
        "hook": [(4, U3, 2), (6, D5, 2), (8, D6, 4), (20, R8, 2), (22, D6, 2), (24, D5, 4)],
    },
    # Bread-and-butter Korg Pa700 Reference 8-Beat Pop
    "8beat_standard": {
        "meter": "4/4", "tempo": 112, "swing": 0.0,
        "tracks": ["Standard Kit Amb", "Standard PercKit", "Finger Bass DN1", "Concert Grand", "SteelGtrPro DNC", "Real Strings 1", "Tight Brass 1", "Strat N Cln DNC"],
        "drum_mode": "pop_8", "kicks": [0, 8, 10], "snares": [4, 12],
        "bass_mode": "pop_sync",
        "acc1_steps": [(0, OPEN, 4, 78), (4, CLOSE, 3, 68), (8, OPEN, 4, 76), (12, CLOSE, 3, 70)],
        "acc2_seq": [(2, STRUM_UP, 2), (6, STRUM_UP, 2), (10, STRUM_UP, 2), (14, STRUM_UP, 2)],
        "hook": [(0, R8, 2), (2, D5, 2), (4, U3, 4), (16, U5, 2), (18, U3, 2), (20, R8, 4)],
    },
    # Crisp Studio 16-Beat Pop (Toto / Hall & Oates / Whitney mid-tempo 16th hi-hat pocket)
    "standard_16_beat": {
        "meter": "4/4", "tempo": 99, "swing": 0.10,
        "tracks": ["Studio Kit", "Standard PercKit", "JB Finger BsDN1", "Tine EP Dyno", "Strat N Cln Mute", "Warm Pad", "PopAltoSax DN1", "Bell Tine EP"],
        "drum_mode": "pop_16", "kicks": [0, 7, 10], "snares": [4, 12],
        "perc_steps": [(2, 69, 52), (6, 69, 56), (10, 69, 52), (14, 69, 58)],
        "bass_pat": [(0, R, 4), (6, L5, 1), (7, R, 3), (10, D5, 3), (14, B7, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 3, 76), (3, JAZZ_SHELL, 2, 68), (8, JAZZ_SHELL, 4, 74), (14, HIGH_STAB, 2, 70)],
        "acc2_mode": "funk_chuck",
        "hook": [(6, U3, 1), (7, U5, 3), (22, U5, 1), (23, R8, 3)],
    },
    # Romantic Mid-Tempo Love Pop ("Love Me Like You Do" / Leona Lewis shimmering synth-piano pop)
    "love_pop": {
        "meter": "4/4", "tempo": 100, "swing": 0.0,
        "tracks": ["Pop Kit Amb", "Standard PercKit", "Synth Bass Warm", "Grand&MovingPad", "Chorus Guitar", "Real Strings 2", "Warm Pad", "Bell Tine EP"],
        "drum_mode": "pop_8", "kicks": [0, 3, 8, 11], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, R, 3), (8, D5, 3), (11, L5, 5)],
        "acc1_steps": [(0, OPEN, 3, 76), (3, CLOSE, 3, 72), (8, OPEN, 3, 76), (11, CLOSE, 5, 72)],
        "acc2_seq": [(0, R8, 2), (2, D5, 2), (6, U3, 2), (10, R8, 2), (14, D5, 2)],
        "hook": [(0, U5, 3), (3, U3, 3), (6, R8, 2), (11, D6, 5), (16, U3, 3), (19, R8, 5)],
    },
    # Jason Mraz / Jack Johnson laid-back Soft Acoustic Guitar Pop ("I'm Yours")
    "soft_guitar_pop": {
        "meter": "4/4", "tempo": 94, "swing": 0.16,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "RealFolk Gtr DNC", "Real Ukulele", "Wurly Clean", "Warm Pad", "Whistle DN1"],
        "drum_mode": "pop_8", "snare_note": 37, "kicks": [0, 8], "snares": [4, 12],
        "perc_steps": [(2, 70, 52), (6, 70, 58), (10, 70, 52), (14, 70, 58)],
        "bass_pat": [(0, R, 4), (6, D3, 2), (8, D5, 4), (12, D6, 2), (14, D5, 2)],
        "acc1_steps": [(2, CHUCK, 2, 78), (6, STRUM_UP, 2, 74), (10, CHUCK, 2, 78), (14, STRUM_UP, 2, 74)],
        "acc2_seq": [(0, R8, 2), (4, U3, 2), (8, U5, 2), (12, U3, 2)],
        "hook": [(0, U3, 2), (2, U5, 3), (6, U6, 2), (8, U5, 4), (20, U3, 2), (22, R8, 4)],
    },
    # Ariana Grande ("One Last Time"): 125 BPM progressive EDM-Pop piano chords + pulsing synth bass
    "one_last_pop": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Dance Kit Remix", "Standard PercKit", "Disclosure Bass", "2000’s Piano", "Chorus Gtr Pro", "Big Side Attack", "Next Dance DNC", "Moving Bell"],
        "drum_mode": "four_floor", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (3, R, 3), (6, R, 2), (8, R, 2), (11, D5, 3), (14, B7, 2)],
        "acc1_mode": "house_piano", "acc2_mode": "synth_seq_16", "acc3_mode": "trance_gate",
        "hook": [(0, R8, 3), (3, U3, 3), (6, U5, 2), (8, U3, 4), (16, U5, 3), (19, U6, 3), (22, U5, 4)],
        "fill_type": "edm_riser",
    },
    # Barry Manilow ("Copacabana"): Disco-Show-Latin hybrid! Cowbell, congas, brass punches, montuno piano
    "copacabana_pop": {
        "meter": "4/4", "tempo": 118, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 1", "Finger E.Bass 1", "Bright Piano", "Strat N Cln Mute", "Real Strings 1", "Tight Brass 1", "Whistle DN1"],
        "drum_mode": "disco", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(0, 56, 72), (2, 63, 66), (4, 56, 68), (6, 64, 74), (8, 56, 72), (10, 62, 64), (12, 56, 68), (14, 63, 76), (15, 71, 64, V_4)],
        "bass_pat": [(0, R, 2), (2, R8, 2), (6, D5, 2), (8, R, 2), (10, R8, 2), (12, D5, 2), (14, D6, 2)],
        "acc1_mode": "salsa_montuno", "acc2_mode": "funk_chuck",
        "acc4_steps": [(0, HIGH_STAB, 2), (3, HIGH_STAB, 1), (6, HIGH_STAB, 2), (14, THIRDS, 2)],
        "hook": [(0, D5, 2), (2, R8, 2), (4, U3, 2), (6, U5, 4), (18, U6, 2), (20, U5, 2), (22, U3, 4)],
        "fill_type": "latin_timbale",
    },
    # Stevie Wonder ("As"): Uplifting soul-jazz 4-on-the-floor kick, Clavinet + Fender Rhodes, active melodic bass
    "as_groove": {
        "meter": "4/4", "tempo": 116, "swing": 0.14,
        "tracks": ["Funk Kit 1 Amb", "Latin Perc.Kit 2", "Finger Bass DN1", "Suit Case88 EP1", "Classic Clav DNC", "Warm Strings", "Brass & Sax", "Harmonica 1 DN1"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "perc_steps": [(0, 54, 54), (4, 39, 74), (6, 63, 66), (12, 39, 76), (14, 64, 68)],
        "bass_pat": [(0, R, 2), (2, D2, 2), (4, D3, 2), (6, D5, 2), (8, D6, 2), (10, B7, 2), (12, R8, 2), (14, D5, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 3, 78), (3, JAZZ_SHELL, 2, 72), (6, JAZZ_SHELL, 2, 76), (10, JAZZ_SHELL, 3, 74), (14, JAZZ_SHELL, 2, 72)],
        "acc2_seq": [(1, R, 1), (3, D5, 1), (6, R8, 2), (9, D3, 1), (11, D5, 1), (14, B7, 2)],
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 3), (10, U5, 4), (16, U6, 2), (18, U5, 2), (20, U3, 4)],
        "cadence": "jazz_ii_V", "fill_type": "funk_sync",
    },
    # Modern Top-40 Synth-Guitar Pop (Dua Lipa / Max Martin punchy syncopated synth bass + tight pluck)
    "modern_pop": {
        "meter": "4/4", "tempo": 115, "swing": 0.06,
        "tracks": ["Dance Kit", "Standard PercKit", "Phunk Synth Bass", "Single Coil Pro", "Club E. Piano", "Square Pad", "Tight Brass 2", "Thin PulSeq DNC"],
        "drum_mode": "four_floor", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(4, 39, 80), (11, 37, 58), (12, 39, 82)],
        "bass_pat": [(0, R, 2), (3, R, 2), (6, R8, 2), (8, R, 3), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "funk_chuck", "acc2_mode": "rhodes_color",
        "hook": [(0, U3, 2), (3, R8, 2), (6, D5, 2), (10, R8, 2), (18, U5, 2), (21, U3, 3), (26, R8, 3)],
        "fill_type": "edm_riser",
    },
    # Bruno Mars / Jamiroquai Groovy Pop-Funk
    "groovy_pop": {
        "meter": "4/4", "tempo": 113, "swing": 0.15,
        "tracks": ["Groove Kit", "Standard PercKit", "Dark Bs&Slap DN1", "Strat N Cln DNC", "Tine EP Phaser", "Warm Strings", "Tight Brass 1", "Synth Clav"],
        "drum_mode": "funk_16", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_mode": "funk_16", "acc1_mode": "funk_chuck", "acc2_mode": "rhodes_color",
        "hook": [(0, R8, 1), (2, U3, 2), (6, U5, 2), (14, B7, 2), (16, R8, 2), (22, D5, 3)],
        "fill_type": "funk_sync",
    },
    # Monkees / Smash Mouth ("I'm a Believer"): Bright Vox organ, brisk tambourine 8-beat, bouncy bass
    "believer_pop": {
        "meter": "4/4", "tempo": 160, "swing": 0.0,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "JB Pick Bs DN1", "VOX Legend", "SteelGtrPro DNC", "Pop Grand", "Tight Brass 1", "60’s Organ"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 10], "snares": [4, 12],
        "perc_steps": [(0, 54, 62), (2, 54, 52), (4, 54, 74), (6, 54, 52), (8, 54, 62), (10, 54, 52), (12, 54, 74), (14, 54, 56)],
        "bass_pat": [(0, R, 3), (4, D3, 3), (8, D5, 3), (12, D6, 2), (14, D5, 2)],
        "acc1_steps": [(0, CLOSE, 2, 78), (4, HIGH_STAB, 2, 76), (6, CLOSE, 2, 74), (10, CLOSE, 2, 72), (12, HIGH_STAB, 2, 78)],
        "acc2_mode": "pop_strum",
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 4), (8, U6, 2), (10, U5, 2), (12, U3, 4)],
    },
    # Bobby Hebb / Boney M ("Sunny"): Disco-soul strings, Rhodes, steady walking-octave disco bass
    "sunny_pop": {
        "meter": "4/4", "tempo": 120, "swing": 0.05,
        "tracks": ["Pop Std. Kit 1", "Latin Perc.Kit 1", "Finger E.Bass 2", "Tine EP Dyno", "Strat N Cln Mute", "Real Strings 1", "Jazz Trumpet DN1", "Jazz Flute Expr."],
        "drum_mode": "disco", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, R8, 1), (4, R, 2), (6, D3, 2), (8, D5, 3), (11, R8, 1), (12, B7, 2), (14, D5, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 4, 76), (6, JAZZ_SHELL, 2, 72), (10, JAZZ_SHELL, 3, 74), (14, JAZZ_SHELL, 2, 70)],
        "acc2_mode": "offbeat_chop", "acc4_mode": "thirds_swell",
        "hook": [(2, R8, 2), (4, U3, 2), (6, U5, 4), (18, U5, 2), (20, U3, 2), (22, R8, 4)],
    },
    # Laid-Back Lounge / Sade-style Slow Pop
    "slow_pop": {
        "meter": "4/4", "tempo": 84, "swing": 0.12,
        "tracks": ["Lounge Kit Amb", "Latin Perc.Kit 2", "Fretless Bass 2", "Suit Case88 EP1", "Nylon GuitarDNC", "Warm Pad", "Tenor Sax DN1", "SoftAltoSax DN1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6, 10], "snares": [4, 12],
        "perc_steps": [(2, 70, 48), (6, 63, 60), (10, 70, 48), (14, 64, 62)],
        "bass_pat": [(0, R, 5), (6, D5, 2), (8, R, 4), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "bossa_violao", "acc2_mode": "travis_pick",
        "hook": [(4, D5, 4), (8, D6, 2), (10, R8, 6), (20, U3, 4), (24, R8, 8)],
    },
    # Jess Glynne ("Hold My Hand"): Bright Piano House-Pop with energetic horn section & claps!
    "hold_my_pop": {
        "meter": "4/4", "tempo": 123, "swing": 0.0,
        "tracks": ["House Kit 1", "Standard PercKit", "Synth Bass 1", "M1 Piano", "Strat N Cln DNC", "Warm Strings", "Brass of Power", "PopAltoSax DN1"],
        "drum_mode": "house", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(4, 39, 86), (12, 39, 86), (14, 54, 64)],
        "bass_mode": "house_pump", "acc1_mode": "house_piano",
        "acc4_steps": [(0, HIGH_STAB, 2), (6, HIGH_STAB, 2), (12, THIRDS, 3)],
        "hook": [(0, R8, 2), (3, R8, 2), (6, U3, 3), (10, U5, 2), (12, U3, 2), (14, R8, 2)],
    },
    # Easy Sunday Morning Pop ("Sunday Morning" Maroon 5 neo-soul piano & swing)
    "morning_pop": {
        "meter": "4/4", "tempo": 90, "swing": 0.22,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Finger Bass DN1", "Wurly Amp", "Clean Jazz 1", "Jazz Organ", "Tight Brass 2", "Jazz Sax DN1"],
        "drum_mode": "funk_16", "kicks": [0, 7, 8, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (4, D3, 3), (7, D4, 1), (8, D5, 4), (12, D6, 2), (14, B7, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 3, 76), (6, JAZZ_SHELL, 3, 72), (12, JAZZ_SHELL, 4, 74)],
        "acc2_mode": "offbeat_chop", "acc3_mode": "organ_bubble",
        "hook": [(2, U3, 2), (4, U5, 3), (18, U6, 2), (20, U5, 2), (22, U3, 3)],
        "cadence": "jazz_ii_V",
    },
    # Pharrell Williams ("Happy"): 160 BPM energetic neo-soul Motown shuffle, brisk claps on 2 & 4, pentatonic bass!
    "happy_pop": {
        "meter": "4/4", "tempo": 160, "swing": 0.20, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Bass", "Wurly Logic", "Strat N Cln Mute", "Gospel Organ 1", "Choir Aahs GM", "Tight Brass 1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "perc_steps": [(4, 39, 90), (12, 39, 90), (14, 39, 74)],
        "bass_pat": [(0, R, 3), (4, B3, 2), (6, D3, 2), (8, D5, 3), (12, B7, 2), (14, R8, 2)],
        "acc1_steps": [(2, CLOSE, 2, 78), (6, HIGH_STAB, 2, 80), (10, CLOSE, 2, 76), (14, HIGH_STAB, 2, 80)],
        "acc2_mode": "offbeat_chop",
        "hook": [(0, R8, 2), (4, B7, 2), (6, R8, 4), (16, U3, 2), (20, R8, 2), (22, D5, 4)],
    },
    # Radio Chart Pop Hit (Ed Sheeran "Shape of You" marimba/kalimba trop-pop syncopation!)
    "pop_hit": {
        "meter": "4/4", "tempo": 96, "swing": 0.08,
        "tracks": ["Pop Kit Amb", "Latin Perc.Kit 2", "Synth Bass 1", "Marimba", "Real Nylon Gtr", "Warm Pad", "Chorus Guitar", "Kalimba 1"],
        "drum_mode": "reggaeton_dembow", "kicks": [0, 6, 8, 12], "snares": [3, 6, 11, 14],
        "bass_pat": [(0, R, 3), (3, R, 3), (6, D3, 2), (8, D5, 3), (11, D5, 3), (14, B7, 2)],
        "acc1_steps": [(0, R8, 2, 84), (3, U3, 2, 82), (6, R8, 2, 84), (8, R8, 2, 80), (11, U3, 2, 82), (14, D5, 2, 78)],
        "acc2_mode": "offbeat_chop",
        "hook": [(0, R8, 2), (3, U3, 2), (6, R8, 2), (16, U5, 2), (19, U3, 2), (22, R8, 2)],
    },
    #Billy Joel / Vanessa Carlton / Coldplay ("Clocks" / "A Thousand Miles"): Driving 8th/ostinato Piano Pop!
    "piano_pop": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "JB Finger BsDN1", "Live Piano", "RealFolk Gtr DNC", "Real Strings 1", "Soft Horns 1", "Glockenspiel"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 12], "snares": [4, 12],
        "bass_mode": "root_8",
        "acc1_steps": [(0, U5, 2, 82), (2, U3, 2, 74), (4, R8, 2, 78), (6, U5, 2, 82), (8, U3, 2, 74), (10, R8, 2, 78), (12, U5, 2, 80), (14, U3, 2, 74)],
        "acc2_mode": "pop_strum",
        "hook": [(0, U8, 3), (3, U5, 3), (6, U3, 2), (16, U5, 3), (19, U3, 3), (22, R8, 2)],
    },
    # Smooth West-Coast Yacht-Pop / Maroon-Steely Cool Pop
    "cool_pop": {
        "meter": "4/4", "tempo": 106, "swing": 0.14,
        "tracks": ["Cool Kit Amb", "Standard PercKit", "JB Finger BsDN2", "Tine EP Amp/Pha", "Single Coil", "Warm Pad", "Sweet FlugelHorn", "Jazz Flute Expr."],
        "drum_mode": "pop_16", "kicks": [0, 6, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (4, L5, 2), (6, R, 3), (10, D3, 2), (12, D5, 4)],
        "acc1_mode": "jazz_comp", "acc2_mode": "funk_chuck",
        "hook": [(0, U3, 4), (6, D5, 2), (8, D6, 4), (20, U5, 2), (22, U3, 4)],
    },
    # The Beatles Early 60s Merseybeat ("She Loves You" / "A Hard Day's Night"): Ringo sizzle hats, 12-string jangle!
    "liverpool_1": {
        "meter": "4/4", "tempo": 138, "swing": 0.06,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Pick", "Strum 12Str. DNC", "VOX Legend", "RealFolk Gtr DNC", "Pop Grand", "Harmonica 1 DN1"],
        "drum_mode": "pop_8", "hat_note": 46, "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "perc_steps": [(4, 54, 76), (12, 54, 76), (4, 39, 72, V_34), (12, 39, 72, V_34)],
        "bass_pat": [(0, R, 2), (2, D3, 2), (4, D5, 2), (6, D6, 2), (8, R8, 2), (10, D6, 2), (12, D5, 2), (14, D3, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "offbeat_chop",
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 4), (16, U6, 2), (18, U5, 2), (20, U3, 4)],
    },
    # The Beatles Late-60s ("Penny Lane" / "Ob-La-Di"): Bouncy quarter-note staccato piano, melodic Hofner bass, piccolo trumpet!
    "liverpool_2": {
        "meter": "4/4", "tempo": 114, "swing": 0.12, "swing8": True,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Flat", "Bright Piano", "RealFolk Gtr DNC", "Strings Quartet", "Piccolo", "Concert Trumpet"],
        "drum_mode": "pop_8", "kicks": [0, 8], "snares": [4, 12], "ride_note": 53,
        "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, R8, 2), (14, D5, 2)],
        "acc1_steps": [(0, CLOSE, 2, 80), (4, CLOSE, 2, 78), (8, CLOSE, 2, 80), (12, CLOSE, 2, 78)],
        "acc2_mode": "offbeat_chop", "acc3_mode": "spiccato_8",
        "hook": [(0, U5, 2), (2, U6, 2), (4, U5, 2), (6, U3, 2), (8, R8, 4), (20, U3, 2), (22, U5, 4)],
    },
    # Crisp 90s/00s Acoustic-Synth Pop Beat ("Torn" Natalie Imbruglia)
    "pop_beat": {
        "meter": "4/4", "tempo": 98, "swing": 0.0,
        "tracks": ["Pop Std. Kit 2", "Standard PercKit", "Finger E.Bass 1", "SteelGtrPro DNC", "Strat N Cln DNC", "Warm Pad", "Pop Grand", "E.Gtr Ch/Dly DNC"],
        "drum_mode": "pop_16", "kicks": [0, 6, 10, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, R, 2), (10, R, 4), (14, L5, 2)],
        "acc1_mode": "pop_strum", "acc2_seq": [(0, R8, 2), (3, U3, 2), (6, D5, 2), (10, R8, 2), (14, U3, 2)],
        "hook": [(0, U3, 3), (3, U5, 3), (6, R8, 4), (18, U3, 2), (20, D5, 4)],
    },
    # Toto "Rosanna" / "Everybody Wants to Rule the World": Half-time / 12-feel Easy Pop Shuffle
    "easy_pop_shuffle": {
        "meter": "4/4", "tempo": 106, "swing": 0.28, "swing8": True,
        "tracks": ["Studio Kit", "Standard PercKit", "JB Finger BsDN1", "Pop Grand", "Chorus Guitar", "Analog Pad 1", "Tight Brass 2", "Synth Lead"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "perc_steps": [(2, 70, 50), (6, 70, 58), (10, 70, 50), (14, 70, 58)],
        "bass_pat": [(0, R, 4), (6, D3, 2), (8, D5, 4), (14, D6, 2)],
        "acc1_steps": [(0, OPEN, 2, 76), (2, CLOSE, 2, 64), (4, CLOSE, 2, 74), (8, OPEN, 2, 76), (10, CLOSE, 2, 64), (12, CLOSE, 2, 74)],
        "hook": [(0, U5, 2), (2, R8, 2), (4, U3, 4), (16, U5, 2), (18, U6, 2), (20, U5, 4)],
    },
    # 60s Brill Building / Roy Orbison ("Oh, Pretty Woman" / "Stand By Me" beat)
    "classic_beat": {
        "meter": "4/4", "tempo": 120, "swing": 0.0,
        "tracks": ["VintageKit 1 Amb", "Latin Perc.Kit 1", "Acoustic Bass 1", "Real El. Gtr ST1", "Classic Piano", "Strings&Orch.V.", "Tenor Sax DN1", "Vibraphone 1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "perc_steps": [(0, 81, 56), (6, 73, 62), (12, 74, 66)],
        "bass_pat": [(0, R, 4), (6, D3, 2), (8, D5, 4), (12, R8, 2), (14, D5, 2)],
        "acc1_mode": "pop_strum",
        "hook": [(0, R, 2), (2, R, 2), (4, D3, 2), (6, D5, 2), (8, B7, 4), (16, R8, 4)],
    },
    # ABBA ("Dancing Queen" / "Mamma Mia"): Sparkling layered grand piano gliss/octaves, melodic bass, lush strings
    "classic_pop": {
        "meter": "4/4", "tempo": 104, "swing": 0.0,
        "tracks": ["Pop Std. Kit 1", "Standard PercKit", "JB Pick Bs DN1", "G.Piano Stack 1", "RealFolk Gtr DNC", "Full Strings", "Marimba", "Flute"],
        "drum_mode": "four_floor", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(4, 54, 72), (12, 54, 74)],
        "bass_mode": "disco_oct",
        "acc1_steps": [(0, OPEN, 3, 82), (3, HIGH_STAB, 1, 72), (4, OPEN, 4, 80), (8, OPEN, 3, 82), (12, HIGH_STAB, 4, 80)],
        "acc2_mode": "pop_strum",
        "hook": [(0, U5, 2), (2, U3, 2), (4, U5, 2), (6, U6, 4), (16, U5, 2), (18, U3, 2), (20, R8, 4)],
    },
    # The Shadows ("Apache"): Iconic galloping tom-snare rhythm, brisk acoustic steel guitar, clean echo Strat!
    "shadow_pop": {
        "meter": "4/4", "tempo": 116, "swing": 0.0,
        "tracks": ["VintageKit 2 Amb", "Latin Perc.Kit 1", "Vintage P. Pick", "SteelGtrPro DNC", "Single Coil Pro", "Warm Strings", "French Section", "E.Gtr Ch/Dly DNC"],
        "drum_mode": "pop_8", "kicks": [0, 8], "snares": [4, 12],
        "perc_steps": [(0, 64, 76), (2, 63, 66), (3, 63, 64), (4, 62, 74), (8, 64, 76), (10, 63, 66), (11, 63, 64), (12, 62, 74)],
        "bass_pat": [(0, R, 4), (4, D5, 2), (6, D5, 2), (8, R, 4), (12, L5, 2), (14, L5, 2)],
        "acc1_steps": [(0, STRUM_DN, 3, 80), (3, STRUM_UP, 1, 72), (4, STRUM_DN, 4, 78), (8, STRUM_DN, 3, 80), (11, STRUM_UP, 1, 72), (12, STRUM_DN, 4, 78)],
        "hook": [(0, R8, 3), (3, R8, 1), (4, U3, 4), (8, U5, 6), (16, U6, 3), (19, U5, 1), (20, U3, 6)],
        "cadence": "cinematic_bVI",
    },
    # Kelly Clarkson / Avril / Maroon Pop-Rock
    "pop_rock": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "Crunch Gtr DNC", "RealFolk Gtr DNC", "Rock Piano", "Warm Pad", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "kicks": [0, 6, 8, 10], "snares": [4, 12],
        "bass_mode": "root_8", "acc1_mode": "rock_power_8", "acc2_mode": "pop_strum",
        "hook": [(0, R8, 2), (2, U5, 2), (6, U3, 2), (8, R8, 4), (18, D5, 2), (20, R8, 4)],
        "fill_type": "rock_tom",
    },
    # Amy Winehouse / Duffy ("Valerie" / "Mercy"): 60s Retro Soul-Pop Beat, upright/flat bass, baritone sax, Wurlitzer
    "retro_beat": {
        "meter": "4/4", "tempo": 108, "swing": 0.14,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Wurly Amp", "Strat N Cln DNC", "60’s Organ", "Baritone Sax DN1", "Tight Brass 1"],
        "drum_mode": "motown_4", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "perc_steps": [(4, 54, 78), (12, 54, 78)],
        "bass_pat": [(0, R, 3), (3, R, 1), (4, D3, 2), (6, D5, 2), (8, D6, 3), (12, D5, 4)],
        "acc1_steps": [(2, CLOSE, 2, 78), (6, CLOSE, 2, 76), (10, CLOSE, 2, 78), (14, CLOSE, 2, 76)],
        "hook": [(0, R, 2), (4, D3, 2), (6, D5, 4), (16, D6, 2), (20, D5, 2), (22, D3, 4)],
    },
    # Train / Elton ("Crocodile Rock" / "Hey Soul Sister" bouncy Pop Shuffle)
    "pop_shuffle": {
        "meter": "4/4", "tempo": 116, "swing": 0.28, "swing8": True,
        "tracks": ["Pop Std. Kit 1", "Standard PercKit", "Finger Bass DN1", "Bright Piano", "RealFolk Gtr DNC", "Perc. Organ 1", "Tight Brass 2", "Tenor Sax DN1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_mode": "boogie_8",
        "acc1_steps": [(0, CLOSE, 2, 78), (2, CLOSE, 2, 68), (4, HIGH_STAB, 2, 78), (8, CLOSE, 2, 78), (10, CLOSE, 2, 68), (12, HIGH_STAB, 2, 78)],
        "acc2_mode": "pop_strum",
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 2), (6, U6, 2), (8, U5, 4), (20, U3, 4)],
    },
    # Ed Sheeran ("Perfect") / Seal ("Kiss from a Rose"): Lush 6/8 Slow Pop
    "6_8_slow_pop": {
        "meter": "6/8", "tempo": 68, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "Finger Bass DN1", "SteelGtrPro DNC", "Concert Grand", "Real Strings 1", "Warm Pad", "Sweet FlugelHorn"],
        "drum_mode": "ballad_6_8", "kicks": [0, 5, 10],
        "bass_pat": [(0, R, 5), (5, L5, 1), (6, D5, 4), (10, D3, 2)],
        "acc1_steps": [(0, R, 2, 74), (2, D5, 2, 66), (4, U3, 2, 70), (6, R8, 2, 74), (8, D5, 2, 66), (10, D3, 2, 68)],
        "acc2_seq": [(0, OPEN, 6), (6, CLOSE, 6)],
        "hook": [(0, U3, 4), (4, U5, 2), (6, R8, 6), (12, U5, 4), (16, U3, 2), (18, D5, 6)],
    },
    # Tears for Fears / Michael Jackson ("The Way You Make Me Feel"): Groove-laden 12/8 Pop!
    "12_8_pop": {
        "meter": "12/8", "tempo": 112, "swing": 0.0,
        "tracks": ["Studio Kit", "Standard PercKit", "Synth Bass 1", "Bell Tine EP", "Strat N Cln DNC", "BX3 Full", "Tight Brass 1", "PopAltoSax DN1"],
        "drum_mode": "blues_12_8", "kicks": [0, 5, 6, 11], "snares": [3, 9],
        "bass_pat": [(0, R, 2), (2, R, 1), (3, D3, 2), (5, D4, 1), (6, D5, 3), (9, B7, 2), (11, D5, 1)],
        "acc1_steps": [(0, CLOSE, 2, 80), (2, CLOSE, 1, 70), (5, HIGH_STAB, 2, 78), (9, CLOSE, 2, 76)],
        "acc4_steps": [(2, HIGH_STAB, 1), (5, HIGH_STAB, 2)],
        "hook": [(0, R8, 2), (2, U3, 1), (3, U5, 3), (12, U6, 2), (14, U5, 1), (15, U3, 3)],
    },
    # Louis Prima / Paolo Conte ("Just a Gigolo"): Swinging Italian-American Jump-Pop Shuffle!
    "gigol_shuffle": {
        "meter": "4/4", "tempo": 124, "swing": 0.30, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Big Band Brass 1", "Tenor Growl DN1", "Jazz Clarinet DN1" if False else "JazzClarinet DN1"],
        "drum_mode": "jazz_swing", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_mode": "walking_jazz",
        "acc1_steps": [(0, JAZZ_SHELL, 2, 78), (2, JAZZ_SHELL, 2, 68), (6, HIGH_STAB, 2, 80), (10, JAZZ_SHELL, 2, 74), (14, JAZZ_SHELL, 2, 72)],
        "acc2_mode": "gypsy_pompe",
        "acc4_steps": [(6, HIGH_STAB, 2), (14, THIRDS, 2)],
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 2), (6, D6, 2), (8, D5, 4), (18, U3, 2), (20, R8, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },

    # =========================================================================
    # 2. BALLAD (32 Styles)
    # =========================================================================
    # Passenger ("Let Her Go"): Delicate 16th-note fingerpicked acoustic folk guitar + glockenspiel/piano hook!
    "let_her_ballad": {
        "meter": "4/4", "tempo": 76, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "RealFolk Gtr DNC", "Concert Grand", "Real Strings 1", "Warm Flute", "Glockenspiel"],
        "drum_mode": "ballad_4_4", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (8, D5, 6), (14, D3, 2)],
        "acc1_mode": "travis_pick",
        "acc2_seq": [(0, U3, 2), (2, R8, 2), (4, D5, 2), (6, R8, 2), (8, U5, 2), (10, U3, 2), (12, R8, 4)],
        "hook": [(0, U3, 1), (1, U5, 2), (3, U3, 1), (4, R8, 2), (6, D5, 2), (8, R8, 4), (16, U5, 2), (18, U6, 2), (20, U5, 4)],
    },
    # Lukas Graham ("7 Years"): Intimate music-box/piano octave ostinato + emotive strings & crisp snare
    "years_ballad": {
        "meter": "4/4", "tempo": 62, "swing": 0.0,
        "tracks": ["Studio Kit", "Standard PercKit", "Finger Bass DN1", "Pop Grand", "Music Box", "Movie Str.1 DNC", "Cello", "ConcertStrings 1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 3, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 7), (8, L5, 6), (14, R, 2)],
        "acc1_steps": [(0, OPEN, 4, 74), (4, CLOSE, 4, 68), (8, OPEN, 4, 74), (12, CLOSE, 4, 68)],
        "acc2_seq": [(0, U5, 1), (1, R8, 1), (2, U3, 2), (8, U5, 1), (9, R8, 1), (10, D6, 2)],
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 4), (16, U5, 2), (18, U3, 2), (20, R8, 4)],
    },
    # Country-Pop Pedal Steel & Acoustic Steel Guitar Ballad
    "steel_ballad": {
        "meter": "4/4", "tempo": 74, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "SteelGtrPro DNC", "Pedal Steel", "Classic Piano", "Warm Strings", "Harmonica 1 DN1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, L5, 8)],
        "acc1_mode": "travis_pick",
        "acc2_seq": [(4, THIRDS, 4), (12, THIRDS, 4)],
        "hook": [(2, THIRDS, 4), (8, U3, 4), (18, THIRDS, 6)],
        "cadence": "country_IV_V",
    },
    # Ariana Grande ("Dangerous Woman"): Sultry, smoky 6/8 blues-pop ballad with tremolo guitar, B3 organ, heavy snare!
    "dangerous_bld": {
        "meter": "6/8", "tempo": 67, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "Dark E.Bass 2", "Single Coil Pro", "BX3 Jazz", "Movie Str.2 DNC", "Dist. Gtr 1 DNC", "Tenor Growl DN1"],
        "drum_mode": "ballad_6_8", "kicks": [0, 4, 10],
        "bass_pat": [(0, R, 4), (4, R, 2), (6, D5, 4), (10, B7, 2)],
        "acc1_steps": [(0, R, 2, 72), (2, D3, 2, 68), (4, D5, 2, 72), (6, R8, 2, 76), (8, D5, 2, 68), (10, D3, 2, 66)],
        "acc2_seq": [(0, OPEN, 6), (6, HIGH_STAB, 6)],
        "hook": [(0, R8, 4), (4, B3, 2), (6, D5, 6), (12, B7, 4), (16, D5, 2), (18, R8, 6)],
        "cadence": "cinematic_bVI", "fill_type": "rock_tom",
    },
    # Default Startup Style! Warm Acoustic Brush Ballad (Norah Jones / Diana Krall intimate trio + nylon + strings)
    "brush_ballad": {
        "meter": "4/4", "tempo": 73, "swing": 0.16, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Concert Grand", "Nylon GuitarDNC", "Warm Strings", "Sweet FlugelHorn", "Vibraphone 1"],
        "drum_mode": "jazz_brush", "kicks": [0, 10],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, D5, 6), (14, L5, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 4, 72), (6, JAZZ_SHELL, 3, 66), (12, JAZZ_SHELL, 4, 70)],
        "acc2_mode": "travis_pick",
        "hook": [(4, U3, 3), (8, D5, 5), (20, U5, 3), (24, U3, 5)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Adele ("Someone Like You" / "Hello") Modern Pop-Soul Piano & Sub Ballad
    "modern_ballad": {
        "meter": "4/4", "tempo": 78, "swing": 0.0,
        "tracks": ["Studio Kit", "Standard PercKit", "Synth Bass Warm", "Concert Grand", "Bell Tine EP", "Real Strings 1", "Atmoschoir Pad", "Cello"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, L5, 8)],
        "acc1_steps": [(0, R, 1, 72), (1, D5, 1, 64), (2, R8, 1, 68), (3, D5, 1, 62), (4, U3, 1, 72), (5, D5, 1, 62), (6, R8, 1, 68), (7, D5, 1, 62),
                       (8, R, 1, 72), (9, D5, 1, 64), (10, R8, 1, 68), (11, D5, 1, 62), (12, U3, 2, 72), (14, D5, 2, 64)],
        "hook": [(0, U5, 6), (6, U3, 2), (8, R8, 8), (16, U3, 6), (22, D6, 2), (24, D5, 8)],
    },
    # Eric Clapton ("Wonderful Tonight"): Slow clean Strat bend/arpeggio + soft rimshot
    "slow_gtr_ballad": {
        "meter": "4/4", "tempo": 74, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Finger Bass DN1", "RealFolk Gtr DNC", "Strat N Cln DNC", "Warm Strings", "Tine EP Phaser", "E.Gtr Ch/Dly DNC"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 7), (8, D5, 5), (14, D3, 2)],
        "acc1_mode": "travis_pick",
        "acc2_seq": [(0, CLOSE, 4), (8, CLOSE, 4), (12, D5, 2), (14, R8, 2)],
        "hook": [(2, D5, 2), (4, D6, 2), (6, U3, 4), (10, U9, 2), (12, R8, 4), (18, D6, 2), (20, D5, 6)],
    },
    # Richard Marx / Whitney Soft FM E.Piano Ballad ("Right Here Waiting" DX7 bell tines!)
    "soft_ballad": {
        "meter": "4/4", "tempo": 75, "swing": 0.0,
        "tracks": ["Pop Kit Amb", "Standard PercKit", "Fretless Bass 2", "FM Legend EP", "Nylon GuitarDNC", "Warm Strings", "Soprano Sax DN1", "Bell Tine EP"],
        "drum_mode": "ballad_4_4", "kicks": [0, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 8), (8, L5, 6), (14, R, 2)],
        "acc1_mode": "piano_arp", "acc2_mode": "rhodes_color",
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 4), (8, U9, 4), (12, D5, 4), (16, U3, 4), (20, R8, 8)],
    },
    # Elton John ("Your Song"): Expressive acoustic Concert Grand chord-and-grace ballad + solo acoustic guitar + strings
    "piano_ballad": {
        "meter": "4/4", "tempo": 72, "swing": 0.0,
        "tracks": ["Studio Kit", "Standard PercKit", "Finger E.Bass 1", "Concert Grand", "ClassicSteel DNC", "ConcertStrings 1", "Classic Harp", "Oboe 1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D2, 2), (8, D3, 4), (12, D5, 4)],
        "acc1_steps": [(0, OPEN, 3, 76), (3, D5, 1, 60), (4, CLOSE, 3, 72), (7, R8, 1, 62), (8, OPEN, 4, 76), (12, CLOSE, 2, 70), (14, D5, 2, 64)],
        "acc2_mode": "travis_pick",
        "hook": [(0, U3, 4), (4, U9, 2), (6, R8, 6), (16, U5, 4), (20, U3, 4), (24, R8, 6)],
    },
    # Billy Joel ("Piano Man") / Norah ("Come Away With Me"): Gentle 3/4 Piano Waltz Ballad + Harmonica
    "3_4_piano_ballad": {
        "meter": "3/4", "tempo": 84, "swing": 0.08,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "Concert Grand", "RealFolk Gtr DNC", "Warm Strings", "Accordion", "Harmonica 1 DN1"],
        "drum_mode": "waltz_3_4", "kicks": [0], "snares": [4, 8],
        "bass_mode": "waltz_walk",
        "acc1_steps": [(0, R, 2, 74), (2, D5, 2, 62), (4, CLOSE, 3, 72), (8, CLOSE, 3, 68)],
        "acc2_seq": [(4, STRUM_DN, 2), (8, STRUM_UP, 2)],
        "hook": [(0, U5, 4), (4, U3, 4), (8, R8, 4), (12, U9, 4), (16, R8, 4), (20, D5, 4)],
    },
    # Celine Dion ("My Heart Will Go On"): Sweeping Orchestral Ballad 1 with Harp, Flute/Whistle, Strings
    "orchestral_bld_1": {
        "meter": "4/4", "tempo": 76, "swing": 0.0,
        "tracks": ["Room Kit Amb", "Standard PercKit", "Fretless Bass 2", "Concert Grand", "Classic Harp", "Movie Str.1 DNC", "French Section", "Whistle DN1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 10], "snares": [4, 12],
        "perc_steps": [(0, 81, 62)],
        "bass_pat": [(0, R, 8), (8, D5, 6), (14, L5, 2)],
        "acc1_mode": "piano_arp",
        "acc2_seq": [(0, R, 1), (1, D3, 1), (2, D5, 1), (3, R8, 1), (4, U3, 2), (6, U5, 2)],
        "acc4_mode": "thirds_swell",
        "hook": [(0, R8, 3), (3, U9, 1), (4, U3, 4), (8, U5, 6), (14, U3, 2), (16, U9, 4), (20, R8, 8)],
        "fill_type": "orchestral_timp",
    },
    # Andrea Bocelli / Josh Groban Cinematic Symphonic Ballad 2 (spiccato strings -> full tutti!)
    "orchestral_bld_2": {
        "meter": "4/4", "tempo": 72, "swing": 0.0,
        "tracks": ["Ambient Kit", "Trinity Perc.Kit", "Class.Contrabs", "Strings Quartet", "Concert Grand", "OrchestraTutti 1", "Soft Horns 2", "Real Violin DNC"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [12],
        "perc_steps": [(0, 47, 68, V_34), (14, 45, 62, V_34)],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, D5, 8)],
        "acc1_steps": [(0, OPEN, 4, 74), (4, OPEN, 4, 70), (8, OPEN, 4, 74), (12, OPEN, 4, 72)],
        "acc3_mode": "spiccato_8",
        "hook": [(0, D5, 4), (4, R8, 4), (8, U3, 6), (14, U5, 2), (16, U6, 4), (20, U5, 8)],
        "fill_type": "orchestral_timp",
    },
    # MTV Unplugged Intimate Acoustic Session (Cajón + Nylon + Upright Bass + B3)
    "unplugged": {
        "meter": "4/4", "tempo": 74, "swing": 0.08,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "Concert Gtr DNC", "RealFolk Gtr DNC", "BX3 Jazz", "Classic Piano", "Cello"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6, 8], "snares": [4, 12],
        "perc_steps": [(0, 64, 68), (4, 62, 66), (7, 70, 48), (10, 63, 62), (12, 62, 68)],
        "bass_pat": [(0, R, 5), (6, L5, 2), (8, R, 5), (14, D3, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "travis_pick",
        "hook": [(4, U3, 2), (6, R8, 2), (8, D5, 4), (20, U5, 2), (22, U3, 4)],
    },
    # Extreme ("More Than Words") / Acoustic Percussive Slap-Strum Guitar Ballad
    "guitar_ballad": {
        "meter": "4/4", "tempo": 82, "swing": 0.06,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "ClassicSteel DNC", "Nylon GuitarDNC", "Warm Pad", "Real Strings 1", "Concert Gtr Pro"],
        "drum_mode": "ballad_4_4", "kicks": [0, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, R, 2), (10, D5, 6)],
        "acc1_steps": [(0, R, 2, 76), (2, CLOSE, 2, 72), (4, CHUCK, 1, 82), (6, CLOSE, 3, 74), (10, CLOSE, 2, 72), (12, CHUCK, 1, 82), (14, STRUM_UP, 2, 68)],
        "hook": [(0, U3, 3), (3, U5, 3), (6, U3, 2), (10, R8, 6)],
    },
    # Carpenters / Carole King ("Close to You" / "It's Too Late" 70s Warm Piano & Wurly Ballad)
    "70_s_ballad": {
        "meter": "4/4", "tempo": 74, "swing": 0.05,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Classic Piano", "Wurly Clean", "Warm Strings", "Flute", "Oboe 1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 7, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 5), (6, D2, 1), (7, D3, 1), (8, D5, 6), (14, D3, 2)],
        "acc1_steps": [(0, OPEN, 4, 76), (4, CLOSE, 4, 72), (8, OPEN, 4, 76), (12, CLOSE, 4, 72)],
        "acc2_mode": "rhodes_color",
        "hook": [(0, D5, 2), (2, D6, 2), (4, U3, 4), (16, U5, 2), (18, U3, 2), (20, R8, 6)],
    },
    # Eric Clapton ("Tears in Heaven"): Signature Nylon Guitar syncopated bass-and-chord fingerpicking!
    "unplugged_heaven": {
        "meter": "4/4", "tempo": 78, "swing": 0.08,
        "tracks": ["Brush Kit 2 Amb", "Latin Perc.Kit 2", "Fretless Bass 2", "Real Nylon Gtr", "Concert Gtr DNC", "Warm Pad", "Organ Low 1", "Soprano Sax DN1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6], "snares": [4, 12],
        "perc_steps": [(2, 70, 44), (6, 70, 52), (10, 70, 44), (14, 70, 52)],
        "bass_pat": [(0, R, 5), (6, L6, 4), (10, L5, 6)],
        "acc1_steps": [(0, R, 2, 78), (2, CLOSE, 3, 72), (6, CLOSE, 4, 76), (12, D5, 2, 68), (14, U3, 2, 70)],
        "hook": [(0, U3, 2), (2, U5, 4), (6, U3, 4), (16, R8, 2), (18, U9, 4), (22, R8, 6)],
    },
    # Alicia Keys / Boyz II Men Neo-Soul R&B Groovy Ballad ("If I Ain't Got You" / 16th R&B pocket)
    "groovy_ballad": {
        "meter": "4/4", "tempo": 74, "swing": 0.18,
        "tracks": ["HipHop Kit 1", "Standard PercKit", "Dark R&B Bass1", "R&B E. Piano", "Concert Grand", "Warm Strings", "Soft Horns 1", "Tenor Sax DN1"],
        "drum_mode": "pop_16", "kicks": [0, 7, 10, 15], "snares": [4, 12],
        "perc_steps": [(4, 80, 56), (12, 81, 62)],
        "bass_pat": [(0, R, 5), (7, D3, 1), (8, D5, 2), (10, R, 4), (15, LT, 1)],
        "acc1_mode": "jazz_comp", "acc2_mode": "piano_arp",
        "hook": [(2, R8, 2), (4, U3, 2), (6, U5, 4), (18, U6, 2), (20, U5, 2), (22, U3, 4)],
    },
    # Phil Collins / Vangelis ("In the Air Tonight" / "Blade Runner"): Lush 80s Analog CS-80 Pad + Gated Drum Fill!
    "analog_ballad": {
        "meter": "4/4", "tempo": 82, "swing": 0.0,
        "tracks": ["Gate Kit Amb", "Electro Kit 1", "Synth Bass 80ish", "Analog Pad 1", "DW8000 EP", "Jurassic Pad", "Fat Synth", "Old Portamento"],
        "drum_mode": "ballad_4_4", "kick_note": 36, "snare_note": 40, "kicks": [0, 10], "snares": [12],
        "perc_steps": [(0, 78, 56), (4, 37, 64), (8, 79, 52)],
        "bass_pat": [(0, R, 8), (8, R, 4), (12, B7, 4)],
        "acc1_steps": [(0, QUARTAL, 8, 74), (8, OPEN, 8, 76)],
        "acc2_mode": "synth_seq_16",
        "hook": [(0, U5, 6), (6, U3, 2), (8, U9, 8), (16, R8, 6), (22, B7, 2), (24, D5, 8)],
        "cadence": "modal_bVII", "fill_type": "rock_tom",
    },
    # Procol Harum ("A Whiter Shade of Pale"): Baroque Bach-style Hammond Organ Ballad + stepwise descending bass!
    "organ_ballad": {
        "meter": "4/4", "tempo": 74, "swing": 0.0,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Flat", "DRAWBARS", "Concert Grand", "BX3 Gospel", "Warm Strings", "Perc. Organ 1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [4, 12], "ride_note": 51,
        "bass_pat": [(0, R8, 4), (4, B7, 4), (8, D6, 4), (12, D5, 4), (16, D4, 4), (20, D3, 4), (24, D2, 4), (28, D5, 4)],
        "acc1_steps": [(0, OPEN, 4, 74), (4, CLOSE, 4, 70), (8, OPEN, 4, 74), (12, CLOSE, 4, 70)],
        "hook": [(0, U3, 6), (6, U9, 1), (7, R8, 1), (8, D6, 4), (12, D5, 4), (16, R8, 4), (20, U9, 4), (24, U3, 8)],
    },
    # Romantic 3/4 Waltz Ballad ("Moon River" / "Fascination")
    "waltz_ballad": {
        "meter": "3/4", "tempo": 90, "swing": 0.06,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Nylon GuitarDNC", "Concert Grand", "Real Strings 1", "Warm Flute", "Harmonica 1 DN1"],
        "drum_mode": "waltz_3_4",
        "bass_pat": [(0, R, 8), (8, D5, 4)],
        "acc1_steps": [(0, R, 2, 70), (2, D5, 2, 62), (4, U3, 2, 68), (6, D5, 2, 62), (8, R8, 2, 68), (10, D5, 2, 60)],
        "acc2_seq": [(4, CLOSE, 3), (8, CLOSE, 3)],
        "hook": [(0, D5, 4), (4, U3, 6), (10, U9, 2), (12, R8, 8), (20, D5, 4)],
    },
    # Classic Soulful 6/8 Ballad 1 ("If You Don't Know Me By Now" / "At Last")
    "6_8_ballad_1": {
        "meter": "6/8", "tempo": 68, "swing": 0.0,
        "tracks": ["Studio Kit", "Standard PercKit", "JB Finger BsDN1", "Tine EP Dyno", "Strat N Cln DNC", "Real Strings 1", "Soft Horns 1", "Tenor Sax DN1"],
        "drum_mode": "ballad_6_8", "kicks": [0, 10],
        "bass_pat": [(0, R, 6), (6, D5, 4), (10, D3, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 2, 74), (2, D5, 2, 62), (4, U3, 2, 68), (6, JAZZ_SHELL, 4, 76), (10, D5, 2, 64)],
        "hook": [(0, R8, 4), (4, U3, 2), (6, U5, 6), (14, U6, 2), (16, U5, 2), (18, U3, 6)],
    },
    # Cinematic Piano & Strings 6/8 Ballad 2 ("A Thousand Years" Christina Perri)
    "6_8_ballad_2": {
        "meter": "6/8", "tempo": 70, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "Concert Grand", "RealFolk Gtr DNC", "Movie Str.1 DNC", "Cello", "Violin Expr. DNC"],
        "drum_mode": "ballad_6_8", "kicks": [0, 4],
        "bass_pat": [(0, R, 6), (6, L5, 6)],
        "acc1_steps": [(0, CLOSE, 2, 74), (2, CLOSE, 2, 70), (4, CLOSE, 2, 72), (6, OPEN, 2, 76), (8, CLOSE, 2, 70), (10, CLOSE, 2, 70)],
        "hook": [(0, U3, 4), (4, R8, 2), (6, U5, 6), (12, U3, 4), (16, U9, 2), (18, R8, 6)],
    },
    # Intimate Jazz-Folk 6/8 Brush Ballad
    "6_8_brush_ballad": {
        "meter": "6/8", "tempo": 72, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Soft Jazz Guitar", "Warm Strings", "Sweet FlugelHorn", "RealClarinet DN1"],
        "drum_mode": "ballad_6_8", "snare_note": 40, "kicks": [0],
        "bass_pat": [(0, R, 4), (4, D3, 2), (6, D5, 4), (10, D6, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 4, 70), (6, JAZZ_SHELL, 4, 72), (10, JAZZ_SHELL, 2, 64)],
        "hook": [(2, D5, 2), (4, R8, 2), (6, U3, 6), (14, U9, 4), (18, R8, 6)],
        "cadence": "jazz_ii_V",
    },
    # Ultra-Slow 6/8 Torch Song ("Unchained Melody" harp-like guitar arpeggio)
    "6_8_slow": {
        "meter": "6/8", "tempo": 64, "swing": 0.0,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Single Coil", "Classic Piano", "Full Strings", "Choir Aahs GM", "Tenor Sax 1 DNC"],
        "drum_mode": "ballad_6_8", "kicks": [0, 8],
        "bass_pat": [(0, R, 6), (6, R, 2), (8, D5, 4)],
        "acc1_steps": [(0, R, 2, 74), (2, D3, 2, 68), (4, D5, 2, 70), (6, R8, 2, 76), (8, D5, 2, 70), (10, D3, 2, 68)],
        "hook": [(0, R8, 6), (6, U3, 4), (10, U5, 2), (12, U6, 6), (18, U5, 6)],
    },
    # Classic 12/8 R&B / Doo-Wop / Soul Ballad ("Purple Rain" / "End of the Road")
    "12_8_ballad": {
        "meter": "12/8", "tempo": 72, "swing": 0.0,
        "tracks": ["Power Kit 2 Amb", "Standard PercKit", "JB Finger BsDN1", "Bell Tine EP", "Chorus Guitar", "Real Strings 2", "Gospel Organ 1", "E.Gtr Ch/Dly DNC"],
        "drum_mode": "blues_12_8", "kicks": [0, 6], "snares": [3, 9],
        "bass_pat": [(0, R, 5), (5, D3, 1), (6, D5, 5), (11, L5, 1)],
        "acc1_steps": [(0, OPEN, 3, 76), (3, CLOSE, 2, 70), (5, CLOSE, 1, 66), (6, OPEN, 3, 76), (9, CLOSE, 3, 72)],
        "hook": [(0, U5, 3), (3, U3, 3), (6, R8, 6), (15, U9, 3), (18, R8, 6)],
    },
    # Expansive 6/4 Cinema / Prog Ballad (True 6-beat 24-substep measure!)
    "6_4_ballad": {
        "meter": "6/4", "tempo": 82, "swing": 0.0,
        "tracks": ["Room Kit Amb", "Standard PercKit", "Fretless Bass 2", "Grand&MovingPad", "RealFolk Gtr DNC", "Symphonic Ens.", "French Section", "SopranoVox1 DNC"],
        "drum_mode": "ballad_4_4", "kicks": [0, 12, 18], "snares": [8, 20],
        "bass_pat": [(0, R, 12), (12, D5, 8), (20, L5, 4)],
        "acc1_mode": "piano_arp", "acc2_mode": "travis_pick",
        "hook": [(0, R8, 8), (8, U3, 4), (12, U5, 8), (20, U3, 4), (24, U6, 8), (32, U5, 16)],
    },
    # Gary Moore / B.B. King ("Still Got the Blues" / "The Thrill Is Gone"): Soulful Minor/Major Blues Ballad
    "blues_ballad": {
        "meter": "4/4", "tempo": 76, "swing": 0.24, "swing8": True,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Finger Bass DN1", "Tine EP Phaser", "Clean Jazz 1", "Jimmy Organ", "Real Strings 1", "Crunch Gtr DNC"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "jazz_comp", "acc3_mode": "organ_bubble",
        "hook": [(0, U3, 2), (2, U5, 4), (6, U6, 2), (8, U5, 6), (18, B3, 2), (20, R8, 6)],
        "cadence": "blues_V_IV",
    },
    # Bob Marley ("No Woman, No Cry" / Lovers Rock): Warm One-Drop Reggae Ballad with Hammond bubble!
    "reggae_ballad": {
        "meter": "4/4", "tempo": 75, "swing": 0.14,
        "tracks": ["Studio Kit", "Latin Perc.Kit 2", "Dark E.Bass 2", "Strat N Cln DNC", "Jazz Organ", "Concert Grand", "Warm Pad", "Real Nylon Gtr"],
        "drum_mode": "reggae_onedrop", "kicks": [8], "snares": [8],
        "bass_pat": [(0, R, 3), (4, D3, 2), (6, D5, 2), (8, R, 4), (14, L5, 2)],
        "acc1_mode": "reggae_skank", "acc2_mode": "organ_bubble",
        "hook": [(0, U3, 2), (2, R8, 2), (4, D5, 4), (16, U5, 2), (18, U3, 2), (20, R8, 4)],
    },
    # Intimate Singer-Songwriter Unplugged Ballad 1 (Nylon + Piano + Cello)
    "unpluggedballad1": {
        "meter": "4/4", "tempo": 74, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "Real Nylon Gtr", "Classic Piano", "Cello", "Warm Flute", "Mandolin DNC"],
        "drum_mode": "ballad_4_4", "kicks": [0, 10], "snares": [4, 12],
        "perc_steps": [(4, 81, 52), (14, 70, 48)],
        "bass_pat": [(0, R, 7), (8, D3, 4), (12, D5, 4)],
        "acc1_mode": "travis_pick", "acc2_mode": "rhodes_color",
        "hook": [(0, D5, 4), (4, R8, 4), (8, U9, 4), (12, U3, 4), (16, U5, 8)],
    },
    # Warm 12-String & Accordion Unplugged Ballad 2
    "unpluggedballad2": {
        "meter": "4/4", "tempo": 77, "swing": 0.05,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "Strum 12Str. DNC", "Wurly Clean", "Accordion", "Strings Quartet", "RealFolk GtrST 2"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 5), (6, L5, 2), (8, D5, 5), (14, L6, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "piano_arp",
        "hook": [(2, U3, 2), (4, D5, 4), (10, R8, 4), (18, U5, 2), (20, U3, 6)],
    },
    # Solo Steel-String Arpeggio Unplugged Guitar 1
    "unplugged_gtr_1": {
        "meter": "4/4", "tempo": 73, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "ClassicSteel DNC", "RealFolk Gtr DNC", "Warm Pad", "Violin Expr. DNC", "Concert Gtr Pro"],
        "drum_mode": "ballad_4_4", "kicks": [0], "snares": [12],
        "bass_pat": [(0, R, 8), (8, L5, 8)],
        "acc1_steps": [(0, R, 2, 76), (2, D5, 2, 66), (4, U3, 2, 72), (6, R8, 2, 68), (8, D3, 2, 72), (10, D5, 2, 66), (12, U3, 4, 74)],
        "hook": [(0, U5, 4), (4, U3, 4), (8, R8, 8), (16, U9, 4), (20, D5, 8)],
    },
    # Dual Spanish Nylon & Folk Unplugged Guitar 2
    "unplugged_gtr_2": {
        "meter": "4/4", "tempo": 78, "swing": 0.04,
        "tracks": ["Real Kit 2 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "Concert Gtr DNC", "SteelGtrPro DNC", "Warm Strings", "Pan Flute DN1", "Real Nylon Gtr"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [4, 12],
        "perc_steps": [(6, 63, 58), (14, 64, 62)],
        "bass_pat": [(0, R, 6), (6, D5, 2), (8, R, 6), (14, LT, 2)],
        "acc1_mode": "bossa_violao", "acc2_mode": "travis_pick",
        "hook": [(0, R8, 3), (3, U3, 3), (6, U5, 2), (8, U3, 8), (18, U9, 3), (21, R8, 7)],
    },

    # =========================================================================
    # 3. BALLROOM (24 Styles — Strict Competition Tempo & Dance Character)
    # =========================================================================
    "english_waltz": {
        "meter": "3/4", "tempo": 88, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Concert Grand", "Classic Harp", "Full Strings", "French Section", "Flute"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 8), (8, L5, 4)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": OPEN,
        "acc2_seq": [(0, R, 2), (2, D5, 2), (4, R8, 2), (6, U3, 2), (8, U5, 4)],
        "hook": [(0, U3, 8), (8, U5, 4), (12, U6, 8), (20, U5, 4)],
    },
    "quick_step": {
        "meter": "4/4", "tempo": 196, "swing": 0.24, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Big Band Brass 1", "Clar & Sax Ens 1", "Vibraphone 1"],
        "drum_mode": "dixie", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "two_feel",
        "acc1_steps": [(0, CLOSE, 2, 76), (6, HIGH_STAB, 2, 82), (12, CLOSE, 2, 76)],
        "acc2_mode": "gypsy_pompe",
        "hook": [(0, R8, 2), (4, U3, 2), (6, U5, 4), (16, U6, 2), (20, U5, 2), (22, R8, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Pasodoble ("España Cañí"): Martial Spanish 2/4 bullfight snare, castanets, flamenco rasgueado, Dual Trumpets!
    "pasodoble": {
        "meter": "2/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Standard Kit Amb", "Latin Perc.Kit 1", "Class.Contrabs", "Concert Gtr DNC", "OrchestraTutti 1", "Dual Trumpets", "Sforzato Brass", "Concert Trumpet"],
        "drum_mode": "march_2_4", "snare_note": 38,
        "perc_steps": [(0, 85, 76), (2, 85, 68), (3, 85, 64), (4, 85, 76), (6, 85, 68)],
        "bass_pat": [(0, R, 3), (4, L5, 3)],
        "acc1_steps": [(0, STRUM_DN, 2, 84), (2, STRUM_UP, 1, 74), (3, STRUM_DN, 1, 78), (4, STRUM_DN, 2, 84), (6, STRUM_UP, 2, 76)],
        "hook": [(0, R8, 2), (2, B2, 1), (3, R8, 1), (4, D5, 4), (8, R8, 2), (10, U3, 2), (12, U5, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "flamenco_rasg",
    },
    # Modern Ballroom Paso Dance (4/4 driving Spanish dramatic march)
    "paso_dance": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Latin Perc.Kit 1", "Picked E. Bass 2", "Real Nylon Gtr", "Accordion", "Movie Brass", "Real Strings 1", "Trumpet Expr.1"],
        "drum_mode": "pop_8", "kicks": [0, 4, 8, 12], "snares": [2, 6, 10, 14],
        "perc_steps": [(0, 85, 74), (6, 85, 70), (12, 85, 76)],
        "bass_pat": [(0, R, 3), (4, D5, 3), (8, R, 3), (12, B2, 2), (14, R, 2)],
        "acc1_mode": "pop_strum",
        "hook": [(0, U5, 3), (3, S5, 1), (4, U5, 4), (8, U3, 4), (12, B2, 2), (14, R8, 2)],
        "cadence": "flamenco_bVI_V", "fill_type": "flamenco_rasg",
    },
    # Strauss Viennese Waltz ("Blue Danube"): Brisk 178 BPM 3/4 with orchestral horns & strings!
    "viennese_waltz": {
        "meter": "3/4", "tempo": 178, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Trinity Perc.Kit", "Class.Contrabs", "OrchestraTutti 1", "Classic Harp", "ConcertStrings 1", "French Section", "Flute"],
        "drum_mode": "viennese_3_4",
        "perc_steps": [(0, 81, 60)],
        "bass_pat": [(0, R, 5), (8, L5, 3)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": CLOSE,
        "hook": [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, D5, 8), (20, U5, 4)],
        "fill_type": "orchestral_timp",
    },
    # Competition Ballroom Jive: 172 BPM bouncy boogie-swing triple-step!
    "jive": {
        "meter": "4/4", "tempo": 172, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "Bright Piano", "Clean Jazz 1", "Tight Brass 1", "Baritone Sax DN1", "Tenor Growl DN1"],
        "drum_mode": "jazz_swing", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "boogie_8", "acc1_mode": "boogie_comp", "acc2_mode": "offbeat_chop",
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 2), (6, U6, 2), (8, B7, 4), (20, R8, 4)],
        "fill_type": "jazz_triplet",
    },
    # Carlos Gardel / Buenos Aires Milonga-Tango ("Por una Cabeza"): Staccato bandoneon, solo violin, piano drag!
    "argentina_tango": {
        "meter": "4/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Class.Contrabs", "Bandoneon DNC", "Concert Grand", "Chamber Strings", "Real Violin DNC", "Bandoneon Short"],
        "drum_mode": "tango",
        "bass_mode": "tango_marcato", "acc1_mode": "tango_staccato",
        "acc2_seq": [(0, CLOSE, 1), (4, CLOSE, 1), (8, CLOSE, 1), (12, HIGH_STAB, 2), (14, CLOSE, 2)],
        "hook": [(0, D5, 2), (2, S5, 2), (4, D5, 4), (8, U3, 3), (11, U9, 1), (12, R8, 4)],
        "cadence": "tango_V_I",
    },
    # Gotan Project ("Santa María"): Electro-Tango with deep house kick, dub bass, bandoneon & violin!
    "modern_tango": {
        "meter": "4/4", "tempo": 124, "swing": 0.06,
        "tracks": ["Electro Kit 1", "Standard PercKit", "Synth Bass Warm", "Bandoneon DNC", "Nylon GuitarDNC", "Dark Pad", "Violin DNC", "Tango Accordion"],
        "drum_mode": "four_floor", "kicks": [0, 4, 8, 12], "snares": [4, 12, 14],
        "bass_mode": "tango_332", "acc1_mode": "tango_332", "acc2_mode": "travis_pick",
        "hook": [(0, R8, 3), (6, B7, 3), (12, S5, 2), (14, D5, 2), (16, R8, 6)],
        "cadence": "tango_V_I", "fill_type": "edm_riser",
    },
    "slow_waltz_1": {
        "meter": "3/4", "tempo": 89, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "Classic Piano", "Nylon GuitarDNC", "Real Strings 1", "Warm Pad", "Sweet FlugelHorn"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 6), (6, D5, 6)],
        "acc1_mode": "waltz_oom_pah", "acc2_seq": [(2, D5, 2), (6, U3, 2), (10, D5, 2)],
        "hook": [(0, U5, 6), (6, U3, 6), (12, U9, 8), (20, R8, 4)],
    },
    "slow_waltz_2": {
        "meter": "3/4", "tempo": 93, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Real Ac. Bass 1", "Bell Tine EP", "SteelGtrPro DNC", "ConcertStrings 1", "Classic Oboe", "Celesta"],
        "drum_mode": "waltz_3_4", "bass_mode": "waltz_walk",
        "acc1_steps": [(0, R, 4, 72), (4, OPEN, 4, 70), (8, CLOSE, 4, 68)],
        "hook": [(0, R8, 4), (4, U3, 4), (8, U5, 4), (12, U6, 6), (18, U5, 6)],
    },
    # Sevillanas / Fandangos 3/4 Flamenco with Palmas, Castanets & Rasgueado!
    "3_4_flamenco": {
        "meter": "3/4", "tempo": 126, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "Acoustic Bass 1", "Concert Gtr DNC", "Real Nylon Gtr", "Strings&Orch.V.", "Flute", "Concert Gtr Pro"],
        "drum_mode": "flamenco", "kicks": [0, 6], "snares": [4, 8, 10],
        "bass_pat": [(0, R, 6), (6, B2, 3), (9, R, 3)],
        "acc1_steps": [(0, STRUM_DN, 3, 84), (3, STRUM_UP, 1, 74), (4, CHUCK, 2, 80), (6, STRUM_DN, 3, 82), (9, STRUM_UP, 3, 76)],
        "hook": [(0, U5, 4), (4, S5, 2), (6, U5, 2), (8, U3, 4), (12, U9, 4), (16, B2, 4), (20, R8, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "flamenco_rasg",
    },
    # Rumba Flamenca 4/4 (Paco de Lucía / Camarón cajón + ventilador guitar + palmas!)
    "flamenco": {
        "meter": "4/4", "tempo": 118, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Latin Perc.Kit 1", "Fretless Bass 2", "Concert Gtr DNC", "Real Nylon Gtr", "Warm Strings", "RealClarinet DN1", "Concert Gtr Pro"],
        "drum_mode": "flamenco", "kicks": [0, 6, 12], "snares": [3, 8, 10, 14],
        "bass_pat": [(0, R, 5), (6, D5, 2), (8, S5, 4), (12, D5, 4)],
        "acc1_steps": [(0, STRUM_DN, 2, 84), (3, STRUM_UP, 1, 74), (4, CHUCK, 2, 82), (6, STRUM_UP, 2, 78), (10, STRUM_UP, 2, 76), (12, CHUCK, 2, 82), (14, STRUM_DN, 2, 80)],
        "hook": [(0, R8, 2), (2, B2, 2), (4, D3, 4), (8, D4, 2), (10, D3, 2), (12, B2, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "flamenco_rasg",
    },
    "swing_fox": {
        "meter": "4/4", "tempo": 130, "swing": 0.26, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Soft Jazz Guitar", "Glenn & Friends", "Sax Ensemble", "Mute Trumpet"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "hook": [(0, D5, 2), (2, D6, 2), (4, R8, 4), (16, U3, 2), (18, U9, 2), (20, R8, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "slow_fox": {
        "meter": "4/4", "tempo": 116, "swing": 0.24, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Concert Grand", "Jazz Gtr 1 DNC", "Real Strings 1", "Clar & Sax Ens 1", "Vibraphone 1"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp",
        "hook": [(0, U3, 4), (6, U5, 2), (8, U3, 6), (20, U9, 4), (24, R8, 6)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "fox_shuffle": {
        "meter": "4/4", "tempo": 132, "swing": 0.30, "swing8": True,
        "tracks": ["Pop Std. Kit 2", "Standard PercKit", "Finger Bass DN1", "Pop Grand", "SteelGtrPro DNC", "Accordion", "Tight Brass 2", "PopAltoSax DN1"],
        "drum_mode": "pop_8", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R8, 2), (4, D5, 2), (6, D6, 2), (8, R, 2), (10, R8, 2), (12, D5, 2), (14, D3, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, R8, 2), (2, D6, 2), (4, D5, 4), (16, U3, 2), (18, U9, 2), (20, R8, 4)],
    },
    "foxtrot": {
        "meter": "4/4", "tempo": 126, "swing": 0.25, "swing8": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Classic Piano", "Jazz Gtr 1 DNC", "Strings&Orch.V.", "Jazz Trb. DN1", "JazzClarinet DN1"],
        "drum_mode": "jazz_swing", "bass_mode": "two_feel",
        "acc1_steps": [(2, JAZZ_SHELL, 2, 72), (6, JAZZ_SHELL, 2, 74), (10, JAZZ_SHELL, 2, 72), (14, JAZZ_SHELL, 2, 74)],
        "hook": [(0, D5, 4), (4, U3, 2), (6, U9, 2), (8, R8, 6), (20, D6, 4), (24, D5, 6)],
        "cadence": "jazz_ii_V",
    },
    "boogie_woogie": {
        "meter": "4/4", "tempo": 146, "swing": 0.28, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "Honky-Tonk", "Clean Jazz 1", "BX3 Rock 1", "Tight Brass 1", "Tenor Growl DN1"],
        "drum_mode": "pop_8", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_mode": "boogie_8",
        "acc1_steps": [(0, CLOSE, 2, 82), (2, HIGH_STAB, 2, 76), (6, CLOSE, 2, 80), (8, HIGH_STAB, 2, 78), (12, CLOSE, 2, 82), (14, HIGH_STAB, 2, 76)],
        "hook": [(0, B3, 1), (1, D3, 3), (4, D5, 2), (6, R8, 2), (8, B7, 2), (10, D6, 2), (12, D5, 4)],
        "cadence": "blues_V_IV",
    },
    # Brian Setzer / Louis Jordan ("Jump, Jive an' Wail"): High-energy Jump Blues Swing!
    "big_band_jump": {
        "meter": "4/4", "tempo": 164, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Oct. Jazz Guitar", "Big Band Brass 1", "Sax Ensemble", "Jazz Trumpet DN1"],
        "drum_mode": "jazz_swing", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_mode": "walking_jazz", "acc1_mode": "boogie_comp",
        "acc4_steps": [(0, HIGH_STAB, 2), (6, HIGH_STAB, 2), (12, THIRDS, 3)],
        "hook": [(0, R8, 2), (4, R8, 2), (6, U3, 2), (8, U5, 4), (16, B7, 2), (20, D6, 2), (22, D5, 4)],
        "cadence": "blues_V_IV", "fill_type": "jazz_triplet",
    },
    "big_band_fox": {
        "meter": "4/4", "tempo": 128, "swing": 0.24, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Glenn & Boys", "Mute Ensemble 1", "Clar & Sax Ens 2"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp",
        "hook": [(0, U3, 2), (2, U5, 4), (8, U6, 2), (10, U5, 4), (16, U3, 4), (20, R8, 6)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Count Basie / Sinatra Classic Big Band Swing ("Fly Me to the Moon")
    "big_band_swing": {
        "meter": "4/4", "tempo": 134, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Big Band Brass 2", "Real Sax Ens.", "JazzTrumpet1 DNC"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz",
        "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "acc4_steps": [(2, HIGH_STAB, 2), (10, THIRDS, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, R8, 3), (4, B7, 3), (8, D6, 2), (10, D5, 4), (18, U3, 2), (20, R8, 6)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Blackpool Tower Ballroom Wurlitzer / Theatre Organ Waltz!
    "organ_waltz": {
        "meter": "3/4", "tempo": 96, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Organ Low 1", "Big Theatre Org.", "Theatre Organ 1", "Theatre Organ 2", "Warm Strings", "Glockenspiel"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 6), (8, L5, 4)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": CLOSE,
        "hook": [(0, U3, 4), (4, U5, 4), (8, R8, 4), (12, U6, 6), (18, U5, 6)],
    },
    # Theatre Organ Foxtrot
    "organ_foxtrot": {
        "meter": "4/4", "tempo": 130, "swing": 0.24, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Organ Low 2", "Theatre Organ 1", "Jazz Gtr 1 DNC", "Big Theatre Org.", "Vibraphone 1", "Jazz Organ"],
        "drum_mode": "jazz_brush", "bass_mode": "two_feel",
        "acc1_steps": [(4, CLOSE, 2, 76), (12, CLOSE, 2, 76)],
        "acc2_mode": "gypsy_pompe",
        "hook": [(0, D5, 2), (2, D6, 2), (4, U3, 4), (8, U9, 2), (10, R8, 4)],
    },
    # Chubby Checker ("The Twist"): Early-60s Rock'n'Roll Twist with honky-tonk piano & yakety tenor sax!
    "twist": {
        "meter": "4/4", "tempo": 156, "swing": 0.0,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Pick", "Rock Piano", "Single Coil", "60’s Organ", "Baritone Sax Pro", "Tenor Growl DN1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "perc_steps": [(4, 39, 78), (12, 39, 78)],
        "bass_pat": [(0, R, 2), (2, D3, 2), (4, D5, 2), (6, D6, 2), (8, D5, 2), (10, D3, 2), (12, R, 4)],
        "acc1_mode": "boogie_comp",
        "hook": [(0, R8, 2), (2, R8, 2), (4, U3, 2), (6, U5, 2), (8, U6, 2), (10, U5, 4)],
        "cadence": "blues_V_IV",
    },
    # The Olympics ("Hully Gully"): Early 60s party line-dance cowbell/tambourine & Farfisa organ!
    "hully_gully": {
        "meter": "4/4", "tempo": 124, "swing": 0.06,
        "tracks": ["VintageKit 2 Amb", "Latin Perc.Kit 1", "Vintage P. Bass", "60’s Organ", "Strat N Cln DNC", "Bright Piano", "Tight Brass 1", "PopAltoSax DN1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 10], "snares": [4, 12],
        "perc_steps": [(0, 56, 68), (4, 54, 76), (8, 56, 68), (12, 54, 76)],
        "bass_pat": [(0, R, 3), (3, D3, 1), (4, D5, 4), (8, R, 3), (12, D5, 4)],
        "acc1_steps": [(2, HIGH_STAB, 2, 78), (6, CLOSE, 2, 76), (10, HIGH_STAB, 2, 78), (14, CLOSE, 2, 76)],
        "hook": [(0, D5, 2), (3, R8, 3), (8, U3, 2), (11, R8, 3)],
    },

    # =========================================================================
    # 4. DANCE (32 Styles)
    # =========================================================================
    "synth_beat": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Synth Kit 1", "Electro Kit 1", "Synth Bass 1", "Techno Stab DNC", "Thin PulSeq DNC", "Square Pad", "Fat Synth", "MonoSaw Detune"],
        "drum_mode": "four_floor", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_mode": "disco_oct", "acc1_mode": "house_piano", "quartal": True, "acc2_mode": "synth_seq_16",
        "hook": [(0, R8, 2), (2, D5, 2), (4, U3, 2), (6, R8, 2), (10, B7, 2), (12, D5, 4)],
        "fill_type": "edm_riser",
    },
    "dance_to_trance": {
        "meter": "4/4", "tempo": 138, "swing": 0.0,
        "tracks": ["Trance Kit", "Dance Kit", "Euro Bass", "Parallel Trance", "Trance Filter", "Big Side Attack", "Power Saw", "Fast Glide Saw"],
        "drum_mode": "trance", "bass_mode": "offbeat_edm",
        "acc1_steps": [(0, OPEN, 2, 78), (3, OPEN, 2, 76), (6, OPEN, 2, 80), (10, OPEN, 2, 74), (12, OPEN, 2, 78), (14, OPEN, 2, 76)],
        "acc2_mode": "synth_seq_16", "acc3_mode": "trance_gate",
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 2), (8, U5, 2), (11, U6, 2), (14, U5, 2)],
        "fill_type": "edm_riser",
    },
    "edm_happy_hour": {
        "meter": "4/4", "tempo": 128, "swing": 0.0,
        "tracks": ["Dance Kit Remix", "House Kit 1", "Basic Saw Bass", "2000’s Piano", "Next Dance DNC", "Warm Buzz", "Power Saw", "Octo Lead"],
        "drum_mode": "four_floor", "kicks": [0, 4, 8, 12, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (6, R8, 2), (8, R, 2), (10, D5, 2), (14, R8, 2)],
        "acc1_mode": "house_piano", "acc3_mode": "trance_gate",
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 3), (7, U6, 1), (8, U5, 4), (16, U3, 2), (18, R8, 6)],
        "fill_type": "edm_riser",
    },
    "edm_reggaeton": {
        "meter": "4/4", "tempo": 102, "swing": 0.04,
        "tracks": ["Dance Kit Remix", "Latin Perc.Kit 2", "Jungle Bass", "Marimba Syn Seq", "Real Nylon Gtr", "Square Pad", "Tight Brass 2", "Dance Lead"],
        "drum_mode": "reggaeton_dembow", "bass_mode": "reggaeton_sub",
        "acc1_steps": [(0, CLOSE, 2, 80), (3, HIGH_STAB, 2, 78), (6, CLOSE, 2, 80), (11, HIGH_STAB, 2, 76), (14, CLOSE, 2, 78)],
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 2), (11, D5, 2), (14, R8, 2)],
        "fill_type": "edm_riser",
    },
    "edm_remix": {
        "meter": "4/4", "tempo": 130, "swing": 0.0,
        "tracks": ["House Kit 2", "Electro Kit 2", "SimplePulse Bass", "Rhythmical Synth", "MonoSaw 2 Oct.", "Big Side Attack", "Bros Buzz Y+", "Rich Lead"],
        "drum_mode": "four_floor", "bass_mode": "house_pump", "acc1_mode": "house_piano", "acc3_mode": "trance_gate",
        "hook": [(0, R8, 1), (2, R8, 1), (3, U3, 2), (6, U5, 2), (8, U8, 3), (14, U5, 2)],
        "fill_type": "edm_riser",
    },
    # Daft Punk ("Get Lucky" / "Lose Yourself to Dance"): Funky 16th Single-Coil Strat + Octave Slap/Finger Bass + Rhodes!
    "nu_disco": {
        "meter": "4/4", "tempo": 116, "swing": 0.12,
        "tracks": ["Dance Kit", "Standard PercKit", "JB Fing.Slap Bs", "Strat N Cln DNC", "Suit Case88 EP1", "Analog Pad 1", "Tight Brass 1", "Vocoder" if False else "Thin PulSeq DNC"],
        "drum_mode": "disco", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(4, 39, 86), (12, 39, 86)],
        "bass_pat": [(0, R, 2), (2, R8, 2), (4, R, 2), (6, D5, 2), (8, R, 2), (10, R8, 2), (12, B7, 2), (14, R8, 2)],
        "acc1_mode": "funk_chuck", "acc2_mode": "jazz_comp",
        "hook": [(2, U3, 1), (3, U5, 2), (6, U6, 2), (10, U5, 2), (14, U3, 2)],
        "fill_type": "funk_sync",
    },
    "dance_pop_reload": {
        "meter": "4/4", "tempo": 126, "swing": 0.0,
        "tracks": ["House Kit 1", "Dance Kit", "Euro Bass", "90’s Piano", "Chorus Gtr Pro", "Symphonic Ens.", "Power Saw", "Next Dance DNC"],
        "drum_mode": "four_floor", "bass_mode": "offbeat_edm", "acc1_mode": "house_piano", "acc2_mode": "synth_seq_16",
        "hook": [(0, U5, 3), (3, U5, 3), (6, U6, 2), (8, U5, 2), (10, U3, 2), (12, R8, 4)],
        "fill_type": "edm_riser",
    },
    # Trap ("Turn Down for What" / Modern Atlanta 808): Half-time snare on beat 3, booming 808 sub, rapid hi-hat rolls, brass stabs!
    "trap": {
        "meter": "4/4", "tempo": 140, "swing": 0.06,
        "tracks": ["HipHop Kit 1", "Electro Kit 3", "Jungle Bass", "Metallic Syn Seq", "Dark Pad", "Brass of Power", "Bell Tine EP", "Fast Glide Saw"],
        "drum_mode": "trap_halftime",
        "bass_mode": "trap_808",
        "acc1_steps": [(0, R8, 2, 82), (3, B2, 2, 78), (6, R8, 2, 80), (12, D5, 4, 78)],
        "acc4_steps": [(0, HIGH_STAB, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, R8, 3), (3, B3, 3), (6, R8, 2), (8, B2, 4), (16, R8, 3), (19, D5, 5)],
        "cadence": "modal_bVII", "fill_type": "edm_riser",
    },
    # Classic 90s Club House (Robin S "Show Me Love" M1 Piano + Organ Bass!)
    "house_class": {
        "meter": "4/4", "tempo": 122, "swing": 0.14,
        "tracks": ["House Kit 1", "Latin Perc.Kit 1", "Organ Low 1", "M1 Piano", "60’s Organ", "Warm Pad", "Strings&Orch.V.", "Dance Lead"],
        "drum_mode": "house",
        "bass_pat": [(0, R, 2), (3, D3, 2), (6, D5, 2), (9, B7, 2), (10, R8, 2), (14, D5, 2)],
        "acc1_mode": "house_piano",
        "hook": [(0, R8, 2), (3, U3, 2), (6, D5, 2), (9, B7, 2), (10, R8, 2), (14, D5, 2)],
    },
    # Disclosure / Duke Dumont Deep House (Quartal warm chords + syncopated FM/Disclosure bass)
    "deep_house": {
        "meter": "4/4", "tempo": 122, "swing": 0.16,
        "tracks": ["House Kit 2", "Standard PercKit", "Disclosure Bass", "Club E. Piano", "Warm Pad", "Dark Anna", "Muted Guitar" if False else "Strat N Cln Mute", "Deep Modul. DNC"],
        "drum_mode": "house", "open_hat_note": 42,
        "bass_pat": [(2, R, 2), (5, R, 2), (8, D5, 3), (14, B7, 2)],
        "acc1_mode": "house_piano", "quartal": True,
        "hook": [(2, U3, 3), (8, R8, 4), (18, U5, 3), (24, U3, 4)],
    },
    "deep_remix": {
        "meter": "4/4", "tempo": 124, "swing": 0.12,
        "tracks": ["Dance Kit", "House Kit 2", "Dr. Octave", "Suit E.Piano 1", "RealFolk Gtr DNC", "Motion Ocean", "Soft Horns 1", "Marimba Syn Seq"],
        "drum_mode": "house", "bass_mode": "house_pump",
        "acc1_steps": [(0, QUARTAL, 3, 76), (6, QUARTAL, 4, 78), (12, QUARTAL, 4, 74)],
        "acc2_mode": "pop_strum",
        "hook": [(0, D5, 2), (3, R8, 3), (6, U3, 3), (12, R8, 4)],
    },
    "reggaeton_dj": {
        "meter": "4/4", "tempo": 98, "swing": 0.06,
        "tracks": ["HipHop Kit 2", "Latin Perc.Kit 1", "Phat Bass", "Dance Syn Perc", "Concert Gtr DNC", "Techno Stab DNC", "Tight Brass 1", "Summit Pulse"],
        "drum_mode": "reggaeton_dembow", "kicks": [0, 4, 8, 12], "snares": [3, 6, 11, 14],
        "bass_pat": [(0, R, 4), (6, B7, 2), (8, R, 4), (14, D5, 2)],
        "acc1_steps": [(0, HIGH_STAB, 1, 82), (3, HIGH_STAB, 1, 78), (6, HIGH_STAB, 1, 82), (11, HIGH_STAB, 1, 78)],
        "hook": [(0, R8, 2), (3, B3, 2), (6, D5, 2), (8, R8, 4)],
    },
    "trance": {
        "meter": "4/4", "tempo": 136, "swing": 0.0,
        "tracks": ["Trance Kit", "Electro Kit 1", "Euro Bass", "Parallel Trance", "MonoSaw 3 Oct.", "Ravelian Pad", "Big Side Attack", "Trance Filter"],
        "drum_mode": "trance",
        "bass_pat": [(1, R, 1), (2, R, 1), (3, R8, 1), (5, R, 1), (6, R, 1), (7, R8, 1), (9, R, 1), (10, R, 1), (11, R8, 1), (13, D5, 1), (14, D5, 1), (15, R8, 1)],
        "acc2_mode": "synth_seq_16", "acc3_mode": "trance_gate",
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 2), (6, U8, 4), (12, U6, 2), (14, U5, 2)],
        "fill_type": "edm_riser",
    },
    # Tribal House (Dense polyrhythmic congas, bongos, toms, deep sub kick!)
    "tribal": {
        "meter": "4/4", "tempo": 125, "swing": 0.10,
        "tracks": ["House Kit 2", "Latin Perc.Kit 1", "Sub" if False else "Jungle Bass", "Wood&Metal Seq", "Techno Stab DNC", "Dronas Pad", "Kalimba 1", "Blown Bottle"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "perc_steps": [(0, 64, 84), (2, 60, 68), (3, 63, 78), (5, 61, 66), (6, 64, 80), (7, 70, 56), (9, 62, 72), (10, 63, 78), (12, 64, 82), (14, 60, 74), (15, 63, 76)],
        "bass_pat": [(0, R, 3), (6, R, 2), (10, D5, 2), (14, B7, 2)],
        "acc1_steps": [(3, QUARTAL, 1, 76), (11, QUARTAL, 1, 76)],
        "hook": [(0, R8, 2), (3, D4, 2), (6, D5, 2), (10, B7, 2), (12, R8, 4)],
    },
    # 80s Synthpop / Italo-Disco ("Blue Monday" / Pet Shop Boys / Giorgio Moroder 16th octave bass!)
    "80_s_dance": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Gate Kit Amb", "Synth Kit 2", "Synth Bass 80ish", "FM Stack EP", "Strat N Cln Mute", "Analog Pad 1", "Fat Brass", "Vintage Monster"],
        "drum_mode": "four_floor", "snare_note": 40,
        "bass_pat": [(0, R, 1), (2, R8, 1), (4, R, 1), (6, R8, 1), (8, R, 1), (10, R8, 1), (12, R, 1), (14, R8, 1)],
        "acc1_steps": [(0, OPEN, 2, 78), (6, HIGH_STAB, 2, 80), (12, CLOSE, 3, 78)],
        "acc4_steps": [(0, HIGH_STAB, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 4), (10, U9, 2), (12, U3, 4)],
    },
    # 90s Eurodance (Snap! "Rhythm Is a Dancer" / Haddaway "What Is Love" offbeat bass + M1 piano!)
    "90_s_dance": {
        "meter": "4/4", "tempo": 128, "swing": 0.0,
        "tracks": ["Dance Kit", "House Kit 3", "Euro Bass", "90’s Piano", "Techno Stab DNC", "Warm Buzz", "Power Saw", "Octo Lead"],
        "drum_mode": "euro_90s", "bass_mode": "offbeat_edm",
        "acc1_steps": [(0, HIGH_STAB, 2, 84), (3, HIGH_STAB, 2, 82), (6, HIGH_STAB, 2, 84), (8, CLOSE, 2, 78), (11, HIGH_STAB, 2, 82), (14, CLOSE, 2, 78)],
        "hook": [(0, U3, 2), (3, U5, 2), (6, U3, 2), (8, R8, 2), (11, U9, 2), (14, R8, 2)],
        "fill_type": "edm_riser",
    },
    # Ethno / Balkan / Middle-Eastern Club House (Oud +Kanun + Darbuka + House 4/4!)
    "ethno_house": {
        "meter": "4/4", "tempo": 121, "swing": 0.08,
        "tracks": ["House Kit 1", "Oriental PercKit", "Synth Bass 1", "Oud 1", "Kanoun 1", "Arabic Strings", "Klarnet 1", "Zurna 1"],
        "drum_mode": "four_floor",
        "perc_steps": [(0, 64, 84), (3, 62, 74), (6, 64, 80), (8, 62, 70), (12, 62, 78), (14, 63, 74)],
        "bass_mode": "house_pump",
        "acc1_steps": [(0, R, 2, 80), (3, B2, 2, 76), (6, D3, 2, 80), (10, D4, 2, 76), (12, D3, 2, 78), (14, B2, 2, 74)],
        "hook": [(0, D5, 2), (2, S5, 2), (4, D5, 2), (6, D4, 2), (8, D3, 3), (11, B2, 1), (12, R, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "oriental_darbuka",
    },
    "spanish_remix": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Basic Saw Bass", "Concert Gtr DNC", "Real Nylon Gtr", "Warm Pad", "Trumpet Expr.1", "Accordion"],
        "drum_mode": "four_floor",
        "perc_steps": [(3, 39, 80), (6, 85, 68), (10, 39, 80), (14, 85, 70)],
        "bass_mode": "disco_oct", "acc1_mode": "pop_strum",
        "hook": [(0, U5, 2), (3, S5, 2), (6, U5, 2), (8, U3, 4), (12, B2, 2), (14, R8, 2)],
        "cadence": "flamenco_bVI_V",
    },
    "chacha_remix": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Dance Kit Remix", "Latin Perc.Kit 2", "Phunk Synth Bass", "Bright Piano", "Nylon GuitarDNC", "Tight Brass 1", "Vibraphone 1", "Jazz Flute Expr."],
        "drum_mode": "chacha", "kicks": [0, 4, 8, 12],
        "bass_pat": [(0, R, 3), (4, D5, 2), (6, R8, 2), (8, R, 3), (12, D5, 2), (14, D6, 2)],
        "acc1_mode": "salsa_montuno",
        "hook": [(0, U3, 2), (4, U5, 2), (8, R8, 1), (10, U9, 1), (12, U3, 4)],
        "fill_type": "latin_timbale",
    },
    # Agnes ("Release Me"): Lush Disco-Strings Dance-Pop!
    "release_my_dance": {
        "meter": "4/4", "tempo": 127, "swing": 0.0,
        "tracks": ["Dance Kit", "Standard PercKit", "Euro Bass", "Pop Grand", "Strat N Cln Mute", "Movie Str.1 DNC", "French Section", "Next Dance DNC"],
        "drum_mode": "disco", "bass_mode": "disco_oct", "acc1_mode": "house_piano", "acc3_mode": "spiccato_8",
        "hook": [(0, U5, 3), (3, U6, 3), (6, U5, 2), (8, U3, 4), (12, U9, 2), (14, R8, 2)],
    },
    # OneRepublic ("Counting Stars"): Stomping Folk-Dance Crossover!
    "counting_dance": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "SteelGtrPro DNC", "Pop Grand", "Warm Strings", "Mandolin DNC", "Bright Piano"],
        "drum_mode": "four_floor",
        "perc_steps": [(4, 54, 76), (12, 54, 78)],
        "bass_mode": "root_8", "acc1_mode": "pop_strum", "acc2_mode": "banjo_roll",
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 3), (7, U3, 1), (8, R8, 4)],
    },
    # Chic / Sister Sledge ("Le Freak" / "Good Times") Funky Disco!
    "funky_disco": {
        "meter": "4/4", "tempo": 122, "swing": 0.08,
        "tracks": ["Funk Kit 1 Amb", "Latin Perc.Kit 1", "Finger Bass DN1", "Strat N Cln DNC", "Classic Piano", "Real Strings 1", "Tight Brass 1", "Tenor Sax DN1"],
        "drum_mode": "disco",
        "bass_pat": [(0, R, 2), (2, R, 2), (4, D3, 2), (6, D5, 2), (8, D6, 2), (11, B7, 1), (12, R8, 2), (14, D5, 2)],
        "acc1_mode": "funk_chuck",
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 4), (18, U6, 2), (20, U5, 4)],
    },
    "70_s_disco_remix": {
        "meter": "4/4", "tempo": 121, "swing": 0.04,
        "tracks": ["Dance Kit", "Latin Perc.Kit 2", "Slap Bass 1", "Strat N Cln Mute", "Club E. Piano", "Full Strings", "Brass of Power", "Flute & Muted"],
        "drum_mode": "disco", "bass_mode": "disco_oct", "acc1_mode": "funk_chuck", "acc2_mode": "house_piano",
        "hook": [(0, R8, 1), (2, R8, 1), (4, U5, 4), (16, U6, 2), (18, U5, 2), (20, U3, 4)],
    },
    # Bee Gees / Donna Summer ("Stayin' Alive" / "Hot Stuff") 70s Disco Fever!
    "disco_fever": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Pop Std. Kit 1", "Latin Perc.Kit 1", "JB Pick Bs DN1", "Strat N Cln Mute", "Pop Grand", "Movie Str.1 DNC", "Tight Brass 1", "Falsetto" if False else "Lead" if False else "Jazz Flute Expr."],
        "drum_mode": "disco", "bass_mode": "disco_oct",
        "acc1_steps": [(2, CHUCK, 1, 80), (6, HIGH_STAB, 2, 82), (10, CHUCK, 1, 80), (14, HIGH_STAB, 2, 82)],
        "acc4_steps": [(0, THIRDS, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, U5, 4), (4, U6, 2), (6, U8, 6), (16, U6, 2), (18, U5, 2), (20, U3, 4)],
    },
    # Enrique Iglesias ("Bailando"): Flamenco Guitar + Reggaeton Dembow Dance!
    "bailando_dance": {
        "meter": "4/4", "tempo": 100, "swing": 0.04,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Synth Bass Warm", "Concert Gtr DNC", "Real Nylon Gtr", "Accordion", "Real Strings 1", "Concert Gtr Pro"],
        "drum_mode": "reggaeton_dembow",
        "perc_steps": [(3, 39, 82), (6, 39, 78), (11, 39, 82), (14, 85, 68)],
        "bass_mode": "reggaeton_sub", "acc1_mode": "pop_strum",
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 2), (8, U3, 4), (12, U9, 2), (14, R8, 2)],
        "cadence": "flamenco_bVI_V",
    },
    # Avicii ("Hey Brother" / "Wake Me Up"): Country-Folk Acoustic Strum + Four-on-the-Floor EDM Drop + Trumpet/Saw!
    "brother_dance": {
        "meter": "4/4", "tempo": 125, "swing": 0.0,
        "tracks": ["Dance Kit Remix", "Standard PercKit", "Basic Saw Bass", "SteelGtrPro DNC", "Banjo", "Big Side Attack", "Concert Trumpet", "Power Saw"],
        "drum_mode": "four_floor", "bass_mode": "root_8",
        "acc1_steps": [(0, STRUM_DN, 2, 84), (2, STRUM_UP, 1, 70), (3, STRUM_DN, 2, 80), (6, STRUM_UP, 2, 76), (8, STRUM_DN, 2, 84), (11, STRUM_UP, 2, 76), (14, STRUM_DN, 2, 80)],
        "acc2_mode": "banjo_roll",
        "hook": [(0, R8, 3), (3, U3, 3), (6, U5, 2), (8, U6, 2), (10, U5, 2), (12, U3, 4)],
        "fill_type": "edm_riser",
    },
    # Tacabro ("Tacata") Electro-Latin Club Bounce
    "tacata_dance": {
        "meter": "4/4", "tempo": 126, "swing": 0.06,
        "tracks": ["Electro Kit 2", "Latin Perc.Kit 2", "SimplePulse Bass", "Accordion", "Techno Stab DNC", "Square Pad", "Tight Brass 2", "Summit Pulse"],
        "drum_mode": "four_floor",
        "perc_steps": [(3, 65, 76), (6, 66, 76), (14, 56, 72)],
        "bass_pat": [(0, R, 2), (3, R8, 2), (6, R, 2), (10, R8, 2), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, R8, 1), (2, R8, 1), (4, B3, 2), (6, R8, 2), (12, B7, 2), (14, R8, 2)],
    },
    # Don Omar / Lucenzo ("Danza Kuduro"): Angolan/Portuguese Kuduro Dance + Accordion Hook!
    "kuduro_dance": {
        "meter": "4/4", "tempo": 130, "swing": 0.04,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Euro Bass", "Accordion", "Nylon GuitarDNC", "Synth Brass" if False else "Fat Brass", "Square Pad", "Fisa Master"],
        "drum_mode": "four_floor", "snares": [3, 6, 11, 14],
        "bass_pat": [(0, R, 3), (3, D5, 3), (6, R, 2), (8, R, 3), (11, D5, 3), (14, B7, 2)],
        "acc1_steps": [(0, THIRDS, 2, 84), (3, THIRDS, 2, 82), (6, THIRDS, 2, 84), (10, CLOSE, 2, 78), (12, CLOSE, 2, 78)],
        "hook": [(0, U3, 2), (3, U5, 2), (6, U6, 2), (8, U5, 2), (10, U3, 2), (12, U9, 2), (14, R8, 2)],
    },
    # Western Country-House Remix
    "western_remix": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["House Kit 1", "Standard PercKit", "Basic Saw Bass", "RealFolk Gtr DNC", "Pedal Steel", "Harmonica 1 DN1", "Warm Pad", "Fiddle"],
        "drum_mode": "four_floor", "bass_mode": "offbeat_edm", "acc1_mode": "pop_strum", "acc2_mode": "banjo_roll",
        "hook": [(0, R8, 2), (2, D6, 2), (4, D5, 2), (6, D3, 2), (8, R, 4), (16, U3, 2), (18, U5, 6)],
    },
    # Rednex ("Cotton Eye Joe"): Eurodance Stomp + Blazing Fiddle & 5-String Banjo!
    "cowboy_dance": {
        "meter": "4/4", "tempo": 132, "swing": 0.0,
        "tracks": ["Dance Kit", "Standard PercKit", "Euro Bass", "Banjo", "SteelGtrPro DNC", "Fiddle", "Power Saw", "Fiddle"],
        "drum_mode": "four_floor",
        "perc_steps": [(4, 39, 88), (12, 39, 88)],
        "bass_mode": "disco_oct", "acc1_mode": "oom_pah_off", "acc2_mode": "banjo_roll",
        "hook": [(0, U5, 2), (2, U5, 1), (3, U6, 1), (4, U5, 2), (6, U3, 2), (8, R8, 2), (10, U9, 2), (12, R8, 4)],
    },
    # Shakira ("Waka Waka"): Bright African Soukous Clean Guitar Arpeggio + Percussion + Afro-Dance Beat!
    "waka_dance": {
        "meter": "4/4", "tempo": 127, "swing": 0.06,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Finger Bass DN1", "Single Coil Pro", "Marimba", "Scat Voices DNC", "Tight Brass 1", "Kalimba 1"],
        "drum_mode": "four_floor",
        "perc_steps": [(0, 64, 78), (3, 63, 74), (6, 62, 72), (8, 70, 60), (11, 63, 74), (14, 64, 78)],
        "bass_pat": [(0, R, 3), (3, D3, 3), (6, D5, 2), (8, R8, 3), (11, D5, 3), (14, D3, 2)],
        "acc1_steps": [(0, R8, 1, 80), (2, U3, 1, 78), (3, U5, 1, 82), (6, U3, 2, 78), (8, R8, 1, 80), (10, U5, 1, 82), (11, U6, 1, 80), (14, U5, 2, 78)],
        "hook": [(0, U3, 2), (2, U3, 2), (4, U5, 2), (6, R8, 4), (16, U5, 2), (18, U6, 2), (20, U5, 4)],
    },
    # PSY ("Gangnam Style"): Electro-Shuffle K-Pop Bounce!
    "gangnam_dance": {
        "meter": "4/4", "tempo": 132, "swing": 0.22, "swing8": True,
        "tracks": ["Dance Kit Remix", "Electro Kit 1", "Bass Phat Saw", "Monster & Dist.", "Techno Stab DNC", "Big Side Attack", "Tight Brass 2", "Power Saw"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, R8, 2), (6, R, 2), (8, R, 2), (10, B7, 2), (12, R, 2), (14, B3, 2)],
        "acc1_steps": [(0, POWER5, 2, 84), (2, POWER5, 2, 78), (6, HIGH_STAB, 2, 86), (10, POWER5, 2, 78), (14, HIGH_STAB, 2, 86)],
        "hook": [(0, R8, 2), (2, R8, 2), (4, B7, 2), (6, R8, 4), (12, B3, 2), (14, D3, 2)],
        "fill_type": "edm_riser",
    },

    # =========================================================================
    # 5. ROCK (34 Styles)
    # =========================================================================
    # Foo Fighters ("Learn to Fly" / "Everlong"): Pushed 8th-note wall of guitars + pounding Dave Grohl drums!
    "foo_rock": {
        "meter": "4/4", "tempo": 136, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "Stereo Dist.Gtr", "Crunch Gtr DNC", "RealFolk Gtr DNC", "Rock Piano", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "kicks": [0, 3, 6, 8, 10], "snares": [4, 12],
        "bass_mode": "root_8", "acc1_mode": "rock_power_8",
        "acc2_seq": [(0, POWER8, 3), (3, POWER8, 3), (6, POWER5, 2), (8, POWER8, 4), (12, POWER5, 4)],
        "hook": [(0, U5, 3), (3, U5, 3), (6, U6, 2), (8, U5, 4), (12, U3, 4)],
        "cadence": "rock_bVII_IV", "fill_type": "rock_tom",
    },
    # Green Day ("21 Guns" / "Boulevard"): Acoustic verse -> soaring stadium power-chord anthem!
    "21_gun_anthem": {
        "meter": "4/4", "tempo": 82, "swing": 0.0,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN2", "SteelGtrPro DNC", "Stereo Dist.Gtr", "Real Strings 1", "Pop Grand", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "kicks": [0, 7, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (7, L5, 1), (8, D5, 6), (14, B7, 2)],
        "acc1_mode": "pop_strum",
        "acc2_seq": [(0, POWER8, 6), (8, POWER8, 8)],
        "hook": [(0, U5, 4), (4, U3, 4), (8, U9, 4), (12, R8, 4), (16, U3, 4), (20, D5, 8)],
        "cadence": "rock_bVII_IV", "fill_type": "rock_tom",
    },
    # Kid Rock ("All Summer Long" — "Sweet Home" + "Werewolves of London" piano-guitar rock!)
    "first_kid_rock": {
        "meter": "4/4", "tempo": 104, "swing": 0.04,
        "tracks": ["Rock Kit 2 Amb", "Standard PercKit", "Vintage P. Pick", "Rock Piano", "Crunch Gtr DNC", "RealFolk Gtr DNC", "BX3 Rock 1", "Single Coil Pro"],
        "drum_mode": "rock_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (6, B7, 2), (8, D4, 4), (12, R, 4)],
        "acc1_steps": [(0, OPEN, 3, 84), (3, CLOSE, 3, 80), (6, HIGH_STAB, 2, 84), (8, CLOSE, 4, 78), (12, CLOSE, 4, 80)],
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 3), (16, B7, 2), (18, D6, 2), (20, D5, 4)],
        "cadence": "rock_bVII_IV", "fill_type": "rock_tom",
    },
    # The Killers ("Mr. Brightside"): 148 BPM four-on-the-floor indie-rock kick + iconic 16th arpeggiated bright overdrive!
    "killer_rock": {
        "meter": "4/4", "tempo": 148, "swing": 0.0,
        "tracks": ["Power Kit 2 Amb", "Standard PercKit", "JB Pick Bs DN1", "Crunch Gtr DNC", "Stereo Dist.Gtr", "Analog Pad 1", "Fat Synth", "E.Gtr Ch/Dly DNC"],
        "drum_mode": "four_floor", "hat_note": 46, "snares": [4, 12],
        "bass_mode": "root_8",
        "acc1_steps": [(0, R8, 1, 80), (1, U5, 1, 72), (2, U3, 1, 76), (3, U5, 1, 72), (4, U8, 1, 82), (5, U5, 1, 72), (6, U3, 1, 76), (7, U5, 1, 72),
                       (8, R8, 1, 80), (9, U5, 1, 72), (10, U3, 1, 76), (11, U5, 1, 72), (12, U8, 2, 82), (14, U5, 2, 74)],
        "acc2_mode": "rock_power_8",
        "hook": [(0, U5, 2), (2, U5, 2), (4, U6, 2), (6, U5, 2), (8, U3, 4)],
        "fill_type": "rock_tom",
    },
    # AC/DC ("Highway to Hell"): Tight syncopated crunch guitar stabs with space, rock-solid Phil Rudd pocket!
    "highwayhell_rock": {
        "meter": "4/4", "tempo": 116, "swing": 0.06,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "Vintage P. Pick", "Crunch Gtr DNC", "Stereo Dist.Gtr", "BX3 Rock 2", "Rock Piano", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "kicks": [0, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (6, R, 2), (8, R, 4), (14, L5, 2)],
        "acc1_steps": [(0, POWER8, 2, 90), (6, POWER5, 1, 84), (7, POWER5, 1, 86), (9, POWER8, 3, 90)],
        "hook": [(6, POWER5, 1), (7, POWER5, 1), (9, POWER8, 3), (22, FOURTHS, 2), (25, POWER8, 3)],
        "cadence": "rock_bVII_IV", "fill_type": "rock_tom",
    },
    # Kings of Leon ("Sex on Fire"): Driving 152 BPM 8th-note delay guitar + propulsive kick/tom rock!
    "rock_on_fire": {
        "meter": "4/4", "tempo": 152, "swing": 0.0,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "E.Gtr Ch/Dly DNC", "Stereo Dist.Gtr", "Warm Pad", "BX3 Rock 1", "Crunch Gtr DNC"],
        "drum_mode": "rock_8", "kicks": [0, 3, 6, 8, 11, 14], "snares": [4, 12],
        "bass_mode": "root_8", "acc1_mode": "rock_power_8",
        "hook": [(0, U3, 2), (2, U3, 2), (4, U5, 2), (6, R8, 4), (16, U6, 2), (18, U5, 2), (20, U3, 4)],
        "fill_type": "rock_tom",
    },
    # Guns N' Roses ("Welcome to the Jungle"): Dotted-8th delay punk-metal riff + cowbell + sleazy groove!
    "welcome_rock": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Power Kit 2 Amb", "Standard PercKit", "Picked E. Bass 2", "Dist. Gtr 1 DNC", "Stereo Dist.Gtr", "BX3 Rock 3", "Sforzato Brass", "Crunch Gtr DNC"],
        "drum_mode": "rock_8", "kicks": [0, 6, 8, 11, 14], "snares": [4, 12],
        "perc_steps": [(0, 56, 70), (4, 56, 66), (8, 56, 70), (12, 56, 66)],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, B7, 2), (6, R, 2), (8, B5, 2), (10, D5, 2), (12, D4, 2), (14, B3, 2)],
        "acc1_mode": "rock_power_8",
        "hook": [(0, R8, 3), (3, B7, 3), (6, D5, 2), (8, D4, 2), (10, B3, 2), (12, R, 4)],
        "cadence": "rock_bVII_IV", "fill_type": "rock_tom",
    },
    "rock_star": {
        "meter": "4/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Rock Kit 2 Amb", "Standard PercKit", "JB Pick Bs DN1", "Stereo Dist.Gtr", "RealFolk Gtr DNC", "BX3 Rock 1", "Rock Piano", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "kicks": [0, 7, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, R, 1), (6, B7, 2), (8, R, 4), (12, D4, 2), (14, D5, 2)],
        "acc1_mode": "rock_power_8", "acc2_mode": "pop_strum",
        "hook": [(0, POWER8, 3), (6, FOURTHS, 2), (8, POWER8, 4)],
        "fill_type": "rock_tom",
    },
    # Van Halen / Bon Jovi ("Jump" / "Livin' on a Prayer"): Chugging 8th bass + iconic Oberheim Polysynth brassy stabs!
    "80_s_rock": {
        "meter": "4/4", "tempo": 126, "swing": 0.0,
        "tracks": ["Gate Kit Amb", "Standard PercKit", "Picked E. Bass 4", "Fat Synth", "Stereo Dist.Gtr", "Analog Pad 1", "Power Saw", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "snare_note": 40, "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, R, 2), (6, R, 2), (8, R, 2), (10, R, 2), (12, R, 2), (14, R, 2)],
        "acc1_steps": [(0, OPEN, 3, 86), (6, HIGH_STAB, 4, 88), (12, CLOSE, 4, 84)],
        "acc2_mode": "rock_power_8",
        "hook": [(0, U5, 3), (6, U3, 3), (12, U4 if False else D4, 2), (14, D5, 2), (18, U3, 4), (24, R8, 6)],
        "cadence": "rock_bVII_IV", "fill_type": "rock_tom",
    },
    "rock_punch": {
        "meter": "4/4", "tempo": 128, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "Crunch Gtr DNC", "Rock Piano", "BX3 Rock 2", "Tight Brass 1", "Stereo Dist.Gtr"],
        "drum_mode": "rock_8", "kicks": [0, 2, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (8, R, 2), (10, D5, 2), (14, B7, 2)],
        "acc1_steps": [(0, POWER8, 2, 88), (2, POWER8, 2, 86), (8, POWER8, 2, 88), (10, POWER5, 2, 84), (14, FOURTHS, 2, 82)],
        "hook": [(0, R8, 2), (2, R8, 2), (8, U3, 2), (10, D5, 4)],
        "fill_type": "rock_tom",
    },
    # ZZ Top ("La Grange"): Driving Texas Boogie Blues-Rock!
    "rolling_blues": {
        "meter": "4/4", "tempo": 156, "swing": 0.28, "swing8": True,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "Vintage P. Pick", "Crunch Gtr DNC", "Dist. Gtr 1 DNC", "BX3 Rock 1", "Harmonica 1 DN1", "Rock Piano"],
        "drum_mode": "pop_8", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, B3, 2), (6, D3, 2), (8, R, 2), (10, R, 2), (12, D5, 2), (14, B7, 2)],
        "acc1_steps": [(2, POWER5, 2, 86), (6, FOURTHS, 2, 84), (10, POWER5, 2, 86), (14, FOURTHS, 2, 84)],
        "hook": [(2, B3, 2), (6, D4, 2), (8, R, 4), (18, B7, 2), (22, D5, 4)],
        "cadence": "blues_V_IV", "fill_type": "rock_tom",
    },
    # Lynyrd Skynyrd ("Sweet Home Alabama"): Clean-crunch picked Southern Rock Guitar + Honky-Tonk Piano!
    "alabama_rock": {
        "meter": "4/4", "tempo": 98, "swing": 0.06,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Vintage P. Bass", "Single Coil Pro", "Honky-Tonk", "Crunch Gtr DNC", "BX3 Rock 1", "Slide" if False else "RealFolk Gtr DNC"],
        "drum_mode": "rock_8", "kicks": [0, 6, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, R, 1), (6, B7, 2), (8, D4, 4), (14, D5, 2)],
        "acc1_steps": [(0, R, 1, 82), (2, R, 1, 78), (3, R8, 1, 84), (5, D5, 1, 76), (6, B7, 2, 82), (8, D4, 2, 80), (10, U3, 2, 78), (12, D5, 4, 80)],
        "acc2_mode": "boogie_comp",
        "hook": [(12, R8, 1), (13, B7, 1), (14, D5, 2), (28, D3, 1), (29, D2, 1), (30, R, 2)],
        "cadence": "rock_bVII_IV",
    },
    # Dire Straits / Police ("Sultans of Swing" / "Every Breath") Crisp Clean Strat Rock
    "clean_rock": {
        "meter": "4/4", "tempo": 118, "swing": 0.04,
        "tracks": ["Studio Kit", "Standard PercKit", "JB Finger BsDN1", "Strat N Cln DNC", "Real El. Gtr ST1", "Jazz Organ", "Pop Grand", "Single Coil"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_mode": "pop_sync",
        "acc1_steps": [(0, R, 1, 76), (1, D5, 1, 72), (2, U9, 1, 78), (3, D5, 1, 72), (4, U3, 1, 80), (5, D5, 1, 72), (6, U9, 2, 76),
                       (8, R, 1, 76), (9, D5, 1, 72), (10, U9, 1, 78), (11, D5, 1, 72), (12, U3, 2, 80), (14, D5, 2, 72)],
        "hook": [(2, U5, 2), (4, U3, 2), (6, R8, 4), (18, U9, 2), (20, D5, 4)],
    },
    # Queen ("We Are the Champions"): Majestic 6/8 Stadium Rock Piano & Brian May Guitar Anthem!
    "stadium_ballad": {
        "meter": "6/8", "tempo": 66, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "Rock Piano", "Stereo Dist.Gtr", "OrchestraTutti 1", "Choir Aahs GM", "Dist. Gtr 1 DNC"],
        "drum_mode": "ballad_6_8", "kicks": [0, 4, 10],
        "bass_pat": [(0, R, 6), (6, D5, 4), (10, L5, 2)],
        "acc1_steps": [(0, OPEN, 4, 84), (4, CLOSE, 2, 76), (6, OPEN, 4, 86), (10, CLOSE, 2, 76)],
        "acc2_seq": [(0, POWER8, 6), (6, POWER8, 6)],
        "hook": [(0, U3, 4), (4, U5, 2), (6, U3, 6), (12, U6, 4), (16, U5, 8)],
        "fill_type": "rock_tom",
    },
    # Rolling Stones ("Start Me Up" / "Honky Tonk Women"): Open-G Keith Richards syncopated riff + cowbell + saloon piano!
    "rolling_rock": {
        "meter": "4/4", "tempo": 122, "swing": 0.08,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Bass", "Crunch Gtr DNC", "Honky-Tonk", "BX3 Rock 1", "Tenor Growl DN1", "Single Coil Pro"],
        "drum_mode": "rock_8", "kicks": [0, 8, 10], "snares": [4, 12],
        "perc_steps": [(0, 56, 78), (4, 56, 72), (8, 56, 78), (12, 56, 72)],
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, R, 4), (12, D3, 2), (14, D5, 2)],
        "acc1_steps": [(0, CLOSE, 3, 86), (3, FOURTHS, 3, 88), (8, CLOSE, 4, 84), (14, FOURTHS, 2, 82)],
        "hook": [(0, CLOSE, 3), (3, FOURTHS, 3), (8, CLOSE, 4)],
    },
    # Queen ("A Kind of Magic") / Police Syncopated Bass-Driven Magic Rock
    "magic_rock": {
        "meter": "4/4", "tempo": 126, "swing": 0.14,
        "tracks": ["Power Kit 2 Amb", "Standard PercKit", "JB Pick Bs DN1", "Crunch Gtr DNC", "Fat Synth", "Warm Pad", "Stereo Dist.Gtr", "Dist. Gtr 1 DNC"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, R, 2), (6, D3, 2), (8, D5, 2), (10, D5, 2), (12, D6, 2), (14, D5, 2)],
        "acc1_mode": "rock_power_8",
        "hook": [(0, R8, 2), (4, U3, 2), (6, U5, 4), (16, U6, 2), (20, U5, 4)],
    },
    # Elvis Presley ("Jailhouse Rock"): Stop-time double-hit rock'n'roll break + walking bass!
    "prison_rock": {
        "meter": "4/4", "tempo": 162, "swing": 0.26, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Rock Piano", "Clean Jazz 1", "Tenor Growl DN1", "Baritone Sax DN1", "Single Coil"],
        "drum_mode": "pop_8", "kicks": [0, 2, 8], "snares": [4, 12],
        "bass_mode": "boogie_8",
        "acc1_steps": [(0, HIGH_STAB, 2, 88), (2, CLOSE, 2, 88), (8, CLOSE, 2, 78), (12, CLOSE, 2, 80)],
        "hook": [(0, LT, 2), (2, R8, 4), (8, B3, 2), (10, D3, 2), (12, D5, 4)],
        "cadence": "blues_V_IV",
    },
    # Chuck Berry ("Johnny B. Goode"): Straight-8th rock'n'roll piano + double-stop guitar!
    "johnny_rock": {
        "meter": "4/4", "tempo": 164, "swing": 0.06,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "Crunch Gtr DNC", "Rock Piano", "Tenor Sax DN1", "60’s Organ", "Single Coil Pro"],
        "drum_mode": "rock_8", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "boogie_8",
        "acc1_steps": [(0, POWER5, 2, 84), (2, FOURTHS, 2, 80), (4, POWER5, 2, 84), (6, FOURTHS, 2, 80), (8, POWER5, 2, 84), (10, FOURTHS, 2, 80), (12, POWER5, 2, 84), (14, FOURTHS, 2, 80)],
        "hook": [(0, THIRDS, 2), (2, THIRDS, 2), (4, THIRDS, 2), (6, HIGH_STAB, 2), (8, R8, 4)],
        "cadence": "blues_V_IV",
    },
    # Bill Haley ("Rock Around the Clock"): Slap bass + sax riff + snare rim/brush swing!
    "rock_the_clock": {
        "meter": "4/4", "tempo": 168, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Clean Jazz 1", "Ragtime Piano", "Tenor Sax DN1", "Jazz Trb. DN1", "Single Coil"],
        "drum_mode": "jazz_swing", "kicks": [0, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (4, D3, 2), (8, D5, 2), (12, D6, 2), (14, D5, 2)],
        "acc1_steps": [(0, CLOSE, 2, 80), (4, CLOSE, 2, 82), (8, CLOSE, 2, 80), (12, CLOSE, 2, 82)],
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 2), (6, U3, 2), (8, B7, 4), (12, D5, 4)],
        "cadence": "blues_V_IV",
    },
    # Stray Cats / Carl Perkins Rockabilly: Slap Upright Bass + Twangy Gretsch Guitar!
    "rockabilly": {
        "meter": "4/4", "tempo": 166, "swing": 0.26, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Acous. Bass Pro1", "Single Coil Pro", "RealFolk Gtr DNC", "Rock Piano", "Tenor Growl DN1", "Clean Jazz 1"],
        "drum_mode": "country_train", "kicks": [0, 8], "snares": [4, 12],
        "perc_steps": [(2, 37, 62), (6, 37, 68), (10, 37, 62), (14, 37, 68)],
        "bass_pat": [(0, R, 3), (4, D3, 3), (8, D5, 3), (12, D6, 3)],
        "acc1_steps": [(2, CHUCK, 2, 82), (6, STRUM_UP, 2, 80), (10, CHUCK, 2, 82), (14, STRUM_UP, 2, 80)],
        "hook": [(0, R, 2), (2, B3, 2), (4, D3, 2), (6, D5, 2), (8, R8, 4)],
        "cadence": "blues_V_IV",
    },
    "basic_rock": {
        "meter": "4/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "Crunch Gtr DNC", "Rock Piano", "BX3 Rock 1", "RealFolk Gtr DNC", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "root_8", "acc1_mode": "rock_power_8",
        "hook": [(0, R8, 4), (4, D5, 4), (8, B7, 4), (12, D5, 4)],
        "fill_type": "rock_tom",
    },
    # Deep Purple ("Smoke on the Water"): Iconic Parallel-4ths Organ & Overdriven Guitar Riff (`0 -> b3 -> 4`)!
    "smoke_rock": {
        "meter": "4/4", "tempo": 114, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "Picked E. Bass 2", "Dist. Gtr 1 DNC", "BX3 Rock 3", "Stereo Dist.Gtr", "Rock Piano", "BX3 Rock 4"],
        "drum_mode": "rock_8", "hat_note": 46, "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_mode": "root_8",
        "acc1_steps": [(0, FOURTHS, 3, 90), (4, POWER5, 3, 88), (8, FOURTHS, 4, 90), (14, POWER5, 2, 84)],
        "hook": [(0, R, 3), (4, B3, 3), (8, D4, 4), (14, R, 2), (18, B3, 2), (21, B5, 1), (22, D4, 6)],
        "cadence": "modal_bVII", "fill_type": "rock_tom",
    },
    # Bryan Adams ("Summer of '69"): Driving Palm-Muted 8th Rock Guitar + Bright Strum + Organ!
    "69_s_rock": {
        "meter": "4/4", "tempo": 138, "swing": 0.0,
        "tracks": ["Rock Kit 2 Amb", "Standard PercKit", "JB Pick Bs DN1", "Crunch Gtr DNC", "Strum 12Str. DNC", "BX3 Rock 1", "Pop Grand", "Stereo Dist.Gtr"],
        "drum_mode": "rock_8", "kicks": [0, 6, 8, 12], "snares": [4, 12],
        "perc_steps": [(4, 54, 70), (12, 54, 70)],
        "bass_mode": "root_8", "acc1_mode": "rock_power_8", "acc2_mode": "pop_strum",
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 4), (8, U9, 2), (10, U3, 2), (12, D5, 4)],
        "fill_type": "rock_tom",
    },
    # Dire Straits ("Walk of Life"): Fast 2-beat rockabilly-pop + cheerful Farfisa/VOX Organ Melody!
    "walk_of_rock": {
        "meter": "4/4", "tempo": 172, "swing": 0.08,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "Finger Bass DN1", "VOX Legend", "Single Coil Pro", "SteelGtrPro DNC", "Pedal Steel", "60’s Organ"],
        "drum_mode": "pop_8", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat", "acc1_mode": "oom_pah_off", "acc2_mode": "pop_strum",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U6, 2), (6, U5, 4), (12, U3, 2), (14, R8, 2), (16, U9, 4), (20, R8, 4)],
    },
    "50_s_r_roll": {
        "meter": "4/4", "tempo": 154, "swing": 0.26, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "Saloon Piano", "Clean Jazz 1", "Sax Ensemble", "Tight Brass 1", "Tenor Sax DN1"],
        "drum_mode": "pop_8", "kicks": [0, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, D3, 4)],
        "acc1_steps": [(0, CLOSE, 2, 78), (2, CLOSE, 2, 74), (4, CLOSE, 2, 80), (6, CLOSE, 2, 74), (8, CLOSE, 2, 78), (10, CLOSE, 2, 74), (12, CLOSE, 2, 80), (14, CLOSE, 2, 74)],
        "hook": [(0, D5, 2), (4, U3, 2), (6, R8, 4), (16, B7, 2), (20, D5, 4)],
    },
    "60_s_r_roll": {
        "meter": "4/4", "tempo": 150, "swing": 0.0,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Pick", "60’s Organ", "Single Coil", "Bright Piano", "Baritone Sax DN1", "Harmonica 1 DN1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "perc_steps": [(4, 39, 76), (12, 39, 76)],
        "bass_pat": [(0, R, 3), (3, D3, 1), (4, D5, 3), (8, D6, 3), (12, D5, 4)],
        "acc1_mode": "pop_strum",
        "hook": [(0, R8, 2), (3, U3, 3), (8, U5, 2), (11, U3, 3)],
    },
    "rock_oldie": {
        "meter": "4/4", "tempo": 128, "swing": 0.22, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Single Coil", "Rock Piano", "Cycle Scat 1", "Sax Ensemble", "Jazz Gtr 1 DNC"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, D5, 6), (14, D6, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, U5, 4), (4, U3, 4), (8, R8, 4), (12, D6, 4)],
    },
    # Procol Harum / Animals ("House of the Rising Sun"): Arpeggiated Electric Guitar 6/8 Slow Rock + Vox/B3 Organ!
    "6_8_slow_rock": {
        "meter": "6/8", "tempo": 74, "swing": 0.0,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Bass", "Single Coil Pro", "VOX Legend", "BX3 Rock 1", "Rock Piano", "Crunch Gtr DNC"],
        "drum_mode": "ballad_6_8", "kicks": [0, 4, 10],
        "bass_pat": [(0, R, 6), (6, D5, 4), (10, D3, 2)],
        "acc1_steps": [(0, R, 2, 80), (2, D3, 2, 74), (4, D5, 2, 76), (6, R8, 2, 82), (8, D5, 2, 76), (10, D3, 2, 74)],
        "hook": [(0, R8, 4), (4, U3, 2), (6, U5, 6), (12, B7, 4), (16, D5, 2), (18, R8, 6)],
    },
    # Righteous Brothers / Percy Sledge 60s 6/8 Doo-Wop Slow Rock with Triplet Piano!
    "60_s_slow_rock": {
        "meter": "6/8", "tempo": 70, "swing": 0.0,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Classic Piano", "Strat N Cln DNC", "Strings&Orch.V.", "Tenor Sax DN1", "Scat Voices DNC"],
        "drum_mode": "ballad_6_8", "kicks": [0, 10],
        "bass_pat": [(0, R, 6), (6, L5, 4), (10, L6, 2)],
        "acc1_steps": [(0, CLOSE, 2, 78), (2, CLOSE, 2, 72), (4, CLOSE, 2, 72), (6, HIGH_STAB, 2, 80), (8, CLOSE, 2, 72), (10, CLOSE, 2, 72)],
        "hook": [(0, U5, 6), (6, U3, 4), (10, R8, 2), (12, U9, 6), (18, R8, 6)],
    },
    # Santana ("Oye Como Va"): Rock ChaCha with B3 Organ, Congas, Cowbell, Sustaining Overdrive Guitar!
    "rock_chacha": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Rock Kit 1 Amb", "Latin Perc.Kit 1", "JB Finger BsDN1", "BX3 Rock 1", "Crunch Gtr DNC", "Bright Piano", "Tight Brass 1", "Dist. Gtr 1 DNC"],
        "drum_mode": "chacha",
        "bass_pat": [(0, R, 4), (6, B7, 2), (8, D5, 4), (14, R, 2)],
        "acc1_mode": "salsa_montuno",
        "hook": [(0, R8, 2), (4, B7, 2), (6, R8, 4), (16, U3, 2), (18, R8, 2), (20, B7, 2), (22, D5, 4)],
        "cadence": "modal_bVII", "fill_type": "latin_timbale",
    },
    # Santana ("Smooth" / "Black Magic Woman"): Fiery Latin Rock!
    "latin_rock": {
        "meter": "4/4", "tempo": 118, "swing": 0.0,
        "tracks": ["Studio Kit", "Latin Perc.Kit 2", "Finger Bass DN1", "Nylon GuitarDNC", "BX3 Jazz Pc.", "Tight Brass 1", "Bright Piano", "Dist. Gtr 1 DNC"],
        "drum_mode": "salsa_clave", "kicks": [0, 6, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, R, 4), (12, L5, 2), (14, LT, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "salsa_montuno",
        "hook": [(2, R8, 2), (4, U9, 2), (6, U3, 3), (9, U9, 1), (10, R8, 2), (12, LT, 2), (14, R8, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "latin_timbale",
    },
    # Classic 70s Stadium Classic Rock (Bad Company / Free / Eagles)
    "classic_rock": {
        "meter": "4/4", "tempo": 119, "swing": 0.0,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "Crunch Gtr DNC", "Rock Piano", "BX3 Rock 2", "SteelGtrPro DNC", "Dist. Gtr 1 DNC"],
        "drum_mode": "rock_8", "kicks": [0, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (6, B3, 2), (8, D4, 2), (10, D5, 4), (14, B7, 2)],
        "acc1_steps": [(0, POWER8, 4, 86), (6, FOURTHS, 2, 82), (8, POWER5, 4, 84), (12, POWER8, 4, 86)],
        "hook": [(0, R8, 3), (3, B3, 1), (4, D3, 4), (8, D5, 4), (12, B7, 2), (14, R8, 2)],
        "cadence": "rock_bVII_IV", "fill_type": "rock_tom",
    },
    # Status Quo ("Whatever You Want" / "Rockin' All Over the World"): Relentless Boogie-Rock Shuffle!
    "rock_boogie": {
        "meter": "4/4", "tempo": 134, "swing": 0.28, "swing8": True,
        "tracks": ["Rock Kit 2 Amb", "Standard PercKit", "Picked E. Bass 2", "Crunch Gtr DNC", "Honky-Tonk", "Stereo Dist.Gtr", "BX3 Rock 1", "Harmonica 1 DN1"],
        "drum_mode": "pop_8", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_mode": "boogie_8",
        "acc1_steps": [(0, POWER5, 2, 86), (2, D6, 2, 80), (4, POWER5, 2, 86), (6, D6, 2, 80), (8, POWER5, 2, 86), (10, D6, 2, 80), (12, POWER5, 2, 86), (14, D6, 2, 80)],
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 4), (16, B7, 2), (18, D6, 2), (20, D5, 4)],
        "cadence": "blues_V_IV", "fill_type": "rock_tom",
    },
    "rock_shuffle": {
        "meter": "4/4", "tempo": 124, "swing": 0.30, "swing8": True,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "JB Finger BsDN1", "Crunch Gtr DNC", "BX3 Rock 3", "Rock Piano", "Tight Brass 1", "Dist. Gtr 1 DNC"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, D3, 2), (6, D4, 2), (8, D5, 2), (10, D6, 2), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "boogie_comp",
        "hook": [(0, FOURTHS, 2), (2, POWER5, 4), (8, FOURTHS, 2), (10, POWER8, 4)],
        "fill_type": "rock_tom",
    },

    # =========================================================================
    # 6. COUNTRY (24 Styles)
    # =========================================================================
    "acoustic_country": {
        "meter": "4/4", "tempo": 118, "swing": 0.08,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "RealFolk Gtr DNC", "Banjo", "Pedal Steel", "Fiddle", "Mandolin DNC"],
        "drum_mode": "country_train", "bass_mode": "country_2beat",
        "acc1_mode": "pop_strum", "acc2_mode": "banjo_roll", "acc3_mode": "mandolin_chop",
        "hook": [(0, D5, 2), (2, D6, 2), (4, R8, 4), (16, U3, 2), (18, U9, 2), (20, R8, 4)],
        "cadence": "country_IV_V",
    },
    "country_rock": {
        "meter": "4/4", "tempo": 124, "swing": 0.04,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "SteelGtrPro DNC", "Single Coil Pro", "Honky-Tonk", "Pedal Steel", "Crunch Gtr DNC"],
        "drum_mode": "rock_8", "kicks": [0, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (4, D3, 2), (6, D4, 2), (8, D5, 4), (12, D6, 2), (14, D5, 2)],
        "acc1_mode": "pop_strum",
        "hook": [(0, THIRDS, 2), (2, HIGH_STAB, 2), (4, THIRDS, 4), (16, D5, 2), (18, D6, 2), (20, R8, 4)],
        "cadence": "country_IV_V",
    },
    # Lay Down Sally (Eric Clapton Country-Blues Shuffle Groove!)
    "sally_groove": {
        "meter": "4/4", "tempo": 117, "swing": 0.22,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Bass", "Single Coil Pro", "SteelGtrPro DNC", "Wurly Logic", "Pedal Steel", "Single Coil"],
        "drum_mode": "pop_16", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (4, L5, 3), (8, R, 3), (12, L6, 2), (14, B7, 2)],
        "acc1_mode": "funk_chuck", "acc2_mode": "pop_strum",
        "hook": [(0, R, 2), (2, B3, 1), (3, D3, 3), (8, D5, 2), (10, D6, 2), (12, R8, 4)],
        "cadence": "blues_V_IV",
    },
    "easy_country": {
        "meter": "4/4", "tempo": 106, "swing": 0.10,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "ClassicSteel DNC", "Classic Piano", "Pedal Steel", "Harmonica 1 DN1", "RealFolk GtrST 2"],
        "drum_mode": "pop_8", "snare_note": 40, "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat", "acc1_mode": "pop_strum",
        "hook": [(4, THIRDS, 4), (12, HIGH_STAB, 4), (20, THIRDS, 6)],
        "cadence": "country_IV_V",
    },
    "country_blues": {
        "meter": "4/4", "tempo": 114, "swing": 0.26, "swing8": True,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Finger Bass DN1", "Single Coil Pro", "Honky-Tonk", "BX3 Jazz", "Harmonica 1 DN1", "Banjo"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_mode": "boogie_8", "acc1_mode": "boogie_comp",
        "hook": [(0, B3, 1), (1, D3, 3), (4, D5, 2), (6, D6, 2), (8, B7, 4), (12, R8, 4)],
        "cadence": "blues_V_IV",
    },
    # Patsy Cline ("Crazy") / Chris Stapleton ("Tennessee Whiskey") 6/8 Country Ballad!
    "6_8_country_bld": {
        "meter": "6/8", "tempo": 68, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Classic Piano", "Pedal Steel", "SteelGtrPro DNC", "Warm Strings", "Single Coil"],
        "drum_mode": "ballad_6_8", "kicks": [0, 10],
        "bass_pat": [(0, R, 6), (6, D5, 4), (10, D6, 2)],
        "acc1_steps": [(0, CLOSE, 2, 74), (2, CLOSE, 2, 70), (4, CLOSE, 2, 70), (6, HIGH_STAB, 2, 76), (8, CLOSE, 2, 70), (10, CLOSE, 2, 70)],
        "acc2_seq": [(0, THIRDS, 6), (6, THIRDS, 6)],
        "hook": [(0, R, 2), (2, D2, 2), (4, D3, 2), (6, D5, 6), (14, D6, 2), (16, D5, 2), (18, D3, 6)],
        "cadence": "country_IV_V",
    },
    "country_fox": {
        "meter": "4/4", "tempo": 128, "swing": 0.24, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "SteelGtrPro DNC", "Saloon Piano", "Fiddle", "Pedal Steel", "Single Coil"],
        "drum_mode": "jazz_brush", "bass_mode": "country_2beat", "acc1_mode": "oom_pah_off",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U6, 4), (8, U5, 4), (16, U3, 4), (20, R8, 4)],
        "cadence": "country_IV_V",
    },
    # Chet Atkins / Merle Travis Alternating-Thumb Fingerpicking!
    "finger_picking": {
        "meter": "4/4", "tempo": 116, "swing": 0.12,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "RealFolk Gtr DNC", "Clean Jazz 1", "Pedal Steel", "Harmonica 2 DN1", "ClassicSteel DNC"],
        "drum_mode": "pop_8", "snare_note": 37, "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat", "acc1_mode": "travis_pick",
        "acc2_seq": [(0, R, 2), (3, U3, 2), (6, D5, 2), (8, L5, 2), (11, R8, 2), (14, D3, 2)],
        "hook": [(2, U5, 2), (6, U3, 2), (10, U9, 2), (14, R8, 2), (18, U3, 2), (22, D5, 4)],
        "cadence": "country_IV_V",
    },
    "slow_country": {
        "meter": "4/4", "tempo": 80, "swing": 0.08,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "SteelGtrPro DNC", "Pedal Steel", "Concert Grand", "Real Strings 1", "Fiddle"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat", "acc1_mode": "pop_strum", "acc4_mode": "thirds_swell",
        "hook": [(0, THIRDS, 6), (8, HIGH_STAB, 6), (18, U3, 4), (22, R8, 6)],
        "cadence": "country_IV_V",
    },
    # Eagles ("Take It Easy" / "Peaceful Easy Feeling") West Coast Country-Rock!
    "west_coast": {
        "meter": "4/4", "tempo": 134, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Finger Bass DN1", "Strum 12Str. DNC", "Banjo", "Single Coil Pro", "BX3 Jazz", "Pedal Steel"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (6, D3, 2), (8, D5, 4), (14, D6, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "banjo_roll",
        "hook": [(0, U3, 3), (3, U5, 3), (6, U6, 2), (8, U5, 8)],
        "cadence": "country_IV_V",
    },
    # Shania Twain / Luke Bryan Modern Radio Country Hit
    "country_hit": {
        "meter": "4/4", "tempo": 120, "swing": 0.04,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "SteelGtrPro DNC", "Crunch Gtr DNC", "Banjo", "Fiddle", "Pedal Steel"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "bass_mode": "root_8", "acc1_mode": "pop_strum", "acc2_mode": "banjo_roll",
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 4), (16, U6, 2), (18, U5, 2), (20, U3, 4)],
        "cadence": "country_IV_V",
    },
    "country_strum": {
        "meter": "4/4", "tempo": 116, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "RealFolk Gtr DNC", "Strum 12Str. DNC", "Classic Piano", "Harmonica 1 DN1", "Mandolin DNC"],
        "drum_mode": "pop_8", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat",
        "acc1_steps": [(0, R, 2, 82), (2, STRUM_DN, 2, 76), (4, CHUCK, 1, 74), (6, STRUM_UP, 2, 74), (8, L5, 2, 80), (10, STRUM_DN, 2, 76), (12, CHUCK, 1, 74), (14, STRUM_UP, 2, 74)],
        "hook": [(0, U5, 4), (6, U3, 2), (8, R8, 6)],
        "cadence": "country_IV_V",
    },
    # Johnny Cash ("Folsom Prison" / "Ring of Fire") Brisk Train-Beat Country QuickStep!
    "country_quikstep": {
        "meter": "4/4", "tempo": 152, "swing": 0.14,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "ClassicSteel DNC", "Single Coil Pro", "Dual Trumpets", "Saloon Piano", "Fiddle"],
        "drum_mode": "country_train", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat", "acc1_mode": "oom_pah_off",
        "hook": [(0, D5, 2), (2, D6, 2), (4, R8, 6), (12, R8, 2), (14, D6, 2), (16, D5, 6)],
        "cadence": "country_IV_V",
    },
    # True 3/4 Country Waltz ("Tennessee Waltz" / Anne Murray "Could I Have This Dance")
    "3_4_country": {
        "meter": "3/4", "tempo": 104, "swing": 0.08,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "RealFolk Gtr DNC", "Pedal Steel", "Classic Piano", "Fiddle", "Harmonica 1 DN1"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 6), (8, L5, 4)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": STRUM_DN,
        "acc2_seq": [(4, THIRDS, 4), (8, THIRDS, 4)],
        "hook": [(0, D5, 4), (4, D6, 2), (6, R8, 2), (8, U3, 4), (12, U5, 8), (20, U3, 4)],
        "cadence": "country_IV_V",
    },
    "modern_country": {
        "meter": "4/4", "tempo": 112, "swing": 0.0,
        "tracks": ["Rock Kit 2 Amb", "Standard PercKit", "JB Finger BsDN1", "SteelGtrPro DNC", "Crunch Gtr DNC", "Pop Grand", "Banjo", "Pedal Steel"],
        "drum_mode": "pop_8", "kicks": [0, 7, 10], "snares": [4, 12],
        "bass_mode": "pop_sync", "acc1_mode": "pop_strum", "acc2_mode": "banjo_roll",
        "hook": [(0, U3, 3), (3, R8, 3), (6, D5, 2), (8, D6, 4)],
        "cadence": "country_IV_V",
    },
    # Taylor Swift ("Love Story" / early Nashville Country-Pop)
    "country_pop": {
        "meter": "4/4", "tempo": 119, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Standard PercKit", "JB Pick Bs DN1", "RealFolk Gtr DNC", "Banjo", "Real Strings 1", "Mandolin DNC", "Fiddle"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 12], "snares": [4, 12],
        "bass_mode": "root_8", "acc1_mode": "travis_pick", "acc2_mode": "banjo_roll",
        "hook": [(0, U3, 2), (2, U3, 2), (4, U9, 2), (6, R8, 4), (16, U5, 2), (18, U3, 2), (20, R8, 4)],
        "cadence": "country_IV_V",
    },
    "country_beat_1": {
        "meter": "4/4", "tempo": 122, "swing": 0.06,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "SteelGtrPro DNC", "Single Coil", "Saloon Piano", "Pedal Steel", "Fiddle"],
        "drum_mode": "pop_8", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat", "acc1_mode": "pop_strum",
        "hook": [(2, R8, 2), (4, U3, 2), (6, U5, 2), (8, U3, 4)],
        "cadence": "country_IV_V",
    },
    "country_beat_2": {
        "meter": "4/4", "tempo": 128, "swing": 0.22, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Acous. Bass Pro1", "ClassicSteel DNC", "Honky-Tonk", "Fiddle", "Banjo", "Single Coil Pro"],
        "drum_mode": "country_train", "bass_mode": "country_2beat", "acc1_mode": "oom_pah_off",
        "hook": [(0, D5, 2), (2, R8, 2), (4, U9, 2), (6, U3, 2), (8, U5, 4)],
        "cadence": "country_IV_V",
    },
    "country_ballad_1": {
        "meter": "4/4", "tempo": 78, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Finger Bass DN1", "Concert Grand", "RealFolk Gtr DNC", "Pedal Steel", "Warm Strings", "Fiddle"],
        "drum_mode": "ballad_4_4", "kicks": [0, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 7), (8, D5, 7)],
        "acc1_mode": "piano_arp", "acc2_mode": "travis_pick",
        "hook": [(4, THIRDS, 4), (8, U3, 6), (20, THIRDS, 4), (24, R8, 6)],
        "cadence": "country_IV_V",
    },
    "country_ballad_2": {
        "meter": "4/4", "tempo": 74, "swing": 0.06,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "ClassicSteel DNC", "Wurly Clean", "Pedal Steel", "Harmonica 1 DN1", "Mandolin DNC"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, L5, 8)],
        "acc1_mode": "travis_pick",
        "hook": [(0, D5, 4), (4, R8, 4), (8, U9, 2), (10, R8, 6)],
        "cadence": "country_IV_V",
    },
    "country_8_beat": {
        "meter": "4/4", "tempo": 118, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Finger E.Bass 1", "RealFolk Gtr DNC", "Classic Piano", "Pedal Steel", "Single Coil", "Harmonica 2 DN1"],
        "drum_mode": "pop_8", "kicks": [0, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (4, R, 2), (6, D3, 2), (8, D5, 4), (12, D5, 4)],
        "acc1_mode": "pop_strum",
        "hook": [(0, U3, 2), (4, D5, 2), (6, D6, 2), (8, R8, 4)],
        "cadence": "country_IV_V",
    },
    "country_16_beat": {
        "meter": "4/4", "tempo": 100, "swing": 0.10,
        "tracks": ["Studio Kit", "Standard PercKit", "JB Finger BsDN1", "SteelGtrPro DNC", "Tine EP Dyno", "Pedal Steel", "Mandolin DNC", "Single Coil Pro"],
        "drum_mode": "pop_16", "kicks": [0, 6, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, D3, 1), (6, D5, 2), (8, R, 4), (14, L5, 2)],
        "acc1_mode": "travis_pick", "acc2_mode": "banjo_roll",
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 4), (18, D6, 2), (20, D5, 4)],
        "cadence": "country_IV_V",
    },
    # Earl Scruggs / Bill Monroe ("Foggy Mountain Breakdown"): Blazing 5-String Banjo Roll, Mandolin 2&4 Chop, Upright Bass, Fiddle!
    "bluegrass": {
        "meter": "4/4", "tempo": 146, "swing": 0.08,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Real Ac. Bass 1", "RealFolk Gtr DNC", "Banjo", "Mandolin DNC", "Fiddle", "Harmonica 1 DN1"],
        "drum_mode": "country_train", "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "country_2beat",
        "acc1_steps": [(0, R, 3, 82), (4, STRUM_DN, 2, 78), (8, L5, 3, 80), (12, STRUM_DN, 2, 78)],
        "acc2_mode": "banjo_roll", "acc3_mode": "mandolin_chop",
        "hook": [(0, B3, 1), (1, D3, 2), (3, D5, 1), (4, R8, 2), (6, D6, 2), (8, D5, 2), (10, D3, 2), (12, R, 4)],
        "cadence": "country_IV_V",
    },
    # Honky-Tonk Dive Bar Country ("Friends in Low Places" / Garth Brooks): Saloon Piano + Chicken-Pickin' Tele + Pedal Steel!
    "bar_country": {
        "meter": "4/4", "tempo": 116, "swing": 0.24, "swing8": True,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Bass", "Honky-Tonk", "Single Coil Pro", "Pedal Steel", "Fiddle", "Saloon Piano"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, D6, 2), (14, B7, 2)],
        "acc1_mode": "boogie_comp", "acc2_mode": "oom_pah_off",
        "hook": [(0, THIRDS, 2), (2, HIGH_STAB, 2), (4, THIRDS, 4), (12, B3, 1), (13, D3, 3)],
        "cadence": "country_IV_V",
    },
}
