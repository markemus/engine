import random

import assets.suits as asu

import wizard.item_collections as wic
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
