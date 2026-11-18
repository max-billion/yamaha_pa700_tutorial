#!/usr/bin/env python3
"""
Individually Curated Musical Blueprints for Korg Pa700 Styles — Part B (196 Styles):
  7. Latin (36)
  8. Latin Dance (32)
  9. Jazz (36)
  10. Movie & Show (24)
  11. Funk & Blues (32)
  12. World (36)

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

BLUEPRINTS_B = {
    # =========================================================================
    # 7. LATIN (36 Styles)
    # =========================================================================
    # Rio Carnival Samba Enredo: Surdo batucada, tamborim, agogo, cavaquinho, samba whistle!
    "samba_enredo": {
        "meter": "4/4", "tempo": 134, "swing": 0.08,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "JB Finger BsDN1", "Real Cavaquinho", "Nylon GuitarDNC", "Tight Brass 1", "Dual Trumpets", "Whistle DN1"],
        "drum_mode": "samba",
        "perc_steps": [(0, 71, 78, V_4), (2, 71, 72, V_4), (4, 72, 82, V_4), (3, 67, 74), (6, 68, 72), (10, 67, 74), (14, 68, 72)],
        "bass_mode": "samba_surdo",
        "acc1_steps": [(0, CHUCK, 1, 82), (2, STRUM_UP, 1, 78), (3, STRUM_DN, 2, 84), (6, CHUCK, 1, 80), (8, STRUM_DN, 2, 82), (11, STRUM_UP, 2, 80), (14, STRUM_DN, 2, 82)],
        "acc2_mode": "bossa_violao",
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 2), (8, D6, 2), (11, D5, 3), (14, R8, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    "samba_brazil": {
        "meter": "4/4", "tempo": 110, "swing": 0.10,
        "tracks": ["Studio Kit", "Latin Perc.Kit 2", "Finger Bass DN1", "Nylon GuitarDNC", "Real Cavaquinho", "Bright Piano", "Jazz Flute Expr.", "Jazz Trumpet DN1"],
        "drum_mode": "samba", "bass_mode": "samba_surdo",
        "acc1_mode": "bossa_violao", "acc2_mode": "offbeat_chop",
        "hook": [(0, U3, 3), (3, U5, 2), (6, U6, 3), (10, U5, 2), (12, U3, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Jobim / Gilberto ("Girl from Ipanema"): Classic Bossa Nova with Violão, Acoustic Bass, Jazz Piano & Tenor Sax!
    "bossa_nova": {
        "meter": "4/4", "tempo": 124, "swing": 0.04,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Concert Gtr DNC", "Jazz Piano", "Warm Strings", "Jazz Flute Expr.", "Tenor Sax DN1"],
        "drum_mode": "bossa", "bass_mode": "bossa_root5",
        "acc1_mode": "bossa_violao", "acc2_mode": "rhodes_color",
        "hook": [(0, U9, 3), (3, B7, 3), (6, D6, 2), (10, D5, 4), (16, U9, 3), (19, U3, 3), (22, R8, 6)],
        "cadence": "jazz_ii_V", "fill_type": "latin_timbale",
    },
    # Fania All-Stars / Tito Puente Classic Salsa (2-3 Clave, Anticipated Tumbao Bass on 2-and & 4, Piano Montuno, Trombones!)
    "classic_salsa": {
        "meter": "4/4", "tempo": 106, "swing": 0.0,
        "tracks": ["Standard Kit Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Bright Piano", "Jazz Trb. DN1", "Tight Brass 1", "Dual Trumpets", "Trumpet Overb."],
        "drum_mode": "salsa_clave", "clave_dir": "23",
        "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "acc4_steps": [(0, HIGH_STAB, 2), (6, THIRDS, 3), (14, HIGH_STAB, 2)],
        "hook": [(0, R8, 2), (3, U3, 1), (4, U5, 2), (6, U6, 2), (12, U5, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Perez Prado ("Mambo No. 5 / Qué Rico el Mambo"): Heavy Cowbell, Brass Section Riffs, Sax Answer!
    "classic_mambo": {
        "meter": "4/4", "tempo": 112, "swing": 0.0,
        "tracks": ["Jazz Kit 1 Amb", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Live Piano", "Sax Ensemble", "Big Band Brass 1", "Tight Brass 2", "JazzTrumpet1 DNC"],
        "drum_mode": "mambo", "clave_dir": "32",
        "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "acc4_steps": [(2, HIGH_STAB, 2), (6, HIGH_STAB, 2), (10, THIRDS, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, D5, 1), (2, R8, 1), (3, U3, 2), (6, U5, 2), (10, U3, 2), (12, R8, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Classic Cuban Cha-Cha-Chá (Güiro, Cowbell on all 4, Flute charanga melody, Piano guajeo!)
    "classic_chacha": {
        "meter": "4/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Standard Kit Amb", "Latin Perc.Kit 1", "Acoustic Bass 1", "Bright Piano", "Nylon GuitarDNC", "Strings&Orch.V.", "Tight Brass 1", "Flute"],
        "drum_mode": "chacha",
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, D5, 4), (12, R8, 2), (14, D5, 2)],
        "acc1_steps": [(0, MONTUNO, 2, 78), (4, MONTUNO, 2, 76), (8, MONTUNO, 2, 78), (12, D5, 2, 74), (14, R8, 2, 78)],
        "hook": [(0, U5, 2), (4, U3, 2), (8, U5, 2), (12, R8, 1), (13, U9, 1), (14, U3, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Cuban Guajira ("Guantanamera"): Stately arpeggiated Tres/Guitar + Clave + Bongos + Flute!
    "guajira": {
        "meter": "4/4", "tempo": 108, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "Real Nylon Gtr", "Concert Grand", "Warm Strings", "Jazz Flute Expr.", "Concert Gtr Pro"],
        "drum_mode": "chacha",
        "bass_pat": [(0, R, 5), (6, D4, 2), (8, D5, 5), (14, D4, 2)],
        "acc1_steps": [(0, R, 2, 78), (2, D3, 2, 74), (4, D5, 2, 76), (6, D4, 2, 74), (8, D5, 2, 78), (10, U3, 2, 76), (12, D5, 2, 74), (14, D4, 2, 72)],
        "hook": [(0, U3, 3), (3, U5, 3), (6, U4 if False else D4, 2), (8, D5, 6)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Afro-Cuban Rumba Guaguancó: 3-2 Rumba Clave (last note shifted to step 7/15!), Tumbadoras conversation!
    "guaguanc": {
        "meter": "4/4", "tempo": 114, "swing": 0.04,
        "tracks": ["Real Kit 2 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Bright Piano", "Nylon GuitarDNC", "Tight Brass 1", "Jazz Trb. DN1", "Trumpet Expr.1"],
        "drum_mode": "salsa_clave", "clave_dir": "32",
        "perc_steps": [(0, 75, 80), (3, 75, 78), (7, 75, 80), (10, 63, 76), (12, 64, 82), (14, 62, 74)],
        "bass_pat": [(6, D5, 3), (11, D3, 2), (14, R, 3)],
        "acc1_mode": "salsa_montuno",
        "hook": [(0, R8, 2), (3, U3, 2), (7, U5, 3), (12, U3, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Modern Havana Timba (Los Van Van / Irakere): Funk-infused Cuban slap/finger bass + complex montuno + fiery horns!
    "timba": {
        "meter": "4/4", "tempo": 108, "swing": 0.04,
        "tracks": ["Funk Kit 1 Amb", "Latin Perc.Kit 1", "JB Fing.Slap Bs", "Live Piano", "Tight Brass 2", "Sax Ensemble", "Dual Trumpets", "TrumpetShake Y+"],
        "drum_mode": "salsa_clave", "kicks": [0, 3, 6, 11, 14],
        "bass_pat": [(0, R, 2), (3, R8, 1), (6, D5, 2), (9, B7, 1), (11, R, 3), (14, L5, 2)],
        "acc1_mode": "salsa_montuno",
        "acc4_steps": [(0, HIGH_STAB, 1), (3, HIGH_STAB, 2), (9, THIRDS, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, R8, 1), (2, B7, 1), (3, U3, 2), (6, U5, 2), (11, R8, 3)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Afro-Cuban 6/8 Bembe ("x . x . x x . x . x . x" cowbell/agogo polyrhythm)!
    "6_8_afro": {
        "meter": "6/8", "tempo": 116, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "Acoustic Bass 1", "Bright Piano", "Nylon GuitarDNC", "Sax Ensemble", "Tight Brass 1", "Jazz Flute Expr."],
        "drum_mode": "ballad_6_8", "kicks": [0, 6, 10],
        "perc_steps": [(0, 56, 80), (2, 56, 72), (4, 56, 78), (5, 56, 74), (7, 56, 76), (9, 56, 74), (11, 56, 72), (3, 63, 76), (8, 64, 80)],
        "bass_pat": [(0, R, 4), (4, D5, 2), (6, R, 3), (9, B7, 3)],
        "acc1_steps": [(0, MONTUNO, 2, 80), (3, MONTUNO, 2, 76), (6, MONTUNO, 2, 80), (9, MONTUNO, 2, 76)],
        "hook": [(0, R8, 2), (3, U3, 3), (6, U5, 3), (9, U3, 3)],
        "fill_type": "latin_timbale",
    },
    # Puerto Rican Bomba Sicá ("1 . . a 2-and . 3 . 4 ."): Barrel drums + maraca + cuatro/piano!
    "bomba": {
        "meter": "4/4", "tempo": 114, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Latin Perc.Kit 2", "Finger Bass DN1", "Live Piano", "Real Cavaquinho", "Tight Brass 1", "Jazz Trb. DN1", "Concert Trumpet"],
        "drum_mode": "cumbia", "kicks": [0, 3, 6, 12],
        "perc_steps": [(0, 64, 84), (3, 63, 78), (6, 62, 80), (8, 75, 70), (12, 64, 84), (14, 63, 76)],
        "bass_pat": [(0, R, 3), (3, D5, 3), (6, R, 4), (12, L5, 4)],
        "acc1_mode": "salsa_montuno",
        "hook": [(0, U3, 3), (3, U5, 3), (6, R8, 4), (12, D5, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Juan Luis Guerra / Aventura Classic Dominican Bachata: Requinto bright chorus/nylon arpeggio + Bongos + Güira!
    "classic_bachata": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 2", "JB Finger BsDN1", "Chorus Gtr Pro", "Real Nylon Gtr", "Warm Strings", "SoftAltoSax DN1", "Single Coil Pro"],
        "drum_mode": "bachata", "bass_mode": "bachata_sync",
        "acc1_steps": [(0, R8, 2, 78), (2, U3, 2, 74), (4, U5, 2, 78), (6, U3, 2, 76), (8, R8, 2, 78), (10, D5, 2, 74), (12, U3, 2, 80), (14, U5, 2, 76)],
        "acc2_mode": "offbeat_chop",
        "hook": [(0, U5, 2), (2, U6, 2), (4, U5, 2), (6, U3, 2), (8, R8, 4), (12, U3, 2), (14, U5, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Dominican Classic Merengue (2-beat fast Tambora + 16th Güira + Sax/Trumpet Jaleo + Accordion!):
    "classic_merengue": {
        "meter": "4/4", "tempo": 138, "swing": 0.0,
        "tracks": ["Pop Std. Kit 1", "Latin Perc.Kit 1", "Finger E.Bass 1", "Bright Piano", "Accordion", "Tight Brass 1", "Sax Ensemble", "Trumpet Expr.1"],
        "drum_mode": "merengue",
        "bass_pat": [(0, R, 3), (4, D5, 3), (8, R, 3), (12, D5, 3)],
        "acc1_steps": [(0, MONTUNO, 2, 80), (2, MONTUNO, 2, 78), (6, MONTUNO, 2, 82), (10, MONTUNO, 2, 78), (14, MONTUNO, 2, 82)],
        "hook": [(0, R8, 1), (2, U3, 1), (4, U5, 2), (6, U3, 2), (8, R8, 1), (10, U3, 1), (12, U5, 2), (14, R8, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Classic Colombian Cumbia: Offbeat Guacharaca, Conga, Accordion Melody, Triad Bass!
    "cumbia": {
        "meter": "4/4", "tempo": 102, "swing": 0.04,
        "tracks": ["Standard Kit 1", "Latin Perc.Kit 2", "Finger Bass DN1", "Accordion", "Nylon GuitarDNC", "Bright Piano", "Dual Trumpets", "RealClarinet DN1"],
        "drum_mode": "cumbia", "bass_mode": "cumbia_triad",
        "acc1_steps": [(2, THIRDS, 2, 78), (6, THIRDS, 2, 80), (10, THIRDS, 2, 78), (14, THIRDS, 2, 80)],
        "acc2_mode": "oom_pah_off",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U3, 2), (6, R8, 2), (8, D5, 4), (16, U5, 2), (18, U6, 2), (20, U5, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Venezuelan / Colombian Llanero Joropo ("Alma Llanera"): True 3/4-6/8 Folk Harp, Cuatro & Maracas!
    "joropo": {
        "meter": "3/4", "tempo": 156, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "Acoustic Bass 1", "Classic Harp", "Real Cavaquinho", "Real Nylon Gtr", "Marimba", "Flute"],
        "drum_mode": "waltz_3_4", "kicks": [0, 6], "snares": [4, 10],
        "perc_steps": [(0, 70, 72), (2, 70, 56), (4, 70, 76), (6, 70, 64), (8, 70, 72), (10, 70, 62)],
        "bass_pat": [(4, D3, 4), (8, D5, 4), (16, R, 4), (20, L5, 4)],
        "acc1_steps": [(0, R, 2, 80), (2, D5, 2, 74), (4, R8, 2, 78), (6, U3, 2, 80), (8, U5, 2, 78), (10, U3, 2, 74)],
        "acc2_seq": [(0, STRUM_DN, 2), (4, CHUCK, 2), (6, STRUM_UP, 2), (10, CHUCK, 2)],
        "hook": [(0, U5, 2), (2, U6, 2), (4, U5, 2), (6, U3, 2), (8, R8, 4)],
        "cadence": "latin_IV_V",
    },
    # Cuban / Bizet ("Carmen") Habanera: Iconic `dotted-8th + 16th + 8th + 8th` (steps 0, 3, 4, 6) rhythm!
    "habanera": {
        "meter": "4/4", "tempo": 106, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 1", "Class.Contrabs", "Concert Grand", "Concert Gtr DNC", "Chamber Strings", "Cello", "Real Violin DNC"],
        "drum_mode": "tango", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, D5, 1), (4, D5, 2), (6, R, 2), (8, R, 3), (11, L5, 1), (12, L5, 2), (14, R, 2)],
        "acc1_steps": [(0, CLOSE, 3, 76), (3, CLOSE, 1, 68), (4, HIGH_STAB, 2, 78), (6, CLOSE, 2, 72), (8, CLOSE, 3, 76), (12, HIGH_STAB, 2, 78)],
        "hook": [(0, R8, 3), (3, LT, 1), (4, B2, 2), (6, R8, 2), (8, D5, 6)],
        "cadence": "flamenco_bVI_V",
    },
    "guitar_bossa": {
        "meter": "4/4", "tempo": 126, "swing": 0.04,
        "tracks": ["Brush Kit 2 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Real Nylon Gtr", "Concert Gtr Pro", "Suit Case88 EP1", "Warm Pad", "Soft Jazz Guitar"],
        "drum_mode": "bossa", "bass_mode": "bossa_root5", "acc1_mode": "bossa_violao", "acc2_mode": "travis_pick",
        "hook": [(2, U3, 2), (4, U5, 3), (7, U9, 1), (8, R8, 4), (18, D6, 2), (20, D5, 4)],
        "cadence": "jazz_ii_V",
    },
    # Jobim ("Meditation" / "Corcovado"): Slow dreamy Bossa with lush Claus Ogerman strings & Alto Flute
    "meditation_bossa": {
        "meter": "4/4", "tempo": 108, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 2", "Ac. Jazz Bass", "Concert Gtr DNC", "Tine EP Phaser", "ConcertStrings 1", "Jazz Flute Expr.", "Sweet FlugelHorn"],
        "drum_mode": "bossa", "kicks": [0, 8],
        "bass_pat": [(0, R, 6), (6, D5, 2), (8, D5, 6), (14, R, 2)],
        "acc1_mode": "bossa_violao",
        "hook": [(0, D5, 6), (6, D6, 2), (8, D5, 6), (16, U3, 6), (22, U9, 2), (24, R8, 8)],
        "cadence": "jazz_ii_V",
    },
    # Walter Wanderley ("Summer Samba"): Breezy Hammond B3 Organ Bossa!
    "organ_bossa": {
        "meter": "4/4", "tempo": 128, "swing": 0.06,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "BX3 Jazz", "Nylon GuitarDNC", "Jazz Piano", "Vibraphone 1", "Jazz Organ"],
        "drum_mode": "bossa", "bass_mode": "bossa_root5",
        "acc1_steps": [(0, JAZZ_SHELL, 2, 76), (3, JAZZ_SHELL, 2, 74), (6, HIGH_STAB, 3, 78), (10, JAZZ_SHELL, 2, 74), (14, JAZZ_SHELL, 2, 72)],
        "acc2_mode": "bossa_violao",
        "hook": [(0, U5, 2), (3, U3, 3), (6, U9, 2), (8, R8, 4), (16, D6, 2), (19, D5, 5)],
        "cadence": "jazz_ii_V",
    },
    # Sergio Mendes & Brasil '66 ("Mas Que Nada" / "The Look of Love") Pop Bossa!
    "pop_bossa": {
        "meter": "4/4", "tempo": 120, "swing": 0.06,
        "tracks": ["Studio Kit", "Latin Perc.Kit 1", "Finger Bass DN1", "Pop Grand", "Nylon GuitarDNC", "Scat Voices DNC", "Jazz Flute Expr.", "Vibraphone 1"],
        "drum_mode": "bossa", "bass_mode": "bossa_root5", "acc1_mode": "bossa_violao",
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 4), (18, U3, 2), (20, R8, 4)],
    },
    "cool_bossa": {
        "meter": "4/4", "tempo": 122, "swing": 0.08,
        "tracks": ["Cool Kit Amb", "Latin Perc.Kit 2", "Fretless Bass 2", "Suit Case88 EP1", "Real Nylon Gtr", "Warm Pad", "Mute Trumpet", "Soprano Sax DN1"],
        "drum_mode": "bossa", "bass_mode": "bossa_root5", "acc1_mode": "jazz_comp", "acc2_mode": "bossa_violao",
        "hook": [(4, U5, 3), (8, U3, 3), (12, U9, 4), (20, R8, 6)],
        "cadence": "jazz_ii_V",
    },
    # Fast Jazz-Samba / Up-Tempo Bossa ("Samba de Uma Nota Só" / "Wave" double-time)
    "fast_bossa": {
        "meter": "4/4", "tempo": 148, "swing": 0.06,
        "tracks": ["Jazz Kit 2 Amb", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Jazz Piano", "Concert Gtr DNC", "Vibraphone 1", "Jazz Sax DN1", "Flute"],
        "drum_mode": "bossa",
        "bass_pat": [(0, R, 3), (3, L5, 1), (4, L5, 3), (8, R, 3), (11, D5, 1), (12, D5, 3)],
        "acc1_mode": "bossa_violao",
        "hook": [(0, D5, 2), (3, D5, 2), (6, D5, 2), (10, D5, 2), (12, B5, 2), (14, D5, 2)],
        "cadence": "jazz_ii_V",
    },
    "orch_bossa_1": {
        "meter": "4/4", "tempo": 118, "swing": 0.04,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Nylon GuitarDNC", "Concert Grand", "Full Strings", "French Section", "Flute"],
        "drum_mode": "bossa", "bass_mode": "bossa_root5", "acc1_mode": "bossa_violao", "acc4_mode": "thirds_swell",
        "hook": [(0, U5, 6), (6, U3, 2), (8, U9, 8), (16, R8, 8)],
        "cadence": "jazz_ii_V",
    },
    "orch_bossa_2": {
        "meter": "4/4", "tempo": 125, "swing": 0.04,
        "tracks": ["Brush Kit 2 Amb", "Latin Perc.Kit 2", "Ac. Jazz Bass", "Jazz Piano", "Real Nylon Gtr", "ConcertStrings 1", "Soft Trb. DN1", "Oboe 1"],
        "drum_mode": "bossa", "bass_mode": "bossa_root5", "acc1_mode": "jazz_comp", "acc2_mode": "bossa_violao",
        "hook": [(2, R8, 3), (6, U3, 3), (10, U5, 6), (18, U6, 3), (22, U5, 5)],
        "cadence": "jazz_ii_V",
    },
    # Ary Barroso ("Aquarela do Brasil"): Joyful Brazilian Ballroom/Show Samba!
    "brazilian_samba": {
        "meter": "4/4", "tempo": 112, "swing": 0.08,
        "tracks": ["Standard Kit 2", "Latin Perc.Kit 1", "JB Finger BsDN1", "Nylon GuitarDNC", "Live Piano", "Big Band Brass 1", "Sax Ensemble", "Jazz Flute Expr."],
        "drum_mode": "samba", "bass_mode": "samba_surdo", "acc1_mode": "bossa_violao",
        "acc4_steps": [(0, THIRDS, 2), (3, HIGH_STAB, 3), (10, THIRDS, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, D5, 2), (2, R8, 2), (4, U9, 2), (6, U3, 4), (12, U5, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    "salsa_1": {
        "meter": "4/4", "tempo": 104, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Bright Piano", "Jazz Trb. DN1", "Dual Trumpets", "Baritone Sax DN1", "Trumpet Expr.1"],
        "drum_mode": "salsa_clave", "clave_dir": "23", "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "hook": [(2, R8, 2), (6, U3, 2), (10, U5, 2), (14, R8, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    "salsa_2": {
        "meter": "4/4", "tempo": 110, "swing": 0.0,
        "tracks": ["Studio Kit", "Latin Perc.Kit 2", "Finger Bass DN1", "Live Piano", "Tight Brass 1", "Sax Ensemble", "HardTrombone DN1", "Trumpet Overb."],
        "drum_mode": "salsa_clave", "clave_dir": "32", "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 2), (12, D5, 2), (14, R8, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    "mambo": {
        "meter": "4/4", "tempo": 116, "swing": 0.0,
        "tracks": ["Jazz Kit 2 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Bright Piano", "Big Band Brass 2", "Real Sax Ens.", "Vibraphone 1", "TrumpetShake Y+"],
        "drum_mode": "mambo", "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "hook": [(0, R8, 1), (2, R8, 1), (4, U3, 2), (6, U5, 2), (14, U6, 2), (16, U5, 4)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Jennifer Lopez / Marc Anthony / Camila ("Sway" / "Havana") Pop ChaCha!
    "pop_chacha": {
        "meter": "4/4", "tempo": 115, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 1", "JB Finger BsDN1", "Pop Grand", "Nylon GuitarDNC", "Tight Brass 2", "Real Strings 1", "Jazz Trumpet DN1"],
        "drum_mode": "chacha",
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, R, 4), (12, B7, 2), (14, D5, 2)],
        "acc1_steps": [(0, MONTUNO, 3, 80), (6, MONTUNO, 2, 78), (8, CLOSE, 3, 76), (12, CLOSE, 2, 76), (14, HIGH_STAB, 2, 80)],
        "hook": [(0, R8, 2), (4, U3, 2), (6, U9, 2), (8, R8, 4)],
        "fill_type": "latin_timbale",
    },
    # Ballroom / Bolero-Rhumba 1 ("Bésame Mucho"): Slow romantic Latin Rhumba with maracas, bongos, requinto nylon!
    "rhumba_1": {
        "meter": "4/4", "tempo": 102, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "Concert Gtr DNC", "Classic Piano", "Real Strings 1", "Sweet FlugelHorn", "Real Nylon Gtr"],
        "drum_mode": "bossa", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D5, 2), (8, D5, 6), (14, R, 2)],
        "acc1_mode": "travis_pick",
        "hook": [(0, R8, 4), (4, U9, 2), (6, U3, 4), (10, U5, 6), (18, U3, 4), (22, R8, 6)],
    },
    "rhumba_2": {
        "meter": "4/4", "tempo": 108, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Latin Perc.Kit 1", "Fretless Bass 2", "Real Nylon Gtr", "Tine EP Dyno", "ConcertStrings 1", "Alto Sax DN1", "Marimba"],
        "drum_mode": "chacha", "kicks": [0, 10],
        "bass_pat": [(0, R, 5), (6, D3, 2), (8, D5, 6), (14, L5, 2)],
        "acc1_mode": "bossa_violao",
        "hook": [(2, U5, 3), (6, U3, 3), (10, R8, 6), (18, U9, 3), (22, D5, 5)],
    },
    "bachata": {
        "meter": "4/4", "tempo": 118, "swing": 0.0,
        "tracks": ["Studio Kit", "Latin Perc.Kit 2", "Finger Bass DN1", "Chorus Guitar", "Real Nylon Gtr", "Tine EP Phaser", "Warm Pad", "Single Coil"],
        "drum_mode": "bachata", "bass_mode": "bachata_sync",
        "acc1_steps": [(0, R8, 2, 76), (3, U3, 1, 74), (4, U5, 2, 78), (6, U8, 2, 80), (10, U5, 2, 74), (12, U3, 2, 78), (14, R8, 2, 74)],
        "hook": [(0, U3, 2), (3, U5, 3), (6, U6, 2), (8, U5, 4), (12, U3, 2), (14, R8, 2)],
        "fill_type": "latin_timbale",
    },
    # Cal Tjader / Poncho Sanchez Cool Vibraphone Latin Jazz!
    "cool_latin_jazz": {
        "meter": "4/4", "tempo": 118, "swing": 0.04,
        "tracks": ["Cool Kit Amb", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Jazz Piano", "Vibraphone 1", "Nylon GuitarDNC", "Mute Trumpet", "Jazz Flute Expr."],
        "drum_mode": "salsa_clave", "clave_dir": "23",
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, B7, 4), (12, D5, 4)],
        "acc1_mode": "jazz_comp",
        "acc2_seq": [(0, U3, 2), (3, U5, 2), (6, U9, 3), (12, R8, 3)],
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 4), (14, B7, 2), (16, D6, 4)],
        "cadence": "jazz_ii_V", "fill_type": "latin_timbale",
    },
    # Tito Puente / Arturo Sandoval Blazing Latin Big Band!
    "latin_big_band": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Jazz Kit 1 Amb", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Live Piano", "Big Band Brass 1", "Sax Ensemble", "HardTrombone DN1", "Trumpet Overb."],
        "drum_mode": "mambo", "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "acc4_steps": [(0, HIGH_STAB, 2), (3, THIRDS, 2), (6, HIGH_STAB, 2), (12, THIRDS, 3)],
        "hook": [(0, R8, 2), (3, U3, 2), (6, U5, 2), (9, U8, 3), (14, U5, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Ricky Martin / Gloria Estefan ("Conga" / "Livin' la Vida Loca") Upbeat Latin Pop!
    "latin_pop": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 1", "JB Finger BsDN1", "Real Nylon Gtr", "Bright Piano", "Tight Brass 1", "Strat N Cln Mute", "Concert Trumpet"],
        "drum_mode": "salsa_clave", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, D3, 1), (6, D5, 2), (8, R, 3), (12, D5, 2), (14, R8, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "salsa_montuno",
        "hook": [(0, U3, 2), (2, U3, 2), (4, U5, 2), (6, R8, 4), (14, U3, 2), (16, U5, 4)],
        "fill_type": "latin_timbale",
    },
    # Luis Miguel ("Historia de un Amor" / "Sabor a Mí"): Lush Romantic Latin Bolero!
    "latin_bolero": {
        "meter": "4/4", "tempo": 90, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "Concert Gtr DNC", "Concert Grand", "Movie Str.1 DNC", "Sweet FlugelHorn", "Real Nylon Gtr"],
        "drum_mode": "bossa", "kicks": [0, 10], "snares": [4, 12],
        "perc_steps": [(0, 64, 72), (4, 60, 64), (6, 60, 62), (8, 63, 70), (12, 61, 68), (14, 70, 52)],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, D5, 6), (14, L5, 2)],
        "acc1_mode": "travis_pick",
        "hook": [(0, U5, 4), (4, U6, 2), (6, U5, 2), (8, U3, 8), (18, U9, 3), (21, R8, 7)],
        "cadence": "latin_IV_V",
    },

    # =========================================================================
    # 8. LATIN DANCE (32 Styles)
    # =========================================================================
    # Daddy Yankee ("Gasolina") Classic Old-School Reggaeton 1
    "reggaeton_1": {
        "meter": "4/4", "tempo": 95, "swing": 0.04,
        "tracks": ["HipHop Kit 1", "Latin Perc.Kit 1", "Jungle Bass", "Strings&Orch.V.", "Techno Stab DNC", "Real Nylon Gtr", "Tight Brass 1", "Fast Glide Saw"],
        "drum_mode": "reggaeton_dembow", "bass_mode": "reggaeton_sub",
        "acc1_steps": [(0, HIGH_STAB, 1, 84), (3, HIGH_STAB, 1, 80), (6, HIGH_STAB, 1, 84), (8, HIGH_STAB, 1, 80), (11, HIGH_STAB, 1, 80), (14, HIGH_STAB, 1, 82)],
        "hook": [(0, R8, 2), (3, B2, 2), (6, R8, 2), (8, D5, 2), (11, B2, 2), (14, R8, 2)],
        "cadence": "flamenco_bVI_V",
    },
    # Luis Fonsi / J Balvin ("Despacito"): Romantic Nylon Guitar + Melodic Pop Reggaeton 2!
    "reggaeton_2": {
        "meter": "4/4", "tempo": 90, "swing": 0.04,
        "tracks": ["HipHop Kit 2", "Latin Perc.Kit 2", "Synth Bass Warm", "Real Nylon Gtr", "Marimba", "Warm Pad", "Chorus Guitar", "Mandolin DNC"],
        "drum_mode": "reggaeton_dembow", "bass_mode": "reggaeton_sub",
        "acc1_mode": "pop_strum",
        "acc2_seq": [(0, R8, 2), (3, U3, 2), (6, U5, 2), (11, U3, 2), (14, R8, 2)],
        "hook": [(0, U3, 2), (2, U5, 1), (3, U6, 3), (6, U5, 2), (8, U3, 4), (16, U9, 2), (19, R8, 5)],
    },
    # Hybrid Dominican Bachata + Argentine Bandoneon Tango!
    "bachatango": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 2", "JB Finger BsDN1", "Bandoneon DNC", "Chorus Gtr Pro", "Chamber Strings", "Real Violin DNC", "Single Coil Pro"],
        "drum_mode": "bachata", "bass_mode": "tango_332",
        "acc1_mode": "tango_staccato",
        "acc2_seq": [(0, R8, 2), (3, U3, 2), (6, U5, 2), (10, U3, 2), (12, R8, 2), (14, D5, 2)],
        "hook": [(0, U5, 3), (3, S5, 1), (4, U5, 2), (6, U3, 2), (8, R8, 4)],
        "cadence": "tango_V_I", "fill_type": "latin_timbale",
    },
    # Elvis Crespo ("Suavemente"): Blazing Hot Merengue with Sax/Trumpet Jaleos!
    "hot_merengue": {
        "meter": "4/4", "tempo": 142, "swing": 0.0,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Finger Bass DN1", "Live Piano", "Sax Ensemble", "Tight Brass 2", "Accordion", "Dual Trumpets"],
        "drum_mode": "merengue",
        "bass_pat": [(0, R, 2), (3, D5, 1), (4, D5, 3), (8, R, 2), (11, L5, 1), (12, L5, 3)],
        "acc1_mode": "salsa_montuno",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U3, 2), (6, R8, 2), (8, U3, 2), (10, U5, 2), (12, U6, 4)],
        "fill_type": "latin_timbale",
    },
    # Marc Anthony ("Vivir Mi Vida") Modern Pop-Salsa!
    "modern_salsa": {
        "meter": "4/4", "tempo": 106, "swing": 0.0,
        "tracks": ["Studio Kit", "Latin Perc.Kit 1", "JB Finger BsDN1", "Live Piano", "Tight Brass 1", "Real Nylon Gtr", "Dual Trumpets", "Jazz Trb. DN1"],
        "drum_mode": "salsa_clave", "kicks": [0, 4, 8, 12],
        "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "hook": [(0, R8, 3), (3, R8, 3), (6, U3, 2), (8, U5, 4), (12, U3, 4)],
        "fill_type": "latin_timbale",
    },
    # King Africa ("La Bomba") Party Latin-Dance Bomba!
    "bomba_dance": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Finger E.Bass 2", "Bright Piano", "Tight Brass 1", "Accordion", "Sax Ensemble", "TrumpetShake Y+"],
        "drum_mode": "four_floor",
        "perc_steps": [(0, 56, 76), (3, 63, 74), (6, 64, 78), (10, 63, 74), (12, 56, 76), (14, 65, 78)],
        "bass_mode": "cumbia_triad", "acc1_mode": "salsa_montuno",
        "hook": [(0, R8, 2), (2, R8, 2), (4, U3, 2), (6, U5, 4), (12, U3, 2), (14, R8, 2)],
        "fill_type": "latin_timbale",
    },
    # Shakira & Alejandro Sanz ("La Tortura"): Reggaeton-Cumbia-Accordion Dance!
    "tortura_dance": {
        "meter": "4/4", "tempo": 100, "swing": 0.06,
        "tracks": ["HipHop Kit 1", "Latin Perc.Kit 2", "Synth Bass Warm", "Accordion", "Real Nylon Gtr", "Strat N Cln Mute", "Dark Pad", "Tango Accordion"],
        "drum_mode": "reggaeton_dembow", "bass_mode": "reggaeton_sub",
        "acc1_steps": [(0, THIRDS, 2, 80), (3, THIRDS, 2, 78), (6, CLOSE, 2, 80), (11, THIRDS, 2, 78), (14, CLOSE, 2, 76)],
        "acc2_mode": "pop_strum",
        "hook": [(0, R8, 2), (3, B2, 2), (6, D3, 2), (8, D4, 2), (10, D3, 2), (12, B2, 2), (14, R, 2)],
        "cadence": "flamenco_bVI_V",
    },
    # Gipsy Kings ("Bamboleo" / "Volare"): Energetic Rumba-Catalana Ventilador Strumming + Palmas + Dance Beat!
    "gipsy_dance": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 1", "Finger Bass DN1", "Concert Gtr DNC", "Real Nylon Gtr", "Bright Piano", "Accordion", "Concert Gtr Pro"],
        "drum_mode": "flamenco", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(3, 39, 82), (6, 39, 80), (10, 39, 80), (14, 39, 82)],
        "bass_pat": [(0, R, 3), (3, D3, 1), (4, D5, 4), (8, R, 3), (12, D5, 4)],
        "acc1_mode": "pop_strum",
        "hook": [(0, U5, 2), (2, U6, 2), (4, U5, 2), (6, U3, 2), (8, U9, 2), (10, U3, 2), (12, R8, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "flamenco_rasg",
    },
    # Caribbean Limbo Rock ("How Low Can You Go" Steel Drums & Calypso Percussion!)
    "limbo": {
        "meter": "4/4", "tempo": 116, "swing": 0.06,
        "tracks": ["Standard Kit 1", "Latin Perc.Kit 1", "Finger Bass DN1", "Steel Drums GM", "RealFolk Gtr DNC", "Marimba", "Tight Brass 1", "Warm Steel"],
        "drum_mode": "cumbia", "kicks": [0, 6, 8, 14],
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, R, 4), (12, D3, 2), (14, D5, 2)],
        "acc1_steps": [(0, THIRDS, 2, 82), (3, HIGH_STAB, 2, 80), (6, THIRDS, 2, 82), (10, THIRDS, 2, 78), (12, CLOSE, 2, 78)],
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 2), (8, D6, 2), (10, D5, 4)],
    },
    # Ritchie Valens / Los Lobos ("La Bamba"): Classic I-IV-V Son Jarocho Rock'n'Roll!
    "bamba": {
        "meter": "4/4", "tempo": 148, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "JB Pick Bs DN1", "Single Coil Pro", "RealFolk Gtr DNC", "Accordion", "Bright Piano", "Concert Gtr Pro"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 12], "snares": [4, 12],
        "perc_steps": [(0, 56, 72), (4, 56, 68), (8, 56, 72), (12, 56, 68)],
        "bass_pat": [(0, R, 2), (2, D3, 2), (4, D5, 2), (6, D4, 2), (8, D4, 2), (10, D6, 2), (12, D5, 2), (14, B7, 2)],
        "acc1_mode": "pop_strum",
        "hook": [(6, R, 2), (8, D3, 2), (10, D5, 2), (12, R8, 2), (14, U3, 2), (16, U4 if False else D4, 2), (18, U3, 2), (20, D5, 4)],
        "cadence": "latin_IV_V",
    },
    # Bellini ("Samba de Janeiro"): Club Four-on-the-Floor + Carnival Samba Synth Brass Hook!
    "disco_samba": {
        "meter": "4/4", "tempo": 132, "swing": 0.04,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Euro Bass", "Fat Brass", "Real Cavaquinho", "Live Piano", "Whistle DN1", "Brass of Power"],
        "drum_mode": "samba", "kicks": [0, 4, 8, 12],
        "bass_mode": "disco_oct", "acc1_mode": "house_piano",
        "hook": [(0, R8, 2), (2, R8, 2), (3, U3, 3), (6, U5, 2), (8, U6, 2), (10, U5, 2), (12, U3, 4)],
        "fill_type": "latin_timbale",
    },
    "mambo_party": {
        "meter": "4/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Pop Std. Kit 1", "Latin Perc.Kit 1", "Finger Bass DN1", "Bright Piano", "Tight Brass 1", "Sax Ensemble", "Nylon GuitarDNC", "Dual Trumpets"],
        "drum_mode": "mambo", "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "hook": [(0, U5, 2), (3, U5, 2), (6, U6, 2), (8, U5, 2), (12, U3, 2), (14, R8, 2)],
        "fill_type": "latin_timbale",
    },
    # Lou Bega ("Mambo No. 5"): Electro-Swing Mambo Drum Loop + Trumpet/Sax Riff + Piano!
    "mambo_five": {
        "meter": "4/4", "tempo": 174, "swing": 0.16, "swing8": True,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Jazz Piano", "Tight Brass 1", "Baritone Sax DN1", "BX3 Jazz", "JazzTrumpet1 DNC"],
        "drum_mode": "mambo", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, D6, 4)],
        "acc1_steps": [(0, CLOSE, 2, 82), (6, HIGH_STAB, 2, 84), (12, CLOSE, 2, 80)],
        "hook": [(0, R8, 2), (2, R8, 2), (4, B3, 2), (6, D3, 2), (8, D5, 2), (10, D5, 2), (12, R8, 4)],
        "cadence": "blues_V_IV", "fill_type": "latin_timbale",
    },
    # Prince Royce / Romeo Santos Sensual Urban Modern Bachata!
    "modern_bachata": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["HipHop Kit 1", "Latin Perc.Kit 2", "Dark R&B Bass1", "E.Gtr Ch/Dly DNC", "Real Nylon Gtr", "R&B E. Piano", "Warm Pad", "Chorus Gtr Pro"],
        "drum_mode": "bachata", "bass_mode": "bachata_sync",
        "acc1_steps": [(0, R8, 1, 78), (2, U3, 1, 76), (3, U5, 2, 80), (6, U8, 2, 82), (10, U5, 2, 76), (12, U3, 2, 78), (14, U9, 2, 74)],
        "hook": [(0, U5, 3), (3, U6, 1), (4, U5, 2), (6, U3, 2), (8, U9, 4), (12, R8, 4)],
        "fill_type": "latin_timbale",
    },
    # Cole Porter ("Begin the Beguine") Classic Martinique/Ballroom Beguine!
    "classic_beguine": {
        "meter": "4/4", "tempo": 114, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Concert Grand", "Nylon GuitarDNC", "Full Strings", "RealClarinet DN1", "Sweet FlugelHorn"],
        "drum_mode": "bossa", "kicks": [0, 6, 8, 12],
        "bass_pat": [(0, R, 5), (6, D5, 2), (8, L5, 4), (12, D5, 4)],
        "acc1_steps": [(0, OPEN, 3, 76), (3, CLOSE, 3, 72), (6, CLOSE, 2, 74), (8, OPEN, 4, 76), (12, CLOSE, 4, 74)],
        "hook": [(0, D5, 4), (4, D6, 2), (6, R8, 2), (8, U3, 6), (14, U9, 2), (16, R8, 8)],
    },
    # Julio Iglesias / Pop-Orchestral Modern Beguine
    "modern_beguine": {
        "meter": "4/4", "tempo": 118, "swing": 0.0,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 2", "Finger Bass DN1", "Pop Grand", "SteelGtrPro DNC", "Real Strings 1", "French Section", "Tenor Sax DN1"],
        "drum_mode": "chacha", "kicks": [0, 6, 8, 14],
        "bass_pat": [(0, R, 5), (6, D5, 2), (8, R, 5), (14, L5, 2)],
        "acc1_mode": "pop_strum",
        "hook": [(0, R8, 3), (3, U3, 3), (6, U5, 2), (8, U6, 4), (12, U5, 4)],
    },
    "tropicana_dance": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "JB Finger BsDN1", "Steel Drums GM", "Bright Piano", "Tight Brass 1", "Nylon GuitarDNC", "Marimba"],
        "drum_mode": "salsa_clave", "kicks": [0, 4, 8, 12],
        "bass_mode": "cumbia_triad", "acc1_mode": "salsa_montuno",
        "hook": [(0, U3, 2), (3, U5, 2), (6, U8, 2), (10, U5, 2), (12, U3, 4)],
        "fill_type": "latin_timbale",
    },
    # Bebel Gilberto / Thievery Corporation Electronic Lounge Modern Bossa
    "modern_bossa": {
        "meter": "4/4", "tempo": 124, "swing": 0.08,
        "tracks": ["Lounge Kit Amb", "Latin Perc.Kit 2", "Synth Bass Warm", "Suit Case88 EP1", "Real Nylon Gtr", "Motion Ocean", "Jazz Flute Expr.", "SoftAltoSax DN1"],
        "drum_mode": "bossa", "kicks": [0, 6, 8, 11],
        "bass_mode": "bossa_root5", "acc1_mode": "bossa_violao",
        "hook": [(2, U9, 3), (6, R8, 3), (10, D6, 4), (18, U3, 3), (22, U9, 5)],
    },
    "disco_chacha": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Pop Std. Kit 1", "Latin Perc.Kit 1", "JB Pick Bs DN1", "Strat N Cln Mute", "Bright Piano", "Movie Str.1 DNC", "Tight Brass 2", "Jazz Flute Expr."],
        "drum_mode": "disco", "bass_mode": "disco_oct", "acc1_mode": "salsa_montuno",
        "hook": [(0, U5, 2), (4, U5, 2), (8, U6, 1), (10, U5, 1), (12, U3, 4)],
    },
    # Harry Belafonte ("Banana Boat / Jamaica Farewell") Trinidad Steel-Pan Calypso!
    "calypso": {
        "meter": "4/4", "tempo": 118, "swing": 0.06,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "Acoustic Bass 1", "Steel Drums GM", "Real Nylon Gtr", "Marimba", "Jazz Trumpet DN1", "Warm Steel"],
        "drum_mode": "cumbia", "kicks": [0, 6, 8, 12],
        "perc_steps": [(0, 56, 72), (3, 56, 70), (6, 56, 74), (10, 63, 72), (12, 64, 76)],
        "bass_pat": [(0, R, 3), (3, D3, 3), (6, D5, 2), (8, R8, 4), (12, D5, 4)],
        "acc1_steps": [(0, THIRDS, 2, 82), (3, THIRDS, 2, 80), (6, HIGH_STAB, 2, 82), (10, THIRDS, 2, 78), (14, THIRDS, 2, 80)],
        "hook": [(0, U5, 3), (3, U3, 3), (6, R8, 2), (8, U9, 2), (10, U3, 2), (12, R8, 4)],
    },
    # Bob Marley ("Three Little Birds" / "One Love") Classic Roots Reggae 1!
    "reggae_1": {
        "meter": "4/4", "tempo": 88, "swing": 0.16,
        "tracks": ["VintageKit 1 Amb", "Latin Perc.Kit 2", "Dark E.Bass 2", "Strat N Cln Mute", "BX3 Jazz", "Classic Piano", "Tight Brass 1", "Melodica"],
        "drum_mode": "reggae_onedrop", "kicks": [8], "snares": [8],
        "bass_mode": "reggae_drop", "acc1_mode": "reggae_skank", "acc3_mode": "organ_bubble",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U3, 2), (6, R8, 4), (16, D6, 2), (18, D5, 4)],
    },
    # UB40 / Shaggy Pop-Dancehall Reggae 2 (Steppers 4-kick + Horn Section!)
    "reggae_2": {
        "meter": "4/4", "tempo": 92, "swing": 0.12,
        "tracks": ["Studio Kit", "Standard PercKit", "Synth Bass Warm", "Single Coil", "Pop Grand", "Jazz Organ", "Brass & Sax", "Tenor Sax DN1"],
        "drum_mode": "reggae_onedrop", "kicks": [0, 4, 8, 12], "snares": [8],
        "bass_pat": [(0, R, 2), (3, R, 2), (6, D5, 2), (8, R, 3), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "reggae_skank",
        "hook": [(2, HIGH_STAB, 2), (6, THIRDS, 2), (18, U5, 2), (20, U3, 2), (22, R8, 4)],
    },
    "latin_club": {
        "meter": "4/4", "tempo": 124, "swing": 0.04,
        "tracks": ["House Kit 1", "Latin Perc.Kit 1", "Disclosure Bass", "Live Piano", "Concert Gtr DNC", "Techno Stab DNC", "Tight Brass 2", "Jazz Sax DN1"],
        "drum_mode": "house",
        "perc_steps": [(0, 64, 76), (3, 63, 72), (6, 62, 74), (10, 63, 74), (14, 64, 78)],
        "bass_mode": "house_pump", "acc1_mode": "salsa_montuno",
        "hook": [(0, R8, 2), (3, U3, 2), (6, U5, 3), (12, U3, 2), (14, R8, 2)],
    },
    # Simon & Garfunkel / Altiplano ("El Cóndor Pasa"): Andean Huayno with Pan Flute, Charango/Mandolin & Bombo!
    "andean": {
        "meter": "4/4", "tempo": 106, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 2", "Acoustic Bass 1", "Mandolin DNC", "Real Nylon Gtr", "Pan Flute DN1", "Warm Strings", "Whistle Robin"],
        "drum_mode": "cumbia", "kicks": [0, 4, 8, 12],
        "perc_steps": [(0, 41, 84), (3, 41, 64), (4, 41, 80), (8, 41, 84), (11, 41, 64), (12, 41, 80), (2, 70, 56), (6, 70, 56), (10, 70, 56), (14, 70, 56)],
        "bass_pat": [(0, R, 3), (4, D3, 3), (8, D5, 3), (12, R, 3)],
        "acc1_steps": [(0, STRUM_DN, 2, 80), (2, STRUM_UP, 1, 72), (3, STRUM_DN, 1, 76), (4, CHUCK, 2, 78), (8, STRUM_DN, 2, 80), (10, STRUM_UP, 1, 72), (11, STRUM_DN, 1, 76), (12, CHUCK, 2, 78)],
        "hook": [(0, D5, 2), (2, R8, 2), (4, U3, 4), (8, U5, 3), (11, U3, 1), (12, R8, 4)],
        "cadence": "modal_bVII",
    },
    # Kaoma ("Lambada - Chorando Se Foi"): Iconic Bandoneon/Accordion Melody + Zouky-Cumbia Rhythm!
    "lambada": {
        "meter": "4/4", "tempo": 118, "swing": 0.04,
        "tracks": ["Pop Kit 1 Amb", "Latin Perc.Kit 1", "JB Finger BsDN1", "Accordion", "Single Coil Pro", "Nylon GuitarDNC", "Warm Pad", "Fisa Master"],
        "drum_mode": "cumbia", "kicks": [0, 3, 8, 11],
        "bass_pat": [(0, R, 3), (3, D5, 3), (6, R8, 2), (8, R, 3), (11, D5, 3), (14, R, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, U5, 3), (3, U3, 1), (4, U9, 2), (6, R8, 2), (8, U9, 2), (10, U3, 2), (12, U9, 2), (14, D5, 2)],
        "cadence": "flamenco_bVI_V",
    },
    # Proyecto Uno ("El Tiburón" / "Meneaito"): 90s Merengue-House Party!
    "meneaito": {
        "meter": "4/4", "tempo": 126, "swing": 0.0,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Synth Bass 1", "Live Piano", "Tight Brass 2", "Techno Stab DNC", "Sax Ensemble", "Dance Lead"],
        "drum_mode": "merengue", "bass_mode": "disco_oct", "acc1_mode": "salsa_montuno",
        "hook": [(0, HIGH_STAB, 2), (3, HIGH_STAB, 2), (6, THIRDS, 2), (12, R8, 2), (14, U3, 2)],
    },
    # Los Del Rio ("Macarena"): Electro-Flamenco Pop Claps, Trumpet Hook & Tumbao Bass!
    "macarena": {
        "meter": "4/4", "tempo": 104, "swing": 0.04,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Synth Bass Warm", "Bright Piano", "Concert Gtr DNC", "Tight Brass 1", "Warm Pad", "Jazz Trumpet DN1"],
        "drum_mode": "chacha", "kicks": [0, 4, 8, 12],
        "perc_steps": [(4, 39, 86), (12, 39, 86)],
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, R, 4), (14, D5, 2)],
        "acc1_mode": "salsa_montuno", "acc2_mode": "pop_strum",
        "hook": [(0, R8, 2), (2, R8, 2), (4, R8, 2), (6, U3, 2), (8, R8, 2), (10, R8, 2), (12, D5, 4)],
    },
    # Luiz Gonzaga / Classic Baião ("Anna" / "Asa Branca"): Zabumba `dotted-8th + 16th` kick + Triangle + Accordion!
    "bayon": {
        "meter": "4/4", "tempo": 112, "swing": 0.06,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "Accordion", "Real Nylon Gtr", "Real Strings 1", "Classic Piano", "Marimba"],
        "drum_mode": "pop_8", "kicks": [0, 3, 8, 11], "snares": [4, 12],
        "perc_steps": [(0, 80, 62), (2, 81, 76), (4, 80, 62), (6, 81, 76), (8, 80, 62), (10, 81, 76), (12, 80, 62), (14, 81, 76)],
        "bass_pat": [(0, R, 3), (3, D5, 3), (6, R8, 2), (8, R, 3), (11, D5, 3), (14, R, 2)],
        "acc1_mode": "pop_strum",
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 3), (7, U5, 3), (10, U3, 2), (12, R8, 4)],
    },
    "unplugged_gipsy": {
        "meter": "4/4", "tempo": 118, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Concert Gtr DNC", "Real Nylon Gtr", "Accordion", "Mandolin DNC", "Concert Gtr Pro"],
        "drum_mode": "flamenco", "kicks": [0, 6, 12], "snares": [4, 10, 14],
        "bass_pat": [(0, R, 5), (6, D5, 2), (8, R, 5), (14, L5, 2)],
        "acc1_mode": "pop_strum", "acc2_mode": "travis_pick",
        "hook": [(0, U3, 2), (3, U5, 2), (6, U3, 2), (8, U9, 2), (10, R8, 2), (12, LT, 2), (14, R8, 2)],
        "cadence": "flamenco_bVI_V", "fill_type": "flamenco_rasg",
    },
    "unplugged_reggae": {
        "meter": "4/4", "tempo": 90, "swing": 0.14,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "RealFolk Gtr DNC", "Real Nylon Gtr", "Wurly Clean", "Accordion", "Whistle DN1"],
        "drum_mode": "reggae_onedrop", "kicks": [8], "snares": [8],
        "perc_steps": [(0, 64, 70), (6, 63, 66), (14, 70, 56)],
        "bass_mode": "reggae_drop", "acc1_mode": "reggae_skank",
        "hook": [(2, U5, 2), (6, U3, 2), (10, R8, 4), (18, U9, 2), (22, R8, 4)],
    },
    "sambalegre": {
        "meter": "4/4", "tempo": 122, "swing": 0.08,
        "tracks": ["Real Kit 2 Amb", "Latin Perc.Kit 1", "JB Finger BsDN1", "Real Cavaquinho", "Live Piano", "Tight Brass 1", "Jazz Flute Expr.", "Trumpet Expr.1"],
        "drum_mode": "samba", "bass_mode": "samba_surdo", "acc1_mode": "bossa_violao",
        "hook": [(0, R8, 2), (2, U3, 2), (3, U5, 3), (8, U6, 2), (10, U5, 2), (12, U3, 4)],
        "fill_type": "latin_timbale",
    },
    "samba_dance": {
        "meter": "4/4", "tempo": 126, "swing": 0.06,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "Synth Bass 1", "Bright Piano", "Real Nylon Gtr", "Fat Brass", "Whistle DN1", "Sax Ensemble"],
        "drum_mode": "samba", "kicks": [0, 4, 8, 12], "bass_mode": "samba_surdo", "acc1_mode": "house_piano",
        "hook": [(0, U5, 2), (3, U6, 2), (6, U5, 2), (8, U3, 2), (11, R8, 3), (14, U3, 2)],
        "fill_type": "latin_timbale",
    },

    # =========================================================================
    # 9. JAZZ (36 Styles)
    # =========================================================================
    "swing_band": {
        "meter": "4/4", "tempo": 138, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Big Band Brass 1", "Sax Ensemble", "Jazz Trumpet DN1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "hook": [(0, D5, 2), (2, R8, 2), (4, U3, 4), (10, U5, 2), (12, U3, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Gordon Goodwin's Big Phat Band: Crisp Modern Syncopated Big Band!
    "modern_big_band": {
        "meter": "4/4", "tempo": 144, "swing": 0.26, "swing8": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "JB Finger BsDN1", "Tine EP Dyno", "Clean Jazz 1", "Tight Brass 1", "Real Sax Ens.", "TrumpetShake Y+"],
        "drum_mode": "bebop", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp",
        "acc4_steps": [(0, HIGH_STAB, 1), (3, THIRDS, 2), (10, HIGH_STAB, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, R8, 1), (2, U3, 2), (6, B5, 1), (8, U5, 4), (14, B7, 2), (16, R8, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Count Basie / Quincy Jones Heavy Shuffle Big Band!
    "big_band_shuffle": {
        "meter": "4/4", "tempo": 132, "swing": 0.32, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Oct. Jazz Guitar", "Big Band Brass 2", "Baritone Sax DN1", "Tenor Growl DN1"],
        "drum_mode": "jazz_swing", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_mode": "boogie_8", "acc1_mode": "boogie_comp",
        "hook": [(0, R, 2), (2, B3, 2), (4, D3, 2), (6, D5, 4), (16, B7, 2), (18, D6, 2), (20, D5, 4)],
        "cadence": "blues_V_IV", "fill_type": "jazz_triplet",
    },
    "latin_jazz_band": {
        "meter": "4/4", "tempo": 130, "swing": 0.0,
        "tracks": ["Jazz Kit 2 Amb", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Jazz Piano", "Nylon GuitarDNC", "Tight Brass 1", "Jazz Flute Expr.", "JazzTrumpet1 DNC"],
        "drum_mode": "salsa_clave", "clave_dir": "23", "bass_mode": "salsa_tumbao", "acc1_mode": "salsa_montuno",
        "hook": [(0, U3, 2), (3, U5, 3), (8, U9, 2), (11, R8, 3)],
        "cadence": "jazz_ii_V", "fill_type": "latin_timbale",
    },
    # Dizzy Gillespie ("Manteca" / "A Night in Tunisia"): Afro-Cuban Ostinato Bass (`0 . . 4 . . 5 .`) + Dizzy Muted/Open Trumpet!
    "afro_cuban_jazz": {
        "meter": "4/4", "tempo": 136, "swing": 0.04,
        "tracks": ["Jazz Kit 1 Amb", "Latin Perc.Kit 1", "Real Ac. Bass 1", "Live Piano", "Vibraphone 1", "Big Band Brass 1", "Alto Sax DN1", "Mute Trumpet"],
        "drum_mode": "mambo", "clave_dir": "32",
        "bass_pat": [(0, R, 4), (6, D5, 4), (10, B5, 2), (12, D5, 4)],
        "acc1_steps": [(0, JAZZ_SHELL, 3, 80), (6, JAZZ_SHELL, 3, 82), (10, HIGH_STAB, 2, 78), (12, JAZZ_SHELL, 4, 80)],
        "hook": [(0, R8, 2), (3, U3, 2), (6, U5, 2), (8, B5, 2), (10, D5, 2), (12, B3, 2), (14, R, 2)],
        "cadence": "flamenco_bVI_V", "fill_type": "latin_timbale",
    },
    # Charlie Parker / Bud Powell Blazing BeBop Quartet!
    "bebop": {
        "meter": "4/4", "tempo": 188, "swing": 0.24, "swing8": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Vibraphone 1", "Alto Sax DN1", "Jazz Trumpet DN1"],
        "drum_mode": "bebop",
        "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4), (12, C5, 4), (16, D5, 4), (20, B7, 4), (24, R8, 4), (28, LT, 4)],
        "acc1_steps": [(2, JAZZ_SHELL, 2, 74), (10, JAZZ_SHELL, 2, 76), (14, HIGH_STAB, 2, 72)],
        "hook": [(0, D5, 2), (2, D6, 2), (4, B7, 2), (6, B5, 2), (8, D5, 2), (10, D3, 2), (12, R, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Bill Evans ("Waltz for Debby" / "Someday My Prince Will Come") Medium 3/4 Jazz Waltz!
    "medium_jazzwaltz": {
        "meter": "3/4", "tempo": 128, "swing": 0.24, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Soft Jazz Guitar", "Vibraphone 1", "Sweet FlugelHorn", "Tenor Sax DN1"],
        "drum_mode": "waltz_3_4", "ride_note": 51,
        "bass_mode": "waltz_walk",
        "acc1_steps": [(0, JAZZ_SHELL, 3, 72), (6, JAZZ_SHELL, 3, 70), (10, JAZZ_SHELL, 2, 66)],
        "hook": [(0, U5, 4), (4, U3, 4), (8, U9, 4), (12, R8, 8), (20, D6, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Coltrane ("My Favorite Things") Fast 3/4 Modal/Bop Jazz Waltz!
    "fast_jazz_waltz": {
        "meter": "3/4", "tempo": 168, "swing": 0.22, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Warm Strings", "Vibraphone 1", "Soprano Sax DN1"],
        "drum_mode": "viennese_3_4", "bass_mode": "waltz_walk",
        "acc1_steps": [(0, QUARTAL, 3, 76), (6, JAZZ_SHELL, 3, 74)],
        "hook": [(0, R8, 4), (4, U5, 4), (8, U5, 4), (12, U9, 4), (16, R8, 4), (20, D5, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "bigger_band": {
        "meter": "4/4", "tempo": 140, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Big Band Brass 1", "Trpts & Trombs", "Reed of Power"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "acc4_steps": [(0, HIGH_STAB, 2), (6, THIRDS, 2), (12, HIGH_STAB, 3)],
        "hook": [(0, U5, 2), (2, U6, 2), (4, U5, 4), (14, U3, 2), (16, R8, 6)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Glenn Miller ("Moonlight Serenade" / "In the Mood"): Clarinet-Led Reed Section (`Glenn & Friends`)!
    "serenade_band": {
        "meter": "4/4", "tempo": 122, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Glenn & Friends", "Mute Ensemble 1", "Clar & Sax Ens 1"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "acc4_mode": "thirds_swell",
        "hook": [(0, D3, 2), (2, D5, 2), (4, R8, 2), (6, D3, 2), (8, D5, 2), (10, R8, 2), (12, U3, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "medium_big_band": {
        "meter": "4/4", "tempo": 128, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Soft Jazz Guitar", "Glenn & Boys", "Sax Ensemble", "Jazz Trb. DN1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "hook": [(2, D5, 2), (4, D6, 2), (6, R8, 4), (18, U3, 2), (20, U9, 2), (22, R8, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Buddy Rich ("Sing, Sing, Sing" / Up-Tempo Roaring Big Band!)
    "fast_big_band": {
        "meter": "4/4", "tempo": 176, "swing": 0.24, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Big Band Brass 1", "Sax Ensemble", "Trumpet Overb."],
        "drum_mode": "bebop", "kicks": [0, 4, 8, 12],
        "perc_steps": [(0, 41, 80, V_34), (3, 43, 76, V_34), (6, 41, 82, V_34), (12, 45, 78, V_34)],
        "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp",
        "hook": [(0, R8, 3), (3, B3, 3), (6, D3, 2), (8, D5, 4), (14, R8, 2)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "swing_ballad_1": {
        "meter": "4/4", "tempo": 82, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Jazz Piano", "Soft Jazz Guitar", "Warm Strings", "Mute Trumpet", "Tenor Sax 1 DNC"],
        "drum_mode": "jazz_brush", "bass_mode": "two_feel", "acc1_mode": "jazz_comp",
        "hook": [(0, U3, 4), (4, U9, 4), (8, R8, 6), (18, D6, 2), (20, D5, 8)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "swing_ballad_2": {
        "meter": "4/4", "tempo": 88, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Suit Case88 EP1", "Jazz Gtr 1 DNC", "Real Sax Ens.", "Soft Trb. DN1", "Vibraphone 1"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp",
        "hook": [(2, D5, 2), (4, R8, 4), (8, U3, 4), (12, U5, 4), (20, U3, 6)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "slow_swing_brush": {
        "meter": "4/4", "tempo": 78, "swing": 0.28, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Concert Grand", "Soft Jazz Guitar", "Chamber Strings", "Sweet FlugelHorn", "JazzClarinet DN1"],
        "drum_mode": "jazz_brush", "bass_mode": "two_feel",
        "acc1_steps": [(0, JAZZ_SHELL, 4, 70), (8, JAZZ_SHELL, 4, 70), (14, JAZZ_SHELL, 2, 64)],
        "hook": [(4, U5, 4), (8, U3, 4), (12, R8, 8)],
        "cadence": "jazz_ii_V",
    },
    # Sinatra & Nelson Riddle Orchestral Swing (Strings + French Horns + Harp + Swing Rhythm Section!)
    "orchestral_swing": {
        "meter": "4/4", "tempo": 130, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Concert Grand", "Jazz Gtr 1 DNC", "ConcertStrings 1", "French Section", "Jazz Trb. DN1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "acc4_mode": "thirds_swell",
        "hook": [(0, D5, 4), (4, R8, 4), (8, U3, 4), (12, U5, 4), (16, U6, 4), (20, U5, 8)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "classic_swing": {
        "meter": "4/4", "tempo": 136, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Clar & Sax Ens 1", "Big Band Brass 2", "Vibraphone 1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "hook": [(0, R8, 2), (2, D6, 2), (4, D5, 2), (6, D3, 2), (8, D2, 2), (10, D3, 2), (12, D5, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "acoustic_jazz": {
        "meter": "4/4", "tempo": 134, "swing": 0.26, "swing8": True,
        "tracks": ["Jazz Kit 3 Amb", "Standard PercKit", "Real Ac. Bass 1", "Concert Grand", "Real Nylon Gtr", "Vibraphone 1", "Soprano Sax DN1", "Jazz Gtr 1 DNC"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp",
        "hook": [(0, U3, 3), (4, U5, 3), (8, U9, 4), (16, R8, 6)],
        "cadence": "jazz_ii_V",
    },
    "easy_swing": {
        "meter": "4/4", "tempo": 118, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Soft Jazz Guitar", "Cool Sax Ens.", "Soft Trb. DN1", "Jazz Flute Expr."],
        "drum_mode": "jazz_brush", "bass_mode": "two_feel", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "hook": [(0, D5, 2), (2, D6, 2), (4, U3, 4), (12, R8, 4)],
        "cadence": "jazz_ii_V",
    },
    "easy_jazzwaltz": {
        "meter": "3/4", "tempo": 114, "swing": 0.24, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Jazz Piano", "Nylon GuitarDNC", "Warm Strings", "Jazz Flute Expr.", "Vibraphone 1"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 8), (8, D5, 4)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": JAZZ_SHELL,
        "hook": [(0, U3, 4), (4, R8, 4), (8, D6, 4), (12, D5, 8)],
        "cadence": "jazz_ii_V",
    },
    # New Orleans Bourbon Street Dixieland ("When the Saints"): Tuba 2-beat, Banjo 4-strum, Clarinet & Tailgate Trombone!
    "dixieland": {
        "meter": "4/4", "tempo": 162, "swing": 0.24, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Tuba Gold", "Banjo", "Ragtime Piano", "Jazz Trb. DN1", "Jazz Cornet DN1", "RealClarinet DN1"],
        "drum_mode": "dixie", "perc_steps": [(4, 76, 68), (12, 77, 68)],
        "bass_mode": "country_2beat",
        "acc1_steps": [(0, STRUM_DN, 2, 78), (4, CHUCK, 2, 82), (8, STRUM_DN, 2, 78), (12, CHUCK, 2, 82)],
        "acc2_mode": "stride_piano",
        "hook": [(0, R8, 2), (2, U3, 2), (4, U5, 2), (6, U6, 2), (8, U5, 4), (12, U3, 2), (14, R8, 2)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Roaring 1920s Charleston (`0` and `6` = Beat 1 and `2-and` iconic Charleston syncopation!)
    "charleston": {
        "meter": "4/4", "tempo": 158, "swing": 0.22, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Tuba Gold", "Banjo", "Ragtime Piano", "Mute Trumpet", "Jazz Trb. DN1", "JazzClarinet DN1"],
        "drum_mode": "dixie", "kicks": [0, 6], "snares": [4, 12],
        "perc_steps": [(0, 76, 74), (6, 76, 78)],
        "bass_pat": [(0, R, 4), (6, L5, 4), (12, D5, 4)],
        "acc1_steps": [(0, CLOSE, 3, 84), (6, HIGH_STAB, 4, 86)],
        "hook": [(0, U3, 3), (6, R8, 5), (16, U5, 3), (22, U3, 5)],
        "cadence": "jazz_ii_V",
    },
    # Fats Waller / Art Tatum Harlem Stride Piano!
    "stride": {
        "meter": "4/4", "tempo": 144, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Clar & Sax Ens 1", "Mute Trumpet", "Ragtime Piano"],
        "drum_mode": "jazz_brush", "bass_mode": "two_feel",
        "acc1_steps": [(0, LR, 2, 82), (2, JAZZ_SHELL, 2, 78), (4, L5, 2, 80), (6, JAZZ_SHELL, 2, 78), (8, LR, 2, 82), (10, JAZZ_SHELL, 2, 78), (12, D5, 2, 80), (14, HIGH_STAB, 2, 78)],
        "hook": [(0, U5, 2), (2, D6, 2), (4, R8, 2), (6, U3, 2), (8, U5, 4)],
        "cadence": "jazz_ii_V",
    },
    # Scott Joplin ("The Entertainer" / "Maple Leaf Rag"): Straight 2/4 Syncopated Ragtime Piano!
    "ragtime": {
        "meter": "2/4", "tempo": 102, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Alp Tuba", "Ragtime Piano", "Banjo", "RealClarinet DN1", "Jazz Cornet DN1", "Honky-Tonk"],
        "drum_mode": "polka_2_4",
        "bass_pat": [(0, R, 2), (4, L5, 2)],
        "acc1_steps": [(1, CLOSE, 1, 76), (2, HIGH_STAB, 2, 80), (5, CLOSE, 1, 76), (6, HIGH_STAB, 2, 80)],
        "hook": [(0, D2, 1), (1, B3, 1), (2, D3, 2), (4, R8, 1), (5, D3, 1), (6, R8, 2)],
        "cadence": "country_IV_V",
    },
    # Jimmy Smith Slow Hammond B3 Organ Trio!
    "slow_organ_swing": {
        "meter": "4/4", "tempo": 88, "swing": 0.28, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Organ Low 1", "Jimmy Organ", "Jazz Gtr 1 DNC", "BX3 Jazz", "Tenor Sax DN1", "Jazz Organ"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp",
        "hook": [(0, B3, 1), (1, D3, 3), (4, D5, 4), (8, B7, 4), (12, D5, 4)],
        "cadence": "blues_V_IV",
    },
    "medium_org_swing": {
        "meter": "4/4", "tempo": 134, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Organ Low 2", "BX3 Jazz Pc.", "Clean Jazz 1", "Jimmy Organ", "Jazz Sax DN1", "Jazz Trumpet DN1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp", "acc2_mode": "gypsy_pompe",
        "hook": [(0, R8, 2), (2, B7, 2), (4, D5, 2), (6, B5, 2), (8, D4, 2), (10, B3, 2), (12, R, 4)],
        "cadence": "blues_V_IV", "fill_type": "jazz_triplet",
    },
    # Jimmy Smith ("The Cat" / "Back at the Chicken Shack") Greasy Organ Blues!
    "organ_blues": {
        "meter": "4/4", "tempo": 122, "swing": 0.30, "swing8": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "Organ Low Pc.", "Jimmy Organ", "Clean Jazz 1", "BX3 Rock 1", "Tight Brass 1", "Tenor Growl DN1"],
        "drum_mode": "jazz_swing", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_mode": "boogie_8",
        "acc1_steps": [(0, CLOSE, 3, 82), (6, HIGH_STAB, 2, 84), (10, CLOSE, 2, 78), (14, HIGH_STAB, 2, 80)],
        "hook": [(0, R8, 2), (2, UB7, 2), (4, R8, 2), (6, B5, 1), (7, D5, 3), (12, B3, 2), (14, R, 2)],
        "cadence": "blues_V_IV", "fill_type": "jazz_triplet",
    },
    # Dave Brubeck / Miles Davis Cool Jazz Quartet
    "jazz_quartet": {
        "meter": "4/4", "tempo": 132, "swing": 0.26, "swing8": True,
        "tracks": ["Jazz Kit 3 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Vibraphone 1", "Soft Jazz Guitar", "Mute Trumpet", "Alto Sax DN1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp",
        "hook": [(2, U3, 2), (4, U5, 4), (8, U9, 2), (10, R8, 6)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Note manual spelling "Classic JazzWalz" -> True 3/4 Jazz Waltz!
    "classic_jazzwalz": {
        "meter": "3/4", "tempo": 134, "swing": 0.24, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Concert Grand", "Jazz Gtr 1 DNC", "Clar & Sax Ens 1", "Vibraphone 1", "Jazz Flute Expr."],
        "drum_mode": "waltz_3_4", "ride_note": 51, "bass_mode": "waltz_walk",
        "acc1_steps": [(4, JAZZ_SHELL, 3, 74), (8, JAZZ_SHELL, 3, 70)],
        "hook": [(0, D5, 4), (4, U3, 4), (8, U9, 4), (12, R8, 6), (18, D5, 6)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "jazz_club": {
        "meter": "4/4", "tempo": 124, "swing": 0.26, "swing8": True,
        "tracks": ["Cool Kit Amb", "Standard PercKit", "Ac. Jazz Bass", "Suit Case88 EP1", "Jazz Gtr 1 DNC", "Jazz Organ", "Mute Trumpet", "Jazz Tenor Sax 1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp",
        "hook": [(0, U9, 3), (4, U3, 3), (8, D5, 6), (18, D6, 2), (20, R8, 6)],
        "cadence": "jazz_ii_V",
    },
    "jazz_brush": {
        "meter": "4/4", "tempo": 96, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Jazz Piano", "Soft Jazz Guitar", "Warm Pad", "Sweet FlugelHorn", "Tenor Sax DN1"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp",
        "hook": [(0, D5, 3), (4, U3, 3), (8, U9, 6), (18, R8, 6)],
        "cadence": "jazz_ii_V",
    },
    # George Benson / Wes Montgomery Smooth Octave-Guitar Soft Jazz!
    "soft_jazz": {
        "meter": "4/4", "tempo": 116, "swing": 0.20, "swing8": True,
        "tracks": ["Cool Kit Amb", "Latin Perc.Kit 2", "JB Finger BsDN1", "Tine EP Phaser", "Oct. Jazz Guitar", "Warm Strings", "Jazz Flute Expr.", "Soft Jazz Guitar"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp",
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 4), (8, U5, 4), (16, U6, 2), (18, U5, 6)],
        "cadence": "jazz_ii_V",
    },
    # Django Reinhardt & Stéphane Grappelli ("Minor Swing"): Gypsy Jazz Manouche *La Pompe* Acoustic Guitars + Upright Bass + Violin!
    "django": {
        "meter": "4/4", "tempo": 176, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Real Ac. Bass 1", "ClassicSteel DNC", "Concert Gtr Pro", "Classic Musette", "RealClarinet DN1", "Real Violin DNC"],
        "drum_mode": "gypsy_pompe", "bass_mode": "walking_jazz",
        "acc1_mode": "gypsy_pompe",
        "acc2_seq": [(0, STRUM_DN, 2), (4, CHUCK, 1), (8, STRUM_DN, 2), (12, CHUCK, 1)],
        "hook": [(0, R, 2), (2, D3, 2), (4, D5, 2), (6, R8, 2), (8, U3, 2), (10, R8, 2), (12, LT, 2), (14, R8, 2)],
        "cadence": "flamenco_bVI_V", "fill_type": "jazz_triplet",
    },
    "unplugged_swing": {
        "meter": "4/4", "tempo": 128, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "RealFolk Gtr DNC", "Classic Piano", "Accordion", "Mandolin DNC", "JazzClarinet DN1"],
        "drum_mode": "jazz_brush", "bass_mode": "two_feel", "acc1_mode": "gypsy_pompe",
        "hook": [(0, U3, 2), (2, U5, 2), (4, R8, 4), (12, D6, 2), (14, D5, 2)],
        "cadence": "jazz_ii_V",
    },
    # Manhattan Transfer / Scat Choir Vocal Swing!
    "vocal_swing": {
        "meter": "4/4", "tempo": 138, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Scat Voices DNC", "Big Band Brass 1", "Cycle Scat 1"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U6, 2), (6, U5, 4), (14, U3, 2), (16, R8, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    "vocal_jazz": {
        "meter": "4/4", "tempo": 120, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Concert Grand", "Soft Jazz Guitar", "Cycle Scat 2", "Mute Trumpet", "Scat Voices DNC"],
        "drum_mode": "jazz_brush", "bass_mode": "walking_alt", "acc1_mode": "jazz_comp",
        "hook": [(2, R8, 2), (4, U9, 2), (6, U3, 4), (16, D6, 2), (18, D5, 6)],
        "cadence": "jazz_ii_V",
    },

    # =========================================================================
    # 10. MOVIE & SHOW (24 Styles — Iconic Film & Broadway Scores!)
    # =========================================================================
    # "Earned It" / "Crazy in Love (2014 Remix)": Sultry 6/8 Cinematic Dark Strings, Sub Pulse & Piano!
    "fifty_shades": {
        "meter": "6/8", "tempo": 66, "swing": 0.0,
        "tracks": ["HipHop Kit 1", "Standard PercKit", "Dark R&B Bass1", "Concert Grand", "Tremolo Strings", "Movie Str.1 DNC", "Cello", "Violin Expr. DNC"],
        "drum_mode": "ballad_6_8", "kicks": [0, 4],
        "perc_steps": [(6, 39, 78), (0, 41, 70, V_34)],
        "bass_pat": [(0, R, 6), (6, S5, 3), (9, D5, 3)],
        "acc1_steps": [(0, CLOSE, 2, 76), (2, CLOSE, 2, 70), (4, CLOSE, 2, 72), (6, OPEN, 4, 80), (10, CLOSE, 2, 70)],
        "hook": [(0, R8, 4), (4, U3, 2), (6, S5, 4), (10, D5, 2), (12, R8, 6)],
        "cadence": "cinematic_bVI",
    },
    # JAMES BOND 007 ("Dr. No" Monty Norman / John Barry): Iconic `5 -> #5 -> 6 -> #5` Vamp + Surf Spy Guitar + Brass Stabs!
    "special_agent": {
        "meter": "4/4", "tempo": 130, "swing": 0.14, "swing8": True,
        "tracks": ["Standard Kit Amb", "Jazz Kit 1 Amb", "JB Pick Bs DN1", "Single Coil Pro", "Vibraphone 1", "Movie Str.1 DNC", "Tight Brass 1", "Brass of Power"],
        "drum_mode": "jazz_swing", "ride_note": 51, "kicks": [0, 6, 8],
        "bass_pat": [(0, D5, 4), (4, S5, 4), (8, D6, 4), (12, S5, 4)],
        "acc1_steps": [(0, R, 2, 84), (2, D3, 1, 78), (3, D5, 1, 80), (4, B7, 2, 82), (6, D6, 2, 80), (8, D5, 2, 82), (11, D3, 1, 76), (12, R, 4, 84)],
        "acc4_steps": [(0, HIGH_STAB, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, D5, 4), (4, S5, 4), (8, D6, 4), (12, S5, 4), (16, R, 2), (18, D2, 1), (19, B3, 5), (24, D2, 4)],
        "cadence": "cinematic_bVI", "fill_type": "orchestral_timp",
    },
    # ENNIO MORRICONE ("The Good, the Bad and the Ugly"): Galloping Snare/Timpani, Ocarina Fifth-Fourth Call, Twang Guitar, Choir!
    "spaghetti_western": {
        "meter": "4/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Room Kit Amb", "Trinity Perc.Kit", "Picked E. Bass 2", "Real Nylon Gtr", "Single Coil Pro", "Atmoschoir Pad", "Concert Trumpet", "Ocarina"],
        "drum_mode": "pop_8", "kicks": [0, 8], "snares": [4, 12],
        "perc_steps": [(0, 47, 78), (2, 38, 58), (3, 38, 62), (4, 45, 76), (8, 47, 78), (10, 38, 58), (11, 38, 62), (12, 45, 76)],
        "bass_pat": [(0, R, 4), (4, D5, 4), (8, R, 4), (12, L5, 4)],
        "acc1_steps": [(0, R, 2, 80), (2, D5, 1, 74), (3, R8, 1, 78), (4, U3, 4, 80), (8, R, 2, 80), (10, D5, 1, 74), (11, R8, 1, 78), (12, D5, 4, 78)],
        "hook": [(0, U5, 1), (1, R8, 1), (2, U5, 1), (3, R8, 1), (4, U5, 6), (12, D6, 4), (16, D5, 4), (20, D4, 4), (24, R8, 8)],
        "cadence": "modal_bVII", "fill_type": "orchestral_timp",
    },
    # BURT BACHARACH ("Raindrops Keep Fallin'" / "Walk On By"): Sweet FlugelHorn, Tack/Bright Piano, Ukulele/Nylon Bounce!
    "burt_s_bounce": {
        "meter": "4/4", "tempo": 114, "swing": 0.16, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 2", "Vintage P. Flat", "Bright Piano", "Real Ukulele", "Warm Strings", "Marimba", "Sweet FlugelHorn"],
        "drum_mode": "pop_8", "snare_note": 37, "kicks": [0, 6, 8], "snares": [4, 12],
        "perc_steps": [(2, 73, 56), (6, 74, 62), (10, 70, 50), (14, 81, 58)],
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, R, 4), (12, D6, 2), (14, D5, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 3, 76), (6, JAZZ_SHELL, 3, 78), (12, JAZZ_SHELL, 4, 74)],
        "acc2_mode": "offbeat_chop",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U6, 4), (8, U5, 2), (10, U3, 2), (12, U9, 4)],
        "cadence": "jazz_ii_V",
    },
    # John Williams ("Star Wars / Raiders / Superman"): Heroic Triplet Brass Fanfare + Orchestral Snare & Timpani!
    "screenepicmarch1": {
        "meter": "4/4", "tempo": 120, "swing": 0.18, "swing8": True,
        "tracks": ["Room Kit Amb", "Trinity Perc.Kit", "Class.Contrabs", "Strings&Orch.V.", "Movie Brass", "French Section", "OrchestraTutti 1", "Concert Trumpet"],
        "drum_mode": "march_2_4",
        "perc_steps": [(0, 47, 88), (6, 45, 78), (8, 47, 86), (12, 55, 76, V_34), (14, 45, 82)],
        "bass_pat": [(0, R, 4), (4, R, 2), (6, D5, 2), (8, R, 4), (12, L5, 4)],
        "acc1_mode": "spiccato_8",
        "acc4_steps": [(0, OPEN, 4), (6, THIRDS, 2), (8, HIGH_STAB, 4)],
        "hook": [(0, R8, 4), (4, U5, 4), (8, U3, 1), (9, U9, 1), (10, R8, 2), (12, U8, 4)],
        "cadence": "march_V_I", "fill_type": "orchestral_timp",
    },
    # Hans Zimmer ("Pirates / Dark Knight / Gladiator"): Relentless Spiccato Strings Ostinato + Taiko War Drums + Low Horns!
    "screenepicmarch2": {
        "meter": "4/4", "tempo": 128, "swing": 0.0,
        "tracks": ["Power Kit 2 Amb", "Trinity Perc.Kit", "Cello", "ConcertStrings 2", "Movie Stack 1", "French Section", "Sforzato Brass", "Atmoschoir Pad"],
        "drum_mode": "pop_8", "kicks": [0, 3, 6, 8, 12, 14], "snares": [4, 12],
        "perc_steps": [(0, 41, 92), (3, 43, 84), (6, 41, 90), (8, 41, 88), (12, 43, 86), (14, 45, 82)],
        "bass_pat": [(0, R, 2), (2, R, 1), (3, R, 2), (6, D5, 2), (8, R, 2), (12, B7, 2), (14, D5, 2)],
        "acc1_steps": [(i, R if i % 4 != 2 else D5, 1, 80 if i % 4 == 0 else 66) for i in range(16)],
        "acc3_mode": "spiccato_8",
        "hook": [(0, R8, 3), (3, D5, 3), (6, S5, 2), (8, D5, 4), (12, D4, 2), (14, D3, 2)],
        "cadence": "cinematic_bVI", "fill_type": "orchestral_timp",
    },
    # Danny Elfman / Addams Family ("Beetlejuice" / Quirky Gothic Comedy): Harpsichord + Xylophone + Finger Snaps!
    "weird_movie": {
        "meter": "4/4", "tempo": 130, "swing": 0.16, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "SFX Kit 1", "Tuba Gold", "Harpsichord 1", "Xylophone", "Tremolo Strings", "Bassoon", "Old Portamento"],
        "drum_mode": "dixie", "kicks": [0, 8], "snares": [4, 12],
        "perc_steps": [(6, 39, 86), (7, 39, 86), (22 % 16, 76, 74)],
        "bass_pat": [(0, R, 2), (2, D2, 2), (4, B3, 2), (6, D4, 2), (8, D5, 4), (12, B5, 2), (14, D5, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, R8, 1), (2, D2, 1), (4, U3, 1), (6, B5, 2), (8, U5, 4)],
        "cadence": "cinematic_bVI",
    },
    # HENRY MANCINI ("The Pink Panther" / "Peter Gunn"): Sneaky Chromatic Bass + Breathy Tenor Sax + Triangle/Hi-Hat!
    "mystery_man": {
        "meter": "4/4", "tempo": 118, "swing": 0.28, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Strat N Cln Mute", "Mute Ensemble 1", "Vibraphone 1", "Tenor Sax DN1"],
        "drum_mode": "jazz_brush", "perc_steps": [(4, 81, 58), (12, 39, 68)],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, D2, 2), (6, B3, 2), (8, D3, 2), (10, D5, 2), (12, B5, 2), (14, D5, 2)],
        "acc1_steps": [(2, JAZZ_SHELL, 2, 74), (10, JAZZ_SHELL, 3, 76)],
        "hook": [(2, D2, 1), (3, D3, 3), (6, C5, 1), (7, D5, 3), (12, R8, 2), (14, B7, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Irving Berlin ("Puttin' on the Ritz"): Vaudeville Syncopated Ritz Swing + Clarinet + Woodblocks!
    "ritz_swing": {
        "meter": "4/4", "tempo": 132, "swing": 0.26, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Ragtime Piano", "Banjo", "Glenn & Friends", "Mute Trumpet", "RealClarinet DN1"],
        "drum_mode": "jazz_swing",
        "perc_steps": [(0, 76, 72), (3, 77, 70), (6, 76, 74), (12, 77, 72)],
        "bass_mode": "two_feel",
        "acc1_steps": [(0, CLOSE, 2, 78), (3, CLOSE, 2, 76), (6, HIGH_STAB, 2, 80), (10, CLOSE, 2, 76), (14, HIGH_STAB, 2, 80)],
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 2), (8, U6, 2), (11, R8, 3)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # Broadway Tap-Shoe Rhythm (`76/77` Woodblock clack-clack tap steps!) + Show Brass!
    "tap_dance": {
        "meter": "4/4", "tempo": 138, "swing": 0.26, "swing8": True,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Bright Piano", "Jazz Gtr 1 DNC", "Trpts & Brass", "Xylophone", "Piccolo"],
        "drum_mode": "jazz_swing",
        "perc_steps": [(0, 76, 80), (2, 77, 70), (3, 76, 74), (4, 77, 82), (6, 76, 72), (8, 76, 80), (10, 77, 72), (11, 76, 76), (12, 77, 84), (14, 76, 78)],
        "bass_mode": "walking_jazz", "acc1_mode": "stride_piano",
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 2), (6, U3, 2), (8, U5, 4)],
        "cadence": "jazz_ii_V",
    },
    # Disney / Alan Menken ("Beauty and the Beast") Lush Show/Movie Ballad!
    "movie_ballad": {
        "meter": "4/4", "tempo": 80, "swing": 0.0,
        "tracks": ["Studio Kit", "Trinity Perc.Kit", "Fretless Bass 2", "Concert Grand", "Classic Harp", "Movie Str.1 DNC", "Oboe 1", "Flute"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [4, 12],
        "perc_steps": [(0, 81, 64)],
        "bass_pat": [(0, R, 8), (8, D5, 6), (14, D3, 2)],
        "acc1_mode": "piano_arp",
        "hook": [(0, D5, 2), (2, D6, 2), (4, R8, 2), (6, U3, 2), (8, U5, 8)],
    },
    # Bert Kaempfert ("A Swingin' Safari" / "Baby Elephant Walk"): Piccolo + Bassoon/Tuba + Jungle Tom Bounce!
    "safari_swing": {
        "meter": "4/4", "tempo": 124, "swing": 0.24, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 1", "Acous. Bass Pro1", "Single Coil", "Marimba", "Mute Ensemble 1", "Bassoon", "Piccolo"],
        "drum_mode": "jazz_brush",
        "perc_steps": [(0, 45, 76), (3, 47, 72), (6, 45, 74), (10, 48, 70), (12, 45, 76)],
        "bass_pat": [(0, R, 3), (4, D5, 3), (8, R8, 3), (12, D5, 3)],
        "acc1_mode": "offbeat_chop",
        "hook": [(0, R8, 2), (2, B3, 2), (4, D3, 2), (6, D5, 2), (8, D6, 2), (10, B7, 2), (12, R8, 4)],
        "cadence": "blues_V_IV",
    },
    "hollywood_1": {
        "meter": "4/4", "tempo": 116, "swing": 0.18, "swing8": True,
        "tracks": ["Room Kit Amb", "Trinity Perc.Kit", "Class.Contrabs", "Concert Grand", "Classic Harp", "OrchestraTutti 1", "French Section", "Real Violin DNC"],
        "drum_mode": "jazz_brush", "bass_mode": "two_feel", "acc1_mode": "piano_arp", "acc4_mode": "thirds_swell",
        "hook": [(0, D5, 4), (4, U3, 4), (8, U9, 4), (12, R8, 4), (16, U5, 8)],
    },
    "hollywood_2": {
        "meter": "4/4", "tempo": 142, "swing": 0.24, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Trinity Perc.Kit", "Ac. Jazz Bass", "Live Piano", "Big Band Brass 1", "ConcertStrings 1", "Trpts & Trombs", "Xylophone"],
        "drum_mode": "jazz_swing", "bass_mode": "walking_jazz", "acc1_mode": "stride_piano",
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 2), (8, U6, 4), (12, U8, 4)],
        "cadence": "jazz_ii_V",
    },
    # Elmer Bernstein ("The Magnificent Seven"): Heroic Syncopated Prairie Gallop + French Horns & Strings!
    "western_movie": {
        "meter": "4/4", "tempo": 134, "swing": 0.0,
        "tracks": ["Room Kit Amb", "Trinity Perc.Kit", "Class.Contrabs", "RealFolk Gtr DNC", "ConcertStrings 1", "French Section", "Dual Trumpets", "Movie Brass"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 12], "snares": [4, 12],
        "perc_steps": [(0, 47, 82), (6, 45, 78), (12, 47, 80)],
        "bass_pat": [(0, R, 3), (3, R, 3), (6, D5, 2), (8, R, 4), (12, B7, 4)],
        "acc1_steps": [(0, STRUM_DN, 2, 82), (2, STRUM_UP, 1, 74), (3, STRUM_DN, 2, 80), (6, STRUM_UP, 2, 78), (8, STRUM_DN, 4, 82), (12, STRUM_DN, 4, 80)],
        "hook": [(0, R8, 4), (4, U5, 6), (10, U3, 2), (12, U9, 2), (14, R8, 2), (16, B7, 6)],
        "cadence": "modal_bVII", "fill_type": "orchestral_timp",
    },
    # Carl Stalling / Raymond Scott ("Powerhouse" / Looney Tunes): Frantic Xylophone, Bassoon, Mute Trombone & Woodblocks!
    "cartoon_time": {
        "meter": "4/4", "tempo": 156, "swing": 0.12,
        "tracks": ["Jazz Kit 2 Amb", "SFX Kit 1", "Alp Tuba", "Xylophone", "Strings Quartet", "Mute Trumpet", "Bassoon", "Piccolo"],
        "drum_mode": "polka_2_4",
        "perc_steps": [(2, 76, 78), (6, 77, 78), (10, 56, 72), (14, 71, 70, V_4)],
        "bass_pat": [(0, R, 2), (2, B5, 2), (4, D5, 2), (6, LT, 2), (8, R, 2), (10, D3, 2), (12, D5, 2), (14, R8, 2)],
        "acc1_steps": [(i, [R8, U9, U3, B5, U5, U3, U9, B2][i % 8], 1, 82) for i in range(0, 16, 2)],
        "hook": [(0, U5, 1), (1, U6, 1), (2, U5, 1), (3, B5, 1), (4, U5, 2), (6, R8, 2)],
    },
    # Francis Lai / Michel Legrand ("Love Story" / "Umbrellas of Cherbourg"): Harpsichord/Piano + Solo Violin/Flute!
    "love_movie": {
        "meter": "4/4", "tempo": 88, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Class.Contrabs", "Concert Grand", "Harpsichord 1", "Movie Str.1 DNC", "Flute", "Violin Expr. DNC"],
        "drum_mode": "ballad_4_4", "kicks": [0, 8], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D5, 2), (8, R, 8)],
        "acc1_mode": "piano_arp",
        "hook": [(0, U3, 2), (2, R8, 2), (4, U3, 2), (6, R8, 2), (8, U3, 4), (12, U9, 4)],
        "cadence": "flamenco_bVI_V",
    },
    # Artie Shaw ("Begin the Beguine"): Soaring Solo Clarinet + Shimmering Big Band Beguine!
    "artie_s_theme": {
        "meter": "4/4", "tempo": 124, "swing": 0.12,
        "tracks": ["Brush Kit 2 Amb", "Latin Perc.Kit 1", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Glenn & Friends", "Mute Ensemble 1", "RealClarinet DN1"],
        "drum_mode": "bossa", "kicks": [0, 6, 8, 14],
        "bass_pat": [(0, R, 5), (6, D5, 2), (8, D5, 5), (14, R, 2)],
        "acc1_mode": "jazz_comp",
        "hook": [(0, R, 2), (2, D2, 2), (4, D3, 2), (6, D5, 2), (8, D6, 2), (10, R8, 2), (12, U3, 4)],
        "cadence": "jazz_ii_V",
    },
    "love_ballad": {
        "meter": "4/4", "tempo": 78, "swing": 0.0,
        "tracks": ["Studio Kit", "Standard PercKit", "Fretless Bass 2", "Bell Tine EP", "Concert Grand", "Full Strings", "Sweet FlugelHorn", "Soprano Sax DN1"],
        "drum_mode": "ballad_4_4", "kicks": [0, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 8), (8, L5, 6), (14, D3, 2)],
        "acc1_mode": "piano_arp",
        "hook": [(0, U5, 4), (4, U3, 4), (8, R8, 6), (14, U9, 2), (16, U3, 8)],
    },
    # Glenn Miller Army Air Force Band ("American Patrol" / "In the Mood")!
    "army_band": {
        "meter": "4/4", "tempo": 136, "swing": 0.26, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Jazz Gtr 1 DNC", "Glenn & Boys", "Trpts & Trombs", "Sax Ensemble"],
        "drum_mode": "jazz_swing", "kicks": [0, 4, 8, 12],
        "bass_mode": "walking_jazz", "acc1_mode": "boogie_comp",
        "hook": [(0, D3, 2), (2, D5, 2), (4, R8, 2), (6, D3, 2), (8, D5, 2), (10, R8, 2), (12, D6, 4)],
        "cadence": "jazz_ii_V", "fill_type": "jazz_triplet",
    },
    # CHRISTMAS WALTZ ("Silver Bells" / "Skaters' Waltz"): Sleigh Bells (GM 83!), Celesta, Tubular Bells, Warm Strings!
    "christmas_waltz": {
        "meter": "3/4", "tempo": 104, "swing": 0.08,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "Concert Grand", "Celesta", "ConcertStrings 1", "French Section", "Tubular Bell"],
        "drum_mode": "waltz_3_4",
        "perc_steps": [(0, 83, 82), (4, 83, 72), (8, 83, 72), (0, 81, 58, V_34)],
        "bass_pat": [(0, R, 6), (8, L5, 4)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": OPEN,
        "acc2_seq": [(0, R8, 2), (2, U3, 2), (4, U5, 2), (6, U8, 2), (8, U5, 2), (10, U3, 2)],
        "hook": [(0, U5, 4), (4, U3, 4), (8, R8, 4), (12, U9, 6), (18, R8, 6)],
        "cadence": "christmas_II_V",
    },
    # CHRISTMAS SWING ("Winter Wonderland" / "Sleigh Ride" / Michael Bublé Holiday Big Band + Jingle Bells!):
    "chrismas_swing": {
        "meter": "4/4", "tempo": 130, "swing": 0.28, "swing8": True,
        "tracks": ["Jazz Kit 1 Amb", "Standard PercKit", "Ac. Jazz Bass", "Jazz Piano", "Celesta", "Big Band Brass 1", "Real Strings 1", "Glockenspiel"],
        "drum_mode": "jazz_swing",
        "perc_steps": [(0, 83, 84), (4, 83, 78), (8, 83, 84), (12, 83, 78), (14, 83, 66)],
        "bass_mode": "walking_jazz", "acc1_mode": "jazz_comp",
        "acc2_seq": [(2, HIGH_STAB, 2), (10, HIGH_STAB, 2)],
        "hook": [(0, U5, 2), (2, U5, 2), (4, U5, 4), (8, U5, 2), (10, U5, 2), (12, U5, 4), (16, U5, 2), (18, U8, 2), (20, U3, 2), (22, U9, 2), (24, R8, 6)],
        "cadence": "christmas_II_V", "fill_type": "jazz_triplet",
    },
    # Broadway Showstopper ("Cabaret" / "New York, New York") Theatre Swing!
    "theatre_swing": {
        "meter": "4/4", "tempo": 122, "swing": 0.26, "swing8": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "Ac. Jazz Bass", "Live Piano", "Banjo", "Trpts & Brass", "Sax Ensemble", "Jazz Trb. DN1"],
        "drum_mode": "jazz_swing", "bass_mode": "two_feel",
        "acc1_steps": [(0, OPEN, 3, 82), (4, CLOSE, 3, 80), (8, OPEN, 3, 82), (12, HIGH_STAB, 3, 82)],
        "hook": [(0, D5, 2), (2, D6, 2), (4, D5, 4), (8, U3, 2), (10, U9, 2), (12, R8, 4)],
        "cadence": "jazz_ii_V",
    },
    # "Seventy-Six Trombones" / Broadway Parade Theatre March!
    "theatre_march": {
        "meter": "6/8", "tempo": 122, "swing": 0.0,
        "tracks": ["Standard Kit Amb", "Trinity Perc.Kit", "Tuba Gold", "Bright Piano", "OrchestraTutti 1", "HardTrombone DN1", "Trpts & Trombs", "Piccolo"],
        "drum_mode": "ballad_6_8", "kicks": [0, 6],
        "perc_steps": [(0, 38, 80), (2, 38, 62), (4, 38, 68), (6, 38, 82), (10, 38, 72), (6, 55, 74, V_4)],
        "bass_pat": [(0, R, 5), (6, L5, 5)],
        "acc1_steps": [(0, CLOSE, 2, 82), (4, CLOSE, 2, 76), (6, HIGH_STAB, 2, 84), (10, CLOSE, 2, 76)],
        "hook": [(0, R8, 4), (4, D5, 2), (6, U3, 4), (10, R8, 2), (12, U5, 6)],
        "cadence": "march_V_I",
    },

    # =========================================================================
    # 11. FUNK & BLUES (32 Styles)
    # =========================================================================
    # THE BLUES BROTHERS ("Everybody Needs Somebody to Love"): Driving 8th Bass, Rapid Stax Horn Punches, B3, Cropper Tele!
    "everybody_bros": {
        "meter": "4/4", "tempo": 168, "swing": 0.0,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "Vintage P. Pick", "Single Coil Pro", "BX3 Rock 1", "Tight Brass 1", "Baritone Sax DN1", "Rock Piano"],
        "drum_mode": "pop_8", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(4, 54, 78), (12, 54, 78)],
        "bass_mode": "root_8",
        "acc1_steps": [(0, CLOSE, 2, 84), (3, HIGH_STAB, 2, 86), (6, CLOSE, 2, 82), (8, CLOSE, 2, 84), (12, HIGH_STAB, 2, 86)],
        "acc4_steps": [(0, HIGH_STAB, 1), (2, HIGH_STAB, 1), (4, THIRDS, 2), (12, HIGH_STAB, 2)],
        "hook": [(0, R8, 1), (2, R8, 1), (4, U3, 2), (6, U5, 2), (8, U6, 2), (10, U5, 2), (12, U3, 4)],
        "cadence": "blues_V_IV",
    },
    # Sam & Dave / Blues Brothers ("Soul Man"): Iconic Parallel-6th/3rd Guitar & Horn Riff!
    "soul_bros": {
        "meter": "4/4", "tempo": 116, "swing": 0.06,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "Vintage P. Bass", "Single Coil Pro", "Wurly Amp", "Tight Brass 2", "Tenor Growl DN1", "BX3 Gospel"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, R, 1), (6, B7, 2), (8, R, 2), (10, D5, 2), (14, B7, 2)],
        "acc1_steps": [(0, THIRDS, 2, 86), (3, THIRDS, 2, 84), (6, HIGH_STAB, 2, 88), (12, CHUCK, 2, 80)],
        "hook": [(0, THIRDS, 2), (3, THIRDS, 2), (6, HIGH_STAB, 4), (14, B7, 2), (16, R8, 4)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    # Chicago Electric Shuffle Blues (Muddy Waters / B.B. King / Buddy Guy)
    "blues": {
        "meter": "4/4", "tempo": 108, "swing": 0.30, "swing8": True,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Finger Bass DN1", "Clean Jazz 1", "Rock Piano", "Jimmy Organ", "Harmonica 1 DN1", "Crunch Gtr DNC"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_mode": "boogie_8", "acc1_mode": "boogie_comp",
        "hook": [(0, B3, 1), (1, D3, 3), (4, D5, 2), (6, R8, 2), (8, B7, 2), (10, B5, 1), (11, D5, 3)],
        "cadence": "blues_V_IV",
    },
    # Otis Redding / Aretha Classic Memphis 60s Soul!
    "soul": {
        "meter": "4/4", "tempo": 112, "swing": 0.08,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Wurly Amp", "Strat N Cln DNC", "Gospel Organ 1", "Brass & Sax", "Tenor Sax DN1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "perc_steps": [(4, 54, 72), (12, 54, 74)],
        "bass_mode": "motown_soul",
        "acc1_steps": [(4, CLOSE, 2, 80), (12, CLOSE, 2, 80)],
        "acc4_steps": [(6, THIRDS, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, R8, 2), (3, U3, 3), (6, D5, 2), (8, D6, 4)],
        "cadence": "blues_V_IV",
    },
    # STEVIE WONDER ("Superstition"): Iconic Syncopated 16th-Note Clavinet Pentatonic Riff + Drum Pickup + Moog Bass + Horns!
    "talkin_funk": {
        "meter": "4/4", "tempo": 101, "swing": 0.16,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "Synth Bass Warm", "Classic Clav DNC", "Clav Wah", "Tight Brass 1", "Tenor Sax DN1", "Jazz Trumpet DN1"],
        "drum_mode": "funk_16", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (3, B3, 1), (4, R, 2), (6, B7, 2), (8, R, 2), (10, D5, 2), (12, B7, 2), (14, R, 2)],
        "acc1_steps": [(0, R, 1, 88), (2, R8, 1, 82), (3, B7, 1, 84), (4, R8, 2, 86), (7, D5, 1, 80), (8, B5, 1, 78), (9, D5, 1, 82), (10, B3, 2, 84), (12, R, 2, 88), (14, B7, 2, 80)],
        "acc4_steps": [(6, HIGH_STAB, 2), (14, THIRDS, 2)],
        "hook": [(0, R8, 2), (3, UB7, 1), (4, R8, 2), (6, U3, 2), (8, R8, 4)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    # DONALD FAGEN / STEELY DAN ("I.G.Y." / "Peg"): Ultra-Crisp Bernard Purdie Ghost Shuffle + Dyno Rhodes + Muted Strat + Horns!
    "donald_mood": {
        "meter": "4/4", "tempo": 104, "swing": 0.22,
        "tracks": ["Studio Kit", "Standard PercKit", "JB Finger BsDN1", "Tine EP Dyno", "Strat N Cln Mute", "Tight Brass 2", "PopAltoSax DN1", "Harmonica 2 DN1"],
        "drum_mode": "funk_16", "kicks": [0, 6, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (3, D5, 1), (6, D6, 2), (8, B7, 2), (10, D5, 3), (14, R, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 3, 80), (3, JAZZ_SHELL, 2, 76), (6, QUARTAL, 3, 78), (11, JAZZ_SHELL, 3, 76)],
        "acc2_mode": "funk_chuck",
        "hook": [(2, U9, 2), (4, U3, 2), (6, U5, 4), (18, U6, 2), (20, U5, 4)],
        "cadence": "jazz_ii_V", "fill_type": "funk_sync",
    },
    # Tower of Power ("What Is Hip?") / Earth, Wind & Fire: 16-Beat Capital Soul with Relentless 16th Finger Bass!
    "16beat_soul": {
        "meter": "4/4", "tempo": 108, "swing": 0.08,
        "tracks": ["Funk Kit 1 Amb", "Latin Perc.Kit 1", "JB Finger BsDN2", "Strat N Cln Mute", "BX3 Jazz Pc.", "Tight Brass 1", "Baritone Sax Pro", "TrumpetShake Y+"],
        "drum_mode": "funk_16", "kicks": [0, 3, 6, 10, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 1), (1, R, 1), (2, B3, 1), (3, D3, 1), (4, D5, 2), (6, D6, 1), (7, B7, 1), (8, R8, 2), (10, B7, 2), (12, D5, 2), (14, D3, 2)],
        "acc1_mode": "funk_chuck",
        "acc4_steps": [(0, HIGH_STAB, 1), (3, HIGH_STAB, 2), (9, THIRDS, 2), (14, HIGH_STAB, 2)],
        "hook": [(0, R8, 1), (3, U3, 2), (6, U5, 2), (9, UB7, 2), (12, R8, 2)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    # JAMES BROWN ("Get Up / Soul Power / Papa's Got a Brand New Bag"): Heavy ON THE ONE + `e-and` Chank Guitar + Maceo Sax!
    "soul_power": {
        "meter": "4/4", "tempo": 112, "swing": 0.14,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "Finger Bass DN1", "Single Coil Pro", "Jimmy Organ", "Tight Brass 1", "Jazz Trb. DN1", "PopAltoSax DN1"],
        "drum_mode": "funk_16", "kicks": [0, 7, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (7, D5, 1), (10, B7, 2), (12, D5, 2), (14, R, 2)],
        "acc1_steps": [(4, HIGH_STAB, 1, 90), (6, CHUCK, 1, 78), (9, HIGH_STAB, 2, 88), (12, HIGH_STAB, 1, 88)],
        "hook": [(0, R8, 3), (6, B3, 1), (7, D3, 2), (10, D5, 2), (14, B7, 2)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    # LEVEL 42 ("Lessons in Love" / "Something About You"): Mark King 16th-Note Machine-Gun Octave Slap Bass + Synth Brass!
    "level_funk": {
        "meter": "4/4", "tempo": 106, "swing": 0.06,
        "tracks": ["Gate Kit Amb", "Standard PercKit", "JB Slap Bass", "Bell Tine EP", "Strat N Cln Mute", "Analog Pad 1", "Fat Brass", "Rich Lead"],
        "drum_mode": "funk_16", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "bass_mode": "slap_machine",
        "acc1_steps": [(0, OPEN, 3, 78), (6, HIGH_STAB, 3, 80), (12, CLOSE, 4, 76)],
        "acc2_mode": "funk_chuck",
        "hook": [(0, U5, 2), (3, U3, 2), (6, U9, 2), (8, R8, 4), (14, D5, 2)],
        "fill_type": "funk_sync",
    },
    # Eric Clapton ("Before You Accuse Me" Unplugged) Acoustic Blues Shuffle!
    "acoustic_shuffle": {
        "meter": "4/4", "tempo": 110, "swing": 0.28, "swing8": True,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "ClassicSteel DNC", "Saloon Piano", "Harmonica 1 DN1", "RealFolk Gtr DNC", "Concert Gtr Pro"],
        "drum_mode": "pop_8", "snare_note": 37, "kicks": [0, 8], "snares": [4, 12],
        "bass_mode": "boogie_8", "acc1_mode": "boogie_comp",
        "hook": [(0, B3, 1), (1, D3, 3), (4, D5, 2), (6, D3, 2), (8, R, 4)],
        "cadence": "blues_V_IV",
    },
    # 6/8 "Amazing Grace" Soulful Gospel Organ, Piano & Choir!
    "grace_gospel": {
        "meter": "6/8", "tempo": 66, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "JB Finger BsDN1", "BX3 Gospel", "Concert Grand", "Choir Aahs GM", "Tight Brass 1", "Gospel Organ 1"],
        "drum_mode": "ballad_6_8", "kicks": [0, 4, 10],
        "perc_steps": [(6, 54, 76)],
        "bass_pat": [(0, R, 4), (4, D3, 2), (6, D5, 4), (10, D6, 2)],
        "acc1_steps": [(0, OPEN, 4, 82), (4, CLOSE, 2, 76), (6, OPEN, 4, 84), (10, CLOSE, 2, 78)],
        "hook": [(0, D5, 4), (4, R8, 2), (6, U3, 2), (8, R8, 4), (12, U3, 6), (18, U9, 6)],
        "cadence": "pop_IV_V",
    },
    # Sister Act / Kirk Franklin Upbeat Church Praise Gospel!
    "gospel": {
        "meter": "4/4", "tempo": 118, "swing": 0.16,
        "tracks": ["Studio Kit", "Standard PercKit", "5StringsBass RX", "Bright Piano", "BX3 Gospel", "Choir Aahs GM", "Tight Brass 2", "Strat N Cln DNC"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8, 14], "snares": [4, 12],
        "perc_steps": [(2, 54, 62), (4, 39, 86), (6, 54, 68), (10, 54, 62), (12, 39, 86), (14, 54, 70)],
        "bass_pat": [(0, R, 3), (3, D2, 1), (4, D3, 2), (6, D4, 2), (8, D5, 3), (12, D6, 2), (14, B7, 2)],
        "acc1_steps": [(0, OPEN, 3, 84), (3, HIGH_STAB, 3, 82), (8, OPEN, 4, 84), (12, CLOSE, 2, 80), (14, HIGH_STAB, 2, 82)],
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 4), (12, U6, 2), (14, U5, 2)],
    },
    "gospel_swing": {
        "meter": "4/4", "tempo": 112, "swing": 0.26, "swing8": True,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Finger Bass DN1", "Gospel Organ 1", "Live Piano", "Choir Aahs GM", "Strat N Cln DNC", "Tenor Growl DN1"],
        "drum_mode": "jazz_swing", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(4, 39, 82), (12, 39, 82)],
        "bass_mode": "walking_jazz", "acc1_mode": "boogie_comp",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U6, 4), (8, U5, 4)],
        "cadence": "blues_V_IV",
    },
    "gospel_shuffle": {
        "meter": "12/8", "tempo": 112, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "JB Finger BsDN1", "Live Piano", "BX3 Gospel", "Choir Aahs GM", "Brass & Sax", "Gospel Organ 1"],
        "drum_mode": "blues_12_8", "kicks": [0, 5, 6, 11], "snares": [3, 9],
        "perc_steps": [(3, 54, 78), (9, 54, 78)],
        "bass_pat": [(0, R, 2), (2, D2, 1), (3, D3, 2), (5, D4, 1), (6, D5, 2), (8, D6, 1), (9, B7, 2), (11, R8, 1)],
        "acc1_steps": [(0, OPEN, 2, 84), (2, CLOSE, 1, 78), (5, HIGH_STAB, 2, 82), (9, CLOSE, 3, 80)],
        "hook": [(0, R8, 2), (2, U3, 1), (3, U5, 3), (6, U6, 2), (8, U5, 1), (9, U3, 3)],
    },
    "modern_gospel_1": {
        "meter": "4/4", "tempo": 110, "swing": 0.14,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "5StringsBass RX", "R&B E. Piano", "BX3 Gospel", "Choir Aahs GM", "Tight Brass 1", "Fat Synth"],
        "drum_mode": "funk_16", "kicks": [0, 3, 6, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (3, D3, 2), (6, D5, 2), (9, B5, 1), (10, D5, 2), (14, B7, 2)],
        "acc1_mode": "jazz_comp", "acc3_mode": "organ_bubble",
        "hook": [(0, U5, 2), (3, U3, 2), (6, R8, 2), (9, B7, 1), (10, R8, 4)],
    },
    "modern_gospel_2": {
        "meter": "4/4", "tempo": 96, "swing": 0.18,
        "tracks": ["HipHop Kit 1", "Standard PercKit", "Dark R&B Bass1", "Concert Grand", "Gospel Organ 1", "Atmoschoir Pad", "Strat N Cln DNC", "Bell Tine EP"],
        "drum_mode": "pop_16", "kicks": [0, 7, 8, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 5), (7, D3, 1), (8, D5, 4), (12, D6, 2), (14, B7, 2)],
        "acc1_steps": [(0, JAZZ_SHELL, 4, 80), (6, OPEN, 2, 78), (8, JAZZ_SHELL, 4, 80), (14, HIGH_STAB, 2, 76)],
        "hook": [(0, U3, 3), (3, U5, 3), (6, U6, 2), (8, U5, 6)],
    },
    # Stevie Wonder ("Love's in Need of Love Today" / Neo-Soul Warm Groove)
    "love_4_all": {
        "meter": "4/4", "tempo": 102, "swing": 0.16,
        "tracks": ["Cool Kit Amb", "Latin Perc.Kit 2", "Fretless Bass 2", "Suit Case88 EP1", "Nylon GuitarDNC", "Warm Strings", "Sweet FlugelHorn", "Harmonica 1 DN1"],
        "drum_mode": "pop_16", "snare_note": 37, "kicks": [0, 6, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 5), (6, D5, 2), (8, R, 4), (12, D6, 2), (14, D5, 2)],
        "acc1_mode": "jazz_comp",
        "hook": [(0, D5, 2), (2, R8, 2), (4, U9, 4), (8, U3, 6)],
        "cadence": "jazz_ii_V",
    },
    # Sly & the Family Stone ("Dance to the Music"): Fuzz/Synth Bass, Organ, Horns & Scat!
    "dance_to_rhythm": {
        "meter": "4/4", "tempo": 124, "swing": 0.10,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "JB Slap Bass", "60’s Organ", "Strat N Cln Mute", "Tight Brass 1", "Baritone Sax DN1", "Scat Voices DNC"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "bass_pat": [(0, R, 2), (2, R, 2), (4, D3, 2), (6, D5, 2), (8, R, 2), (10, B7, 2), (12, D5, 2), (14, R, 2)],
        "acc1_mode": "oom_pah_off", "acc2_mode": "funk_chuck",
        "hook": [(0, R8, 2), (4, R8, 2), (6, B7, 2), (8, R8, 4)],
        "cadence": "blues_V_IV",
    },
    # The Supremes ("You Can't Hurry Love"): Snare + Tambourine on ALL FOUR BEATS (0, 4, 8, 12), Driving Bass, Vibraphone!
    "motown_beat_1": {
        "meter": "4/4", "tempo": 184, "swing": 0.16, "swing8": True,
        "tracks": ["VintageKit 1 Amb", "Standard PercKit", "Vintage P. Flat", "Bright Piano", "Baritone Sax DN1", "Vibraphone 1", "Strings&Orch.V.", "Tight Brass 1"],
        "drum_mode": "motown_4", "kicks": [0, 4, 8, 12], "snares": [0, 4, 8, 12],
        "perc_steps": [(0, 54, 80), (4, 54, 82), (8, 54, 80), (12, 54, 82)],
        "bass_pat": [(0, R, 4), (4, R, 2), (6, D5, 4), (10, D6, 2), (12, R, 4)],
        "acc1_steps": [(4, CLOSE, 2, 82), (12, CLOSE, 2, 82)],
        "hook": [(0, D5, 2), (2, D6, 2), (4, R8, 4), (12, U3, 2), (14, R8, 2)],
    },
    # The Temptations ("My Girl" / Four Tops): Syncopated Bass Riff + Guitar Pentatonic Climb + Horn Answers!
    "motown_beat_2": {
        "meter": "4/4", "tempo": 108, "swing": 0.10,
        "tracks": ["VintageKit 2 Amb", "Standard PercKit", "Vintage P. Flat", "Single Coil", "Classic Piano", "Real Strings 1", "Tight Brass 2", "Tenor Sax DN1"],
        "drum_mode": "pop_8", "kicks": [0, 6, 8], "snares": [4, 12],
        "perc_steps": [(4, 54, 76), (12, 54, 76)],
        "bass_pat": [(0, R, 3), (6, R, 2), (8, D5, 4), (14, D3, 2)],
        "acc1_steps": [(4, CHUCK, 2, 82), (12, CHUCK, 2, 82)],
        "hook": [(0, R, 2), (2, D2, 2), (4, D3, 2), (6, D5, 2), (8, D6, 2), (10, R8, 6)],
    },
    # Grover Washington Jr. / Bill Withers ("Just the Two of Us"): Tight Rimshot + Fender Rhodes + Slap/Finger Bass + Conga!
    "rimshot_mood": {
        "meter": "4/4", "tempo": 96, "swing": 0.16,
        "tracks": ["Studio Kit", "Latin Perc.Kit 2", "JB Finger BsDN1", "Suit Case88 EP1", "Strat N Cln Mute", "Warm Strings", "Soprano Sax DN1", "Steel Drums GM"],
        "drum_mode": "funk_16", "snare_note": 37, "kicks": [0, 6, 10], "snares": [4, 12],
        "perc_steps": [(3, 63, 64), (11, 63, 66), (14, 64, 70)],
        "bass_pat": [(0, R, 3), (3, D5, 1), (6, R8, 2), (8, R, 3), (12, B7, 2), (14, D5, 2)],
        "acc1_mode": "jazz_comp", "acc2_mode": "funk_chuck",
        "hook": [(0, D5, 2), (2, D6, 2), (4, R8, 2), (6, U9, 2), (8, U3, 4)],
        "cadence": "flamenco_bVI_V",
    },
    "groovy_funk": {
        "meter": "4/4", "tempo": 109, "swing": 0.14,
        "tracks": ["Groove Kit", "Standard PercKit", "FunkSlapBass RX", "Classic Clav DNC", "Strat N Cln Mute", "Tight Brass 1", "Wurly Amp", "Synth Lead"],
        "drum_mode": "funk_16", "bass_mode": "funk_16", "acc1_mode": "funk_chuck",
        "hook": [(0, R8, 1), (2, B7, 1), (3, R8, 2), (6, B3, 1), (7, D3, 2), (12, D5, 2)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    "easy_funk": {
        "meter": "4/4", "tempo": 104, "swing": 0.14,
        "tracks": ["Cool Kit Amb", "Standard PercKit", "Finger Bass DN1", "Tine EP Phaser", "Single Coil", "Warm Pad", "Sweet FlugelHorn", "Jazz Flute Expr."],
        "drum_mode": "pop_16", "kicks": [0, 7, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 4), (7, D3, 1), (8, D5, 4), (14, B7, 2)],
        "acc1_mode": "jazz_comp", "acc2_mode": "funk_chuck",
        "hook": [(4, U3, 3), (8, R8, 4), (20, U5, 3), (24, U3, 4)],
    },
    # Al Green ("Let's Stay Together") / Commodores Smooth Soul Ballad
    "soul_ballad": {
        "meter": "4/4", "tempo": 84, "swing": 0.12,
        "tracks": ["VintageKit 1 Amb", "Latin Perc.Kit 2", "Vintage P. Flat", "Suit Case88 EP1", "Clean Jazz 1", "Real Strings 1", "Soft Horns 1", "Jimmy Organ"],
        "drum_mode": "ballad_4_4", "kicks": [0, 6, 10], "snares": [4, 12],
        "perc_steps": [(6, 63, 62), (14, 64, 64)],
        "bass_pat": [(0, R, 5), (6, D3, 2), (8, D5, 5), (14, D6, 2)],
        "acc1_mode": "jazz_comp", "acc3_mode": "organ_bubble",
        "hook": [(0, U3, 4), (4, U5, 2), (6, U6, 4), (10, U5, 6)],
    },
    "cool_funk": {
        "meter": "4/4", "tempo": 105, "swing": 0.18,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "Dark Bs&Slap DN1", "Wurly Amp/Comp", "Strat N Cln Mute", "Jazz Organ", "Mute Trumpet", "Jazz Sax DN1"],
        "drum_mode": "funk_16", "kicks": [0, 3, 8, 11], "snares": [4, 12],
        "bass_pat": [(0, R, 2), (3, R, 2), (6, B7, 2), (8, R, 2), (11, D5, 2), (14, B3, 2)],
        "acc1_mode": "funk_chuck",
        "hook": [(0, U3, 2), (3, R8, 2), (8, B7, 2), (11, D5, 3)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    # Kool & The Gang / Parliament ("Jungle Boogie" / "Flash Light") Classic 70s P-Funk!
    "classic_funk": {
        "meter": "4/4", "tempo": 108, "swing": 0.12,
        "tracks": ["Funk Kit 1 Amb", "Standard PercKit", "Autofilter Bass", "Clav Wah", "Strat N Cln Mute", "Tight Brass 1", "Tenor Growl DN1", "Old Portamento"],
        "drum_mode": "funk_16", "kicks": [0, 6, 8, 10], "snares": [4, 12],
        "perc_steps": [(4, 39, 82), (12, 39, 82)],
        "bass_mode": "funk_16", "acc1_mode": "funk_chuck",
        "hook": [(0, R8, 3), (3, B7, 1), (4, D5, 2), (6, B3, 2), (8, R, 4)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    # Doobie Brothers ("Long Train Runnin'"): Percussive 16th Acoustic/Electric Strum + Harmonica + Congas!
    "70_s_beat_groove": {
        "meter": "4/4", "tempo": 116, "swing": 0.08,
        "tracks": ["VintageKit 2 Amb", "Latin Perc.Kit 1", "Finger E.Bass 1", "Strat N Cln DNC", "Wurly Logic", "BX3 Rock 1", "Tight Brass 2", "Harmonica 1 DN1"],
        "drum_mode": "funk_16", "kicks": [0, 4, 8, 12], "snares": [4, 12],
        "perc_steps": [(2, 63, 66), (6, 64, 70), (10, 63, 66), (14, 64, 70)],
        "bass_pat": [(0, R, 3), (3, R, 1), (6, B7, 2), (8, R, 4), (12, D5, 2), (14, B7, 2)],
        "acc1_steps": [(0, STRUM_DN, 2, 84), (2, CHUCK, 1, 78), (3, STRUM_UP, 1, 82), (4, CHUCK, 1, 80), (6, STRUM_UP, 2, 82), (8, STRUM_DN, 2, 84), (11, STRUM_UP, 1, 80), (12, CHUCK, 2, 80), (14, STRUM_UP, 2, 82)],
        "hook": [(0, B7, 2), (2, R8, 2), (4, B3, 2), (6, R8, 4)],
        "cadence": "blues_V_IV",
    },
    # Luther Vandross / Janet / Jam & Lewis Smooth Funk R&B!
    "funk_r_b": {
        "meter": "4/4", "tempo": 106, "swing": 0.16,
        "tracks": ["HipHop Kit 2", "Standard PercKit", "Phunk Synth Bass", "Bell Tine EP", "Strat N Cln Mute", "Warm Pad", "Tight Brass 2", "PopAltoSax DN1"],
        "drum_mode": "funk_16", "kicks": [0, 7, 10, 14], "snares": [4, 12],
        "bass_pat": [(0, R, 3), (6, R8, 1), (7, R, 3), (10, D5, 2), (14, B7, 2)],
        "acc1_mode": "jazz_comp", "acc2_mode": "funk_chuck",
        "hook": [(0, U3, 2), (3, U5, 3), (8, U9, 2), (10, R8, 4)],
    },
    # Herbie Hancock ("Chameleon" / "Rockit") / Zapp Electro-Funk!
    "elektrik_funk": {
        "meter": "4/4", "tempo": 104, "swing": 0.12,
        "tracks": ["Electro Kit 1", "Synth Kit 1", "Monofilter Bass", "Classic Clav DNC", "Tine EP Amp/Pha", "Techno Stab DNC", "Fat Synth", "Fast Glide Saw"],
        "drum_mode": "funk_16", "kicks": [0, 6, 8], "snares": [4, 12],
        "bass_pat": [(0, LT, 1), (1, R, 2), (4, B2, 1), (5, D2, 2), (8, D5, 2), (11, B7, 2), (14, R8, 2)],
        "acc1_mode": "funk_chuck",
        "hook": [(0, R8, 2), (3, UB7, 2), (6, U3, 3), (12, D5, 4)],
        "cadence": "blues_V_IV", "fill_type": "funk_sync",
    },
    # Pointer Sisters / Sister Sledge ("We Are Family" / "He's So Shy") Funky Sisters!
    "funky_sisters": {
        "meter": "4/4", "tempo": 116, "swing": 0.08,
        "tracks": ["Pop Std. Kit 1", "Latin Perc.Kit 1", "JB Slap Bass", "Suit Case88 EP1", "Strat N Cln DNC", "Real Strings 1", "Tight Brass 1", "Bright Piano"],
        "drum_mode": "disco",
        "bass_pat": [(0, R, 3), (3, D3, 1), (4, D5, 2), (6, D6, 2), (8, R8, 3), (12, D6, 2), (14, D5, 2)],
        "acc1_mode": "house_piano", "acc2_mode": "funk_chuck",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U6, 2), (6, U5, 4), (16, U3, 2), (18, R8, 4)],
    },
    # Allman Brothers / Elmore James Bottleneck Slide Blues!
    "slide_blues": {
        "meter": "12/8", "tempo": 98, "swing": 0.0,
        "tracks": ["Rock Kit 1 Amb", "Standard PercKit", "Vintage P. Bass", "Crunch Gtr DNC", "Honky-Tonk", "BX3 Rock 1", "Harmonica 1 DN1", "Pedal Steel"],
        "drum_mode": "blues_12_8", "kicks": [0, 5, 6], "snares": [3, 9],
        "bass_pat": [(0, R, 2), (2, R, 1), (3, D3, 2), (5, D5, 1), (6, D6, 2), (8, B7, 1), (9, D6, 2), (11, D5, 1)],
        "acc1_steps": [(0, POWER5, 2, 84), (2, FOURTHS, 1, 80), (3, POWER5, 2, 84), (6, POWER5, 2, 84), (9, FOURTHS, 3, 82)],
        "hook": [(0, B3, 1), (1, D3, 2), (3, D5, 3), (6, R8, 2), (8, B7, 1), (9, D5, 3)],
        "cadence": "blues_V_IV",
    },
    # Sade / Erykah Badu Neo-Soul Cool Vocal Groove!
    "cool_vocal": {
        "meter": "4/4", "tempo": 94, "swing": 0.20,
        "tracks": ["Lounge Kit Amb", "Latin Perc.Kit 2", "Dark R&B Bass2", "Rhodes" if False else "Suit Case88 EP1", "Clean Jazz 1", "Scat Voices DNC", "Mute Trumpet", "Tenor Sax 1 DNC"],
        "drum_mode": "pop_16", "snare_note": 37, "kicks": [0, 7, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 5), (7, D5, 1), (8, R, 4), (14, B7, 2)],
        "acc1_mode": "jazz_comp",
        "hook": [(2, U9, 3), (6, U3, 3), (10, D5, 6)],
        "cadence": "jazz_ii_V",
    },

    # =========================================================================
    # 12. WORLD (36 Styles — Authentic Regional Rhythms & Instruments!)
    # =========================================================================
    # ASTOR PIAZZOLLA ("Libertango"): 3+3+2 Nuevo Tango Tresillo (`0, 6, 12`) with Bandoneon, Piano & Strings!
    "libertad_tango": {
        "meter": "4/4", "tempo": 136, "swing": 0.0, "tango_332": True,
        "tracks": ["Jazz Kit 2 Amb", "Standard PercKit", "Real Ac. Bass 1", "Bandoneon DNC", "Concert Grand", "ConcertStrings 1", "Real Violin DNC", "Bandoneon Sync"],
        "drum_mode": "tango", "bass_mode": "tango_332", "acc1_mode": "tango_332",
        "acc2_seq": [(0, R, 2), (2, D2, 2), (4, D3, 2), (6, R, 2), (8, D2, 2), (10, D3, 2), (12, D5, 2), (14, D3, 2)],
        "hook": [(0, U3, 6), (6, U9, 6), (12, R8, 4), (16, B7, 6), (22, S5, 6), (28, D5, 4)],
        "cadence": "tango_V_I",
    },
    # Andalusian Spanish Dance (Castanets, Flamenco Guitar, Trumpet!)
    "spanish_dance": {
        "meter": "4/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 1", "Acoustic Bass 1", "Concert Gtr DNC", "Real Nylon Gtr", "Strings&Orch.V.", "Concert Trumpet", "Accordion"],
        "drum_mode": "flamenco",
        "perc_steps": [(0, 85, 76), (3, 85, 70), (6, 85, 76), (10, 39, 78), (12, 85, 76), (14, 39, 78)],
        "bass_pat": [(0, R, 4), (6, D5, 2), (8, S5, 4), (12, D5, 4)],
        "acc1_mode": "pop_strum",
        "hook": [(0, U5, 3), (3, S5, 1), (4, U5, 2), (6, U3, 2), (8, U9, 2), (10, B2, 2), (12, R8, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "flamenco_rasg",
    },
    # Hawaiian Slack-Key, Ukulele & Pedal Steel Island Sway ("Aloha Oe" / "Blue Hawaii")!
    "hawaiian": {
        "meter": "4/4", "tempo": 98, "swing": 0.14, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 2", "Real Ac. Bass 1", "Real Ukulele", "Pedal Steel", "Nylon GuitarDNC", "Marimba", "Whistle Sine"],
        "drum_mode": "jazz_brush", "kicks": [0, 8],
        "bass_pat": [(0, R, 6), (6, D5, 2), (8, D5, 6), (14, R, 2)],
        "acc1_steps": [(0, STRUM_DN, 2, 74), (2, STRUM_UP, 2, 70), (4, STRUM_DN, 2, 76), (6, STRUM_UP, 2, 70), (8, STRUM_DN, 2, 74), (10, STRUM_UP, 2, 70), (12, STRUM_DN, 2, 76), (14, STRUM_UP, 2, 70)],
        "acc2_seq": [(0, THIRDS, 8), (8, THIRDS, 8)],
        "hook": [(0, D5, 2), (2, D6, 2), (4, U3, 4), (8, U5, 6), (14, U3, 2), (16, R8, 8)],
        "cadence": "country_IV_V",
    },
    # Russian Kozachok / Kalinka ("Casatchock"): Energetic 2/4 Balalaika/Mandolin Tremolo + Accordion + Tuba Oom-Pah!
    "casatchock": {
        "meter": "2/4", "tempo": 134, "swing": 0.0,
        "tracks": ["Standard Kit 1", "Standard PercKit", "Tuba Gold", "Accordion", "Mandolin Trem.", "Real Strings 1", "RealClarinet DN1", "Mandolin DNC"],
        "drum_mode": "polka_2_4",
        "perc_steps": [(2, 54, 78), (6, 54, 78)],
        "bass_pat": [(0, R, 2), (4, L5, 2)],
        "acc1_mode": "oom_pah_off",
        "acc2_seq": [(0, R8, 2), (2, U3, 2), (4, U5, 2), (6, U3, 2)],
        "hook": [(0, U5, 2), (2, U3, 1), (3, U9, 1), (4, R8, 2), (6, LT, 2), (8, R8, 2), (10, U3, 2), (12, U5, 4)],
        "cadence": "flamenco_bVI_V",
    },
    # Greek Tsifteteli / Rumba with Bouzouki & Doumbek!
    "greek_rumba": {
        "meter": "4/4", "tempo": 106, "swing": 0.0,
        "tracks": ["Turkish Kit", "Oriental PercKit", "Acoustic Bass 1", "Bouzouki", "Real Nylon Gtr", "Accordion", "Klarnet 1", "Mandolin Trem."],
        "drum_mode": "oriental_4_4", "kicks": [0, 6, 8, 12], "snares": [4, 10, 14],
        "bass_mode": "oriental_maq",
        "acc1_steps": [(0, THIRDS, 2, 82), (3, THIRDS, 2, 78), (6, THIRDS, 2, 82), (10, CLOSE, 2, 76), (12, THIRDS, 2, 80)],
        "acc2_mode": "pop_strum",
        "hook": [(0, U3, 2), (2, U9, 1), (3, U3, 1), (4, U5, 2), (6, U3, 2), (8, R8, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "oriental_darbuka",
    },
    # Greek Hasapiko ("Xasapiko"): Stately 4/4 / 2/4 Tavern Bouzouki in Harmonized Thirds!
    "xasapiko": {
        "meter": "4/4", "tempo": 102, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Oriental PercKit", "Real Ac. Bass 1", "Bouzouki", "ClassicSteel DNC", "Accordion", "Baglama" if False else "Ac. Baglama 1", "Klarnet 1"],
        "drum_mode": "polka_2_4",
        "perc_steps": [(0, 64, 80), (4, 62, 74), (8, 64, 80), (12, 62, 74)],
        "bass_pat": [(0, R, 3), (4, D5, 3), (8, R, 3), (12, L5, 2), (14, LT, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, THIRDS, 2), (2, THIRDS, 2), (4, HIGH_STAB, 4), (8, THIRDS, 2), (10, R8, 2), (12, D5, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "oriental_darbuka",
    },
    # Mikis Theodorakis ("Zorba's Dance" Sirtaki): Iconic Bouzouki Grace-Note Dance!
    "sirtaki": {
        "meter": "4/4", "tempo": 116, "swing": 0.0,
        "tracks": ["Standard Kit 1", "Oriental PercKit", "Acoustic Bass 1", "Bouzouki", "RealFolk Gtr DNC", "Accordion", "Mandolin Trem.", "Bouzouki"],
        "drum_mode": "polka_2_4",
        "perc_steps": [(2, 54, 72), (6, 54, 72), (10, 54, 72), (14, 54, 72)],
        "bass_pat": [(0, R, 3), (4, D5, 3), (8, R, 3), (12, D5, 3)],
        "acc1_steps": [(0, R, 2, 80), (2, CLOSE, 2, 78), (4, L5, 2, 78), (6, CLOSE, 2, 78), (8, R, 2, 80), (10, CLOSE, 2, 78), (12, L5, 2, 78), (14, CLOSE, 2, 78)],
        "hook": [(0, U3, 3), (3, U9, 1), (4, U3, 2), (6, U5, 2), (8, U3, 3), (11, R8, 1), (12, U9, 4)],
        "cadence": "country_IV_V", "fill_type": "oriental_darbuka",
    },
    # Kassav' French Antillean Zouk: Four-on-the-Floor Kick + `1 . . a 2 . + .` Caribbean Rim/Hat + Chorus Guitar + Brass!
    "zouk": {
        "meter": "4/4", "tempo": 108, "swing": 0.08,
        "tracks": ["Dance Kit", "Latin Perc.Kit 1", "JB Slap Bass", "Chorus Gtr Pro", "DX" if False else "FM Legend EP", "Tight Brass 1", "Warm Pad", "Lead" if False else "Dance Lead"],
        "drum_mode": "four_floor", "snares": [3, 6, 11, 14],
        "perc_steps": [(2, 70, 58), (6, 56, 68), (10, 70, 58), (14, 56, 68)],
        "bass_pat": [(0, R, 3), (3, D5, 2), (6, R8, 2), (8, R, 3), (11, D5, 2), (14, D3, 2)],
        "acc1_steps": [(0, R8, 1, 80), (2, U3, 1, 78), (3, U5, 2, 82), (6, U3, 2, 78), (10, R8, 2, 78), (14, U5, 2, 80)],
        "hook": [(0, THIRDS, 2), (3, HIGH_STAB, 3), (8, THIRDS, 2), (11, HIGH_STAB, 3)],
        "cadence": "latin_IV_V",
    },
    # Ranchera 3/4 Mexican Waltz ("Cielito Lindo" / Vicente Fernández): Guitarrón, Vihuela, Dual Trumpets & Violins!
    "mexican_waltz": {
        "meter": "3/4", "tempo": 138, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 2", "Acous. Bass Pro1", "Real Nylon Gtr", "Accordion", "ConcertStrings 1", "Dual Trumpets", "Trumpet Expr.1"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 5), (8, L5, 4)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": STRUM_DN, "acc4_mode": "Mariachi_tpts",
        "hook": [(0, U5, 4), (4, U3, 4), (8, U9, 4), (12, R8, 8), (20, U3, 4)],
        "cadence": "latin_IV_V",
    },
    # Los Tigres del Norte Mexican Norteño: Brisk 2/4 Polka Bajo Sexto + Diatonic Accordion in Thirds!
    "norteno": {
        "meter": "2/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Finger E.Bass 1", "Strum 12Str. DNC", "Accordion", "Alto Sax DN1", "Fisa 16,8’", "Acc.16,8,4’ Plus"],
        "drum_mode": "polka_2_4",
        "bass_pat": [(0, R, 3), (4, L5, 3)],
        "acc1_mode": "oom_pah_off",
        "acc2_seq": [(0, THIRDS, 2), (2, THIRDS, 1), (3, HIGH_STAB, 1), (4, THIRDS, 3)],
        "hook": [(0, THIRDS, 2), (2, HIGH_STAB, 2), (4, THIRDS, 2), (6, R8, 2)],
        "cadence": "country_IV_V",
    },
    # Banda Machos Quebradita ("Kebradita"): Fast Tecnobanda Cumbia-Polka Bounce + Brass & Tuba!
    "kebradita": {
        "meter": "2/4", "tempo": 144, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Latin Perc.Kit 1", "Tuba Gold", "Tight Brass 1", "Dual Trumpets", "RealClarinet DN1", "Fat Synth", "TrumpetShake Y+"],
        "drum_mode": "polka_2_4",
        "perc_steps": [(2, 56, 76), (6, 65, 78)],
        "bass_pat": [(0, R, 2), (3, D3, 1), (4, D5, 2), (6, R8, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, THIRDS, 1), (2, THIRDS, 1), (4, HIGH_STAB, 2), (6, THIRDS, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Javier Solís / Pedro Infante Romantic Bolero Ranchero!
    "bolero_ranchero": {
        "meter": "4/4", "tempo": 98, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Latin Perc.Kit 2", "Acous. Bass Pro1", "Real Nylon Gtr", "Concert Gtr DNC", "Real Strings 1", "Dual Trumpets", "Trumpet Expr.2"],
        "drum_mode": "bossa", "kicks": [0, 10], "snares": [4, 12],
        "bass_pat": [(0, R, 6), (6, D3, 2), (8, D5, 6), (14, L5, 2)],
        "acc1_steps": [(0, R, 2, 76), (2, STRUM_DN, 2, 74), (4, CHUCK, 2, 76), (6, STRUM_UP, 2, 74), (8, L5, 2, 76), (10, STRUM_DN, 2, 74), (12, CHUCK, 2, 76), (14, STRUM_UP, 2, 74)],
        "hook": [(0, THIRDS, 4), (4, HIGH_STAB, 2), (6, THIRDS, 6)],
        "cadence": "latin_IV_V",
    },
    "mariachi_waltz": {
        "meter": "3/4", "tempo": 144, "swing": 0.0,
        "tracks": ["Real Kit 1 Amb", "Latin Perc.Kit 2", "Acous. Bass Pro1", "RealFolk Gtr DNC", "Classic Harp", "Violin & Viola", "Dual Trumpets", "Trumpet Expr.1"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": STRUM_DN, "acc4_mode": "Mariachi_tpts",
        "hook": [(0, THIRDS, 4), (4, THIRDS, 2), (6, HIGH_STAB, 6)],
        "cadence": "latin_IV_V",
    },
    "mariachi_polka": {
        "meter": "2/4", "tempo": 128, "swing": 0.0,
        "tracks": ["Standard Kit 1", "Standard PercKit", "Acous. Bass Pro1", "RealFolk Gtr DNC", "Violin & Viola", "Classic Harp", "Dual Trumpets", "Concert Trumpet"],
        "drum_mode": "polka_2_4", "bass_pat": [(0, R, 3), (4, L5, 3)],
        "acc1_mode": "oom_pah_off", "acc4_mode": "Mariachi_tpts",
        "hook": [(0, R8, 1), (1, U9, 1), (2, U3, 2), (4, U5, 2), (6, U3, 2)],
        "cadence": "latin_IV_V",
    },
    # Mariachi Son Jalisciense ("El Son de la Negra"): Famous 6/8-vs-3/4 Sesquiáltera Alternating Bar Rhythm!
    "mariachi_son": {
        "meter": "6/8", "tempo": 132, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Acous. Bass Pro1", "Real Nylon Gtr", "Classic Harp", "Violin & Viola", "Dual Trumpets", "Trumpet Expr.1"],
        "drum_mode": "ballad_6_8", "kicks": [0, 6],
        # Bar 1 in 6/8 (0, 3, 6, 9), Bar 2 in 3/4 hemiola (12, 16, 20)!!
        "bass_pat": [(0, R, 3), (3, D5, 3), (6, R8, 3), (9, D5, 3), (12, R, 4), (16, D3, 4), (20, D5, 4)],
        "acc1_steps": [(0, STRUM_DN, 2, 84), (2, STRUM_UP, 1, 76), (3, STRUM_DN, 2, 82), (6, STRUM_DN, 2, 84), (8, STRUM_UP, 2, 78), (10, STRUM_DN, 2, 82)],
        "hook": [(0, THIRDS, 3), (3, THIRDS, 3), (6, HIGH_STAB, 6), (12, THIRDS, 4), (16, THIRDS, 4), (20, HIGH_STAB, 4)],
        "cadence": "latin_IV_V",
    },
    "mariachi_cumbia": {
        "meter": "4/4", "tempo": 108, "swing": 0.0,
        "tracks": ["Standard Kit 1", "Latin Perc.Kit 2", "Acous. Bass Pro1", "Real Nylon Gtr", "Accordion", "Violin & Viola", "Dual Trumpets", "Concert Trumpet"],
        "drum_mode": "cumbia", "bass_mode": "cumbia_triad", "acc1_mode": "oom_pah_off", "acc4_mode": "Mariachi_tpts",
        "hook": [(0, THIRDS, 2), (3, THIRDS, 2), (6, HIGH_STAB, 4), (12, R8, 2), (14, U3, 2)],
        "cadence": "latin_IV_V", "fill_type": "latin_timbale",
    },
    # Italian Liscio / Neapolitan Waltz ("O Sole Mio" / Romagna Fisa + Mandolin)!
    "italian_waltz": {
        "meter": "3/4", "tempo": 156, "swing": 0.0,
        "tracks": ["Standard Kit 2", "Standard PercKit", "Acoustic Bass 1", "Fisa Master", "Mandolin Trem.", "RealFolk Gtr DNC", "Clarinet Pro 1", "Acc.Clarinet OT"],
        "drum_mode": "viennese_3_4", "bass_pat": [(0, R, 4), (4, D3, 4), (8, D5, 4)],
        "acc1_mode": "waltz_oom_pah",
        "hook": [(0, U5, 4), (4, U6, 2), (6, U5, 2), (8, U3, 4), (12, U9, 6), (18, R8, 6)],
    },
    "italian_polka": {
        "meter": "2/4", "tempo": 128, "swing": 0.0,
        "tracks": ["Standard Kit 1", "Standard PercKit", "Accordion Bass", "Fisa Master", "RealClarinet DN1", "RealFolk Gtr DNC", "Alto Sax DN1", "Acc. Piccolo OT"],
        "drum_mode": "polka_2_4", "bass_pat": [(0, R, 2), (4, L5, 2)], "acc1_mode": "oom_pah_off",
        "hook": [(0, R8, 1), (1, U3, 1), (2, U5, 1), (3, U6, 1), (4, U5, 2), (6, U3, 2)],
    },
    # Romagna Italian Mazurka: Graceful 3/4 with characteristic dotted-beat-1 & strong Beat 2/3 lift!
    "italian_mazurka": {
        "meter": "3/4", "tempo": 132, "swing": 0.14, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "Fisa 16,8’", "RealFolk Gtr DNC", "Mandolin DNC", "Clarinet Pro 1", "Fisa Master"],
        "drum_mode": "waltz_3_4", "kicks": [0], "snares": [4, 8],
        "bass_pat": [(0, R, 4), (4, D5, 4), (8, L5, 4)],
        "acc1_steps": [(0, R, 3, 76), (3, D3, 1, 70), (4, HIGH_STAB, 4, 82), (8, CLOSE, 4, 76)],
        "hook": [(0, U3, 3), (3, U5, 1), (4, U6, 4), (8, U5, 4), (12, U3, 4), (16, U9, 4), (20, R8, 4)],
    },
    # Continental Ballroom Liscio Italian Tango (`Fisa Tango` + Mandolin + Strings)
    "italian_tango": {
        "meter": "4/4", "tempo": 122, "swing": 0.0,
        "tracks": ["Standard Kit Amb", "Standard PercKit", "Class.Contrabs", "Fisa Tango", "Mandolin Trem.", "Real Strings 1", "Concert Grand", "Real Violin DNC"],
        "drum_mode": "tango", "bass_mode": "tango_marcato", "acc1_mode": "tango_staccato",
        "hook": [(0, U5, 4), (4, S5, 2), (6, U5, 2), (8, U3, 4), (12, U9, 2), (14, R8, 2)],
        "cadence": "tango_V_I",
    },
    # TURKISH ROMAN HAVASI / KARSILAMA 9/8: Authentic `2+2+2+3` (`0, 4, 8, 12, 14` of 18 steps)!
    "9_8": {
        "meter": "9/8", "tempo": 126, "swing": 0.0,
        "tracks": ["Turkish Kit", "Oriental PercKit", "Fretless Bass 2", "Kanoun 1", "Oud 1", "Arabic Strings", "Ac. Baglama 1", "Klarnet 1"],
        "drum_mode": "turkish_9_8", "acc1_mode": "turkish_9_8",
        "acc2_seq": [(0, R, 2), (4, D3, 2), (8, D5, 2), (12, D4, 2), (14, D3, 2), (16, B2, 2)],
        "hook": [(0, D5, 4), (4, S5, 4), (8, D5, 4), (12, D4, 2), (14, D3, 2), (16, B2, 2), (18, D3, 4), (22, D4, 4), (26, D3, 4), (30, B2, 3), (33, R, 3)],
        "cadence": "flamenco_bVI_V", "fill_type": "oriental_darbuka",
    },
    # Turkish / Arabic Vahde (Wahda 4/4): Deep Darbuka `Düm` on 1, Ornamental `Tek-ka`, Kanun, Nay & Arabic Strings!
    "vahde": {
        "meter": "4/4", "tempo": 96, "swing": 0.0,
        "tracks": ["Turkish Kit", "Arabian Kit 1", "Fretless Bass 2", "Kanoun Trem. 1", "Oud 1", "Arabic Strings", "Nay", "Violin Expr. DNC"],
        "drum_mode": "oriental_4_4", "kicks": [0, 14], "snares": [4, 7, 8, 12],
        "bass_pat": [(0, R, 8), (8, D5, 6), (14, L5, 2)],
        "acc1_steps": [(0, R, 3, 80), (4, D3, 2, 74), (6, D4, 2, 74), (8, D5, 4, 78), (12, D4, 2, 72), (14, B2, 2, 74)],
        "hook": [(0, D5, 4), (4, S5, 2), (6, D5, 2), (8, D4, 4), (12, D3, 2), (14, B2, 2), (16, R, 8)],
        "cadence": "flamenco_bVI_V", "fill_type": "oriental_darbuka",
    },
    # Energetic Anatolian 2/4 Oyun Havası ("Ankara'nın Bağları"): Baglama Saz + Zurna/Klarnet + Darbuka!
    "2_4_oyun": {
        "meter": "2/4", "tempo": 126, "swing": 0.0,
        "tracks": ["Turkish Kit", "Oriental PercKit", "Finger Bass DN1", "Ac. Baglama Grp.", "Kanoun 1", "Arabic Strings", "Zurna 1", "Ac. Baglama 1"],
        "drum_mode": "polka_2_4",
        "perc_steps": [(0, 64, 90), (3, 62, 76), (4, 62, 84), (6, 63, 78), (7, 62, 72)],
        "bass_pat": [(0, R, 3), (3, D5, 1), (4, R, 2), (6, L5, 2)],
        "acc1_steps": [(0, STRUM_DN, 2, 84), (2, STRUM_UP, 1, 76), (3, STRUM_DN, 1, 80), (4, CHUCK, 2, 82), (6, STRUM_UP, 2, 78)],
        "hook": [(0, D5, 2), (2, D4, 1), (3, D5, 1), (4, D3, 2), (6, B2, 1), (7, R, 1)],
        "cadence": "flamenco_bVI_V", "fill_type": "oriental_darbuka",
    },
    # Classic Turkish / Greek Belly-Dance Çiftetelli (`Düm . Tek-ka Tek Düm . Tek .`)!
    "ciftetelli": {
        "meter": "4/4", "tempo": 98, "swing": 0.0,
        "tracks": ["Arabian Kit 1", "Oriental PercKit", "Fretless Bass 2", "Oud 1", "Kanoun 1", "Arabic Strings", "Nay", "Klarnet 1"],
        "drum_mode": "oriental_4_4", "kicks": [0, 8, 10], "snares": [3, 4, 6, 12],
        "bass_pat": [(0, R, 6), (6, D5, 2), (8, R, 2), (10, R, 4), (14, L5, 2)],
        "acc1_steps": [(0, R, 2, 80), (3, B2, 1, 76), (4, D3, 2, 80), (6, D4, 2, 78), (8, D5, 4, 82), (12, S5, 2, 78), (14, D5, 2, 76)],
        "hook": [(0, R8, 3), (3, S5, 1), (4, D5, 2), (6, D4, 2), (8, D3, 3), (11, B2, 1), (12, R, 4)],
        "cadence": "flamenco_bVI_V", "fill_type": "oriental_darbuka",
    },
    # Celtic Air ("Danny Boy" / "She Moved Through the Fair") Irish Slow Waltz with Uilleann Pipes, Tin Whistle & Harp!
    "irish_slow_waltz": {
        "meter": "3/4", "tempo": 96, "swing": 0.08,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "RealFolk Gtr DNC", "Classic Harp", "Uillean BagPipes", "Fiddle", "Whistle DN1"],
        "drum_mode": "waltz_3_4",
        "perc_steps": [(0, 45, 68), (4, 47, 56), (8, 45, 60)],
        "bass_pat": [(0, R, 8), (8, D5, 4)],
        "acc1_steps": [(0, R, 2, 74), (2, D5, 2, 68), (4, R8, 2, 72), (6, U3, 2, 70), (8, D5, 4, 68)],
        "hook": [(0, D5, 4), (4, D6, 2), (6, R8, 2), (8, U3, 4), (12, U5, 6), (18, U3, 6)],
        "cadence": "modal_bVII",
    },
    # Dubliners ("Marino Waltz" / "Wild Rover") Lively Pub Irish Fast Waltz!
    "irish_fast_waltz": {
        "meter": "3/4", "tempo": 148, "swing": 0.12, "swing8": True,
        "tracks": ["Real Kit 1 Amb", "Standard PercKit", "Acoustic Bass 1", "RealFolk Gtr DNC", "Accordion", "Banjo", "Whistle Robin", "Fiddle"],
        "drum_mode": "viennese_3_4", "bass_pat": [(0, R, 6), (6, L5, 6)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": STRUM_DN,
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 4), (8, U5, 4), (12, U6, 4), (16, U5, 4), (20, U3, 4)],
    },
    # Celtic 6/8 Double Jig ("Irish Washerwoman" / Irish Fox): Bodhrán To-And-Fro + Fiddle + Tin Whistle!
    "irish_fox": {
        "meter": "6/8", "tempo": 114, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "RealFolk Gtr DNC", "Accordion", "Mandolin DNC", "Whistle DN1", "Fiddle"],
        "drum_mode": "ballad_6_8", "kicks": [0, 6],
        "perc_steps": [(0, 45, 78), (2, 47, 62), (4, 45, 70), (6, 47, 78), (8, 45, 64), (10, 47, 70)],
        "bass_pat": [(0, R, 5), (6, L5, 5)],
        "acc1_steps": [(0, STRUM_DN, 3, 80), (4, STRUM_UP, 2, 74), (6, STRUM_DN, 3, 80), (10, STRUM_UP, 2, 74)],
        "hook": [(0, U5, 2), (2, U3, 2), (4, R8, 2), (6, D5, 2), (8, R8, 2), (10, U3, 2)],
        "cadence": "modal_bVII",
    },
    # Energetic Celtic Reel / QuickStep!
    "irish_quickstep": {
        "meter": "6/8", "tempo": 128, "swing": 0.0,
        "tracks": ["Real Kit 2 Amb", "Standard PercKit", "Real Ac. Bass 1", "Strum 12Str. DNC", "Banjo", "Accordion", "HighlandBagPipes", "Fiddle"],
        "drum_mode": "ballad_6_8", "kicks": [0, 4, 6, 10],
        "bass_pat": [(0, R, 3), (3, D3, 3), (6, D5, 3), (9, D6, 3)],
        "acc1_steps": [(0, STRUM_DN, 2, 82), (2, STRUM_UP, 2, 76), (4, STRUM_DN, 2, 80), (6, STRUM_DN, 2, 82), (8, STRUM_UP, 2, 76), (10, STRUM_DN, 2, 80)],
        "hook": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 2), (8, U6, 2), (10, U5, 2)],
        "cadence": "country_IV_V",
    },
    # Bavarian / Oktoberfest German Polka: Oberkrainer Tuba + Accordion + Alp Trumpet & Clarinet!
    "german_polka": {
        "meter": "2/4", "tempo": 126, "swing": 0.0,
        "tracks": ["Standard Kit 1", "Standard PercKit", "Oberkr. Tuba", "ClassicSteel DNC", "Accordion", "Clarinet Pro 1", "Alp Trumpet", "Acc.16,8,4’ Plus"],
        "drum_mode": "polka_2_4",
        "bass_pat": [(0, R, 2), (4, L5, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, THIRDS, 2), (2, HIGH_STAB, 2), (4, THIRDS, 2), (6, R8, 2)],
        "cadence": "country_IV_V",
    },
    # Helene Fischer / Udo Jürgens Classic German Discofox Schlager!
    "classic_schlager": {
        "meter": "4/4", "tempo": 126, "swing": 0.0,
        "tracks": ["Pop Std. Kit 1", "Standard PercKit", "JB Pick Bs DN1", "SteelGtrPro DNC", "Pop Grand", "Full Strings", "Trpts & Brass", "Accordion"],
        "drum_mode": "four_floor", "snares": [4, 12],
        "perc_steps": [(4, 54, 76), (12, 54, 76)],
        "bass_mode": "disco_oct", "acc1_mode": "pop_strum", "acc4_mode": "thirds_swell",
        "hook": [(0, U3, 2), (2, U5, 2), (4, U6, 4), (8, U5, 2), (10, U3, 2), (12, R8, 4)],
        "cadence": "pop_IV_V",
    },
    "german_waltz": {
        "meter": "3/4", "tempo": 146, "swing": 0.0,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Oberkr. Tuba", "RealFolk Gtr DNC", "Accordion", "Alp Trumpet", "Clarinet Pro 1", "Zither"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 4), (8, L5, 4)],
        "acc1_mode": "waltz_oom_pah",
        "hook": [(0, D5, 4), (4, U3, 4), (8, R8, 4), (12, U5, 8), (20, U3, 4)],
        "cadence": "country_IV_V",
    },
    "vienna_waltz": {
        "meter": "3/4", "tempo": 176, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Trinity Perc.Kit", "Class.Contrabs", "ConcertStrings 1", "Concert Grand", "French Section", "Flute", "Real Violin DNC"],
        "drum_mode": "viennese_3_4", "bass_pat": [(0, R, 5), (8, D5, 3)],
        "acc1_mode": "waltz_oom_pah", "acc1_code": OPEN,
        "hook": [(0, R8, 4), (4, U3, 4), (8, U5, 4), (12, U8, 8), (20, U5, 4)],
        "fill_type": "orchestral_timp",
    },
    # Parisian Montmartre Musette Waltz ("Sous le Ciel de Paris"): `French Musette` 8th-note runs + Gypsy Guitar!
    "musette_waltz": {
        "meter": "3/4", "tempo": 164, "swing": 0.12, "swing8": True,
        "tracks": ["Brush Kit 1 Amb", "Standard PercKit", "Real Ac. Bass 1", "ClassicSteel DNC", "French Musette", "Classic Piano", "RealClarinet DN1", "3 Voices Musette"],
        "drum_mode": "waltz_3_4", "bass_mode": "waltz_walk",
        "acc1_mode": "waltz_oom_pah", "acc1_code": CHUCK,
        "acc2_seq": [(0, R8, 2), (2, U9, 2), (4, U3, 2), (6, U5, 2), (8, U3, 2), (10, U9, 2)],
        "hook": [(0, U5, 2), (2, S5, 2), (4, U5, 2), (6, U3, 2), (8, R8, 4), (12, U9, 6), (18, R8, 6)],
        "cadence": "flamenco_bVI_V",
    },
    # Yann Tiersen ("Amélie" / Edith Piaf) Nostalgic French Waltz (Accordion + Toy/Music-Box Piano + Strings)!
    "french_waltz": {
        "meter": "3/4", "tempo": 138, "swing": 0.0,
        "tracks": ["Brush Kit 2 Amb", "Standard PercKit", "Acoustic Bass 1", "Classic Musette", "Concert Grand", "Music Box", "Chamber Strings", "French Musette"],
        "drum_mode": "waltz_3_4", "bass_pat": [(0, R, 6), (8, L5, 4)],
        "acc1_mode": "waltz_oom_pah",
        "acc2_seq": [(0, R, 2), (2, D5, 2), (4, R8, 2), (6, U3, 2), (8, R8, 2), (10, D5, 2)],
        "hook": [(0, U3, 6), (6, U9, 2), (8, R8, 4), (12, D5, 8), (20, R8, 4)],
        "cadence": "flamenco_bVI_V",
    },
    # Mexican Banda Sinaloense: Syncopated Tuba Sousaphone + Tambora/Tarola Rolls + Clarinets & Trumpets!
    "banda": {
        "meter": "2/4", "tempo": 124, "swing": 0.0,
        "tracks": ["Power Kit 1 Amb", "Standard PercKit", "Tuba Gold", "Trpts & Trombs", "Clarinet Ens.", "HardTrombone DN1", "Dual Trumpets", "Trumpet Expr.1"],
        "drum_mode": "march_2_4",
        "perc_steps": [(0, 49, 72, V_34), (4, 38, 84), (6, 38, 72), (7, 38, 76)],
        "bass_pat": [(0, R, 2), (3, D3, 1), (4, D5, 2), (7, LT, 1)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, THIRDS, 2), (2, THIRDS, 1), (3, HIGH_STAB, 3), (6, THIRDS, 2)],
        "cadence": "latin_IV_V",
    },
    # JOHN PHILIP SOUSA ("The Stars and Stripes Forever"): Crisp Military Snare, Bass Drum & Cymbal, Tuba, Brass & Piccolo!
    "us_march": {
        "meter": "2/4", "tempo": 120, "swing": 0.0,
        "tracks": ["Standard Kit Amb", "Trinity Perc.Kit", "Tuba Gold", "French Section", "Trpts & Trombs", "Clar & Sax Ens 1", "Brass of Power", "Piccolo"],
        "drum_mode": "march_2_4",
        "perc_steps": [(0, 57, 74, V_34), (4, 55, 66, V_4)],
        "bass_pat": [(0, R, 2), (4, L5, 2)],
        "acc1_mode": "oom_pah_off",
        "hook": [(0, U5, 2), (2, U5, 1), (3, U6, 1), (4, U5, 2), (6, U3, 2), (8, R8, 2), (10, U3, 2), (12, U5, 4)],
        "cadence": "march_V_I", "fill_type": "orchestral_timp",
    },
}
