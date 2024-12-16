"""Castle is an example game built using the EverRogue engine.

Run from toplevel engine/ directory as 'python3 -m castle.index' so that the package can properly inherit from
the engine.engine subpackage."""
import textwrap

from colorist import BrightColor as BC, Color as C

from engine import game
from engine import interface

from castle import household_items as hi
from castle import human
from castle import castle_style
from castle import potions
from castle import suits


# Main


# Generate a game using the Castle template.
t_game = game.Game("The Howling Manor", castle_style.Castle)
thisLevel = t_game.level_list[0]

# Character creation
adam = human.PlayerHuman(location=thisLevel.start)
adam.name = "Adam"
thisLevel.start.creatures.append(adam)
t_game.set_char(adam)
adam.team = "prisoner"
# adam.team = "neutral"
# adam_limbs = adam.subelements[0].limb_check("name")
# for x in adam_limbs:
#     x.hp = 1000

# Give adam starting equipment
adams_knife = suits.Shank(color="rusty", texture="iron")
adams_pillowcase = hi.Pillowcase(color="dirty", texture="roughspun")
# adams_pillowcase2 = hi.Pillowcase(color="dirty", texture="roughspun")
adams_pillowcase.vis_inv.append(potions.PotionOfStoneskin())
# adams_pillowcase2.vis_inv.append(potions.TentacleGrowthPotion())
adam.subelements[0].limb_check("grasp")[0].grasped = adams_knife
# adam.subelements[0].limb_check("grasp")[0].grasped = adams_pillowcase2
adam.subelements[0].limb_check("grasp")[1].grasped = adams_pillowcase
# adam.subelements[0].subelements[0].equipment.append(suits.Blindfold("dirty", "linen"))
# adam.location.drop_item(suits.Blindfold("dirty", "linen"))
# TODO-DONE this potion doesn't drop when creature dies.
# Give first creature (not Adam) a Potion of Arm Growth
c = adam.location.creatures[0].subelements[0].limb_check("grasp")[1].grasped = potions.ArmGrowthPotion()

# adam.team = "neutral"



i = interface.Interface(t_game)
i.state = "fight"
# Game loop
while True:
    i.command()

# print(game_over)