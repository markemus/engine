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
            if isinstance(collection["wears"][limb.wears], list):
                collection["contains"].extend(collection["wears"][limb.wears])
            else:
                collection["contains"].append(collection["wears"][limb.wears])
        if "grasps" in collection.keys() and limb.wears in collection["grasps"].keys():
            collection["contains"].append(collection["grasps"][limb.wears])

    if "wears" in collection.keys():
        del collection["wears"]
    if "grasps" in collection.keys():
        del collection["grasps"]

    return collection


def limbs_to_collection(limbs, model, color_scheme="same", texture_scheme="same", full=True):
    """Converts a list of Limbs into a Collection of Limbs (for display in an Item or Furniture).
    Limbs will have colors and textures taken from the model, so you probably want Limbs from
    that same Creature class."""
    # We will subclass limbs so that they will have a model attached to them.
    # Note however that limb colors will be generated separately.
    new_limbs = []
    for limb in limbs:
        if type(limb) == tuple:
            new_l = []
            for l in limb:
                # Subclass the limb class so we don't overwrite original class
                new_limb = type(l.__name__, (l,), {})
                new_limb.creature = model(location=None)
                new_l.append(new_limb)
            new_limbs.append(tuple(new_l))
        else:
            # Subclass the limb class so we don't overwrite original class
            new_limb = type(limb.__name__, (limb,), {})
            new_limb.creature = model(location=None)
            new_limbs.append(new_limb)

    collection = {
        "contains": new_limbs,
        "color": model.colors.copy(),
        "color_scheme": color_scheme,
        "texture": model.textures.copy(),
        "texture_scheme": texture_scheme,
        "full": full,
    }

    return collection