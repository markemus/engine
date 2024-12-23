import inspect
import random

import engine.spells
import engine.item as it
import engine.suits_and_collections as sc

import assets.potions

import wizard.spellbook as sb
import wizard.suits as wsu

from assets.human import Human

from colorist import BrightColor as BC, Color as C


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

potions_col = {
    "contains": [(assets.potions.PotionOfStoneskin, assets.potions.TentacleGrowthPotion, assets.potions.PotionOfHealing)],
    "color": ["None"],
    "color_scheme": "same",
    "texture": ["None"],
    "texture_scheme": "same",
    "full": True,
}

firesword_col = sc.suit_to_collection(wsu.firesword, model=Human)
lightsword_col = sc.suit_to_collection(wsu.lightsword, model=Human)

mana_items = {
    "contains": [(wsu.RingOfMana, wsu.ManaLocket)],
    "color": ["sapphire", "ruby", "emerald", "diamond"],
    "color_scheme": "unique",
    "texture": ["in silver", "in gold", "in platinum"],
    "texture_scheme": "unique",
    "full": True,
}

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
    "color": ["None"],
    "color_scheme": "same",
    "texture": ["None"],
    "texture_scheme": "same",
    "full": True,
}
