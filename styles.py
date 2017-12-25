import abc

from goblin import goblin
from hydra import hydra
from orc import orc

"""
Styles are used for game generation.

Do not inherit styles directly or the attributes will be inherited as well. Instead,
register() your classes as abstract subclasses of their parents.
"""
class RoomStyle(abc.ABC):
    count = (1,2)
    colors = []
    textures = []
    furniture = []
    creatures = []

class LevelStyle(abc.ABC):
    roomstyles = []
    creatures = []

class GameStyle(abc.ABC):
    levelorder = [LevelStyle, LevelStyle, LevelStyle]
    links = []
    creatures = []




#example
class TortureChamber():
    count = (1,3)
    colors = ["black", "gray"]
    textures = ["stone", "iron", "dirt", "timber"]
    furniture = []
    creatures = [orc, goblin]
RoomStyle.register(TortureChamber)

class Cell():
    count = (5,10)
    colors = ["unpainted", "grimy"]
    textures = ["stone", "concrete"]
    furniture = []
    creatures = [orc, goblin]
RoomStyle.register(Cell)

class Dungeon():
    roomstyles = [TortureChamber, Cell]
    creatures = []
LevelStyle.register(Dungeon)




class ThroneRoom():
    count = (1, 2)
    colors = ["gold", "red"]
    textures = ["brick", "stone"]
    furniture = []
    creatures = [orc, goblin]
RoomStyle.register(ThroneRoom)

class Kitchen():
    count = (1, 2)
    colors = ["dirty", "smoke-stained", "unpainted"]
    textures = ["brick", "stone"]
    furniture = []
    creatures = [orc, goblin]
RoomStyle.register(Kitchen)

class MainFloor():
    roomstyles = [ThroneRoom, Kitchen]
    creatures = []
LevelStyle.register(MainFloor)




class Castle():
    levelorder = [Dungeon, MainFloor]
    links = [(0,1)]
    creatures = [hydra]
GameStyle.register(Castle)