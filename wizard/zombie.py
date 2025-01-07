import random

import engine.creature as cr
import engine.effectsbook as eff

from wizard.arachne import Arachne
from wizard.elf import DarkElfScout, DarkElfGuard
from wizard.fairy import DarkElfFairy
from wizard.giant_rat import GiantRat
from wizard.giant_bat import GiantBat
from wizard.giant_spider import GiantSpider
from wizard.octopus import CaveOctopus
from wizard.owlbear import Owlbear
from wizard.troll import Troll
from wizard.uruk import Uruk
from wizard.warg import Warg

from assets.goblin import DeepGoblin

from colorist import BrightColor as BC, Color as C


zombie_source_creatures = [Arachne, DarkElfScout, DarkElfGuard, DarkElfFairy, DeepGoblin, GiantRat, GiantBat, GiantSpider, CaveOctopus, Owlbear, Troll, Uruk, Warg]

# TODO-DECIDE store original creature somewhere on limb when it gets removed? Then we could name zombies with class
class Zombie(cr.creature):
    """A reanimated Limb."""
    classname = "zombie"
    team = "monster"
    namelist = ["zombie"]
    can_rest = False
    can_breathe = False
    can_stun = False

    def __init__(self, limb, location):
        self.colors = [limb.creature.color]
        self.textures = [limb.creature.texture]
        super().__init__(location=location)
        self.classname = f"zombie {limb.creature.classname}"
        self.name = f"zombie {limb.creature.classname}"
        self.subelements = [limb]
        # Heal the base limb a bit, since it will have negative hp otherwise
        if limb.hp < int(limb.base_hp / 2):
            limb.hp = int(limb.base_hp / 2)

        for limb in self.limb_check("name"):
            if hasattr(limb, "vital"):
                limb.vital = False
            limb.can_bleed = False
            limb.can_heal = False

        for limb in self.limb_check("grasp"):
            limb.grasped = None

    def _elementGen(self):
        """Zombies should not have limbs generated for them- we will manually set self.subelements."""
        pass

    def _clothe(self):
        """Zombies should not have clothes generated for them when they're created."""
        pass


class ExplodingZombie(Zombie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subelements[0].name = "bloated " + self.subelements[0].name
        self.subelements[0].impact_effects = [eff.ExplodeOnDeath]


class RandomZombie(Zombie):
    def __init__(self, location):
        creature = random.choice(zombie_source_creatures)(location=None)

        # Should have some missing limbs
        # limbs = creature.subelements[0].get_neighbors(creature.subelements[0])
        limbs = creature.limb_check("name")
        random.shuffle(limbs)
        missing_limbs = limbs[:random.randint(0, len(limbs))]

        # missing limbs should leave at least one weapon
        weapons = creature.limb_check("damage")
        in_both = list(set(weapons).intersection(set(missing_limbs)))
        if in_both:
            in_both_parents = creature.get_parents(in_both[0])
            for limb in in_both_parents:
                if limb in missing_limbs:
                    missing_limbs.remove(limb)

        # Remove missing limbs
        for limb in missing_limbs:
            creature.subelements[0].remove_limb(limb)

        # Limbs should have less than full hp
        all_limbs = creature.limb_check("name")
        for limb in all_limbs:
            limb.hp = random.randint(1, limb.base_hp)

        super().__init__(limb=creature.subelements[0], location=location)


class RandomExplodingZombie(ExplodingZombie):
    def __init__(self, location):
        creature = random.choice(zombie_source_creatures)(location=None)

        # Should have some missing limbs
        limbs = creature.limb_check("name")
        random.shuffle(limbs)
        missing_limbs = limbs[:random.randint(0, len(limbs))]

        # missing limbs should leave at least one weapon
        weapons = creature.limb_check("damage")
        in_both = list(set(weapons).intersection(set(missing_limbs)))
        if in_both:
            in_both_parents = creature.get_parents(in_both[0])
            for limb in in_both_parents:
                if limb in missing_limbs:
                    missing_limbs.remove(limb)

        # Remove missing limbs
        for limb in missing_limbs:
            creature.subelements[0].remove_limb(limb)

        # Limbs should have less than full hp
        all_limbs = creature.limb_check("name")
        for limb in all_limbs:
            limb.hp = random.randint(1, limb.base_hp)

        super().__init__(limb=creature.subelements[0], location=location)
