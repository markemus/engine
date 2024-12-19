import engine.place as pl
import engine.item as it

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
    count = (1, 2)
    color = ["green", "orange", "red"]
    texture = ["leafy"]
    vis_collections = [(fruit, (1, 4))]
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
