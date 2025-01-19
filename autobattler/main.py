from engine import game
from engine import interface
from engine import utils

from autobattler import styles
from assets.dwarf import Dwarf
from assets.hobbit import Hobbit
from assets.human import Human
from assets.elf import Elf
from assets.goblin import ServantGoblin
from assets import suits as asu

from colorist import BrightColor as BC, Color as C

# Enable color on windows
import os
os.system("color")


t_game = game.Game("Golemancy", styles.Golem)
homeLevel = t_game.level_list[-1]
firstLevel = t_game.level_list[0]

player_races = utils.listtodict([Dwarf, Hobbit, Human, Elf, ServantGoblin])
utils.dictprint(player_races, pfunc=lambda x, y: f"{x.split(':')[0]}: {BC.CYAN}{y.classname}{BC.OFF}")
r = 100
while r not in player_races.keys():
    r = input(f"{BC.GREEN}Select a race to play as:{BC.OFF} ")

player = player_races[r](location=firstLevel.start)
player.team = "neutral"
player.zorkmids = 60
player.golem = None
player.subelements[0].equip(asu.BagOfHolding(color="brown", texture="leather"))
firstLevel.start.creatures.append(player)
player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
t_game.set_char(player)

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()
