from engine import game
from engine import interface
from engine import utils

from autobattler import styles
from autobattler.golem import LargeGolem, SmallGolem, TorturerGolem
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
while r not in player_races:
    r = input(f"{BC.GREEN}Select a race to play as:{BC.OFF} ")

player = player_races[r](location=firstLevel.start)
player.team = "neutral"
player.zorkmids = 60
player.golem = None
player.level = 0
player.subelements[0].equip(asu.BagOfHolding(color="brown", texture="leather"))
firstLevel.start.creatures.append(player)
player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
t_game.set_char(player)

g = "0"
golem_types = {"1": LargeGolem, "2": SmallGolem, "3": TorturerGolem}
while not g in golem_types:
    utils.dictprint({k: v.classname for (k,v) in golem_types.items()})
    g = input(f"{BC.GREEN}Select a golem type: {BC.OFF}")

gn = input(f"{BC.GREEN}Enter a name for your golem: {BC.OFF}")
player.golem = golem_types[g](location=player.location)
player.golem.name = gn
player.location.addCreature(player.golem)

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()
