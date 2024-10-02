"""An example style- from lowest to highest, build a hierarchy.

This dark castle harbors many deadly creatures. But perhaps great treasure is hidden here?
(No, there isn't.)"""
import engine.place as pl
import engine.styles as st

from castle.dwarf import Dwarf
from castle.elf import Elf
from castle.goblin import Goblin, ServantGoblin
from castle.hobbit import Hobbit
from castle.man import Man
from castle.orc import Orc
from castle import furniture as fur
from engine.styles import LevelStyle, GameStyle, wall, floor


# TODO create creature_classes and populate castle
cc = {"goblinkin": [(Orc, 1), (Goblin, 3), (None, 3)],
      "servants": [(ServantGoblin, 1)],
      "fantasy_city": [(Dwarf, 2), (Elf, 2), (Hobbit, 1), (Man, 5), (None, 3)],
      "castle": [("Skeleton", 2), ("AnimatedArmor", 2), (None, 3)],
      "kitchen": [(ServantGoblin, 1), ("Pot_boy", 3), (None, 3)],
      "animals_indoor": [("Cat", 2), ("Hound", 2), (None, 3)],
      "animals_outdoor": [("Sheep", 5), ("Cow", 3), ("Horse", 1), (None, 3)]
}

# Rooms
class Ballroom(pl.place):
    name = "ballroom"
    sprite = "D"
    count = (0, 2)
    colors = ["gold", "white", "silver"]
    textures = ["marble", "granite", "limestone"]
    creature_classes = [cc["fantasy_city"], cc["fantasy_city"]]
    furniture_classes = []
    subelement_classes = [wall, floor]

class Bathroom(pl.place):
    name = "bathroom"
    sprite = "T"
    count = (1, 3)
    colors = ["white", "blue", "black", "marble"]
    textures = ["tiled"]
    creature_classes = []
    furniture_classes = [fur.Toilet, fur.CabinetMetal]
    subelement_classes = [wall, floor]

class Bedroom(pl.place):
    name = "bedroom"
    sprite = "B"
    count = (2, 5)
    colors = ["blue", "brown", "egg white", "beige"]
    textures = ["painted", "wallpapered"]
    creature_classes = [cc["fantasy_city"]]
    furniture_classes = [fur.Bed, fur.Dresser]
    subelement_classes = [wall, floor]

class Cell(pl.place):
    name = "cell"
    sprite = "C"
    count = (5, 10)
    colors = ["unpainted", "grimy", "grey"]
    textures = ["stone", "concrete"]
    creature_classes = [cc["fantasy_city"]]
    furniture_classes = [fur.Manacles, fur.Puddle, fur.Toilet]
    subelement_classes = [wall, floor]

class DiningRoom(pl.place):
    name = "dining room"
    sprite = "D"
    count = (1, 3)
    colors = ["purple", "red", "gold", "silver"]
    textures = ["draped", "marble", "painted", "lit"]
    creature_classes = [cc["fantasy_city"], cc["fantasy_city"], cc["servants"]]
    furniture_classes = [fur.Carpet, fur.Table, fur.Chair, fur.CabinetElegant]
    subelement_classes = [wall, floor]

class Kitchen(pl.place):
    name = "kitchen"
    sprite = "K"
    count = (1, 2)
    colors = ["dirty", "smoke-stained", "unpainted", "gray", "beige"]
    textures = ["brick", "stone"]
    creature_classes = [cc["servants"]]
    furniture_classes = [fur.Stove, fur.CabinetElegant]
    subelement_classes = [wall, floor]

class Parlor(pl.place):
    name = "parlor"
    sprite = "P"
    count = (1, 3)
    colors = ["blue", "white", "salmon", "gold", "silver"]
    textures = ["painted", "draped", "sunlit"]
    creature_classes = [cc["fantasy_city"], cc["fantasy_city"], cc["fantasy_city"], cc["servants"]]
    furniture_classes = [fur.Carpet, fur.Chair]
    subelement_classes = [wall, floor]

class ThroneRoom(pl.place):
    name = "throne room"
    sprite = "T"
    count = (1, 2)
    colors = ["gold", "red", "silver", "purple"]
    textures = ["brick", "stone", "marble"]
    creature_classes = [cc["fantasy_city"]]
    furniture_classes = [fur.Throne]
    subelement_classes = [wall, floor]

class TortureChamber(pl.place):
    name = "torture chamber"
    sprite = "T"
    count = (1, 3)
    colors = ["black", "gray", "streaked", "dirty"]
    textures = ["stone", "dirt", "timber"]
    creature_classes = [cc["goblinkin"], cc["fantasy_city"]]
    furniture_classes = [fur.Manacles, fur.Table, fur.Rack, fur.CabinetMetal]
    subelement_classes = [wall, floor]


# Levels
class BedroomFloor:
    room_classes = [Bedroom, Bathroom]
    creature_classes = [[(Orc, 1), (Goblin, 1), (None, 3)]]

LevelStyle.register(BedroomFloor)


class Dungeon:
    room_classes = [TortureChamber, Cell]
    creature_classes = [[(Goblin, 3), (None, 3)]]

LevelStyle.register(Dungeon)


class MainFloor:
    room_classes = [ThroneRoom, Kitchen, DiningRoom, Parlor, Ballroom, Bathroom]
    creature_classes = [[(Orc, 3), (None, 3)]]

LevelStyle.register(MainFloor)


# And finally, the game itself.
class Castle:
    levelorder = [Dungeon, MainFloor, BedroomFloor]
    # levelorder = [BedroomFloor]
    links = [(0, 1), (1, 2)]
    # TODO-DECIDE do we want to allow game-wide creature classes? Currently can define per level and per room.
    # creature_classes = [Orc, Goblin]

GameStyle.register(Castle)
