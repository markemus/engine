"""Potions have a one time use permanent effect. The effect needs to be scripted."""
from castle import commonlimbs as cl

from engine import item as I


class PotionOfStoneskin(I.Potion):
    """Creature's skin turns to stone, granting extra HP."""
    name = "Potion of Stoneskin"
    def eat(self, creature):
        print(f"{creature.name}'s skin turns to stone.")
        limbs = creature.subelements[0].limb_check("name")
        for limb in limbs:
            limb.base_hp *= 3
            limb.hp *= 3
            limb.color = "gray"
            limb.texture = "stony"

class ArmGrowthPotion(I.Potion):
    """Creature grows an extra arm. Will only work if the creature has a recognizable torso."""
    name = "Potion of Arm Growth"

    def eat(self, creature):
        # First we find a torso to sprout from.
        wears = creature.subelements[0].limb_check("wears")
        torso = None
        for limb in wears:
            if limb.wears == "body":
                torso = limb
                break

        if torso:
            print(f"An extra arm sprouts from {creature.name}'s {torso.name}!")
            torso.subelements.append(cl.RArm(color="pale", texture="skinned"))
        else:
            print(f"The potion has no effect.")
