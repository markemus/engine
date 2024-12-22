import assets.places
import engine.place as pl
from engine.styles import wall, floor, pillar, door

import assets.furniture as fur

import wizard.furniture

from wizard.giant_rat import GiantRat
from wizard.giant_spider import GiantSpider
from wizard.tunnel_worm import TunnelWorm

from assets.goblin import Goblin

cc = {
    "caverns": [(GiantRat, 7), (Goblin, 2), (None, 1)],
    "tunnels": [(GiantSpider, 3), (TunnelWorm, 5), (None, 2)],
}

# Player apartment rooms
class MagicFoyer(pl.Place):
    name = "foyer"
    sprite = "F"
    count = (1, 2)
    colors = ["oak", "teak", "mahogany"]
    textures = ["paneled"]
    creature_classes = []
    furniture_classes = [fur.Carpet]
    subelement_classes = [wall, floor, wizard.furniture.MagicDoor]

class PlayerBathroom(assets.places.Bathroom):
    count = (1, 2)

class PlayerParlor(assets.places.Parlor):
    count = (1, 2)

class PlayerBedroom(assets.places.Bedroom):
    count = (1, 2)
    furniture_classes = [wizard.furniture.Bed, fur.Dresser]


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
    colors = ["dark", "dripping"]
    textures = ["stone", "mud"]
    creature_classes = [cc["tunnels"]]
    furniture_classes = []
    subelement_classes = [wall, floor]

class CavernRewards(Cavern):
    """A cavern with a chest in it."""
    sprite = "R"
    count = (1, 3)
    furniture_classes = [wizard.furniture.Chest]
