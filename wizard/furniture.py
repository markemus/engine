import engine.place as pl
import engine.item as it

import engine.styles as st

import assets.asset_collections as col
import assets.furniture as fur
import assets.potions as pot

import wizard.elf
import wizard.item_collections as wcol
import wizard.goblin
import wizard.suits as wsu

from colorist import BrightColor as BC, Color as C


lt = {
    "l1_chest_scroll": [(wcol.LevelOneScroll, 1)],
    "l1_chest_mana": [(wsu.RingOfMana, 2), (wsu.ManaLocket, 1)],
    # TODO-DONE add potion of might
    "l1_chest_potion": [(pot.PotionOfStoneskin, 1), (pot.TentacleGrowthPotion, 1), (pot.PotionOfHealing, 1), (pot.PotionOfMight, 1)],
    "l2_chest_scroll": [(wcol.LevelTwoScroll, 1)],
    "l3_chest_scroll": [(wcol.LevelThreeScroll, 1)],
}

class FruitOfLife(it.Potion):
    name = "fruit of life"

    def __init__(self, *args, **kwargs):
        super().__init__(color="red", texture="shiny")

    def effect(self, creature):
        limbs = creature.subelements[0].limb_check("name")
        total_heal = 30
        for limb in limbs:
            to_heal = limb.base_hp - limb.hp
            if to_heal > total_heal:
                to_heal = total_heal
            total_heal -= to_heal
            limb.hp += to_heal
            if to_heal:
                print(f"{BC.CYAN}{limb.name}{BC.OFF} gains {C.RED}({to_heal}/{limb.base_hp}){C.OFF} hp.")
            if total_heal <= 0:
                break

fruit = {
    "contains": [FruitOfLife],
    "color": ["shiny"],
    "color_scheme": "same",
    "texture": ["silver"],
    "texture_scheme": "same",
    "full": True,
}

class Branch(pl.DisplayFurniture):
    name = "branch"
    count = (2, 5)
    color = ["green", "orange", "red"]
    texture = ["leafy"]
    vis_collections = [(fruit, (1, 2))]
class TreeTrunk(pl.Furniture):
    name = "trunk"
    count = (1, 2)
    subelement_classes = [Branch]

class TreeOfLife(pl.Furniture):
    name = "tree of life"
    color = ["brown", "gray", "white"]
    texture = ["wood"]
    count = (1, 2)
    subelement_classes = [TreeTrunk]

class Hammock(pl.Furniture):
    """A dark elf's hammock."""
    name = "hammock"
    count = (1, 2)
    color = ["black"]
    texture = ["silk"]

class MushroomCap(pl.Furniture):
    name = "cap"
    count = (1, 2)

class MushroomCapWithHammock(MushroomCap):
    subelement_classes = [(Hammock, None, None)]

class MushroomStalk(pl.Furniture):
    name = "stalk"
    count = (1, 2)
    subelement_classes = [MushroomCap]

class MushroomStalkWithHammock(MushroomStalk):
    subelement_classes = [MushroomCapWithHammock]

class GiantMushroom(pl.Furniture):
    name = "giant mushroom"
    color = ["purple", "cyan", "magenta"]
    texture = ["blotchy", "spotted", "streaked"]
    count = (2, 7)
    subelement_classes = [MushroomStalk]

class GiantMushroomWithHammock(GiantMushroom):
    """A giant mushroom that sometimes has a nice relaxing hammock hanging from its cap."""
    subelement_classes = [MushroomStalkWithHammock]

# Wizard's home
class MagicDoor(st.door):
    name = "magic door"
    color = ["glowing"]
    texture = ["light"]
    count = (1, 2)

# Bed for wizard's house should only spawn one bed
class Bed(fur.Bed):
    count = (1, 2)

class Doormat(pl.Furniture):
    name = "welcome mat"
    color = ["'Don't let the cat out"]
    texture = ["or the monsters in'"]
    count = (1, 2)

class TrophyPlinth(pl.DisplayFurniture):
    name = "trophy plinth"
    color = ["black", "marble", "granite"]
    texture = ["stone"]
    count = (10, 11)
    # vis_collections = [(wcol.plaque, (1, 2))]
    loot_tables = [[(wcol.Plaque, 1)]]

class DenTable(fur.Table):
    loot_tables = [[(wcol.Jar, 1)], [(wcol.Jar, 1)], [(wcol.Jar, 1)]]


# Caverns
class L1Chest(pl.DisplayFurniture):
    name = "treasure chest"
    color = ["brown", "black", "gray"]
    texture = ["wood"]
    count = (1, 2)
    # A random scroll, or a potion/mana item
    # vis_collections = [(wcol.l1_scrolls, (1, 2)), ((wcol.potions_col, (2, 3)), (wcol.mana_items, (1, 2)))]
    loot_tables = [lt["l1_chest_scroll"], (lt["l1_chest_mana"], lt["l1_chest_potion"])]

class L2Chest(pl.DisplayFurniture):
    name = "treasure chest"
    color = ["brown", "black", "gray"]
    texture = ["wood"]
    count = (1, 2)
    # A random scroll, or a potion/mana item
    # vis_collections = [(wcol.l2_scrolls, (1, 2)), ((wcol.potions_col, (2, 3)), (wcol.mana_items, (1, 2)))]
    loot_tables = [lt["l2_chest_scroll"], (lt["l1_chest_mana"], lt["l1_chest_potion"])]

# TODO-DONE L3chest loot
class L3Chest(pl.DisplayFurniture):
    name = "treasure chest"
    color = ["brown", "black", "gray"]
    texture = ["wood"]
    count = (1, 2)
    loot_tables = [lt["l3_chest_scroll"], lt["l1_chest_potion"]]

class GoblinGrave(pl.DisplayFurniture):
    name = "goblin grave"
    color = ["stone"]
    texture = ["mound"]
    count = (0, 2)
    vis_collections = [(wizard.goblin.goblin_corpse_col, (1, 2))]

class DarkElfGrave(pl.DisplayFurniture):
    name = "dark elf grave"
    color = ["dirt"]
    texture = ["mound"]
    count = (0, 2)
    vis_collections = [(wizard.elf.dark_elf_corpse_col, (1, 2))]

class Stalactite(pl.Element):
    name = "stalactite"
    count = (0, 5)

class Stalagmite(pl.Element):
    name = "stalagmite"
    count = (0, 5)

class Mattress(pl.Furniture):
    name = "mattress"
    count = (5, 10)
    color = ["dirty", "moldy", "ratty", "moth-eaten"]
    texture = ["cloth", "lumpy"]

class Firepit(pl.DisplayFurniture):
    name = "fire pit"
    count = (1, 2)
    color = ["burning", "warm", "cold", "ashen"]
    texture = ["wood", "charcoal"]
    vis_collections = [(wsu.bronze_spit, (1, 2)), (wcol.rat_cooked, (0, 2))]

class PupTent(pl.Furniture):
    """A dark elf scout's tent."""
    name = "pup tent"
    count = (3, 6)
    color = ["black"]
    texture = ["silk"]

class Fresco(pl.Element):
    name = ""
    color = ["a glowing purple fresco of", "a glowing green fresco of", "a glowing blue fresco of"]
    texture = ["a spider eating a dwarf", "dark elves making poisons", "a spider eating an adventurer",
               "dark elves fighting dwarves", "a dark elf ritual", "a spider sitting on its web",
               "a dark elf armorer working", "dark elf soldiers fighting goblins", "a spider eating a goblin"]
    count = (1, 2)

class FrescoWall(st.wall):
    subelement_classes = [Fresco]

class Anvil(pl.Furniture):
    name = "anvil"
    count = (1, 2)
    color = ["black", "matte"]
    texture = ["steel", "iron"]