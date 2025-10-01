import engine.item as it
import engine.suits_and_collections as sc

import assets.suits as asu
import assets.human


class TestTube(it.Item):
    name = "test tube"
    colors = ["clear", "blue", "green", "red", "yellow"]
    textures = ["glass"]

class Beaker(it.Item):
    name = "beaker"

class Microscope(it.Item):
    name = "microscope"

test_tubes_col = {
    "contains": [TestTube, TestTube, TestTube, TestTube],
    "color": ["clear", "blue", "green", "red", "yellow"],
    "color_scheme": "same",
    "texture": ["glass"],
    "texture_scheme": "same",
    "full": False,
}

beaker_col = {
    "contains": [Beaker, Beaker],
    "color": ["clear", "blue", "green", "red", "yellow"],
    "color_scheme": "same",
    "texture": ["glass"],
    "texture_scheme": "same",
    "full": False,
}

microscope_col = {
    "contains": [Microscope],
    "color": ["gray", "black", "silver"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
}

c_partial_poison_armor = sc.suit_to_collection(suit=asu.partial_poison_armorsuit, model=assets.human.Human)
c_partial_flame_armor = sc.suit_to_collection(suit=asu.partial_flame_armorsuit, model=assets.human.Human)
c_partial_blood_armor = sc.suit_to_collection(suit=asu.partial_blood_armorsuit, model=assets.human.Human)
