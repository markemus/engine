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
    room_classes = []
    creature_classes = []

class GameStyle(abc.ABC):
    levelorder = [LevelStyle, LevelStyle, LevelStyle]
    links = []
    # TODO-DECIDE game level creature classes?
    # creature_classes = []

class wall(pl.Element):
    name = "wall"
    count = (4, 5)

class pillar(pl.Element):
    name = "pillar"
    count = (8, 9)


class floor(pl.Platform):
    name = "floor"
    count = (1, 2)
    # cantransfer = True
    # TODO replace canCatch with hasattr("vis_inv")
    canCatch = True

# TODO doors should have their own color and texture instead of borrowing from room.
# TODO-DECIDE can we add windows for rooms on the edges of the level?
class door(pl.Element):
    name = "door"
    sprite = "O"
    printcolor = C.RED

def weight_list(clist, weight):
    """Reweights elements in a creature list in preparation for joining with another creature list.
    e.g. creature_list = weight_list(d_creature_lists["caves"], 3) + d_creature_lists["city"]"""
    # Pivot table
    ziplist = list(zip(*clist))
    # Apply weights and pivot back
    weighted_list = list(zip(*[ziplist[0], [x * weight for x in ziplist[1]]]))
    return weighted_list

# def populate_levels(gamestyle):
#     """Causes level styles to inherit game parent characteristics."""
#     for level in gamestyle.levelorder:
#         level.creature_classes += gamestyle.creature_classes
