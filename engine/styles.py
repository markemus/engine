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
    # TODO we should add a probability that each creature will be generated. Note list-tuple rule in docstring.
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

class door(pl.element):
    name = "door"
    sprite = "O"