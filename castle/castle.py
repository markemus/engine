"""An example style- from lowest to highest, build a hierarchy.

This dark castle harbors many deadly creatures. But perhaps great treasure is hidden here?
(No, there isn't.)"""
import engine.place as pl

from castle.goblin import goblin
from castle.hydra import hydra
from castle.orc import orc
from engine.styles import LevelStyle, GameStyle, wall, floor

# TODO Put the newest version in here. And organize this sort of stuff better.
# First, some room types.
class TortureChamber(pl.place):
    count = (1, 3)
    colors = ["black", "gray"]
    textures = ["stone", "iron", "dirt", "timber"]
    furniture = []
    creature_classes = [(orc, goblin)]
    subelement_classes = [wall, floor]

class Cell(pl.place):
    count = (5, 10)
    colors = ["unpainted", "grimy"]
    textures = ["stone", "concrete"]
    furniture = []
    creature_classes = [(orc, goblin)]
    subelement_classes = [wall, floor]

# Then a level type.
class Dungeon:
    room_classes = [TortureChamber, Cell]
    creature_classes = []


LevelStyle.register(Dungeon)

# Another set of rooms
class ThroneRoom(pl.place):
    count = (1, 2)
    colors = ["gold", "red"]
    textures = ["brick", "stone"]
    furniture = []
    creature_classes = [orc, goblin]
    subelement_classes = [wall, floor]

class Kitchen(pl.place):
    count = (1, 2)
    colors = ["dirty", "smoke-stained", "unpainted"]
    textures = ["brick", "stone"]
    furniture = []
    creature_classes = [orc, goblin]
    subelement_classes = [wall, floor]

# Another level
class MainFloor:
    room_classes = [ThroneRoom, Kitchen]
    creature_classes = []


LevelStyle.register(MainFloor)


# And finally, the game itself.
class Castle:
    levelorder = [Dungeon, MainFloor]
    links = [(0,1)]
    creature_classes = [hydra]


GameStyle.register(Castle)
