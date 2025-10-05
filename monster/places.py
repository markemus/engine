from engine import place as pl
from engine.styles import wall, single_wall, double_wall, floor, water, mirrored_water, lakebed, pillar, door, channel, gateway, dwarven_gateway, passage, staircase

import assets.furniture as afur

import monster.furniture as fur
from monster.glasscat import GlassCat
from monster.giant_rat import GiantRat
from monster.hive_rat import HiveRat
from monster.human import LabAssistant, GuardL1
from monster.lab_monster import LabMonster
from monster.maze_monster import MazeMonster


cc = {
    "laboratory": [(GiantRat, 3), (LabAssistant, 3), (None, 2)],
    "lab_monster": [(LabMonster, 3), (None, 2)],
    "lab_guard": [(GuardL1, 1)],
    "maze_rats": [(HiveRat, 3), (None, 3)],
    "maze_cats": [(GlassCat, 1), (None, 1)],
    "maze_monster": [(MazeMonster, 3), (None, 2)],
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
    count = (3, 7)
    colors = ["white"]
    textures = ["tiled"]
    creature_classes = [cc["laboratory"], cc["laboratory"], cc["laboratory"]]
    furniture_classes = [fur.LabTable]
    subelement_classes = [wall, floor]

class Cell(pl.Place):
    name = "cell"
    sprite = "C"
    count = (2, 5)
    colors = ["unpainted", "grimy", "grey"]
    textures = ["stone", "concrete"]
    creature_classes = [cc["lab_monster"]]
    furniture_classes = [afur.Manacles, afur.Puddle, afur.Toilet, afur.BedPrison]
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

class MazeEntrance(pl.Place):
    name = "maze entrance"
    sprite = "E"
    count = (1, 2)
    colors = ["white"]
    textures = ["painted"]
    creature_classes = []
    furniture_classes = []
    subelement_classes = [single_wall, double_wall, floor]
    door_class = passage

class MazeHallway(pl.Place):
    name = "maze hallway"
    sprite = "M"
    count = (12, 20)
    colors = ["white"]
    textures = ["painted"]
    creature_classes = [cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_rats"], cc["maze_cats"]]
    furniture_classes = []
    subelement_classes = [double_wall, floor]
    door_class = passage

class MazeTreasure(pl.Place):
    name = "maze treasure room"
    sprite = "M"
    count = (0, 6)
    colors = ["white"]
    textures = ["painted"]
    creature_classes = [cc["maze_monster"], cc["maze_monster"]]
    furniture_classes = []
    subelement_classes = [double_wall, floor]
    door_class = passage
