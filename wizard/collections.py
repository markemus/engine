import inspect
import random

import engine.spells
import engine.item as it

from wizard import spellbook


# Assemble a list of all spells in the wizard.spellbook module
all_spells = []
for x in dir(spellbook):
    variable = getattr(spellbook, x)
    if inspect.isclass(variable) and issubclass(variable, engine.spells.Spell) and x not in [spellbook.CreationSpell, spellbook.CorruptionSpell]:
        all_spells.append(variable)
# all_spells = [spellbook.Caltrops, spellbook.GrowTreeOfLife, spellbook.GraftLimb]
class RandomScroll(it.Scroll):
    def __init__(self, color=None, texture=None):
        super().__init__()
        self.spell = random.choice(all_spells)

scrolls = {
    "contains": [RandomScroll],
    "color": ["white"],
    "color_scheme": "same",
    "texture": ["parchment"],
    "texture_scheme": "same",
    "full": True,
}
