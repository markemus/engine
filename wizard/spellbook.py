import math
import random

import engine.creature as cr
import engine.spells as sp
import engine.styles
import engine.utils as utils

import assets.commonlimbs as cl
import assets.dog

import engine.effectsbook as eff
import wizard.suits as su
import wizard.zombie as z

from wizard import ethereal_hand
from wizard import giant_spider
from wizard import fairy
from wizard import owlbear
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
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too low to cast this spell! {C.BLUE}({self.caster.humanity}/{self.humanity_min}){BC.OFF}")


class CorruptionSpell(sp.Spell):
    """A spell that requires corruptive powers and therefore requires a low humanity to cast.
    Subclasses must set humanity_max."""
    humanity_max = None

    def cast(self):
        if self.caster.humanity <= self.humanity_max:
            return super().cast()
            # return self._cast()
        else:
            print(f"{C.RED}{self.caster.name}{BC.MAGENTA}'s humanity is too high to cast this spell! {C.RED}({self.caster.humanity}/{self.humanity_max}){BC.OFF}")


# Creation
class Shadow(CreationSpell):
    name = "Shadow"
    mana_cost = 3
    humanity_min = -5
    description = f"A shadow surrounds a creature, making it harder to hit. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 10
    targets = "friendly"
    original_colors = None
    original_sizes = None

    def _cast(self):
        self.original_colors = {}
        self.original_sizes = {}
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            shadow = eff.Shadow(creature=self.target, limb=limb, controller=self.cont)
            shadow.cast()

        print(f"{BC.MAGENTA}A shadowy gloom surrounds {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")
        return True

    def _expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            effect = [x for x in limb.active_effects if isinstance(x, eff.Shadow)]
            if effect:
                effect = effect[0]
                effect.expire()

        print(f"{BC.MAGENTA}The shadow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")

# TODO this should work on limbs with strength tag, not arms and legs
class Might(CreationSpell):
    name = "Might"
    mana_cost = 5
    humanity_min = -3
    description = f"Make an ally stronger. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "friendly"

    def _cast(self):
        print(f"{BC.MAGENTA}{self.target.name} grows stronger before your eyes!{BC.MAGENTA}")
        limbs = self.target.subelements[0].limb_check("wears")
        for limb in limbs:
            # print(limb.name)
            # limb_wears = [k for k in limb.wears.keys() if limb.wears[k]]
            # if set(limb_wears).intersection({"arm", "animal_leg"}):
            if limb.wears in ["arm", "animal_leg"]:
                might = eff.Might(creature=self.target, limb=limb, controller=self.cont)
                might.cast()
        return True


class Mastery(CreationSpell):
    name = "Mastery"
    mana_cost = 7
    humanity_min = 5
    description = f"Make an ally fight better. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "friendly"

    def _cast(self):
        print(f"{BC.MAGENTA}{self.caster.name} lays their thrumming hands on {self.target.name}.{BC.MAGENTA}")
        mastery = eff.Mastery(creature=self.target, limb=self.target.subelements[0], controller=self.cont)
        mastery.cast()
        return True



class FlamingWeapons(CreationSpell):
    name = "Flaming Weapons"
    mana_cost = 5
    humanity_min = -3
    description = f"Wreath a creature's weapons in magical fire. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = "forever"
    targets = "friendly"
    weapons = []

    def _cast(self):
        weapons = self.cont.combat.get_weapons(self.target, include_webbed=True)
        for weapon in weapons:
            weapon = weapon.damage[1]
            # print(weapon)
            if eff.FireDOT not in weapon.weapon_effects:
                weapon.weapon_effects.append(eff.FireDOT)
                self.weapons.append(weapon)
                print(f"{BC.MAGENTA}Magical flames spring out on {self.target.name}'s {weapon.name}!{BC.OFF}")

        return True

    def _expire(self):
        for weapon in self.weapons:
            weapon.weapon_effects.remove(eff.FireDOT)
            print(f"{BC.MAGENTA}The magical flames on {weapon.name} go out.{BC.OFF}")


class PoisonedWeapons(CreationSpell):
    name = "Poisoned Weapons"
    mana_cost = 5
    humanity_min = -3
    description = f"Cover a creature's weapons in magical poison. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = "forever"
    targets = "friendly"
    weapons = []

    def _cast(self):
        weapons = self.cont.combat.get_weapons(self.target, include_webbed=True)
        for weapon in weapons:
            weapon = weapon.damage[1]
            # print(weapon)
            if eff.Poison not in weapon.weapon_effects:
                weapon.weapon_effects.append(eff.Poison)
                self.weapons.append(weapon)
                print(f"{BC.MAGENTA}Green poison spreads across {self.target.name}'s {weapon.name}!{BC.OFF}")
        return True

    def _expire(self):
        for weapon in self.weapons:
            weapon.weapon_effects.remove(eff.Poison)
            print(f"{BC.MAGENTA}The poison on {weapon.name} dries up and disappears.{BC.OFF}")


class Bleeding(CreationSpell):
    name = "Bleeding"
    mana_cost = 5
    humanity_min = -3
    description = f"Cover a creature's weapons in an anti-coagulating fluid. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = "forever"
    targets = "friendly"
    weapons = []

    def _cast(self):
        weapons = self.cont.combat.get_weapons(self.target, include_webbed=True)
        for weapon in weapons:
            weapon = weapon.damage[1]
            if eff.Bleed not in weapon.weapon_effects:
                weapon.weapon_effects.append(eff.Bleed)
                self.weapons.append(weapon)
                print(f"{BC.MAGENTA}A red liquid spreads across {self.target.name}'s {weapon.name}!{BC.OFF}")
        return True

    def _expire(self):
        for weapon in self.weapons:
            weapon.weapon_effects.remove(eff.Bleed)
            print(f"{BC.MAGENTA}The red liquid on {weapon.name} dries up and disappears.{BC.OFF}")


class Flashbang(CreationSpell):
    name = "Flashbang"
    mana_cost = 3
    humanity_min = -5
    description = f"Temporarily blind your enemies in the area of effect. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
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

    def _expire(self):
        for eye in self.original_see.keys():
            eye.see = self.original_see[eye]
            print(f"{BC.CYAN}{eye.name}{BC.MAGENTA} can see again.{BC.OFF}")

class Caltrops(CreationSpell):
    """Area of effect spell that causes enemies to fall down."""
    name = "Caltrops"
    mana_cost = 5
    humanity_min = -10
    description = f"Causes enemies to fall. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
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

    def _expire(self):
        self._fix_legs()


class Lightning(CreationSpell):
    """Lightning strikes an enemy and has a chance to jump to other enemies."""
    name = "Lightning"
    mana_cost = 5
    humanity_min = -5
    description = f"Lightning strikes an enemy and jumps to other enemies. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "enemy"

    def _cast(self):
        cc = self.cont.combat
        l_damage = 4

        limbs = utils.listtodict(self.target.subelements[0].limb_check("isSurface"), add_x=True)
        utils.dictprint(limbs)
        i = input("Select a limb to shoot lightning at: ")

        if i in limbs.keys() and i != "x":
            # Other limbs to strike from same target
            other_limbs_to_strike = self.target.get_neighbors(limbs[i])
            if other_limbs_to_strike:
                other_limbs_to_strike = other_limbs_to_strike[:random.randrange(0, len(other_limbs_to_strike))]
            print(f"{BC.MAGENTA}Lightning arcs across the room and strikes {BC.YELLOW}{self.target.name}{BC.MAGENTA}'s {C.RED}{limbs[i].name}{BC.MAGENTA}!{BC.OFF}")
            cc.apply_damage(self.target, limbs[i], l_damage)

            for limb in other_limbs_to_strike:
                print(f"{BC.MAGENTA}Lightning spreads through {C.RED}{limb.name}{BC.MAGENTA}!{BC.OFF}")
                cc.apply_damage(self.target, limb, l_damage)

            # Other limbs to strike from other targets
            other_targets = [c for c in self.target.location.creatures if c.team not in [self.caster.team, "neutral"] and c is not self.target]
            if other_targets:
                other_targets = other_targets[:random.randrange(0, len(other_targets))]
                for ot in other_targets:
                    jump_limb = random.choice(ot.subelements[0].limb_check("isSurface"))
                    random_neighbors = ot.get_neighbors(jump_limb)
                    print(f"{BC.MAGENTA}Lightning jumps to {BC.YELLOW}{ot.name}{BC.MAGENTA}'s {C.RED}{jump_limb.name}{BC.MAGENTA}!{BC.OFF}")
                    cc.apply_damage(ot, jump_limb, l_damage)

                    random_neighbors = random_neighbors[:random.randrange(0, len(random_neighbors))]
                    for r_limb in random_neighbors:
                        print(f"{BC.MAGENTA}Lightning spreads through {C.RED}{r_limb.name}{BC.MAGENTA}!{BC.OFF}")
                        cc.apply_damage(ot, r_limb, l_damage)
            print(f"{BC.MAGENTA}The lightning goes out, leaving a searing afterimage.{BC.OFF}")
            return True


class Fireball(CreationSpell):
    """Lightning strikes an enemy and has a chance to jump to other enemies."""
    name = "Fireball"
    mana_cost = 7
    humanity_min = -5
    description = f"A fireball lights an enemy on fire. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "enemy"

    def _cast(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            if not sum([isinstance(e, eff.FireDOT) for e in limb.active_effects]):
                fire = eff.FireDOT(creature=self.target, limb=limb, controller=self.cont)
                fire.cast()
        print(f"{BC.MAGENTA}A gigantic fireball flies across the room and explodes on {self.target.name}!{BC.OFF}")
        return True


class TheFloorIsLava(CreationSpell):
    name = "The Floor is Lava"
    mana_cost = 7
    humanity_min = -5
    description = f"Set the ground on fire. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 20
    targets = "caster"

    def _cast(self):
        print(f"{BC.MAGENTA}The ground beneath your feet bursts into magical flames!{BC.OFF}")
        return True

    def update(self):
        enemies = [x for x in self.caster.location.creatures if x.team != self.caster.team and x.team != "neutral"]
        for enemy in enemies:
            # Flying enemies are unaffected
            if enemy.limb_count("flight") >= 1:
                limbs = []
            # Standing enemies only have their feet burnt
            elif enemy.limb_count("amble") >= 1:
                limbs = enemy.subelements[0].limb_check("amble")
            # Prone enemies catch fire everywhere.
            else:
                limbs = enemy.subelements[0].limb_check("isSurface")
            for limb in limbs:
                if not sum([isinstance(e, eff.FireDOT) for e in limb.active_effects]):
                    fire = eff.FireDOT(creature=enemy, limb=limb, controller=self.cont)
                    fire.cast()

    def _expire(self):
        print(f"{BC.MAGENTA}The flames covering the ground go out.{BC.MAGENTA}")


class GrowTreeOfLife(CreationSpell):
    name = "Grow Tree of Life"
    mana_cost = 10
    humanity_min = 2
    description = f"A tree with healing fruit grows from the floor. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
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
    mana_cost = 7
    humanity_min = -3
    description = f"Summons a three headed dog to aid you. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        """A giant friendly dog with three heads."""
        cerberus = assets.dog.Cerberus(location=self.target.location)
        cerberus.subelements[0].mana_cost = self.mana_cost
        cerberus.team = self.caster.team

        print(f"{BC.MAGENTA}A loyal {C.RED}cerberus{BC.MAGENTA} appears!{BC.OFF}")
        self.target.location.addCreature(cerberus)
        self.caster.companions.append(cerberus)

        if hasattr(self.target, "humanity"):
            self.target.humanity += 1
            print(f"{C.RED}{self.target.name}'s humanity increases!{C.OFF}")
        return True


class SummonSpider(CreationSpell):
    name = "Summon Spider"
    mana_cost = 8
    humanity_min = 0
    description = f"Summons a giant friendly spider. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        spider = giant_spider.GiantSpider(location=self.target.location)
        spider.subelements[0].mana_cost = self.mana_cost
        spider.team = self.caster.team

        print(f"{BC.MAGENTA}A {C.RED}giant spider{BC.MAGENTA} appears!{BC.OFF}")
        self.target.location.addCreature(spider)
        self.caster.companions.append(spider)

        if hasattr(self.target, "humanity"):
            self.target.humanity += 1
            print(f"{C.RED}{self.target.name}'s humanity increases!{C.OFF}")
        return True

class SummonEtherealHand(CreationSpell):
    name = "Summon Ethereal Hand"
    mana_cost = 8
    humanity_min = 3
    description = f"Summons a flying hand holding a shining blade. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        """A giant friendly dog with three heads."""
        hand = ethereal_hand.EtherealHand(location=self.target.location)
        hand.subelements[0].mana_cost = self.mana_cost
        hand.team = self.caster.team

        print(f"{BC.MAGENTA}A flying {C.RED}ethereal hand{BC.MAGENTA} appears!{BC.OFF}")
        self.target.location.addCreature(hand)
        self.caster.companions.append(hand)

        if hasattr(self.target, "humanity"):
            self.target.humanity += 1
            print(f"{C.RED}{self.target.name}'s humanity increases!{C.OFF}")
        return True

class SummonTentacleMonster(CreationSpell):
    name = "Summon Tentacle Monster"
    mana_cost = 12
    humanity_min = 7
    description = f"Summons a friendly tentacle monster. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        tm = tentacle_monster.TentacleMonster(location=self.target.location)
        tm.team = self.caster.team

        print(f"{BC.MAGENTA}A gigantic {C.RED}tentacle monster{BC.MAGENTA} appears!{BC.OFF}")
        self.target.location.addCreature(tm)

        return True


class SummonFairy(CreationSpell):
    name = "Summon Fairy"
    mana_cost = 8
    humanity_min = 8
    description = f"Summons a tiny fairy to aid you. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        f = fairy.Fairy(location=self.target.location)
        f.subelements[0].mana_cost = self.mana_cost
        f.team = self.caster.team

        print(f"{BC.MAGENTA}A tiny {C.RED}fairy{BC.MAGENTA} appears!{BC.OFF}")
        self.target.location.addCreature(f)
        self.caster.companions.append(f)

        if hasattr(self.target, "humanity"):
            self.target.humanity += 1
            print(f"{C.RED}{self.target.name}'s humanity increases!{C.OFF}")
        return True


class SummonOwlbear(CreationSpell):
    name = "Summon Owlbear"
    mana_cost = 15
    humanity_min = 12
    description = f"Summons a giant owlbear to aid you. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        o = owlbear.Owlbear(location=self.target.location)
        o.subelements[0].mana_cost = self.mana_cost
        o.team = self.caster.team

        print(f"{BC.MAGENTA}A gigantic {C.RED}owlbear{BC.MAGENTA} appears!{BC.OFF}")
        self.target.location.addCreature(o)
        self.caster.companions.append(o)

        if hasattr(self.target, "humanity"):
            self.target.humanity += 1
            print(f"{C.RED}{self.target.name}'s humanity increases!{C.OFF}")
        return True



class SummonExcalibur(CreationSpell):
    name = "Summon Excalibur"
    mana_cost = 15
    humanity_min = 10
    description = f"Summons a beautiful and powerful sword. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        hands = self.caster.subelements[0].limb_check("grasp")
        hands = utils.listtodict([h for h in hands if not h.grasped], add_x=True)
        utils.dictprint(hands)
        i = input(f"{BC.GREEN}Raise a hand to summon Excalibur: {BC.OFF}")
        if i in hands.keys() and i != "x":
            hand = hands[i]

            if not hasattr(self.cont, "excalibur"):
                self.cont.excalibur = su.Excalibur("shining", "steel")

            for level in self.cont.game.level_list:
                for room in level.roomLocations.keys():
                    for inv in room.find_invs():
                        if self.cont.excalibur in inv.vis_inv:
                            inv.vis_inv.remove(self.cont.excalibur)
                            print(f"{BC.MAGENTA}Excalibur disappears from {room.name}'s {inv.name}.{BC.OFF}")
                    for creature in room.creatures:
                        for inv in creature.subelements[0].find_invs():
                            if self.cont.excalibur in inv.vis_inv:
                                inv.vis_inv.remove(self.cont.excalibur)
                                print(f"{BC.MAGENTA}Excalibur disappears from {creature.name}'s {inv.name}.{BC.OFF}")
                        for grasper in creature.subelements[0].limb_check("grasp"):
                            if self.cont.excalibur is grasper.grasped:
                                grasper.grasped = None
                                print(f"{BC.MAGENTA}Excalibur disappears from {creature.name}'s {grasper.name}.{BC.OFF}")

            print(f"{BC.MAGENTA}Excalibur appears in {self.caster.name}'s {hand.name}!{BC.OFF}")
            if not hand.grasped and (hand.limb_count("f_grasp") >= 1) and (hand.limb_count("t_grasp") >= 1):
                hand.grasped = self.cont.excalibur
            else:
                self.caster.location.drop_item(self.cont.excalibur)
            return True


# class Trapdoor(CreationSpell):
#     name = "Trapdoor"
#     mana_cost = 10
#     humanity_min = 0
#     description = f"Creates a trapdoor to descend downward into the depths. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
#     rounds = 1
#     targets = "caster"
#
#     def _cast(self):
#         level_index = self.cont.game.level_list.index(self.cont.game.current_level)
#         if level_index + 1 < len(self.cont.game.level_list):
#             next_level = self.cont.game.level_list[level_index + 1]
#
#             next_level_rooms = list(next_level.roomLocations.keys())
#             next_level_rooms.remove(next_level.start)
#             next_level_rooms.remove(next_level.end)
#
#             next_room = random.choice(next_level_rooms)
#             if not self.caster.location.borders[">"]:
#                 door = engine.styles.door(color="brown", texture="wood")
#                 door.addBorder(self.caster.location)
#                 door.addBorder(next_room)
#                 self.caster.location.addElement(door)
#                 next_room.addElement(door)
#                 self.caster.location.get_borders()
#                 next_room.get_borders()
#                 print(f"{BC.MAGENTA}A doorway appears leading down into the depths!{BC.OFF}")
#                 return True
#             else:
#                 print(f"{BC.MAGENTA}There is no space for a doorway here.{BC.OFF}")
#                 return False
#         else:
#             print(f"{BC.MAGENTA}You have reached rock bottom already.{BC.OFF}")
#             return False


class ArmorOfLight(CreationSpell):
    name = "Light Armor"
    mana_cost = 5
    humanity_min = -5
    description = f"Conjures a set of armor made of light. {C.BLUE}(>{humanity_min}) {BC.CYAN}[{mana_cost}]{C.OFF}"
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

    def _expire(self):
        for limb in self.equipped.keys():
            for gear in self.equipped[limb]:
                limb.unequip(gear, force_off=True)
        print(f"{BC.MAGENTA}The glowing armor on {C.RED}{self.target.name}{BC.MAGENTA} fades away and disappears.{BC.OFF}")


# Corruption
class Light(CorruptionSpell):
    name = "Light"
    mana_cost = 3
    humanity_max = 10
    description = f"A glow surrounds a creature, making it easier to hit. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 10
    targets = "enemy"

    def _cast(self):
        self.original_colors = {}
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            halo = eff.Light(creature=self.target, limb=limb, controller=self.cont)
            halo.cast()

        print(f"{BC.MAGENTA}A luminous glow surrounds {C.RED}{self.target.name}{BC.MAGENTA}.{BC.OFF}")
        return True

    def _expire(self):
        limbs = self.target.subelements[0].limb_check("isSurface")
        for limb in limbs:
            effect = [x for x in limb.active_effects if isinstance(x, eff.Light)]
            if effect:
                effect = effect[0]
                effect.expire()

        print(f"{BC.MAGENTA}The glow surrounding {C.RED}{self.target.name}{BC.MAGENTA} fades away.{BC.OFF}")


class GrowFangs(CorruptionSpell):
    name = "Grow Fangs"
    mana_cost = 5
    humanity_max = -3
    description = f"Turn your teeth into powerful vampiric weapons. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def no_fangs(self, head):
        fangs = [x for x in head.subelements if x.name == "fangs"]
        if not fangs:
            return True

    def _cast(self):
        import assets.commonlimbs as cl

        limbs = self.target.subelements[0].limb_check("name")
        jaws = [x for x in limbs if x.name in ["jaw", "mouth", "maw", "snout"]]
        if jaws:
            # We want a random head, not the first one each time
            random.shuffle(jaws)
            # We need a jaw with no fangs (teeth are fine)
            fangless_jaws = [x for x in jaws if self.no_fangs(x)]
            if fangless_jaws:
                jaw = fangless_jaws[0]

                existing_teeth = [x for x in jaw.subelements if x.name == "teeth"]
                if existing_teeth:
                    # existing teeth fall out
                    for teeth in existing_teeth:
                        jaw.remove_limb(teeth)
                        print(f"{BC.MAGENTA}{self.target.name}'s old teeth fall out of their mouth.{BC.OFF}")
                        self.target.location.drop_item(teeth)

                # We need to define a subclass for the caster
                class CVampirism(eff.Vampirism):
                    vampire = self.caster
                class CVampireFangs(cl.VampireFangs):
                    weapon_effects = [CVampirism]

                jaw.subelements.append(CVampireFangs(color="sharp", texture="white"))
                print(f"{BC.MAGENTA}Long sharp teeth erupt from {BC.YELLOW}{self.target.name}{BC.MAGENTA}'s jaws!{BC.OFF}")
                if hasattr(self.target, "humanity"):
                    self.target.humanity -= 1
                    print(f"{C.RED}{self.target.name}'s humanity decreases!{C.OFF}")
                return True
            else:
                print(f"{BC.MAGENTA}{self.target.name} has no jaws.")


class SwordHand(CorruptionSpell):
    name = "Sword Hand"
    mana_cost = 15
    humanity_max = -12
    description = f"Transform one of your hands into a gigantic sword. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        hands = utils.listtodict([h for h in self.target.subelements[0].limb_check("wears") if h.wears == "right hand" or h.wears == "left hand"], add_x=True)
        utils.dictprint(hands)
        i = input("Select a hand to transform: ")
        if i in hands.keys() and i != "x":
            hand = hands[i]
            # Drop grasped and equipment to the floor
            if hand.grasped:
                self.target.location.drop_item(hand.grasped)
                hand.grasped = None
            # Get equipment for all fingers and drop that too
            for limb in hand.limb_check("name"):
                for gear in limb.equipment:
                    if limb.unequip(gear):
                        self.target.location.drop_item(gear)
            # Check we still have enough mana for the spell after removing gear
            enough_mana = self.caster.check_siphon_tag("mana", self.mana_cost)
            if enough_mana:
                arm = self.target.subelements[0].get_parents(hand)[-2]
                self.target.remove_limb(hand)
                swordhand = cl.SwordHand(color="white", texture="bone")
                arm.subelements.append(swordhand)
                print(f"{BC.MAGENTA}{self.target.name}'s {hand.name} transforms into a magnificent {swordhand.name}!{BC.OFF}")
                if hasattr(self.target, "humanity"):
                    self.target.humanity -= 1
                    print(f"{C.RED}{self.target.name}'s humanity decreases!{C.OFF}")
                return True
            else:
                print(f"{BC.MAGENTA}Not enough mana! The spell fizzles.{BC.OFF}")


# class TransformSpider(CorruptionSpell):
#     name = "Become Spider"
#     mana_cost = 10
#     humanity_max = -5
#     description = f"Transform yourself into a giant spider. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
#     rounds = 20
#     targets = "caster"
#     old_char = None
#
#     def _cast(self):
#         if self.caster.can_transform:
#             spider = giant_spider.GiantSpider(location=self.caster.location)
#             # Set game character to be the spider
#             self.old_char = self.caster
#             self.cont.game.char = spider
#             # Deliberately same list, not a copy, so companions will stay updated
#             spider.companions = self.old_char.companions
#             spider.name = self.old_char.name
#             spider.team = self.old_char.team
#             spider.humanity = self.old_char.humanity
#             # Reduce humanity for transforming
#             spider.humanity -= 1
#             # Make sure no other transformation overrides this one- will lead to bugs
#             spider.can_transform = False
#             # Remove old char from room and add spider
#             self.old_char.location.creatures.append(spider)
#             self.old_char.location.creatures.remove(self.old_char)
#
#             print(f"{BC.YELLOW}{self.old_char.name}{BC.MAGENTA} transforms into a {C.RED}giant spider{BC.MAGENTA}!{BC.OFF}")
#             return True
#
#     def _expire(self):
#         self.old_char.humanity = self.cont.game.char.humanity
#         spider = self.cont.game.char
#         self.cont.game.char = self.old_char
#         spider.location.creatures.append(self.old_char)
#         spider.location.creatures.remove(spider)
#         print(f"{C.RED}{self.old_char.name}{BC.MAGENTA} transforms back into a {C.RED}{self.old_char.classname}{BC.MAGENTA}.{BC.OFF}")


class CutLimb(sp.Spell):
    name = "Cut Limb"
    mana_cost = 0
    description = f"Cut a limb at a joint. {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        creature = None
        h = input(f"\n{BC.GREEN}Cut one of your limbs {BC.CYAN}(y){BC.GREEN}, a companion's limb {BC.CYAN}(c){BC.GREEN} or a disembodied limb {BC.CYAN}(o){BC.GREEN}?{BC.OFF} ")
        # Your limbs
        if h == "y":
            creature = self.caster
            limbs = utils.listtodict(self.caster.limb_check("name"), add_x=True)

        # Companion's limbs
        elif h == "c":
            creatures = utils.listtodict(self.caster.get_companions(), add_x=True)
            utils.dictprint(creatures)
            i = input(f"\n{BC.GREEN}Which creature do you want to amputate on?{BC.OFF} ")
            if i in creatures.keys() and i != "x":
                creature = creatures[i]
                limbs = utils.listtodict(creature.limb_check("name"), add_x=True)
            else:
                return False

        # Disembodied limbs
        elif h == "o":
            invs = self.caster.location.find_invs() + self.caster.subelements[0].find_invs()
            invs = utils.listtodict(invs, add_x=True)
            utils.dictprint(invs)
            i = input(f"\n{BC.GREEN}Which inventory contains the limb you want to cut?{BC.OFF} ")

            if i in invs.keys() and i != "x":
                inv = invs[i]
                limbs = utils.listtodict([item for item in inv.vis_inv if isinstance(item, cr.Limb)], add_x=True)
            else:
                return False
        else:
            print(f"{BC.MAGENTA}{self.caster.name} decides not to make any cuts.{BC.OFF}")
            return False

        # Proceed to cut limb
        utils.dictprint(limbs)
        j = input(f"\n{BC.GREEN}Select a limb to cut:{BC.OFF} ")

        if j in limbs.keys() and j != "x":
            full_limb = limbs[j]
            sublimbs = utils.listtodict(full_limb.limb_check("name"), add_x=True)
            utils.dictprint(sublimbs)
            k = input(f"\n{BC.GREEN}Select a joint to make the cut at:{BC.OFF} ")

            if k in sublimbs.keys() and k != "x":
                sublimb = sublimbs[k]
                if creature:
                    creature.remove_limb(sublimb)
                else:
                    full_limb.remove_limb(sublimb)
                self.caster.location.drop_item(sublimb)
                if creature:
                    print(
                        f"{BC.MAGENTA}{self.caster.name} cuts the {sublimb.name} off of the {creature.name}.{BC.OFF}")
                else:
                    print(f"{BC.MAGENTA}{self.caster.name} cuts the {sublimb.name} off of the {full_limb.name}.{BC.OFF}")
                return True


class GraftLimb(CorruptionSpell):
    name = "Graft Limb"
    mana_cost = 0
    humanity_max = 5
    description = f"Graft a disembodied limb onto a friendly creature. {C.RED}(<{humanity_max}) {BC.CYAN}[varies]{C.OFF}"
    rounds = 1
    targets = "friendly"

    def _cast(self):
        invs = self.caster.location.find_invs() + self.caster.subelements[0].find_invs()
        invs = utils.listtodict(invs, add_x=True)
        utils.dictprint(invs)
        i = input(f"\n{BC.GREEN}Which inventory would you like to graft from?{BC.OFF} ")

        if i in invs.keys() and i != "x":
            graft_limbs = utils.listtodict([item for item in invs[i].vis_inv if isinstance(item, cr.Limb) and not item.resurrected], add_x=True)
            utils.dictprint(graft_limbs)
            j = input(f"\n{BC.GREEN}Select a limb to graft:{BC.OFF} ")

            if j in graft_limbs.keys() and j != "x":
                graft_limb = graft_limbs[j]
                # Round down cost to two decimals
                # print([math.floor((x.size / 3) * 100) / 100 for x in graft_limb.limb_check("name")])
                mana_cost = math.floor(sum([(x.size / 3) for x in graft_limb.limb_check("name")]) * 100) / 100

                if self.caster.check_siphon_tag("mana", mana_cost):
                    m = input(f"{BC.GREEN}{graft_limb.name} will cost {mana_cost} mana to maintain, continue (y)?{BC.OFF}")

                    if m == "y":
                        target_limbs = utils.listtodict(self.target.subelements[0].limb_check("isSurface"), add_x=True)
                        utils.dictprint(target_limbs)
                        k = input(f"{BC.GREEN}Select a limb to graft onto: {BC.OFF}")

                        if k in target_limbs.keys() and k != "x":
                            target_limb = target_limbs[k]
                            target_limb.subelements.append(graft_limb)
                            invs[i].vis_inv.remove(graft_limb)
                            if graft_limb.hp < int(graft_limb.base_hp / 2):
                                graft_limb.hp = int(graft_limb.base_hp / 2)
                            # Costs mana to maintain this graft
                            # graft_limb.mana_cost = mana_cost
                            # Stop limbs from being grafted back on repeatedly- once only
                            for limb in graft_limb.limb_check("name"):
                                limb.resurrected = True
                                # limb.mana_cost = math.floor((limb.size / 3) * 100) / 100
                                limb.mana_cost = (limb.size / 3)
                                # Special case for vampirism
                                if hasattr(limb, "weapon_effects"):
                                    for weapon_effect in limb.weapon_effects:
                                        if issubclass(weapon_effect, eff.Vampirism):
                                            weapon_effect.vampire = self.target
                            print(f"{BC.MAGENTA}The {BC.CYAN}{graft_limb.name}{BC.MAGENTA} crudely grafts itself onto the {BC.CYAN}{target_limb.name}{BC.MAGENTA}!{BC.OFF}")
                            print(f"{C.RED}It will cost {mana_cost} mana to maintain this graft.{C.OFF}")
                            # Lowers humanity, if target is appropriate
                            if hasattr(self.caster, "humanity"):
                                self.caster.humanity -= 1
                                print(f"{C.RED}{self.caster.name}'s humanity decreases!{C.OFF}")
                            self.caster.siphon_tag("mana", mana_cost)
                            return True
        return False


class ReanimateLimb(CorruptionSpell):
    name = "Reanimate"
    mana_cost = 5
    humanity_max = -5
    description = f"Reanimates a dead creature as a zombie. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        """Bring a limb in the room back to life."""
        invs = self.caster.location.find_invs()
        invs = utils.listtodict(invs, add_x=True)
        utils.dictprint(invs)
        i = input(f"\n{BC.GREEN}Which inventory would you like to resurrect from?{BC.OFF} ")

        if i in invs.keys() and i != "x":
            inv = invs[i]
            limbs = utils.listtodict([item for item in inv.vis_inv if isinstance(item, cr.Limb) and not item.resurrected], add_x=True)
            utils.dictprint(limbs)
            j = input(f"\n{BC.GREEN}Select a limb to resurrect:{BC.OFF} ")

            if j in limbs.keys() and j != "x":
                limb = limbs[j]
                inv.vis_inv.remove(limb)
                zombie = z.Zombie(limb=limb, location=self.caster.location)
                zombie.team = self.caster.team
                zombie.subelements[0].mana_cost = self.mana_cost
                self.caster.location.addCreature(zombie)
                self.caster.companions.append(zombie)
                # Special case for vampirism
                for limb in zombie.limb_check("name"):
                    if hasattr(limb, "weapon_effects"):
                        for weapon_effect in limb.weapon_effects:
                            if issubclass(weapon_effect, eff.Vampirism):
                                weapon_effect.vampire = zombie
                print(f"{C.RED}{zombie.name}{BC.MAGENTA} rises from the dead!{BC.OFF}")

                # Reduces caster's humanity
                if hasattr(self.caster, "humanity"):
                    self.caster.humanity -= 1
                    print(f"{C.RED}{self.caster.name}'s humanity decreases!{C.OFF}")
                return True


class FleshRip(CorruptionSpell):
    name = "Flesh Rip"
    mana_cost = 5
    humanity_max = -2
    description = f"Rip a small limb off of an enemy. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
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


class Enthrall(CorruptionSpell):
    name = "Enthrall"
    mana_cost = 5
    humanity_max = -5
    description = f"Force an enemy to fight for you. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "enemy"

    def _cast(self):
        if hasattr(self.target, "strong_will" and self.target.strong_will):
            print(f"{C.RED}{self.target.name} cannot be dominated!{C.OFF}")
            return False

        self.target.orig_team = self.target.team
        self.target.team = self.caster.team
        self.target.subelements[0].mana_cost = self.mana_cost
        self.target.ai.target = None
        self.caster.companions.append(self.target)
        print(f"{BC.YELLOW}{self.target.name}{BC.MAGENTA} turns around to fight for your team!{BC.OFF}")
        return True


# TODO should have access to original char's mana
class Possess(CorruptionSpell):
    name = "Possess"
    mana_cost = 10
    humanity_max = -10
    description = f"Take over an enemy's body. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "enemy"

    def _cast(self):
        if hasattr(self.caster, "orig_char"):
            print(f"{BC.MAGENTA}You must return to your body before you can do that!{BC.OFF}")
            return False

        elif hasattr(self.target, "strong_will") and self.target.strong_will:
            print(f"{C.RED}{self.target.name} cannot be possessed!{C.OFF}")
            return False

        else:
            self.target.orig_team = self.target.team
            self.target.team = self.caster.team
            self.target.orig_char = self.caster
            self.target.spellbook = self.caster.spellbook.copy()
            self.target.companions = self.caster.companions.copy()
            self.target.companions.append(self.caster)
            self.target.humanity = self.caster.humanity
            self.target.spellbook.append(Unpossess)

            self.cont.game.char = self.target
            self.cont.combat.char = self.target
            print(f"{BC.MAGENTA}{self.caster.name}'s soul flies out of their body and enters {self.target.name}!{BC.OFF}")
            return True


class Unpossess(sp.Spell):
    name = "Unpossess"
    mana_cost = 0
    description = f"Return to your own body. {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        char = self.caster.orig_char
        self.caster.team = self.caster.orig_team
        self.caster.companions.remove(char)
        char.companions = self.caster.companions.copy()
        char.spellbook = self.caster.spellbook.copy()
        char.humanity = self.caster.humanity
        char.subelements[0].mana_cost = 0

        # Remove Unpossess spell from spellbook
        char.spellbook.remove(self.__class__)

        self.cont.game.char = char
        self.cont.combat.char = char
        print(f"{BC.MAGENTA}{char.name}'s soul returns to their body.{BC.OFF}")
        return True


class Meld(CorruptionSpell):
    name = "Meld"
    mana_cost = 10
    humanity_max = -15
    description = f"Meld two companions into a single creature. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        target_list = [x for x in self.caster.get_companions() if x.location == self.caster.location]
        targets = utils.listtodict(target_list, add_x=True)
        utils.dictprint(targets)
        i = input(f"{BC.GREEN}Pick a creature to meld onto: {BC.OFF}")
        if i in targets.keys() and i != "x":
            j = input(f"{BC.GREEN}Pick a creature to meld in: {BC.OFF}")
            if j in targets.keys() and j not in ["x", i]:
                base_creature = targets[i]
                other_creature = targets[j]
                limbs = other_creature.get_neighbors(other_creature.subelements[0])
                limbs = limbs[:random.randint(1, len(limbs))]
                for limb in limbs:
                    other_creature.subelements[0].remove_limb(limb)
                    # Special case for vampirism
                    if hasattr(limb, "weapon_effects"):
                        for weapon_effect in limb.weapon_effects:
                            if issubclass(weapon_effect, eff.Vampirism):
                                weapon_effect.vampire = base_creature
                base_creature.subelements[0].subelements.extend(limbs)
                base_creature.name = f"{base_creature.name}-{other_creature.name}"[:60]
                base_creature.classname = f"{base_creature.classname}-{other_creature.classname}"[:60]
                added_mana_cost = other_creature.mana_cost / 2
                base_creature.subelements[0].mana_cost += added_mana_cost
                self.caster.companions.remove(other_creature)
                self.caster.location.creatures.remove(other_creature)
                print(f"{BC.MAGENTA}{other_creature.name} melds into {base_creature.name}!{BC.OFF}")
                print(f"{C.RED}It will cost {added_mana_cost} more mana to maintain {base_creature.name}{C.OFF}")


class Distract(CorruptionSpell):
    name = "Disorient"
    mana_cost = 5
    humanity_max = 7
    description = f"Confuse an enemy and focus them on a new target. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "enemy"

    def _cast(self):
        self.target.ai.target = None
        print(f"{BC.YELLOW}{self.target.name}{BC.MAGENTA} is distracted!{BC.OFF}")
        return True


class Fear(CorruptionSpell):
    name = "Fear"
    mana_cost = 5
    humanity_max = -7
    description = f"Terrify an opponent and prevent them from attacking. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "enemy"

    def _cast(self):
        fear = eff.Fear(creature=self.target, limb=self.target.subelements[0], controller=self.cont)
        fear.cast()
        return True


class Stun(CorruptionSpell):
    name = "Stun"
    mana_cost = 7
    humanity_max = -3
    description = f"Stun an opponent and take them out of the fight. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 7
    targets = "enemy"

    def _cast(self):
        if self.target.can_stun:
            self.target.stunned = True
            print(f"{C.RED}{self.target.name} is stunned!{C.OFF}")
            return True
        else:
            print(f"{C.RED}{self.target.name} cannot be stunned.{C.OFF}")

    def update(self):
        self.target.stunned = True

    def _expire(self):
        self.target.stunned = False
        print(f"{C.RED}{self.target.name} is no longer stunned.{C.OFF}")


class PoisonGas(CorruptionSpell):
    name = "Poison Gas"
    mana_cost = 10
    humanity_max = -7
    description = f"Fill the room with magical poison gas. {C.RED}(<{humanity_max}) {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 5
    targets = "caster"

    def _cast(self):
        print(f"{BC.MAGENTA}A magical cloud of poison gas fills the room!{BC.OFF}")
        return True

    def update(self):
        for enemy in [c for c in self.caster.location.creatures if c.team != self.caster.team and c.team != "neutral" and c.can_breathe]:
            print(f"{BC.MAGENTA}{enemy.name} chokes on the poison gas!{BC.OFF}")
            gas_attack = eff.Poison(creature=enemy, limb=enemy.subelements[0], controller=self.cont)
            gas_attack.cast()

    def _expire(self):
        print(f"{BC.MAGENTA}The cloud of gas dissipates and disappears.{BC.OFF}")


# Neither
class Scry(sp.Spell):
    name = "Scry"
    mana_cost = 1
    description = f"See what is happening in a nearby room. {BC.CYAN}[{mana_cost}]{C.OFF}"
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
    description = f"Manifests the door to your home. {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        """Creates a door between current location and the pocket apartment. Door will move whenever this spell is cast."""
        door = [x for x in self.caster.home.start.elements if x.name == "magic door"][0]
        if not door.borders:
            # If this is the first time this spell is called, the door will be present in the foyer but not set up as a door yet.
            door.addBorder(self.caster.home.start)
            door.color = "glowing"
            door.texture = "light"

        # We don't want to lock you into the apartment or overwrite another door.
        if self.caster.location.level != self.caster.home.start.level and not self.caster.location.borders[">"]:
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
    description = f"Grow a long flowing beard worthy of a powerful wizard. {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def no_beard(self, head):
        beards = [x for x in head.subelements if x.name == "beard"]
        if not beards:
            return True

    def _cast(self):
        import assets.commonlimbs as cl

        limbs = self.target.subelements[0].limb_check("name")
        heads = [x for x in limbs if x.name == "head"]
        if heads:
            # We want a random head, not the first one each time
            random.shuffle(heads)
            # Ideally we want a head with no beard but we can replace an existing beard with a big white one in a pinch.
            unbearded_heads = [x for x in heads if self.no_beard(x)]
            if unbearded_heads:
                heads = unbearded_heads
            head = heads[0]

            existing_beards = [x for x in head.subelements if x.name == "beard"]
            if existing_beards:
                # Cut existing beard(s) (should be max one but we'll be thorough)
                for beard in existing_beards:
                    head.remove_limb(beard)
                    print(f"{BC.MAGENTA}{self.target.name}'s old beard hairs fall out of their face.{BC.OFF}")
            head.subelements.append(cl.WizardBeard(color="white", texture="luxuriant", creature=self.target))
            print(f"{BC.MAGENTA}A long flowing beard erupts from {BC.YELLOW}{self.target.name}{BC.MAGENTA}'s face!{BC.OFF}")
            return True


class ReleaseMinion(sp.Spell):
    name = "Release Minion"
    mana_cost = 0
    description = f"Release one of your minions from your mental control. {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"

    def _cast(self):
        minions = utils.listtodict(self.caster.get_companions(), add_x=True)
        utils.dictprint(minions)
        i = input(f"{BC.MAGENTA}Select a minion to release from your mental control: {BC.OFF}")
        if i in minions.keys() and i != "x":
            minion = minions[i]
            if hasattr(minion, "orig_team"):
                minion.team = minion.orig_team
            else:
                minion.team = "neutral"
            self.caster.companions.remove(minion)
            print(f"{BC.YELLOW}{minion.name}{BC.MAGENTA} stops following you.{BC.OFF}")
            return True
        return False


class SetHumanity(sp.Spell):
    name = "Set Humanity"
    mana_cost = 0
    description = f"Cheat and set your humanity to whatever you want. {BC.CYAN}[{mana_cost}]{C.OFF}"
    rounds = 1
    targets = "caster"
    original_humanity = None

    def _cast(self):
        self.original_humanity = self.caster.humanity
        self.caster.humanity = int(input(f"{BC.MAGENTA}Set your humanity: {BC.OFF}"))
        return True
