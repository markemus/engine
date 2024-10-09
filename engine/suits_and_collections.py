"""Suits and Collections instruct the game constructor how to create groups of items. Suits are worn by creatures
when they are initialized with place._populate(). Collections are stored in furniture when they are initialized'
with furniture._fill()."""
import copy

# TODO ensure that each instance of the collection uses the same values from matching tuples- eg shoe and shoe, not shoe and slipper.
def suit_to_collection(suit, model):
    """Converts a Suit into a Collection."""
    collection = copy.copy(suit)
    collection["contains"] = []
    # limb_counts = {key: 0 for key in collection["wears"].keys()}
    # collection["contains"] = list(collection["wears"].values())
    limbs = model("loader").subelements[0].limb_check("name")
    for limb in limbs:
        if limb.wears in collection["wears"].keys():
            collection["contains"].append(collection["wears"][limb.wears])

    del collection["wears"]
    print("\n\n", collection["contains"])
    return collection
