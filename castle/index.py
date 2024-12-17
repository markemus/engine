"""Castle is an example game built using the EverRogue engine.

Run from toplevel engine/ directory as 'python3 -m castle.index' so that the package can properly inherit from
the engine.engine subpackage.

Cheating- if you want to cheat while playing this game, press CTRL-C when in the main command
menu ["Choose a command (h for help): "]. Then code away to your heart's content on the
command line, and when you're done retype the code from the end of this module: [while True: i.command()] to
jump back into the game right where you left off."""
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
t_game = game.Game("Escape From Castle Black", castle_style.Castle)
thisLevel = t_game.level_list[0]

# Character creation
adam = human.PlayerHuman(location=thisLevel.start)
adam.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
thisLevel.start.creatures.append(adam)
t_game.set_char(adam)
adam.team = "prisoner"
# adam.team = "neutral"
# adam_limbs = adam.subelements[0].limb_check("name")
# for x in adam_limbs:
#     x.hp = 1000

# Give adam starting equipment
adams_knife = suits.Shiv(color="rusty", texture="iron")
# adams_knife = suits.Cleaver(color="rusty", texture="iron")
# adams_knife = suits.MaceOfTheKing(color="rusty", texture="iron")
# other_knife = suits.Shank(color="rusty", texture="iron")
adams_pillowcase = hi.Pillowcase(color="dirty", texture="roughspun")
# adams_pillowcase2 = hi.Pillowcase(color="dirty", texture="roughspun")
adams_pillowcase.vis_inv.append(potions.PotionOfStoneskin())
# adams_pillowcase.vis_inv.append(potions.PotionOfHealing())
# adams_pillowcase.vis_inv.append(hi.Pillow(color="stained", texture="fluffy"))
# adams_pillowcase2.vis_inv.append(potions.TentacleGrowthPotion())
adam.subelements[0].limb_check("grasp")[0].grasped = adams_knife
# adam.subelements[0].limb_check("grasp")[0].grasped = adams_pillowcase2
adam.subelements[0].limb_check("grasp")[1].grasped = adams_pillowcase
# adam.subelements[0].subelements[0].equipment.append(suits.Blindfold("dirty", "linen"))
# adam.location.drop_item(suits.Blindfold("dirty", "linen"))
# adam.location.drop_item(other_knife)
# TODO-DONE this potion doesn't drop when creature dies.
# Give first creature (not Adam) a Potion of Arm Growth
c = adam.location.creatures[0].subelements[0].limb_check("grasp")[1].grasped = potions.ArmGrowthPotion()

# adam.team = "neutral"



i = interface.Interface(t_game)
i.state = "fight"
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()
