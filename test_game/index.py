"""Simple test game."""
from engine import creature as cr
from engine import game
from engine import interface
from engine import item as i
from engine import place as pl
from engine.styles import GameStyle, LevelStyle, wall, floor


class Ear(cr.limb):
    name = "ear"
    subelement_classes = []
    isSurface = 1
    appendageRange = (2, 3)
    wears = "ear"

class Eye(cr.limb):
    name = "eye"
    subelement_classes = []
    isSurface = 1
    see = 1
    appendageRange = (2, 3)
    wears = "eye"

class Horn(cr.weapon):
    name = "horn"
    subelement_classes = []
    _damage = 3
    isSurface = True
    appendageRange = (2, 3)
    wears = "horn"

class Teeth(cr.weapon):
    name = "teeth"
    subelement_classes = []
    _damage = 2
    appendageRange = (1, 2)
    wears = "teeth"

class Tongue(cr.limb):
    name = "tongue"
    subelement_classes = []
    appendageRange = (1, 2)
    wears = "tongue"

class Nose(cr.limb):
    name = "nose"
    subelement_classes = []
    isSurface = True
    appendageRange = (1, 2)
    wears = "nose"

class Head(cr.limb):
    name = "head"
    subelement_classes = [Ear, Eye, Horn, Teeth, Tongue, Nose]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"

# Arms
class Finger(cr.limb):
    name = "finger"
    subelement_classes = []
    f_grasp = 1/4
    isSurface = True
    appendageRange = (4, 5)
    wears = "finger"

class Thumb(cr.limb):
    name = "thumb"
    subelement_classes = []
    t_grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "finger"

class Hand(cr.weapon):
    name = "hand"
    subelement_classes = [Finger, Thumb]
    grasp = 1
    isSurface = True
    appendageRange = (1, 2)
    wears = "hand"

class Arm(cr.limb):
    name = "arm"
    subelement_classes = [Hand]
    isSurface = True
    appendageRange = (2, 3)
    wears = "arm"

# Legs
class Foot(cr.limb):
    name = "foot"
    subelement_classes = []
    amble = 1/2
    isSurface = True
    appendageRange = (1, 2)
    wears = "foot"

class Leg(cr.limb):
    name = "leg"
    subelement_classes = [Foot]
    isSurface = True
    appendageRange = (2, 3)
    wears = "leg"

class Head(cr.limb):
    name = "head"
    subelement_classes = [Ear, Eye, Teeth, Tongue, Nose]
    isSurface = True
    appendageRange = (1, 2)
    wears = "head"

# Torso
class Torso(cr.limb):
    name = "torso"
    subelement_classes = [Head, Arm, Leg]
    isSurface = True
    appendageRange = (1, 2)
    wears = "body"

# Suits
# Clothing
class Tunic(i.Item):
    name = "tunic"
    canwear = i.Item.canwear.copy()
    canwear["torso"] = True

class Hose(i.Item):
    name = "hose"
    canwear = i.Item.canwear.copy()
    canwear["leg"] = True

class Shoe(i.Item):
    name = "boot"
    canwear = i.Item.canwear.copy()
    canwear["foot"] = True

class Slipper(i.Item):
    name = "slipper"
    canwear = i.Item.canwear.copy()
    canwear["foot"] = True

# Weapons
class Axe(i.Item):
    name = "axe"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 7

class Spear(i.Item):
    name = "spear"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 8

class Sword(i.Item):
    name = "sword"
    canwear = i.Item.canwear.copy()
    canwear["hand"] = True
    damage = 9

plainsuit = {
    "wears": {
        "body": Tunic,
        "leg": Hose,
        "foot": (Shoe, Slipper)},
    "color": ["red", "blue", "green", "yellow", "striped"],
    "color_scheme": "distinct",
    "texture": ["silk", "cotton", "wool"],
    "texture_scheme": "same",
    "full": True,
    }

weapons = {
    "wears": {
        "hand": (Sword, Spear, Axe)},
    "color": ["gray"],
    "color_scheme": "same",
    "texture": ["steel"],
    "texture_scheme": "same",
    "full": True,
}

class Goblin(cr.creature):
    classname = "goblin"
    namelist = ["Shasri"]
    baseElem = Torso
    colors = ["red", "brown", "green", "black", "beige"]
    textures = ["scaled", "haired", "skinned"]
    suits = [plainsuit, weapons]

class Bedroom(pl.place):
    name = "bedroom"
    sprite = "B"
    count = (2, 5)
    colors = ["blue", "brown", "egg white", "beige"]
    textures = ["painted", "wallpapered"]
    creature_classes = [[(Goblin, 1)]]
    furniture_classes = []
    subelement_classes = [wall, floor]

class TestLevel:
    room_classes = [Bedroom]
    creature_classes = []

class TestGame:
    levelorder = [TestLevel]
    links = []

LevelStyle.register(TestLevel)
GameStyle.register(TestGame)


t_game = game.Game("TestGame", TestGame)
thisLevel = t_game.level_list[0]
shasri = Goblin(thisLevel.start)
thisLevel.start.creatures.append(shasri)
i = interface.Interface(t_game)
t_game.set_char(shasri)


# Game loop
while True:
    i.command()
