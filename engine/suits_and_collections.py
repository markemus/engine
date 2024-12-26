"""Suits and Collections instruct the game constructor how to create groups of items. Suits are worn by creatures
when they are initialized with place._populate(). Collections are stored in furniture when they are initialized'
with furniture._fill()."""
import copy


def suit_to_collection(suit, model):
    """Converts a Suit into a Collection."""
    collection = copy.copy(suit)
    collection["contains"] = []

    limbs = model("loader").subelements[0].limb_check("name")
    for limb in limbs:
        if "wears" in collection.keys() and limb.wears in collection["wears"].keys():
            collection["contains"].append(collection["wears"][limb.wears])
        if "grasps" in collection.keys() and limb.wears in collection["grasps"].keys():
            collection["contains"].append(collection["grasps"][limb.wears])

    if "wears" in collection.keys():
        del collection["wears"]
    if "grasps" in collection.keys():
        del collection["grasps"]

    return collection

# TODO make it possible to put a suit on the limbs (subclass limbs with vis_collection?)
def limbs_to_collection(limbs, model, color_scheme="same", texture_scheme="same", full=True):
    """Converts a list of Limbs into a Collection of Limbs (for display in an Item or Furniture).
    Limbs will have colors and textures taken from the model, so you probably want Limbs from
    that same Creature class."""
    collection = {
        "contains": limbs,
        "color": model.colors.copy(),
        "color_scheme": color_scheme,
        "texture": model.textures.copy(),
        "texture_scheme": texture_scheme,
        "full": full,
    }

    return collection