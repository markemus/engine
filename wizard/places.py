import assets.places
import engine.place as pl
from engine.styles import wall, floor, pillar, door

import assets.furniture as fur

import wizard.furniture

from wizard.giant_rat import GiantRat
from wizard.giant_bat import GiantBat
from wizard.giant_spider import GiantSpider
from wizard.goblin import ShallowGoblinChief, GoblinPetDog
from wizard.tunnel_worm import TunnelWorm

from assets.goblin import Goblin, ShallowGoblin
from assets.dog import Dog

cc = {
    "caverns": [(GiantRat, 3), (GiantBat, 3), (ShallowGoblin, 4), (None, 2)],
    "tunnels": [(GiantSpider, 4), (TunnelWorm, 4)],
}

# Player apartment rooms
class MagicFoyer(pl.Place):
    name = "foyer"
    sprite = "F"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    creature_classes = []
    furniture_classes = [fur.Carpet, wizard.furniture.Doormat]
    subelement_classes = [wall, floor, wizard.furniture.MagicDoor]

class PlayerBathroom(assets.places.Bathroom):
    count = (1, 2)

class PlayerParlor(assets.places.Parlor):
    count = (1, 2)

class PlayerBedroom(assets.places.Bedroom):
    count = (1, 2)
    furniture_classes = [wizard.furniture.Bed, fur.Dresser]

class TrophyRoom(pl.Place):
    name = "trophy room"
    sprite = "T"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    furniture_classes = [fur.Carpet, wizard.furniture.TrophyPlinth]
    subelement_classes = [wall, floor]

# Cavern rooms
class CavernEntrance(pl.Place):
    name = "cavern"
    sprite = "C"
    count = (1, 2)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]

# TODO-DONE goblin equipment is too powerful for l1
class CavernOpen(pl.Place):
    name = "cavern"
    sprite = "C"
    count = (3, 7)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = [cc["caverns"], cc["caverns"], cc["caverns"], cc["caverns"]]
    # creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]

class Tunnel(pl.Place):
    name = "tunnel"
    sprite = "T"
    count = (1, 3)
    colors = ["dark", "dripping"]
    textures = ["stone", "mud"]
    creature_classes = [cc["tunnels"]]
    furniture_classes = []
    subelement_classes = [wall, floor]

class CavernVillage(CavernOpen):
    """A cavern village with some loot."""
    name = "goblin village"
    sprite = "C"
    count = (1, 3)
    furniture_classes = [wizard.furniture.Mattress, wizard.furniture.Firepit, wizard.furniture.L1Chest]

class GoblinChiefVillage(CavernVillage):
    """Village where the goblin chief resides."""
    name = "goblin chief village"
    sprite = "G"
    count = (1, 2)
    creature_classes = [[(ShallowGoblin, 1)], [(ShallowGoblin, 1)], [(ShallowGoblinChief, 1)], [(GoblinPetDog, 1)]]

# TODO add potions to Caverns loot
# TODO add mana gear to Caverns loot
# TODO loot drops on every room, or available for every room.