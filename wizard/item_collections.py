"""Items and collections."""
import inspect
import random

import engine.spells
import engine.item as it
import engine.suits_and_collections as sc

import assets.potions

import wizard.spellbook as sb
import wizard.suits as wsu

from assets.human import Human
from wizard import giant_spider

from colorist import BrightColor as BC, Color as C


# Assemble a list of all spells in the wizard.spellbook module
all_spells = []
for x in dir(sb):
    variable = getattr(sb, x)
    if inspect.isclass(variable) and issubclass(variable, engine.spells.Spell) and variable not in [sb.CreationSpell, sb.CorruptionSpell]:
        all_spells.append(variable)

level_one_spells = [sb.Caltrops, sb.Light, sb.Shadow, sb.GraftLimb, sb.Flashbang, sb.GrowBeard, sb.Fear, sb.Might, sb.SummonEtherealHand, sb.SummonCerberus, sb.PoisonedWeapons, sb.FlamingWeapons]
level_two_spells = [sb.GrowFangs, sb.SummonSpider, sb.ArmorOfLight, sb.Fireball, sb.Lightning, sb.Distract, sb.Scry, sb.FleshRip, sb.Trapdoor, sb.SummonFairy]
level_three_spells = [sb.SummonTentacleMonster, sb.Enthrall, sb.ReanimateLimb, sb.PoisonGas, sb.Possess, sb.GrowTreeOfLife]

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

class LevelTwoScroll(it.Scroll):
    def __init__(self, color=None, texture=None):
        super().__init__()
        self.spell = random.choice(level_two_spells)
        self.name = f"scroll of {self.spell.name}"


class Plaque(it.Item):
    name = "plaque"
    usable = True
    consumable = False
    colors = ["None"]
    textures = ["None"]

    def __init__(self, color=None, texture=None):
        super().__init__(color="", texture="")

    def use(self, creature, cont):
        engraving = input(f"{BC.CYAN}Enter a message to engrave onto the plaque: {BC.OFF}")
        self.color = engraving

c_spider_suit = sc.suit_to_collection(suit=wsu.spider_bronze_suit, model=giant_spider.GiantSpider)
