import inspect
import random

import engine.spells
import engine.item as it

from colorist import BrightColor as BC, Color as C

from wizard import spellbook as sb


# Assemble a list of all spells in the wizard.spellbook module
all_spells = []
for x in dir(sb):
    variable = getattr(sb, x)
    if inspect.isclass(variable) and issubclass(variable, engine.spells.Spell) and variable not in [sb.CreationSpell, sb.CorruptionSpell]:
        all_spells.append(variable)

level_one_spells = [sb.Caltrops, sb.Scry, sb.Light, sb.Shadow, sb.GraftLimb, sb.Flashbang, sb.GrowBeard]
level_two_spells = [sb.GrowTreeOfLife, sb.SummonSpider, sb.ArmorOfLight, sb.Lightning, sb.Distract, sb.FleshRip]
level_three_spells = [sb.SummonTentacleMonster, sb.Enthrall, sb.ReanimateLimb]

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

# TODO make this inscription visible in l:desc() in controller.
class Plaque(it.Item):
    name = "plaque"
    usable = True
    consumable = False

    def __init__(self, color=None, texture=None):
        super().__init__(color="", texture="")

    def use(self, creature):
        engraving = input(f"{BC.CYAN}Enter a message to engrave onto the plaque: {BC.OFF}")
        self.color = engraving


l1_scrolls = {
    "contains": [LevelOneScroll],
    "color": ["white"],
    "color_scheme": "same",
    "texture": ["parchment"],
    "texture_scheme": "same",
    "full": True,
}

plaque = {
    "contains": [Plaque],
    "color": "None",
    "color_scheme": "same",
    "texture": "None",
    "texture_scheme": "same",
    "full": True,
}
