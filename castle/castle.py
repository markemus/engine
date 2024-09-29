"""An example style- from lowest to highest, build a hierarchy.

This dark castle harbors many deadly creatures. But perhaps great treasure is hidden here?
(No, there isn't.)"""
import engine.place as pl

from castle.goblin import Goblin
from castle.hydra import Hydra
from castle.orc import Orc
from castle import furniture as fur
from engine.styles import LevelStyle, GameStyle, wall, floor


# First, some room types.
class TortureChamber(pl.place):
    sprite = "T"
    count = (1, 3)
    colors = ["black", "gray", "streaked", "dirty"]
    textures = ["stone", "dirt", "timber"]
    creature_classes = [(Orc, Goblin)]
    furniture_classes = [fur.Manacles, fur.Table, fur.Rack]
    subelement_classes = [wall, floor]

class Cell(pl.place):
    sprite = "C"
    count = (5, 10)
    colors = ["unpainted", "grimy", "grey"]
    textures = ["stone", "concrete"]
    creature_classes = [(Orc, Goblin)]
    furniture_classes = [fur.Manacles, fur.Puddle]
    subelement_classes = [wall, floor]

# Then a level type.
class Dungeon:
    room_classes = [TortureChamber, Cell]
    creature_classes = []


LevelStyle.register(Dungeon)

# Another set of rooms
class ThroneRoom(pl.place):
    sprite = "T"
    count = (1, 2)
    colors = ["gold", "red", "silver", "purple"]
    textures = ["brick", "stone", "marble"]
    creature_classes = [Orc, Goblin]
    furniture_classes = [fur.Throne]
    subelement_classes = [wall, floor]

class Kitchen(pl.place):
    sprite = "K"
    count = (1, 2)
    colors = ["dirty", "smoke-stained", "unpainted", "gray", "beige"]
    textures = ["brick", "stone"]
    creature_classes = [Orc, Goblin]
    furniture_classes = [fur.Stove]
    subelement_classes = [wall, floor]

class DiningRoom(pl.place):
    sprite = "D"
    count = (1, 3)
    colors = ["purple", "red", "gold", "silver"]
    textures = ["draped", "marble", "painted", "lit"]
    creature_classes = [Orc, Goblin]
    furniture_classes = [fur.Carpet, fur.Table, fur.Chair]
    subelement_classes = [wall, floor]

class Parlor(pl.place):
    sprite = "P"
    count = (1, 3)
    colors = ["blue", "white", "salmon", "gold", "silver"]
    textures = ["painted", "draped", "sunlit"]
    creature_classes = [Orc, Goblin]
    furniture_classes = [fur.Carpet, fur.Chair]
    subelement_classes = [wall, floor]

# Another level
class MainFloor:
    room_classes = [ThroneRoom, Kitchen, DiningRoom, Parlor]
    creature_classes = []


LevelStyle.register(MainFloor)


# And finally, the game itself.
class Castle:
    levelorder = [MainFloor, Dungeon]
    links = [(0, 1)]
    creature_classes = [Hydra]


GameStyle.register(Castle)
