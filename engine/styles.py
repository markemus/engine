"""Styles are used for game generation.

Do not inherit styles directly or the attributes will be inherited as well. Instead,
register() your classes as abstract subclasses of their parents.

The hierarchy is built like a pyramid, from the ground up. At each level of the hierarchy you can define objects that
will be inherited by all the lower levels."""
import abc
from colorist import Color as C
from . import place as pl


class LevelStyle(abc.ABC):
    """creature_classes structure: [[(creature11, weight11), (creature12, weight12)], [(creature21, weight21)]]"""
    level_text = None
    start_room = None
    end_room = None
    room_classes = []
    creature_classes = []

class GameStyle(abc.ABC):
    levelorder = [LevelStyle, LevelStyle, LevelStyle]
    links = []
    start_splash = None
    win_splash = None
    death_splash = None

class wall(pl.Element):
    name = "wall"
    count = (4, 5)

class single_wall(wall):
    count = (1, 2)

class pillar(pl.Element):
    name = "pillar"
    count = (8, 9)

class floor(pl.Platform):
    name = "floor"
    count = (1, 2)
    canCatch = True

class water(pl.Element):
    name = "water"
    count = (1, 2)

class mirrored_water(pl.Element):
    name = "water"
    count = (1, 2)
    canCatch = True

class lakebed(pl.Platform):
    name = "lakebed"
    count = (1, 2)
    canCatch = True

class door(pl.Element):
    name = "door"
    sprite = "O"
    printcolor = C.RED
    colors = ["red", "blue", "white", "black", "green", "yellow", "purple", "orange"]
    textures = ["painted"]

class channel(pl.Element):
    name = "channel"
    sprite = "O"
    printcolor = C.RED
    colors = ["black", "dark", "murky"]
    textures = ["shallow", "watery"]

class gateway(pl.Element):
    name = "gateway"
    sprite = "O"
    printcolor = C.RED
    colors = ["black", "gray", "brown"]
    textures = ["stone"]

class dwarven_gateway(pl.Element):
    name = "gateway"
    sprite = "O"
    printcolor = C.RED
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]

class staircase(pl.Element):
    name = "staircase"
    sprite = "O"
    printcolor = C.RED
    colors = ["carved", "engraved", "etched", "scrolled"]
    textures = ["granite", "obsidian", "marble"]

def weight_list(clist, weight):
    """Reweights elements in a creature list in preparation for joining with another creature list.
    e.g. creature_list = weight_list(d_creature_lists["caves"], 3) + d_creature_lists["city"]"""
    # Pivot table
    ziplist = list(zip(*clist))
    # Apply weights and pivot back
    weighted_list = list(zip(*[ziplist[0], [x * weight for x in ziplist[1]]]))
    return weighted_list
