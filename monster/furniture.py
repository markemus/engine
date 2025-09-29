import engine.place as pl
import monster.item_collections as mcol


class Table(pl.DisplayFurniture):
    name = "table"
    count = (1, 3)
    color = ["gray", "black", "white"]
    texture = ["steel", "aluminum", "metal"]
    vis_collections = [(mcol.test_tubes_col, (0, 2)), (mcol.beaker_col, (0, 2)), (mcol.microscope_col, (0, 2))]


class BrokenCage(pl.Furniture):
    name = "broken cage"
    count = (1, 2)
    color = ["gray", "black"]
    texture = ["steel"]
