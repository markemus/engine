import random

from assets import cat
from assets import potions

from engine import game
from engine import interface
from engine import effectsbook as eff

from wizard import cheats
from wizard import human
from wizard import item_collections as ic
from wizard import spellbook as sb
from wizard import styles
from wizard import suits as su

# Enable color on windows
import os
os.system("color")

# TODO-DONE creatures should die of losing too much hp, or bleed to death, or something that doesn't require them losing their heads.
# Main
# Generate a game using the Wizard template.
t_game = game.Game("The Tomb of the Dwarven King", styles.Wizard)
# Generate the Home level. This is needed for the A Way Home spell- the level should not be in t_game.level_list.
homeLevel = t_game.level_list[-1]
firstLevel = t_game.level_list[0]
# homeLevel = t_game.level_list[1]

player = human.PlayerHuman(location=firstLevel.start)
# player = giant_bat.GiantBat(location=thisLevel.start)
firstLevel.start.creatures.append(player)
familiar = cat.Cat(location=homeLevel.end)
# TODO check before release that this still puts the cat in the den!
homeLevel.end.creatures.append(familiar)
# familiar.familiar = True
# player.name = input(f"{BC.CYAN}Enter your name: {BC.OFF}")
# familiar.name = input(f"{BC.CYAN}Enter the name of your familiar: {BC.OFF}")
player.name = "Adam"
familiar.name = "Cozy"
player.home = homeLevel

# player.team = "neutral"

# thisLevel.start.creatures.append(familiar)
t_game.set_char(player)

# TODO select starting spells for release
# Character setup
player.spellbook.append(random.choice(ic.level_one_spells))
player.spellbook.append(random.choice([sb.SummonCerberus, sb.SummonSpider, sb.SummonEtherealHand]))
# player.spellbook.append(sb.Scry)
# player.spellbook.append(sb.Light)
# player.spellbook.append(sb.Shadow)
# player.spellbook.append(sb.Trapdoor)
# player.spellbook.append(sb.Innocence)
# player.spellbook.append(sb.Lightning)
player.spellbook.append(sb.Fireball)
# player.spellbook.append(sb.SummonSpider)
# player.spellbook.append(sb.SummonCerberus)
# player.spellbook.append(sb.SummonEtherealHand)
# player.spellbook.append(sb.SummonTentacleMonster)
# player.spellbook.append(sb.Distract)
# player.spellbook.append(sb.GrowFangs)
# player.spellbook.append(sb.GraftLimb)
# player.spellbook.append(sb.ReanimateLimb)
# player.spellbook.append(sb.TransformSpider)
# player.spellbook.append(sb.Caltrops)
# player.spellbook.append(sb.FleshRip)
# player.spellbook.append(sb.Fear)
# player.spellbook.append(sb.Might)
# player.spellbook.append(sb.Enthrall)
# player.spellbook.append(sb.Flashbang)
# player.spellbook.append(sb.ArmorOfLight)
# player.spellbook.append(sb.GrowTreeOfLife)
# player.spellbook.append(sb.GrowBeard)
player.spellbook.append(sb.AWayHome)
player.spellbook.append(sb.ReleaseMinion)
player.spellbook.append(sb.SetHumanity)

# TODO player.humanity should be 1 for release
# Player humanity affects which spells they can cast
player.humanity = 5
# player.humanity = -5

# Give player some mana to start the game with
player.subelements[0].subelements[1].subelements[0].subelements[0].equip(su.RingOfMana(color="amethyst", texture="in silver"))
player.subelements[0].subelements[1].subelements[0].subelements[1].equip(su.RingOfMana(color="lapiz", texture="in silver"))
# player.subelements[0].find_invs()[0].vis_inv.append(potions.PotionOfMight())
# player.subelements[0].subelements[1].subelements[0].grasped = su.SwordOfFire(color="bright", texture="steel")
# firstLevel.start.find_invs()[0].vis_inv.append(a_human.Head(color="gray", texture="rotting"))

# TODO disable cheats before release
cheats.skip_level_one(player, t_game)

i = interface.Interface(t_game)
# player.can_fear = False
# might = eff.Poison(creature=player, limb=player.subelements[0].subelements[1], controller=i.cont)
# might.cast()
# Game loop- if you use CTRL-C to cheat, just run this to get back into the game when you're ready.
while True:
    i.command()
