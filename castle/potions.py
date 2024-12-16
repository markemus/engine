"""Potions have a one time use permanent effect. The effect needs to be scripted."""
from colorist import BrightColor as BC, Color as C
from castle import commonlimbs as cl

from engine import item as I


class PotionOfStoneskin(I.Potion):
    """Creature's skin turns to stone, granting extra HP."""
    name = "Potion of Stoneskin"
    def effect(self, creature):
        print(f"{BC.CYAN}{creature.name}'s skin turns to stone.{BC.OFF}")
        limbs = creature.subelements[0].limb_check("name")
        for limb in limbs:
            limb.base_hp *= 3
            limb.hp *= 3
            limb.color = "gray"
            limb.texture = "stony"

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
            torso.subelements.append(cl.RArm(color="pale", texture="skinned"))
        else:
            print(f"{C.RED}The potion has no effect.{C.OFF}")

# TODO add to loot. Do loot in general.
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
        else:
            print(f"{C.RED}The potion has no effect.{C.OFF}")