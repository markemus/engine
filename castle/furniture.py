"""Furniture is a type of item used in rooms. They can hold items, specified in collections.

class BathroomCabinet(pl.DisplayFurniture):
    name = "medicine cabinet"
    color = ["gray", "black", "white"]
    texture = ["metal", "steel"]
    # a range specifying how many will spawn per room.
    count = (0, 3)
    # Collections that will be spawned inside this piece of furniture
    vis_collections = [hi.medicine]"""
import castle.household_items as hi
import castle.castle_collections as cst
from engine import place as pl


class Puddle(pl.Furniture):
    name = "puddle"
    color = ["dark", "grimy"]
    texture = ["wet", "moist", "muddy"]
    count = (0, 2)

class Manacles(pl.Furniture):
    name = "pair of manacles"
    color = ["gray"]
    texture = ["steel", "metal", "iron", "rusty"]
    count = (1, 4)

class Rack(pl.Furniture):
    name = "torture rack"
    color = ["black", "gray", "brown"]
    texture = ["leathery", "rusty", "metal", "wood"]
    count = (0, 2)

class Toilet(pl.Furniture):
    name = "toilet"
    color = ["white", "pink"]
    texture = ["ceramic"]
    count = (1, 2)

class Carpet(pl.Furniture):
    name = "carpet"
    color = ["blue and white", "black and silver", "gold and green", "orange", "blue", "black"]
    texture = ["woven", "patterned", "quilted", "soft"]
    count = (0, 2)

class Stove(pl.DisplayFurniture):
    name = "stove"
    color = ["black", "gray", "white"]
    texture = ["steel", "brick"]
    count = (1, 2)
    vis_collections = [(hi.cookery, (1, 5))]

class KitchenCounter(pl.DisplayFurniture):
    name = "counter"
    color = ["black", "gray", "granite", "marble"]
    texture = ["stone"]
    count = (1, 4)
    vis_collections = [(hi.cooking_tools, (1, 2)), (hi.cooking_utensils, (0, 2)), (hi.serving_utensils, (0, 2))]

class Throne(pl.Furniture):
    name = "throne"
    color = ["gold", "red", "black"]
    texture = ["steel", "velvet", "iron", "wood"]
    count = (1, 2)

class Chair(pl.Furniture):
    name = "chair"
    color = ["brown", "beige", "reddish", "black"]
    texture = ["wood"]
    count = (3, 10)

class Table(pl.DisplayFurniture):
    name = "table"
    color = ["black", "red", "green"]
    texture = ["granite", "marble", "wood"]
    count = (1, 2)
    vis_collections = [(hi.silver, (0, 6)), (hi.serving_utensils, (1, 3))]

class TableWork(pl.DisplayFurniture):
    name = "table"
    color = ["brown", "gray", "dirty", "dusty"]
    texture = ["wood"]
    count = (1, 2)
    vis_collections = [(hi.tools, (0, 2))]

class Bed(pl.DisplayFurniture):
    name = "bed"
    color = ["blue", "green", "gray"]
    texture = ["sheeted", "quilted"]
    count = (1, 3)
    vis_collections = [(hi.linens, (1, 2))]

class BedPrison(pl.DisplayFurniture):
    name = "bed"
    color = ["gray", "brown", "dirty"]
    texture = ["mattress"]
    count = (1, 2)
    vis_collections = [(hi.prison_linens, (1, 2))]

class Dresser(pl.DisplayFurniture):
    name = "dresser"
    color = ["brown", "black", "white"]
    texture = ["wood"]
    count = (1, 2)
    vis_collections = [(cst.plainsuit_c, (1, 3))]

class CabinetElegant(pl.DisplayFurniture):
    name = "cabinet"
    color = ["brown", "black", "white"]
    texture = ["wood"]
    count = (0, 3)
    vis_collections = [(hi.silver, (0, 6))]

class CabinetMetal(pl.DisplayFurniture):
    name = "cabinet"
    color = ["gray", "black", "white"]
    texture = ["metal", "steel"]
    count = (0, 3)

class BathroomCabinet(pl.DisplayFurniture):
    name = "medicine cabinet"
    color = ["gray", "black", "white"]
    texture = ["metal", "steel"]
    count = (0, 3)
    vis_collections = [hi.medicine]

# class Theme:
#     name = "DiningRoom"
#     color_scheme = "antique"
#     n = 6
#     # - > table (settings x 6) teak, chair x 6 mahogany, walls x4 paneled

