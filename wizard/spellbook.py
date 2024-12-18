import random

import engine.creature as cr
import engine.spells as sp
import engine.utils as utils

import wizard.suits as su
import wizard.zombie as z

from assets import giant_spider


from colorist import BrightColor as BC, Color as C


# Creation
# TODO-DECIDE mana costs for spells?
class SummonSpider(sp.Spell):
    name = "Summon Spider"
    description = "Summon an enemy spider."
    rounds = 1
    targets = "caster"

    def cast(self):
        """This is useful if you want to test combat magic on an opponent."""
        humanity_min = -5
        if self.caster.humanity >= humanity_min:
            spider = giant_spider.GiantSpider(location=self.target.location)
            self.target.location.creatures.append(spider)
            print(f"{BC.MAGENTA}A {C.RED}giant spider{BC.MAGENTA} pops into existence!{BC.OFF}")
            return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too low to cast this spell ({humanity_min})!{BC.OFF}")
            return False

class Caltrops(sp.Spell):
    """Area of effect spell that causes enemies to fall down."""
    name = "Caltrops"
    description = "Causes enemies to fall."
    rounds = 5
    targets = "caster"

    def __init__(self, *args, **kwargs):
        self.legs = {}
        super().__init__(*args, **kwargs)

    def cast(self):
        humanity_min = -10
        if self.caster.humanity >= humanity_min:
            self.update()
            print(f"{BC.MAGENTA}Enchanted caltrops scatter themselves across the floor.{BC.OFF}")
            return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too low to cast this spell! ({humanity_min}){BC.OFF}")
            return False

    def _fix_legs(self):
        # reset amble for all limbs from last round
        for leg in self.legs.keys():
            leg.amble = self.legs[leg]

        self.legs = {}

    def update(self):
        """Caltrops will cause some creatures to fall every round."""
        # First reset amble for all limbs from last round
        self._fix_legs()
        # Then affect some limbs for this round
        creatures = self.caster.location.creatures
        for creature in creatures:
            legs = creature.subelements[0].limb_check("amble")
            random.shuffle(legs)
            legs = legs[:random.randint(0, len(legs))]
            for leg in legs:
                # If enough legs are affected, creature will fall over
                self.legs[leg] = leg.amble
                leg.amble = 0

    def expire(self):
        self._fix_legs()


class ArmorOfLight(sp.Spell):
    name = "Light Armor"
    description = "armor made of light"
    rounds = 2
    targets = "friendly"

    def cast(self):
        humanity_min = 5
        if self.caster.humanity >= humanity_min:
            old_suits = self.target.suits
            self.target.suits = [su.lightsuit]
            # Puts the armor on the target
            self.target._clothe()
            self.target.suits = old_suits
            print(f"{BC.MAGENTA}A glowing suit of armor envelops {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")
            return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too low to cast this spell! ({humanity_min}){BC.OFF}")
            return False

    def expire(self):
        self.target.unequip_suit(su.lightsuit)
        # limbs = self.target.subelements[0].limb_check("wears")
        # for limb in limbs:
        #     to_remove = tuple(su.lightsuit["wears"].values())
        #     for equipment in limb.equipment:
        #         if isinstance(equipment, to_remove):
        #             limb.unequip(equipment)
        print(f"{BC.MAGENTA}The glowing armor on {C.RED}{self.target.name}{BC.MAGENTA} fades away and disappears.{BC.OFF}")


# Corruption
class Light(sp.Spell):
    name = "Light"
    description = "A luminous glow that surrounds a creature, making it easier to hit."
    rounds = 10
    targets = "enemy"
    def cast(self):
        humanity_max = 10
        if self.caster.humanity <= humanity_max:
            self.original_colors = {}
            limbs = self.target.subelements[0].limb_check("isSurface")
            for limb in limbs:
                self.original_colors[limb] = limb.color
                limb.color = f"luminous {limb.color}"
                limb.size += 1
            print(f"{BC.MAGENTA}A luminous glow surrounds {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")
            return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too high to cast this spell ({humanity_max})!{BC.OFF}")

    def expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            if limb in self.original_colors.keys():
                limb.color = self.original_colors[limb]
                limb.size -= 1
        print(f"{BC.MAGENTA}The glow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")

class ReanimateLimb(sp.Spell):
    name = "Reanimate Limb"
    description = "Reanimate a zombie."
    rounds = 1
    targets = "caster"

    def cast(self):
        """Bring a limb in the room back to life."""
        humanity_max = 5
        if self.caster.humanity <= humanity_max:
            invs = self.caster.location.find_invs()
            # Drop equipment
            invs = utils.listtodict(invs, add_x=True)
            utils.dictprint(invs)
            i = input(f"\n{BC.GREEN}Which inventory would you like to resurrect from?{BC.OFF} ")

            if i in invs.keys() and i != "x":
                limbs = utils.listtodict([item for item in invs[i].vis_inv if isinstance(item, cr.Limb)], add_x=True)
                utils.dictprint(limbs)
                j = input(f"\n{BC.GREEN}Select a limb to resurrect:{BC.OFF} ")

                if j in limbs.keys() and j != "x":
                    limb = limbs[j]
                    zombie = z.Zombie(limb=limb, location=self.caster.location)
                    zombie.team = self.caster.team
                    self.caster.location.addCreature(zombie)
                    self.caster.companions.append(zombie)
                    print(f"{C.RED}{zombie.name}{BC.MAGENTA} rises from the dead with a moan!{BC.OFF}")
                    return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too high to cast this spell ({humanity_max})!{BC.OFF}")
            return False

# TODO summon tentacle monster- amble on subelements[0] but overwrite leave() so it cannot move.
# TODO fleshrip- tear off a size 1 limb from an opponent
# TODO tree of life- spawns a sapling with healing fruits
# TODO scrying- see desc() for neighboring room
# TODO cloak of shadow- _clothes creature in dark shadow and sets limb size -= 1
# TODO graft limb- graft a disembodied limb onto a friendly creature