"""Castle is an example game built using the EverRogue engine.

Run from toplevel engine/ directory as 'python3 -m castle.index' so that the package can properly inherit from
the engine.engine subpackage."""
from engine import game
from engine import interface

from castle import human
from castle import castle_style
from castle import household_items


# Main
# Generate a game using the Castle template.
t_game = game.Game("The Howling Manor", castle_style.Castle)
thisLevel = t_game.level_list[0]

# Character creation
adam = human.Human(location=thisLevel.start)
adam.name = "Adam"
thisLevel.start.creatures.append(adam)
t_game.set_char(adam)
adam_limbs = adam.subelements[0].limb_check("name")
for x in adam_limbs:
    x.hitpoints = 1000
# TODO make teams mean something
adam.team = "player"
adam.inventory.append(household_items.CandleStick("bright", "silver"))
# adam.subelements[0].subelements[0].inventory.append(suits.Blindfold("", "linen"))

thisLevel.printMap(adam)
adam.speak("hello world", adam.location.creatures[0])

i = interface.Interface(t_game)

# Game loop
while True:
    i.command()
