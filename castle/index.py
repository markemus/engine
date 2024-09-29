"""An example game. Run from main directory as 'python3 -m castle.index'."""
from engine import game
from engine import interface

from castle import man
from castle import castle


# Main
# Generate a game using the Castle template.
t_game = game.Game("The Howling Manor", castle.Castle)
thisLevel = t_game.level_list[0]

# Character creation
# TODO-DONE why is adam starting with four legs?
adam = man.Man("Adam", location=thisLevel.start)
thisLevel.start.creatures.append(adam)
t_game.set_char(adam)
# TODO make teams mean something
adam.team = "player"

thisLevel.printMap(adam)
print(adam.location.name)
adam.location.desc()
adam.speak("hello world", adam.location.creatures[0])

i = interface.Interface(t_game)
print(i.state)
print(adam.location.borders)

# Game loop
while True:
    i.command()
