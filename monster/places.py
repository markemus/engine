from engine import place as pl
from engine.styles import wall, single_wall, floor, water, mirrored_water, lakebed, pillar, door, channel, gateway, dwarven_gateway, staircase

import monster.furniture as fur
from monster.giant_rat import GiantRat
from monster.human import LabAssistant

cc = {
    "laboratory": [(GiantRat, 3), (LabAssistant, 3), (None, 2)],
}


class Laboratory(pl.Place):
    name = "lab"
    sprite = "L"
    count = (1, 2)
    colors = ["white"]
    textures = ["tiled"]
    creature_classes = [cc["laboratory"], cc["laboratory"], cc["laboratory"], cc["laboratory"]]
    furniture_classes = [fur.Table, fur.BrokenCage]
    subelement_classes = [wall, floor]


class GuardRoom(pl.Place):
    name = "guardroom"
    sprite = "G"
    count = (1, 2)
    colors = ["black", "gold", "red"]
    textures = ["painted"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [wall, floor]
