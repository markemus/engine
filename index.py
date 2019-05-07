from engine import game
from engine import interface

import man
import castle


# Main
t_game = game.Game("The Howling Manor", castle.Castle)

thisLevel = t_game.level_list[0]

adam = man.Man("Adam", location=thisLevel.start)
t_game.set_char(adam)
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
