"""Furniture is a type of item used in rooms. They can hold items, specified in collections.
'count' is a range specifying how many will spawn per room."""
import castle.household_items as hi
import castle.castle_collections as cst
from engine import place as pl


class Puddle(pl.furniture):
    name = "puddle"
    color = ["dark", "grimy"]
    texture = ["wet", "moist", "muddy"]
    count = (0, 2)

class Manacles(pl.furniture):
    name = "pair of manacles"
    color = ["gray"]
    texture = ["steel", "metal", "iron", "rusty"]
    count = (1, 4)

class Rack(pl.furniture):
    name = "torture rack"
    color = ["black", "gray", "brown"]
    texture = ["leathery", "rusty", "metal", "wood"]
    count = (0, 2)

class Toilet(pl.furniture):
    name = "toilet"
    color = ["white", "pink"]
    texture = ["ceramic"]
    count = (1, 2)

class Carpet(pl.furniture):
    name = "carpet"
    color = ["blue and white", "black and silver", "gold and green", "orange", "blue", "black"]
    texture = ["woven", "patterned", "quilted", "soft"]
    count = (0, 2)

class Stove(pl.furniture):
    name = "stove"
    color = ["black", "gray", "white"]
    texture = ["steel", "brick"]
    count = (1, 2)

class Throne(pl.furniture):
    name = "throne"
    color = ["gold", "red", "black"]
    texture = ["steel", "velvet", "iron", "wood"]
    count = (1, 2)

class Chair(pl.furniture):
    name = "chair"
    color = ["brown", "beige", "reddish", "black"]
    texture = ["wood"]
    count = (3, 10)

class Table(pl.furniture):
    name = "table"
    color = ["black", "red", "green"]
    texture = ["granite", "marble", "wood"]
    count = (1, 2)
    cantransfer = True
    vis_collections = [(hi.silver, (0, 6))]

class TableWork(pl.furniture):
    name = "table"
    color = ["brown", "gray", "dirty", "dusty"]
    texture = ["wood"]
    count = (1, 2)
    cantransfer = True
    vis_collections = [(hi.tools, (0, 2))]

class Bed(pl.furniture):
    name = "bed"
    color = ["blue", "green", "gray"]
    texture = ["sheeted", "quilted"]
    count = (1, 3)
    vis_collections = [(hi.linens, (1, 2))]

class Dresser(pl.furniture):
    name = "dresser"
    color = ["brown", "black", "white"]
    texture = ["wood"]
    count = (1, 2)
    cantransfer = True
    # TODO this should be an invis_collections
    vis_collections = [(cst.plainsuit_c, (1, 3))]

class CabinetElegant(pl.furniture):
    name = "cabinet"
    color = ["brown", "black", "white"]
    texture = ["wood"]
    count = (0, 3)
    vis_collections = [(hi.silver, (0, 6))]

class CabinetMetal(pl.furniture):
    name = "cabinet"
    color = ["gray", "black", "white"]
    texture = ["metal", "steel"]
    count = (0, 3)

# class Theme:
#     name = "DiningRoom"
#     color_scheme = "antique"
#     n = 6
#     # - > table (settings x 6) teak, chair x 6 mahogany, walls x4 paneled


# TODO add contentsets from household_items.


# TODO vis_inv and invis_inv. vis_inv should be displayed in place.desc(),
#  and objects with invis_inv should be marked with * in desc().

# TODO interaction with objects with inventories (place and remove)
