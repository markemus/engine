from assets import human, cat
from assets import places
from assets import suits

from engine.styles import LevelStyle, GameStyle, wall, floor
from engine import game
from engine import interface

from wizard import spellbook as sb
from wizard import furniture as fur

from colorist import BrightColor as BC, Color as C


class PlayerHuman(human.Human):
    """Just an ordinary human."""
    team = "adventurer"
    suits = [suits.plainsuit, suits.backpack]

class PlayerDen(places.Den):
    # subelement_classes = [wall, floor, fur.TreeOfLife]
    subelement_classes = [wall, floor]

class Home:
    level_text = f"""{BC.BLUE}You are in your home, preparing to set off on your adventure.{BC.OFF}"""
    room_classes = [places.Bathroom, places.Bedroom, places.Parlor, places.Kitchen]
    start_room = PlayerDen
    end_room = places.DiningRoom
    creature_classes = []

LevelStyle.register(Home)

class Wizard:
    # levels will spawn in this order
    levelorder = [Home]
    # Doors will be added linking these levels together- level 0 to level 1, level 1 to level 2, etc.
    links = []
    start_splash = f"""Wizard Game"""
    death_splash = f"""YOU DIED"""

GameStyle.register(Wizard)


# This should go into engine




# Main
# Generate a game using the Wizard template.
t_game = game.Game("The Way of the Wizard", Wizard)
thisLevel = t_game.level_list[0]

player = PlayerHuman(location=thisLevel.start)
familiar = cat.Cat(location=thisLevel.start)
# player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
# familiar.name = input(f"{BC.CYAN}Enter the name of your familiar: {BC.OFF}")
player.name = "Adam"
familiar.name = "Cozy"
player.companions.append(familiar)
thisLevel.start.creatures.append(player)
thisLevel.start.creatures.append(familiar)
t_game.set_char(player)

# Character setup
player.spellbook.append(sb.Light)
player.spellbook.append(sb.SummonSpider)
player.spellbook.append(sb.ReanimateLimb)
player.spellbook.append(sb.Caltrops)
player.spellbook.append(sb.ArmorOfLight)
player.spellbook.append(sb.SummonTentacleMonster)
player.spellbook.append(sb.Scry)
player.spellbook.append(sb.GrowTreeOfLife)
# Player humanity affects which spells they can cast
player.humanity = 1

thisLevel.start.find_invs()[0].vis_inv.append(human.Head(color="gray", texture="rotting"))

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()

# TODO-DECIDE exchange equipment with party?
# TODO-DONE caltrops spell- reduce amble for random limbs for 1 round (repeatedly)
# TODO-DONE armor spell- _clothe yourself in light
