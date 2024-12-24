"""Potions have a one time use permanent effect. The effect needs to be scripted."""
import random

from assets import commonlimbs as cl
from engine import item as I, effectsbook as eff

from colorist import BrightColor as BC, Color as C


class PotionOfStoneskin(I.Potion):
    """Creature's skin turns to stone, granting extra HP."""
    name = "Potion of Stoneskin"
    def effect(self, creature):
        print(f"{BC.CYAN}{creature.name}'s skin turns to stone.{BC.OFF}")
        limbs = creature.subelements[0].limb_check("name")
        for limb in limbs:
            stoniness = eff.Stoneskin(creature, limb, controller=self.cont)
            stoniness.cast()


class ArmGrowthPotion(I.Potion):
    """Creature grows an extra arm. Will only work if the creature has a recognizable torso."""
    name = "Potion of Arm Growth"

    def effect(self, creature):
        # First we find a torso to sprout from.
        wears = creature.subelements[0].limb_check("wears")
        torso = None
        for limb in wears:
            if limb.wears == "body":
                torso = limb
                break

        if torso:
            print(f"{BC.CYAN}An extra arm sprouts from {creature.name}'s {torso.name}!{BC.OFF}")
            armclass = random.choice([cl.RArm, cl.LArm])
            torso.subelements.append(armclass(color="pale", texture="skinned"))
            if hasattr(creature, "humanity"):
                creature.humanity -= 1
        else:
            print(f"{C.RED}The potion has no effect.{C.OFF}")


class LegGrowthPotion(I.Potion):
    """Creature grows an extra leg. Will only work if the creature has a recognizable torso."""
    name = "Potion of Leg Growth"

    def effect(self, creature):
        # First we find a torso to sprout from.
        wears = creature.subelements[0].limb_check("wears")
        torso = None
        for limb in wears:
            if limb.wears == "body":
                torso = limb
                break

        if torso:
            print(f"{BC.CYAN}An extra leg sprouts from {creature.name}'s {torso.name}!{BC.OFF}")
            torso.subelements.append(cl.Leg(color="pale", texture="skinned"))
            if hasattr(creature, "humanity"):
                creature.humanity -= 1
        else:
            print(f"{C.RED}The potion has no effect.{C.OFF}")


# TODO-DONE add to loot. Do loot in general.
# TODO-DONE armor and better equipment in mainfloor level
class TentacleGrowthPotion(I.Potion):
    """Creature grows tentacles out of their face. Useful!"""
    name = "Potion of Tentacle Growth"

    def effect(self, creature):
        wears = creature.subelements[0].limb_check("wears")
        head = None
        for limb in wears:
            if limb.wears == "head":
                head = limb
                break

        if head:
            print(f"{BC.CYAN}Tentacles sprout from {creature.name}'s {head.name}!{BC.OFF}")
            head.subelements.append(cl.PTentacle(color="green", texture="slimy"))
            if hasattr(creature, "humanity"):
                creature.humanity -= 1
        else:
            print(f"{C.RED}The potion has no effect.{C.OFF}")


class PotionOfHealing(I.Potion):
    """Heals a certain amount of HP on random limbs."""
    name = "Potion of Healing"

    def effect(self, creature):
        limbs = creature.subelements[0].limb_check("name")
        total_heal = 30
        for limb in limbs:
            to_heal = limb.base_hp - limb.hp
            if to_heal > total_heal:
                to_heal = total_heal
            total_heal -= to_heal
            limb.hp += to_heal
            if to_heal:
                print(f"{BC.CYAN}{limb.name}{BC.OFF} gains {C.RED}({to_heal}/{limb.base_hp}){C.OFF} hp.")
            if total_heal <= 0:
                break


class PotionOfMana(I.Potion):
    name = "Potion of Mana"

    def effect(self, creature):
        # All equipment recovers full mana, except that used for creating/summoning minions
        minion_mana = sum([x.mana_cost for x in creature.companions])
        for mana_equipment in creature.get_tagged_equipment("mana"):
            missing_mana = mana_equipment.base_mana - mana_equipment.mana
            if missing_mana >= minion_mana:
                missing_mana -= minion_mana
                minion_mana = 0
            elif minion_mana > missing_mana:
                minion_mana -= missing_mana
                missing_mana = 0

            if (mana_equipment.mana < mana_equipment.base_mana) and missing_mana:
                mana_equipment.mana += missing_mana
                print(f"{BC.CYAN}{mana_equipment.name}{BC.OFF} recovers ({missing_mana}) mana.")

# TODO more potions
# TODO potion of Might
