import inspect
import random

import engine.spells
import engine.item as it

from wizard import spellbook as sb


# Assemble a list of all spells in the wizard.spellbook module
all_spells = []
for x in dir(sb):
    variable = getattr(sb, x)
    if inspect.isclass(variable) and issubclass(variable, engine.spells.Spell) and variable not in [sb.CreationSpell, sb.CorruptionSpell]:
        all_spells.append(variable)
# all_spells = [spellbook.Caltrops, spellbook.GrowTreeOfLife, spellbook.GraftLimb]

level_one_spells = [sb.Caltrops, sb.Scry, sb.Light, sb.Shadow, sb.GraftLimb, sb.Flashbang]

class RandomScroll(it.Scroll):
    def __init__(self, color=None, texture=None):
        super().__init__()
        self.spell = random.choice(all_spells)
        self.name = f"scroll of {self.spell.name}"

class LevelOneScroll(it.Scroll):
    """A scroll with a beginner spell."""
    def __init__(self, color=None, texture=None):
        super().__init__()
        self.spell = random.choice(level_one_spells)
        self.name = f"scroll of {self.spell.name}"


l1_scrolls = {
    "contains": [LevelOneScroll],
    "color": ["white"],
    "color_scheme": "same",
    "texture": ["parchment"],
    "texture_scheme": "same",
    "full": True,
}
