import engine.place as pl

import monster.item_collections as mcol

import assets.potions as pot


lt = {
    "l1_chest_potion": [(pot.PotionOfStoneskin, 1), (pot.TentacleGrowthPotion, 1), (pot.PotionOfHealing, 1), (pot.PotionOfBaseMana, 3), (pot.PotionOfMight, 1)],
}


class Table(pl.DisplayFurniture):
    name = "table"
    count = (1, 3)
    color = ["gray", "black", "white"]
    texture = ["steel", "aluminum", "metal"]
    vis_collections = [(mcol.test_tubes_col, (0, 2)), (mcol.beaker_col, (0, 2)), (mcol.microscope_col, (0, 2))]
    loot_tables = [lt["l1_chest_potion"]]


class BrokenCage(pl.Furniture):
    name = "broken cage"
    count = (1, 2)
    color = ["black"]
    texture = ["steel"]
