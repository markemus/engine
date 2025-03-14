import random

import assets.suits as asu

import wizard.item_collections as wic
import wizard.spellbook as sb
import wizard.suits as wsu


def skip_level_one(player, game):
    """Gives equipment that should fairly represent beating level one, and places player at beginning of level 2."""
    # Cheat
    l1_spells = random.sample(wic.level_one_spells, k=2)
    [wic.level_one_spells.remove(s) for s in l1_spells]
    player.spellbook.extend(l1_spells)
    player.subelements[0].subelements[1].subelements[0].grasped = random.choice([wsu.BronzeSwordOfFire("firey", "bronze"), wsu.BronzeSwordOfLight("shining", "bronze"), wsu.BronzeFlail("menacing", "bronze")])
    player.subelements[0].subelements[1].subelements[0].subelements[2].equip(wsu.RingOfMana(color="lapiz", texture="in silver"))
    player.subelements[0].subelements[1].subelements[0].subelements[3].equip(wsu.RingOfMana(color="lapiz", texture="in silver"))

    # Skip
    player.location.creatures.remove(player)
    player.location = game.level_list[1].start
    game.set_current_level(1)
    player.location.creatures.append(player)

def skip_level_two(player, game):
    """Gives equipment that should fairly represent beating level two, and places player at beginning of level 3."""
    # Cheat
    l1_spells = random.sample(wic.level_one_spells, k=2)
    [wic.level_one_spells.remove(s) for s in l1_spells]
    l2_spells = random.sample(wic.level_two_spells, k=3)
    [wic.level_two_spells.remove(s) for s in l2_spells]
    player.spellbook.extend(l1_spells)
    player.spellbook.extend(l2_spells)
    player.subelements[0].subelements[1].subelements[0].subelements[4].equip(wsu.RingOfMana(color="lapiz", texture="in silver"))
    player.subelements[0].equip(wsu.ManaLocket(color="lapiz", texture="in silver"))

    player.suits = [asu.bronze_armorsuit]
    player._clothe()

    # Skip
    player.location.creatures.remove(player)
    player.location = game.level_list[2].start
    game.set_current_level(2)
    player.location.creatures.append(player)

def skip_level_three(player, game):
    # Cheat
    l3_spells = random.sample(wic.level_three_spells, k=3)
    [wic.level_three_spells.remove(s) for s in l3_spells]
    player.spellbook.extend(l3_spells)
    player.subelements[0].subelements[1].subelements[0].grasped = wsu.IronPoisonedScimitar(color="oily", texture="green")

    # Skip
    player.location.creatures.remove(player)
    player.location = game.level_list[3].start
    game.set_current_level(3)
    player.location.creatures.append(player)

def skip_level_four(player, game):
    # Cheat
    player.spellbook.append(sb.SummonExcalibur)

    # Skip
    player.location.creatures.remove(player)
    player.location = game.level_list[4].start
    game.set_current_level(4)
    player.location.creatures.append(player)

def skip_level_five(player, game):
    # Cheat
    player.unequip_suit(asu.bronze_armorsuit)
    player.suits = [asu.iron_armorsuit]
    player._clothe()

    # Skip
    player.location.creatures.remove(player)
    player.location = game.level_list[5].start
    game.set_current_level(5)
    player.location.creatures.append(player)

def skip_level_six(player, game):
    # Cheat
    # Skip
    player.location.creatures.remove(player)
    player.location = game.level_list[6].start
    game.set_current_level(6)
    player.location.creatures.append(player)
