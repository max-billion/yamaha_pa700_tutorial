#!/usr/bin/env python3
"""
Master 379-Style Blueprint Registry for the Korg Pa700 Trainer.

Unites Part A (Pop, Ballad, Ballroom, Dance, Rock, Country = 183 styles) and
Part B (Latin, Latin Dance, Jazz, Movie & Show, Funk & Blues, World = 196 styles)
and provides category-matched Pad Group defaults.
"""

from style_blueprints_a import BLUEPRINTS_A
from style_blueprints_b import BLUEPRINTS_B

CATEGORY_PAD_GROUPS = {
    "Pop":         ["HIT - Percussion", "SEQ - Guitar", "SEQ - Piano", "HIT - Drum"],
    "Ballad":      ["HIT - Orchestral", "SEQ - Piano", "SEQ - Guitar", "HIT - Percussion"],
    "Ballroom":    ["HIT - Orchestral", "SEQ - Orchestral", "SEQ - Piano", "HIT - Percussion"],
    "Dance":       ["HIT - Drum", "SEQ - Groove", "SEQ - Synth&Pad", "HIT - Synth&Pad"],
    "Rock":        ["HIT - Drum", "SEQ - Guitar", "SEQ - Bass", "HIT - Misc&SFX 1"],
    "Country":     ["HIT - Percussion", "SEQ - Guitar", "SEQ - Piano", "HIT - Blocks"],
    "Latin":       ["HIT - Percussion", "SEQ - Percussion", "SEQ - Guitar", "SEQ - Piano"],
    "Latin Dance": ["SEQ - Percussion", "HIT - Percussion", "SEQ - Bass", "SEQ - Synth&Pad"],
    "Jazz":        ["HIT - Percussion", "SEQ - Guitar", "SEQ - Bass", "SEQ - Piano"],
    "Movie & Show":["HIT - Orchestral", "SEQ - Orchestral", "SEQ - Piano", "HIT - Percussion"],
    "Funk & Blues":["HIT - Drum", "SEQ - Groove", "SEQ - Bass", "SEQ - Guitar"],
    "World":       ["HIT - World 1", "HIT - World 2", "HIT - Percussion", "SEQ - Guitar"],
}

STYLE_BLUEPRINTS_379 = {}
STYLE_BLUEPRINTS_379.update(BLUEPRINTS_A)
STYLE_BLUEPRINTS_379.update(BLUEPRINTS_B)


def get_style_blueprint(style_id: str, category: str) -> dict:
    if style_id not in STYLE_BLUEPRINTS_379:
        raise KeyError(f"Missing explicit blueprint for style_id={style_id!r} (category={category!r})")
    bp = dict(STYLE_BLUEPRINTS_379[style_id])
    bp.setdefault("pad_groups", CATEGORY_PAD_GROUPS.get(category, CATEGORY_PAD_GROUPS["Pop"]))
    return bp
