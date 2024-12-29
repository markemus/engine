import assets.places
import engine.place as pl
from engine.styles import wall, floor, water, lakebed, pillar, door

import assets.furniture as fur

import wizard.furniture

from wizard.cave_fish import BlindCaveFish
from wizard.giant_rat import GiantRat
from wizard.giant_bat import GiantBat
from wizard.giant_shrimp import BlindCaveShrimp
from wizard.elf import DarkElfScout, DarkElfChampion, DarkElfGuard
from wizard.giant_spider import GiantSpider, ArmoredGiantSpider
from wizard.goblin import ShallowGoblinChief, GoblinPetDog
from wizard.tunnel_worm import TunnelWorm

from assets.goblin import Goblin, ShallowGoblin


cc = {
    "caverns_1": [(GiantRat, 3), (GiantBat, 3), (ShallowGoblin, 4), (None, 2)],
    "caverns_1_gobs": [(ShallowGoblin, 4), (None, 1)],
    "caverns_2": [(GiantSpider, 1), (DarkElfScout, 4), (ShallowGoblin, 4), (None, 2)],
    "caverns_2_gobs": [(ShallowGoblin, 4), (None, 1)],
    "caverns_2_elves": [(GiantSpider, 1), (DarkElfScout, 4), (None, 1)],
    "fish": [(BlindCaveFish, 1), (BlindCaveShrimp, 1), (None, 1)],
    "tunnels": [(GiantSpider, 4), (TunnelWorm, 4)],
    "dehome_guards": [(ArmoredGiantSpider, 1), (DarkElfGuard, 3)],
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

# Cavern L1 rooms
class CavernEntrance(pl.Place):
    name = "cavern"
    sprite = "E"
    count = (1, 2)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]

class CavernOpen(pl.Place):
    name = "cavern"
    sprite = "C"
    count = (3, 7)
    colors = ["gray", "dark", "dripping"]
    textures = ["stone"]
    creature_classes = [cc["caverns_1"], cc["caverns_1"], cc["caverns_1"], cc["caverns_1"]]
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

class GoblinCavernVillage(CavernOpen):
    """A goblin village in a cavern with some loot."""
    name = "goblin village"
    sprite = "G"
    count = (1, 4)
    furniture_classes = [wizard.furniture.Mattress, wizard.furniture.Firepit, wizard.furniture.L1Chest]
    creature_classes = [cc["caverns_1_gobs"], cc["caverns_1_gobs"], cc["caverns_1_gobs"]]

class GoblinChiefVillage(GoblinCavernVillage):
    """Village where the goblin chief resides."""
    name = "goblin chief village"
    sprite = "K"
    count = (1, 2)
    creature_classes = [[(ShallowGoblin, 1)], [(ShallowGoblin, 1)], [(ShallowGoblinChief, 1)], [(GoblinPetDog, 1)]]

# Cavern L2 rooms
class CavernOpenL2(CavernOpen):
    """An open cavern."""
    creature_classes = [cc["caverns_2"], cc["caverns_2"], cc["caverns_2"], cc["caverns_2"], cc["caverns_2"], cc["caverns_2"]]
    furniture_classes = [wizard.furniture.GiantMushroom, (wizard.furniture.GoblinGrave, wizard.furniture.DarkElfGrave, None, None)] + CavernOpen.furniture_classes.copy()

class GoblinCavernVillageL2(GoblinCavernVillage):
    creature_classes = [cc["caverns_2_gobs"], cc["caverns_2_gobs"], cc["caverns_2_gobs"], cc["caverns_2_gobs"]]
    furniture_classes = [wizard.furniture.GiantMushroom] + GoblinCavernVillage.furniture_classes.copy()

class DarkElfOutpost(CavernOpenL2):
    """A forward scouting base of the dark elves."""
    name = "dark elf outpost"
    sprite = "D"
    count = (1, 4)
    creature_classes = [cc["caverns_2_elves"], cc["caverns_2_elves"], cc["caverns_2_elves"], cc["caverns_2_elves"]]
    furniture_classes = [wizard.furniture.GiantMushroomWithHammock, wizard.furniture.PupTent, wizard.furniture.Firepit, wizard.furniture.L2Chest]


# TODO fire effects should not work here
class CavernLake(pl.Place):
    name = "cave lake"
    sprite = "L"
    count = (1, 5)
    colors = ["slate", "black", "wet"]
    textures = ["dark"]
    creature_classes = [cc["fish"], cc["fish"], cc["fish"], cc["fish"]]
    # creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, water, lakebed, wizard.furniture.Stalactite]
    # Fire spells will fail here
    wet = True


class DarkElfGuardtower(pl.Place):
    name = "guard tower"
    sprite = "T"
    count = (1, 2)
    colors = ["slate", "dark", "black", "granite"]
    textures = ["stone"]
    creature_classes = [[(DarkElfChampion, 1)], [(ArmoredGiantSpider, 1)], [(DarkElfChampion, 1)], [(ArmoredGiantSpider, 1)]]
    furniture_classes = [wizard.furniture.L2Chest]
    subelement_classes = [wall, floor]

class DarkElfRoad(pl.Place):
    name = "highway"
    sprite = "R"
    count = (1, 2)
    colors = ["slate", "dark", "black", "granite"]
    textures = ["stone"]
    creature_classes = [cc["dehome_guards"], cc["dehome_guards"], cc["dehome_guards"]]
    furniture_classes = []
    subelement_classes = [wall, floor, wizard.furniture.Stalactite, wizard.furniture.Stalagmite]
