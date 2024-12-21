import engine.place as pl
import engine.item as it

import engine.styles as st

import assets.asset_collections as col

import wizard.item_collections as wcol

from colorist import BrightColor as BC, Color as C


class FruitOfLife(it.Potion):
    name = "fruit of life"

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
class Trunk(pl.Furniture):
    name = "trunk"
    count = (1, 2)
    subelement_classes = [Branch]

class TreeOfLife(pl.Furniture):
    name = "tree of life"
    color = ["brown", "gray", "white"]
    texture = ["wood"]
    count = (1, 2)
    subelement_classes = [Trunk]

class MagicDoor(st.door):
    name = "magic door"
    color = ["glowing"]
    texture = ["light"]
    count = (1, 2)

class Chest(pl.DisplayFurniture):
    name = "treasure chest"
    color = ["brown", "black", "gray"]
    texture = ["wood"]
    count = (1, 2)
    # TODO refactor vis_collections so we can set spawn rates better and allow random choice between different collections
    #  I want a random weapon or a random scroll, 50/50 odds
    # TODO-DECIDE we might want loot tables or something more complex like that.
    vis_collections = [(col.weapons_c, (1, 2)), (wcol.scrolls, (1, 2))]

class Stalactite(pl.Element):
    name = "stalactite"
    count = (0, 5)

class Stalagmite(pl.Element):
    name = "stalagmite"
    count = (0, 5)