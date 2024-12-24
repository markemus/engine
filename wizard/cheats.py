import random
import wizard.spellbook as sb
import wizard.item_collections as wic
import wizard.suits as wsu

def skip_level_one(player, game):
    """Gives equipment that should fairly represent beating level one, and places player at beginning of level 2."""
    # Cheat
    player.spellbook.extend(random.choices(wic.level_one_spells, k=2))
    player.subelements[0].subelements[1].subelements[0].grasped = random.choice([wsu.BronzeSwordOfFire, wsu.BronzeSwordOfLight, wsu.BronzeFlail])
    player.subelements[0].subelements[1].subelements[0].subelements[2].equip(wsu.RingOfMana(color="lapiz", texture="in silver"))
    player.subelements[0].subelements[1].subelements[0].subelements[3].equip(wsu.RingOfMana(color="lapiz", texture="in silver"))

    # Skip
    player.location.creatures.remove(player)
    player.location = game.level_list[1].start
    game.set_current_level(1)
    player.location.creatures.append(player)