from engine import game
from engine import interface

from monster import styles
from monster import player_monster

from assets import spellbook as sb

from colorist import BrightColor as BC, Color as C

# Enable color on windows
import os
os.system("color")

# Generate a game using the Wizard template.
t_game = game.Game("They Made A Mistake", styles.Monster)
firstLevel = t_game.level_list[0]

player = player_monster.Arachnid(location=firstLevel.start)
player.team = "escapee"
firstLevel.start.creatures.append(player)

player.spellbook.append(sb.CutLimb)
player.spellbook.append(sb.GraftLimb)

t_game.set_char(player)
player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")

i = interface.Interface(t_game)
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()

# TODO-DONE club tail
# TODO slime thrower (weakens and digests)
# TODO-DONE vampiric teeth
# TODO blinding mist generator
# TODO blind fighting creatures (hearing)
# TODO devotion weapons (fire, slime, bleed, poison, for you and enemies)
# TODO negative side effect weapons (light you on fire, blind you, poison you, bleed you). "damaged" weapon
# TODO diseases (weaken, rot, blind, deafen, effect is permanent until cured and spread and worsen)
# TODO weapons that strengthen as fight goes on
# TODO focus weapons that grow in strength when attacking the same limb repeatedly
# TODO dark rooms (everyone's blind unless nightsight or fire (can only see burning limb))
