"""Styles are used for game generation.

Do not inherit styles directly or the attributes will be inherited as well. Instead,
register() your classes as abstract subclasses of their parents.

The hierarchy is built like a pyramid, from the ground up. At each level of the hierarchy you can define objects that
will be inherited by all the lower levels.

Each element in a list will be generated, and a single element will be selected from each tuple. This should work
recursively to let you select lists from tuples of lists etc."""
import abc
from . import place as pl


class LevelStyle(abc.ABC):
    room_classes = []
    creature_classes = []

class GameStyle(abc.ABC):
    levelorder = [LevelStyle, LevelStyle, LevelStyle]
    links = []
    creature_classes = []

class wall(pl.element):
    name = "wall"
    count = (4, 5)

class floor(pl.element):
    name = "floor"
    count = (1, 2)
    canCatch = True


# # An example style- from lowest to highest, build a hierarchy.
# # First, some room types.
# class TortureChamber(pl.place):
#     count = (1, 3)
#     colors = ["black", "gray"]
#     textures = ["stone", "iron", "dirt", "timber"]
#     furniture = []
#     creature_classes = [(orc, goblin)]
#     subelement_classes = [wall, floor]
#
# class Cell(pl.place):
#     count = (5, 10)
#     colors = ["unpainted", "grimy"]
#     textures = ["stone", "concrete"]
#     furniture = []
#     creature_classes = [(orc, goblin)]
#     subelement_classes = [wall, floor]
#
# # Then a level type.
# class Dungeon:
#     room_classes = [TortureChamber, Cell]
#     creature_classes = []
#
# LevelStyle.register(Dungeon)
#
# # Another set of rooms
# class ThroneRoom(pl.place):
#     count = (1, 2)
#     colors = ["gold", "red"]
#     textures = ["brick", "stone"]
#     furniture = []
#     creature_classes = [orc, goblin]
#     subelement_classes = [wall, floor]
#
# class Kitchen(pl.place):
#     count = (1, 2)
#     colors = ["dirty", "smoke-stained", "unpainted"]
#     textures = ["brick", "stone"]
#     furniture = []
#     creature_classes = [orc, goblin]
#     subelement_classes = [wall, floor]
#
# # Another level
# class MainFloor:
#     room_classes = [ThroneRoom, Kitchen]
#     creature_classes = []
#
# LevelStyle.register(MainFloor)
#
#
# # And finally, the game itself.
# class Castle():
#     levelorder = [Dungeon, MainFloor]
#     links = [(0,1)]
#     creature_classes = [hydra]
#
# GameStyle.register(Castle)