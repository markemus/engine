from engine import place as pl
from engine.styles import wall, single_wall, floor, water, mirrored_water, lakebed, pillar, door, channel, gateway, dwarven_gateway, staircase

import monster.furniture as fur
from monster.giant_rat import GiantRat
from monster.human import LabAssistant, GuardL1
from monster.monster import MonsterHuman

cc = {
    "laboratory": [(GiantRat, 3), (LabAssistant, 3), (None, 2)],
    "lab_monster": [(MonsterHuman, 3), (None, 2)],
    "lab_guard": [(GuardL1, 1)],
}


class StarterLaboratory(pl.Place):
    name = "laboratory"
    sprite = "S"
    count = (1, 2)
    colors = ["white"]
    textures = ["tiled"]
    creature_classes = []
    furniture_classes = [fur.LabTable, fur.BrokenCage]
    subelement_classes = [wall, floor]

class Laboratory(pl.Place):
    name = "laboratory"
    sprite = "L"
    count = (5, 10)
    colors = ["white"]
    textures = ["tiled"]
    creature_classes = [cc["laboratory"], cc["laboratory"], cc["lab_monster"]]
    furniture_classes = [fur.LabTable]
    subelement_classes = [wall, floor]


class GuardRoom(pl.Place):
    name = "guardroom"
    sprite = "G"
    count = (1, 2)
    colors = ["black", "gold", "red"]
    textures = ["painted"]
    creature_classes = [cc["lab_guard"]]
    furniture_classes = []
    subelement_classes = [wall, floor]
