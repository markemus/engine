import random

import engine.creature as cr
import engine.spells as sp
import engine.utils as utils

import wizard.furniture as fur
import wizard.suits as su
import wizard.zombie as z

from wizard import giant_spider
from wizard import tentacle_monster

from colorist import BrightColor as BC, Color as C


# Creation
# TODO-DECIDE mana costs for spells?
class Caltrops(sp.Spell):
    """Area of effect spell that causes enemies to fall down."""
    name = "Caltrops"
    description = "Causes enemies to fall. (>-10)"
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
        """Caltrops will cause some enemies to fall every round."""
        # First reset amble for all limbs from last round
        self._fix_legs()
        # Then affect some limbs for this round
        enemies = [x for x in self.caster.location.creatures if x.team != self.caster.team and x.team != "neutral"]
        for enemy in enemies:
            legs = enemy.subelements[0].limb_check("amble")
            if legs:
                random.shuffle(legs)
                legs = legs[:random.randint(0, int(len(legs)/2))]
                for leg in legs:
                    # If enough legs are affected, creature will fall over
                    self.legs[leg] = leg.amble
                    leg.amble = 0

    def expire(self):
        self._fix_legs()


class GrowTreeOfLife(sp.Spell):
    name = "Grow Tree of Life"
    description = "A tree with healing fruits sprouts out of the floor (>2)."
    rounds = 1
    targets = "caster"

    def cast(self):
        humanity_min = 2
        if self.caster.humanity >= humanity_min:
            tree_of_life = fur.TreeOfLife(color=random.choice(fur.TreeOfLife.color), texture=random.choice(fur.TreeOfLife.texture))
            self.caster.location.elements.append(tree_of_life)
            print(f"{BC.MAGENTA}A beautiful tree with shiny silver fruits sprouts up out of the ground!{BC.OFF}")
            return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too low to cast this spell ({humanity_min})!{BC.OFF}")
            return False


class SummonSpider(sp.Spell):
    name = "Summon Spider"
    description = "Summons an enemy spider (>5)."
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

class SummonTentacleMonster(sp.Spell):
    name = "Summon Tentacle Monster"
    description = "Summons a friendly tentacle monster (>7)."
    rounds = 1
    targets = "caster"

    def cast(self):
        humanity_min = 7
        if self.caster.humanity >= humanity_min:
            tm = tentacle_monster.TentacleMonster(location=self.target.location)
            tm.team = self.caster.team
            self.target.location.creatures.append(tm)
            self.caster.companions.append(tm)
            print(f"{BC.MAGENTA}A {C.RED}giant tentacle monster{BC.MAGENTA} pops into existence!{BC.OFF}")
            return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too low to cast this spell ({humanity_min})!{BC.OFF}")
            return False


class ArmorOfLight(sp.Spell):
    name = "Light Armor"
    description = "Conjures a set of armor made of light (>-10)."
    rounds = 20
    targets = "friendly"

    def cast(self):
        humanity_min = -10
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
        print(f"{BC.MAGENTA}The glowing armor on {C.RED}{self.target.name}{BC.MAGENTA} fades away and disappears.{BC.OFF}")


# Corruption
class Light(sp.Spell):
    name = "Light"
    description = "A luminous glow surrounds a creature, making it easier to hit (<10)."
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

class Shadow(sp.Spell):
    name = "Shadow"
    description = "A shadowy murk surrounds a creature, making it harder to hit (<10)."
    rounds = 10
    targets = "friendly"
    original_colors = None
    original_sizes = None

    def cast(self):
        humanity_max = 10
        if self.caster.humanity <= humanity_max:
            self.original_colors = {}
            self.original_sizes = {}
            limbs = self.target.subelements[0].limb_check("isSurface")
            for limb in limbs:
                self.original_colors[limb] = limb.color
                self.original_sizes[limb] = limb.size
                limb.color = f"shadowy {limb.color}"
                if limb.size > 1:
                    limb.size -= 1
            print(f"{BC.MAGENTA}A shadowy gloom surrounds {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")
            return True
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too high to cast this spell ({humanity_max})!{BC.OFF}")

    def expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            if limb in self.original_colors.keys():
                limb.color = self.original_colors[limb]
                limb.size = self.original_sizes[limb]
        print(f"{BC.MAGENTA}The shadow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")


class GraftLimb(sp.Spell):
    name = "Graft Limb"
    description = "Graft a disembodied limb onto a friendly creature (<0)."
    rounds = 1
    targets = "friendly"

    def cast(self):
        humanity_max = 0
        if self.caster.humanity <= humanity_max:
            invs = self.caster.location.find_invs()
            invs = utils.listtodict(invs, add_x=True)
            utils.dictprint(invs)
            i = input(f"\n{BC.GREEN}Which inventory would you like to graft from?{BC.OFF} ")

            if i in invs.keys() and i != "x":
                graft_limbs = utils.listtodict([item for item in invs[i].vis_inv if isinstance(item, cr.Limb)], add_x=True)
                utils.dictprint(graft_limbs)
                j = input(f"\n{BC.GREEN}Select a limb to graft:{BC.OFF} ")

                if j in graft_limbs.keys() and j != "x":
                    graft_limb = graft_limbs[j]
                    target_limbs = utils.listtodict(self.target.subelements[0].limb_check("isSurface"), add_x=True)
                    utils.dictprint(target_limbs)
                    k = input(f"{BC.GREEN}Select a limb to graft onto: {BC.OFF}")

                    if k in target_limbs.keys() and k != "x":
                        target_limb = target_limbs[k]
                        target_limb.subelements.append(graft_limb)
                        print(f"{BC.MAGENTA}The {BC.CYAN}{graft_limb.name}{BC.MAGENTA} crudely grafts itself onto the {BC.CYAN}{target_limb.name}{BC.MAGENTA}!{BC.OFF}")
                        return True
            return False
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too high to cast this spell ({humanity_max})!{BC.OFF}")


class ReanimateLimb(sp.Spell):
    name = "Reanimate"
    description = "Reanimates a dead creature as a zombie (<-7)."
    rounds = 1
    targets = "caster"

    def cast(self):
        """Bring a limb in the room back to life."""
        humanity_max = 5
        if self.caster.humanity <= humanity_max:
            invs = self.caster.location.find_invs()
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


class FleshRip(sp.Spell):
    name = "Flesh Rip"
    description = "Rip a small limb off of an enemy (<-2)."
    rounds = 1
    targets = "enemy"

    def cast(self):
        humanity_max = -2
        if self.caster.humanity <= humanity_max:
            limbs = utils.listtodict([x for x in self.target.subelements[0].limb_check("isSurface") if x.isSurface and x.size <= 1], add_x=True)
            # utils.dictprint(limbs, pfunc=lambda x,y: x + f" {C.RED}({y.hp}){C.OFF}")
            utils.dictprint(limbs)

            j = input(f"{BC.MAGENTA}Pick a limb to tear off of your enemy: {BC.OFF}")
            if j in limbs.keys() and j != "x":
                limb = limbs[j]
                self.target.remove_limb(limb)

                print(f"{BC.MAGENTA}An ethereal force rips the {BC.CYAN}{limb.name}{BC.MAGENTA} off of {BC.YELLOW}{self.target.name}{BC.MAGENTA}'s body!{BC.OFF}")
                self.caster.location.drop_item(limb)
                return True
            else:
                return False
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too high to cast this spell ({humanity_max})!{BC.OFF}")
            return False


# Neither
class Flashbang(sp.Spell):
    name = "Flashbang"
    description = "Temporarily blind your enemies in the area of effect."
    rounds = 5
    targets = "caster"
    original_see = {}

    def cast(self):
        enemies = [x for x in self.caster.location.creatures if x.team != self.caster.team and x.team != "neutral"]
        for enemy in enemies:
            for eye in enemy.subelements[0].limb_check("see"):
                self.original_see[eye] = eye.see
                eye.see = 0
                print(f"{BC.YELLOW}{enemy.name}{BC.MAGENTA}'s {BC.CYAN}{eye.name}{BC.MAGENTA} is blinded!{BC.OFF}")
        return True

    def expire(self):
        for eye in self.original_see.keys():
            eye.see = self.original_see[eye]
            print(f"{BC.CYAN}{eye.name}{BC.MAGENTA} can see again.{BC.OFF}")

class Scry(sp.Spell):
    name = "Scry"
    description = "See what is happening in a nearby room."
    rounds = 1
    targets = "caster"

    def cast(self):
        borders = self.caster.location.borders.copy()
        borders["x"] = "Cancel"
        utils.dictprint(borders)
        i = input(f"{BC.MAGENTA}Which room would you like to scry?{BC.OFF}")

        if i in borders.keys() and borders[i] is not None and i != "x":
            print(borders[i].desc(full=False))
        return True


class SetHumanity(sp.Spell):
    name = "Set Humanity"
    description = "Cheat and set your humanity to whatever you want."
    rounds = 5
    targets = "caster"
    original_humanity = None

    def cast(self):
        self.original_humanity = self.caster.humanity
        self.caster.humanity = int(input(f"{BC.MAGENTA}Set your humanity: {BC.OFF}"))
        return True

    def expire(self):
        print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity returns to its normal value.{BC.OFF}")
        self.caster.humanity = self.original_humanity


# TODO-DONE summon tentacle monster- amble on subelements[0] but overwrite leave() so it cannot move.
# TODO-DONE fleshrip- tear off a size 1 limb from an opponent
# TODO-DONE tree of life- spawns a sapling with healing fruits (furniture with subelements)
# TODO-DONE scrying- see desc() for neighboring room
# TODO-DONE cloak of shadow- _clothes creature in dark shadow and sets limb size -= 1
# TODO graft limb- graft a disembodied limb onto a friendly creature
# TODO-DONE flashbang spell
