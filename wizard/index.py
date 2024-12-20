from assets import human, cat
from assets import places
from assets import suits as asu

from engine.styles import LevelStyle, GameStyle, wall, floor
from engine import game
from engine import interface

from wizard import spellbook as sb
from wizard import furniture as fur
from wizard import suits as su

from colorist import BrightColor as BC, Color as C


class PlayerHuman(human.Human):
    """Just an ordinary human."""
    team = "adventurer"
    suits = [asu.plainsuit, asu.backpack]

class SpecimenHuman(human.Human):
    team = "specimen"
    aggressive = False

class PlayerDen(places.Den):
    subelement_classes = [wall, floor]

class HomeCell(places.Cell):
    count = (1, 2)
    creature_classes = [[(SpecimenHuman, 1)]]

class Home:
    level_text = f"""{BC.BLUE}You are in your home, preparing to set off on your adventure.{BC.OFF}"""
    room_classes = [places.Bathroom, places.Bedroom, places.Parlor, places.Kitchen, HomeCell]
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
player.spellbook.append(sb.Scry)
player.spellbook.append(sb.Light)
player.spellbook.append(sb.Shadow)
# player.spellbook.append(sb.Innocence)
player.spellbook.append(sb.SummonSpider)
player.spellbook.append(sb.SummonTentacleMonster)
player.spellbook.append(sb.GraftLimb)
player.spellbook.append(sb.ReanimateLimb)
player.spellbook.append(sb.Caltrops)
player.spellbook.append(sb.FleshRip)
player.spellbook.append(sb.Flashbang)
player.spellbook.append(sb.ArmorOfLight)
player.spellbook.append(sb.GrowTreeOfLife)
player.spellbook.append(sb.SetHumanity)

# Player humanity affects which spells they can cast
player.humanity = 1

# Give player some mana to start the game with
# player.subelements[0].equip(su.ManaLocket(color="emerald", texture="in silver"))
player.subelements[0].subelements[1].subelements[0].subelements[0].equip(su.RingOfMana(color="amethyst", texture="in silver"))
player.subelements[0].subelements[1].subelements[0].subelements[1].equip(su.RingOfMana(color="lapiz", texture="in silver"))

thisLevel.start.find_invs()[0].vis_inv.append(human.Head(color="gray", texture="rotting"))

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()

# TODO put head into a jar, add a hand to another