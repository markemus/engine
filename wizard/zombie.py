import random

import engine.creature as cr
import engine.effectsbook as eff

from wizard.arachnid import Arachnid
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


zombie_source_creatures = [Arachnid, DarkElfScout, DarkElfGuard, DarkElfFairy, DeepGoblin, GiantRat, GiantBat, GiantSpider, CaveOctopus, Owlbear, Troll, Uruk, Warg]


class Zombie(cr.creature):
    """A reanimated Limb."""
    classname = "zombie"
    team = "necromancer"
    namelist = ["zombie"]
    can_rest = False
    can_breathe = False
    can_stun = False
    can_fear = False
    can_poison = False

    def __init__(self, limb, location):
        self.colors = [limb.color]
        self.textures = [limb.texture]
        super().__init__(location=location)
        if limb.creature:
            self.classname = f"zombie {limb.creature.classname}"
            self.name = f"zombie {limb.creature.name}"
        else:
            self.classname = f"zombie {limb.name}"
            self.name = f"zombie {limb.name}"

        self.subelements = [limb]
        # Heal the base limb a bit, since it might have negative hp otherwise
        if limb.hp < int(limb.base_hp / 2):
            limb.hp = int(limb.base_hp / 2)

        for limb in self.limb_check("name"):
            if hasattr(limb, "vital"):
                limb.vital = False
            limb.can_bleed = False
            limb.can_heal = False
            # Limbs that have been resurrected cannot be resurrected again (spells that create Zombies should enforce).
            limb.resurrected = True
            limb.creature = self

        for limb in self.limb_check("grasp"):
            limb.grasped = None
            limb.grasp = 0
            # Zombies can't hold weapons, but they can grapple, of course
            class Entangled(eff.Entangled):
                entangling_limb = limb
            if not sum([issubclass(e, eff.Entangled) for e in limb.weapon_effects]):
                limb.weapon_effects.append(Entangled)

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


class MeldedRandomZombie(Zombie):
    def __init__(self, location):
        base_creature = random.choice(zombie_source_creatures)(location=None)
        other_creature = random.choice(zombie_source_creatures)(location=None)

        limbs = other_creature.get_neighbors(other_creature.subelements[0])
        limbs = limbs[:random.randint(1, len(limbs))]
        for limb in limbs:
            other_creature.subelements[0].remove_limb(limb)
        base_creature.subelements[0].subelements.extend(limbs)
        base_creature.name = f"{base_creature.name}-{other_creature.name}"[:60]
        base_creature.classname = f"{base_creature.classname}-{other_creature.classname}"[:60]

        super().__init__(limb=base_creature.subelements[0], location=location)
