import random

import engine.creature as cr
import engine.spells as sp
import engine.utils as utils

import assets.dog

import wizard.suits as su
import wizard.zombie as z

from wizard import giant_spider
from wizard import tentacle_monster

from colorist import BrightColor as BC, Color as C
# If we run into trouble with circular imports, import within the function instead of on module level.


class CreationSpell(sp.Spell):
    """A spell that requires creative powers and therefore has a minimal humanity to cast.
    Subclasses must set humanity_min."""
    humanity_min = None
    def cast(self):
        if self.caster.humanity >= self.humanity_min:
            return super().cast()
            # return self._cast()
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too low to cast this spell! ({self.humanity_min}){BC.OFF}")


class CorruptionSpell(sp.Spell):
    """A spell that requires corruptive powers and therefore requires a low humanity to cast.
    Subclasses must set humanity_max."""
    humanity_max = None

    def cast(self):
        if self.caster.humanity <= self.humanity_max:
            return super().cast()
            # return self._cast()
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too high to cast this spell ({self.humanity_max})!{BC.OFF}")

# Creation
class Flashbang(CreationSpell):
    name = "Flashbang"
    mana_cost = 3
    humanity_min = -5
    description = f"Temporarily blind your enemies in the area of effect (>{humanity_min}) [{mana_cost}]."
    rounds = 5
    targets = "caster"
    original_see = {}

    def _cast(self):
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

class Caltrops(CreationSpell):
    """Area of effect spell that causes enemies to fall down."""
    name = "Caltrops"
    mana_cost = 5
    humanity_min = -10
    description = f"Causes enemies to fall. (>{humanity_min}) [{mana_cost}]"
    rounds = 5
    targets = "caster"


    def __init__(self, *args, **kwargs):
        self.legs = {}
        super().__init__(*args, **kwargs)

    def _cast(self):
        self.update()
        print(f"{BC.MAGENTA}Enchanted caltrops scatter themselves across the floor.{BC.OFF}")
        return True

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


class GrowTreeOfLife(CreationSpell):
    name = "Grow Tree of Life"
    mana_cost = 10
    humanity_min = 2
    description = f"A tree with healing fruit grows from the floor (>{humanity_min}) [{mana_cost}]."
    rounds = 1
    targets = "caster"

    def _cast(self):
        import wizard.furniture as fur

        tree_of_life = fur.TreeOfLife(color=random.choice(fur.TreeOfLife.color), texture=random.choice(fur.TreeOfLife.texture))
        self.caster.location.elements.append(tree_of_life)
        print(f"{BC.MAGENTA}A beautiful tree with shiny silver fruits sprouts up out of the ground!{BC.OFF}")
        return True


class SummonCerberus(CreationSpell):
    name = "Summon Cerberus"
    mana_cost = 5
    humanity_min = 1
    description = f"Summons a three headed dog to aid you (>{humanity_min}) [{mana_cost}]."
    rounds = 1
    targets = "caster"

    def _cast(self):
        """This is useful if you want to test combat magic on an opponent."""
        cerberus = assets.dog.Cerberus(location=self.target.location)
        cerberus.mana_cost = self.mana_cost
        cerberus.team = self.caster.team
        self.target.location.creatures.append(cerberus)
        self.caster.companions.append(cerberus)
        print(f"{BC.MAGENTA}A {C.RED}cerberus{BC.MAGENTA} pops into existence!{BC.OFF}")
        return True


class SummonSpider(CreationSpell):
    name = "Summon Spider"
    mana_cost = 5
    humanity_min = 0
    description = f"Summons an enemy spider (>{humanity_min}) [{mana_cost}]."
    rounds = 1
    targets = "caster"

    def _cast(self):
        """This is useful if you want to test combat magic on an opponent."""
        spider = giant_spider.GiantSpider(location=self.target.location)
        spider.mana_cost = self.mana_cost
        self.target.location.creatures.append(spider)
        print(f"{BC.MAGENTA}A {C.RED}giant spider{BC.MAGENTA} pops into existence!{BC.OFF}")
        return True


class SummonTentacleMonster(CreationSpell):
    name = "Summon Tentacle Monster"
    mana_cost = 10
    humanity_min = 5
    description = f"Summons a friendly tentacle monster (>{humanity_min}) [{mana_cost}]."
    rounds = 1
    targets = "caster"

    def _cast(self):
        tm = tentacle_monster.TentacleMonster(location=self.target.location)
        tm.team = self.caster.team
        tm.mana_cost = self.mana_cost
        self.tm = tm
        self.target.location.creatures.append(tm)
        self.caster.companions.append(tm)
        print(f"{BC.MAGENTA}A {C.RED}giant tentacle monster{BC.MAGENTA} pops into existence!{BC.OFF}")
        return True

    # TODO-DECIDE I really want permanent summons. Think of a way to do it that isn't brokenly unbalanced or awful.
    #  or at least, make them die instead of disappear.
    # def expire(self):
    #     print(f"{BC.MAGENTA}The tentacle monster winks out of existence.{BC.OFF}")
    #     self.caster.companions.remove(self.tm)
    #     self.tm.location.creatures.remove(self.tm)


# TODO-DONE bug will occur if creature dies wearing the armor (it'll be available to be picked up).
#  possible fix- set gear to be deleted by creature.die(). But what if a limb is chopped off?
class ArmorOfLight(CreationSpell):
    name = "Light Armor"
    mana_cost = 5
    humanity_min = -5
    description = f"Conjures a set of armor made of light (>{humanity_min}) [{mana_cost}]."
    rounds = 20
    targets = "friendly"
    equipped = {}

    def find_all_equipped(self):
        # Store the equipment information. We need to make sure equipment will be removed on expire even if limbs are chopped off.
        for equipment_type in set(su.lightsuit["wears"].values()):
            for limb in self.target.subelements[0].limb_check("name"):
                for gear in limb.equipment:
                    if isinstance(gear, equipment_type):
                        if limb in self.equipped.keys():
                            # Everything on the limb that needs to be unequipped on expire
                            self.equipped[limb].append(gear)
                        else:
                            self.equipped[limb] = [gear]

    def _cast(self):
        old_suits = self.target.suits
        self.target.suits = [su.lightsuit]
        # Puts the armor on the target
        self.target._clothe()
        self.find_all_equipped()
        self.target.suits = old_suits
        print(f"{BC.MAGENTA}A glowing suit of armor envelops {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")
        return True

    def expire(self):
        for limb in self.equipped.keys():
            for gear in self.equipped[limb]:
                limb.unequip(gear, force_off=True)
        print(f"{BC.MAGENTA}The glowing armor on {C.RED}{self.target.name}{BC.MAGENTA} fades away and disappears.{BC.OFF}")


# Corruption
class Light(CorruptionSpell):
    name = "Light"
    mana_cost = 3
    humanity_max = 10
    description = f"A glow surrounds a creature, making it easier to hit (<{humanity_max}) [{mana_cost}]."
    rounds = 10
    targets = "enemy"

    def _cast(self):
        self.original_colors = {}
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            self.original_colors[limb] = limb.color
            limb.color = f"luminous {limb.color}"
            limb.size += 1
        print(f"{BC.MAGENTA}A luminous glow surrounds {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")
        return True

    def expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            if limb in self.original_colors.keys():
                limb.color = self.original_colors[limb]
                limb.size -= 1
        print(f"{BC.MAGENTA}The glow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")

class Shadow(CorruptionSpell):
    name = "Shadow"
    mana_cost = 3
    humanity_max = 10
    description = f"A shadow surrounds a creature, making it harder to hit (<{humanity_max}) [{mana_cost}]."
    rounds = 10
    targets = "friendly"
    original_colors = None
    original_sizes = None

    def _cast(self):
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

    def expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            if limb in self.original_colors.keys():
                limb.color = self.original_colors[limb]
                limb.size = self.original_sizes[limb]
        print(f"{BC.MAGENTA}The shadow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")

# TODO-DECIDE rework innocence so player can't cast magic or attack? Hard to code.
# class Innocence(CorruptionSpell):
#     name = "Innocence"
#     mana_cost = 3
#     humanity_max = 5
#     description = f"Target will appear harmless to their enemies (>{humanity_max}) [{mana_cost}]."
#     rounds = 10
#     targets = "friendly"
#     original_team = None
#
#     def _cast(self):
#         if self.target.team != "neutral":
#             self.original_team = self.target.team
#             self.target.team = "neutral"
#             return True
#         else:
#             print(f"{BC.YELLOW}{self.target.name}{BC.MAGENTA} is already neutral!{BC.OFF}")
#             return False
#
#     def expire(self):
#         self.target.team = self.original_team
#         print(f"{BC.YELLOW}{self.target.name}{BC.MAGENTA} suddenly appears quite menacing!{BC.OFF}")


class GraftLimb(CorruptionSpell):
    name = "Graft Limb"
    mana_cost = 10
    humanity_max = 0
    description = f"Graft a disembodied limb onto a friendly creature (<{humanity_max}) [{mana_cost}]."
    rounds = 1
    targets = "friendly"

    def _cast(self):
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
                    # Lowers humanity, if target is appropriate
                    if hasattr(self.target, "humanity"):
                        self.target.humanity -= 1
                    return True
        return False


class ReanimateLimb(CorruptionSpell):
    name = "Reanimate"
    mana_cost = 5
    humanity_max = 5
    description = f"Reanimates a dead creature as a zombie (<{humanity_max}) [{mana_cost}]."
    rounds = 1
    targets = "caster"

    def _cast(self):
        """Bring a limb in the room back to life."""
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
                zombie.mana_cost = self.mana_cost
                self.caster.location.addCreature(zombie)
                self.caster.companions.append(zombie)
                print(f"{C.RED}{zombie.name}{BC.MAGENTA} rises from the dead with a moan!{BC.OFF}")
                return True


class FleshRip(CorruptionSpell):
    name = "Flesh Rip"
    mana_cost = 5
    humanity_max = -2
    description = f"Rip a small limb off of an enemy (<{humanity_max}) [{mana_cost}]."
    rounds = 1
    targets = "enemy"

    def _cast(self):
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


# TODO set mana cost on creature- how to do it fairly?
class Enthrall(CorruptionSpell):
    name = "Enthrall"
    mana_cost = 7
    humanity_max = -5
    description = f"Force an enemy to fight for you for a little while (<{humanity_max}) [{mana_cost}]."
    rounds = 15
    targets = "enemy"
    old_team = None

    def _cast(self):
        self.old_team = self.target.team
        self.target.team = self.caster.team
        self.target.ai.target = None
        print(f"{BC.YELLOW}{self.target.name}{BC.MAGENTA} turns around to fight for your team!{BC.OFF}")
        return True

    def expire(self):
        self.target.team = self.old_team
        self.target.ai.target = None
        print(f"{BC.MAGENTA}The enthralling wears off and {BC.YELLOW}{self.target.name}{BC.MAGENTA} turns against you again.{BC.OFF}")

# TODO should work on friendly targets too
class Distract(CorruptionSpell):
    name = "Disorient"
    mana_cost = 5
    humanity_max = 7
    description = f"Confuse an enemy and focus them on a new target (<{humanity_max}) [{mana_cost}]."
    rounds = 1
    targets = "enemy"

    def _cast(self):
        self.target.ai.target = None
        print(f"{BC.YELLOW}{self.target.name}{BC.MAGENTA} is distracted!{BC.OFF}")


# Neither
class Scry(sp.Spell):
    name = "Scry"
    mana_cost = 1
    description = f"See what is happening in a nearby room [{mana_cost}]."
    rounds = 1
    targets = "caster"

    def _cast(self):
        borders = self.caster.location.borders.copy()
        borders["x"] = "Cancel"
        utils.dictprint(borders)
        i = input(f"{BC.MAGENTA}Which room would you like to scry?{BC.OFF} ")

        if i in borders.keys() and borders[i] is not None and i != "x":
            print(borders[i].desc(full=False))
        return True


class AWayHome(sp.Spell):
    name = "A Way Home"
    mana_cost = 5
    description = f"Manifests the door to your home. [{mana_cost}]"
    rounds = 1
    targets = "caster"

    # TODO-DONE test once we have two levels
    def _cast(self):
        """Creates a door between current location and the pocket apartment. Door will move whenever this spell is cast."""
        door = [x for x in self.caster.home.start.elements if x.name == "magic door"][0]
        if not door.borders:
            # If this is the first time this spell is called, the door will be present in the foyer but not set up as a door yet.
            door.addBorder(self.caster.home.start)

        # We don't want to lock you into the apartment or overwrite another door.
        if self.caster.location.level != self.caster.home.start.level and not self.caster.location.borders[">"]:
            # TODO-DONE test moving the door
            if len(door.borders) > 1:
                # Remove door from old location
                old_room = door.borders[1]
                door.borders.remove(old_room)
                old_room.removeElement(door)
                old_room.get_borders()

            door.addBorder(self.caster.location)
            self.caster.location.addElement(door)
            self.caster.home.start.get_borders()
            self.caster.location.get_borders()

            print(f"{BC.MAGENTA}A shimmering door of light appears before you.{BC.OFF}")
            return True
        else:
            print(f"{BC.MAGENTA}You cannot cast that spell here.{BC.OFF}")


class GrowBeard(sp.Spell):
    name = "Grow Long Beard"
    mana_cost = 5
    description = f"Grow a long flowing beard worthy of a powerful wizard[{mana_cost}]."
    rounds = 1
    targets = "caster"

    def _cast(self):
        import assets.commonlimbs as cl

        limbs = self.target.subelements[0].limb_check("name")
        heads = [x for x in limbs if x.name == "head"]
        if heads:
            # We want a random head, not the first one each time
            random.shuffle(heads)
            head = heads[0]
            existing_beards = [x for x in head.subelements if x.name == "beard"]
            if existing_beards:
                # Cut existing beard(s) (should be max one but we'll be thorough)
                for beard in existing_beards:
                    head.remove_limb(beard)
            head.subelements.append(cl.Beard(color="white", texture="luxuriant"))
            print(f"{BC.MAGENTA}A long flowing beard erupts from {BC.YELLOW}{self.target.name}{BC.MAGENTA}'s face!{BC.OFF}")


class ReleaseMinion(sp.Spell):
    name = "Release Minion"
    mana_cost = 0
    description = "Release one of your minions from your mental control."
    rounds = 1
    targets = "caster"

    def _cast(self):
        minions = utils.listtodict([x for x in self.caster.companions if not hasattr(x, "familiar")], add_x=True)
        utils.dictprint(minions)
        i = input(f"{BC.MAGENTA}Select a minion to release from your mental control: {BC.OFF}")
        if i in minions.keys() and i != "x":
            minion = minions[i]
            minion.team = "neutral"
            self.caster.companions.remove(minion)
            print(f"{BC.YELLOW}{minion.name}{BC.MAGENTA} stops following you.{BC.OFF}")
            return True
        return False


class SetHumanity(sp.Spell):
    name = "Set Humanity"
    mana_cost = 0
    description = f"Cheat and set your humanity to whatever you want [{mana_cost}]."
    rounds = 5
    targets = "caster"
    original_humanity = None

    def _cast(self):
        self.original_humanity = self.caster.humanity
        self.caster.humanity = int(input(f"{BC.MAGENTA}Set your humanity: {BC.OFF}"))
        return True

    def expire(self):
        print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity returns to its normal value.{BC.OFF}")
        self.caster.humanity = self.original_humanity


# TODO-DONE graft limb- graft a disembodied limb onto a friendly creature
# TODO-DONE grow beard spell
# TODO fireball- DOT
# TODO transform yourself into a monster temporarily (or permanently)
# TODO summon an ethereal hand with a glowing sword
# TODO-DONE enthrall- an enemy creature joins your side
# TODO lightning- damages a few neighboring limbs and has a chance to jump to another enemy
# TODO conjure flaming sword for yourself
# TODO-DONE disguise as another class (sneak through areas)
# TODO sword hands
# TODO-DONE mana costs
# TODO-DONE Manifest portal to apartment
# TODO-DONE scrolls to learn spells (eat() for now)
# TODO-DONE distract- enemy chooses a new target (may choose same one again though)
# TODO-DONE mana max reduced to maintain minions.
# TODO weapon effects (inherit from spells)
# TODO spell of tunneling- makes a tunnel to the next level in current room
# TODO-DONE store maintenance costs for summoned creatures in a tag on the creature themselves.
