"""Suits and Collections instruct the game constructor how to create groups of items. Suits are worn by creatures
when they are initialized with place._populate(). Collections are stored in furniture when they are initialized'
with furniture._fill()."""
import copy

# TODO-DONE ensure that each instance of the collection uses the same values from matching tuples- eg shoe and shoe, not shoe and slipper.
#  to do this, we should use a seed instead of random selection from a tuple. This same issue exists for _clothe().
def suit_to_collection(suit, model):
    """Converts a Suit into a Collection."""
    collection = copy.copy(suit)
    collection["contains"] = []

    limbs = model("loader").subelements[0].limb_check("name")
    for limb in limbs:
        if limb.wears in collection["wears"].keys():
            collection["contains"].append(collection["wears"][limb.wears])

    del collection["wears"]
    # print("\n\n", collection["contains"])
    return collection
