import engine.place as pl
from engine.styles import wall, floor, pillar, door

import assets.furniture as fur

import wizard.furniture

from wizard.rat import GiantRat
from wizard.giant_spider import GiantSpider

from assets.goblin import Goblin

cc = {
    "caverns": [(GiantRat, 7), (Goblin, 2), (None, 1)],
    "tunnels": [(GiantSpider, 8), (None, 2)],
}

class MagicFoyer(pl.Place):
    name = "foyer"
    sprite = "F"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    creature_classes = []
    furniture_classes = [fur.Carpet]
    subelement_classes = [wall, floor, wizard.furniture.MagicDoor]


class CavernEntrance(pl.Place):
    name = "cavern"
    sprite = "C"
    count = (1, 2)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]


class Cavern(pl.Place):
    name = "cavern"
    sprite = "C"
    count = (3, 7)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = [cc["caverns"], cc["caverns"], cc["caverns"], cc["caverns"], cc["caverns"]]
    # creature_classes = []
    # TODO we need spawn rates for furniture_classes (better than just (0, 10)- rare furniture should exist)
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]

class Tunnel(pl.Place):
    name = "tunnel"
    sprite = "T"
    count = (1, 3)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = [cc["tunnels"]]
    furniture_classes = []
    subelement_classes = [wall, floor]

class CavernRewards(Cavern):
    """A cavern with a chest in it."""
    count = (1, 3)
    furniture_classes = [wizard.furniture.Chest]