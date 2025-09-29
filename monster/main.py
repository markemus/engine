from engine import game
from engine import interface

from monster import styles
from monster import player_monster

from colorist import BrightColor as BC, Color as C

# Enable color on windows
import os
os.system("color")

# Generate a game using the Wizard template.
t_game = game.Game("They Made A Mistake", styles.Monster)
firstLevel = t_game.level_list[0]

player = player_monster.Human(location=firstLevel.start)
player.team = "escapee"
firstLevel.start.creatures.append(player)
t_game.set_char(player)
player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()
