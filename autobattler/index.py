from engine import game
from engine import interface

from autobattler import styles
from assets import human

from colorist import BrightColor as BC, Color as C

# Enable color on windows
import os
os.system("color")


t_game = game.Game("Golemancy", styles.Golem)
homeLevel = t_game.level_list[-1]
firstLevel = t_game.level_list[0]

player = human.Human(location=firstLevel.start)
firstLevel.start.creatures.append(player)


player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
t_game.set_char(player)

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()
