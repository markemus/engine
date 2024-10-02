"""Suits and Collections instruct the game constructor how to create groups of items. Suits are worn by creatures
when they are initialized with place._populate(). Collections are stored in furniture when they are initialized'
with furniture._fill()."""
import copy

def suit_to_collection(suit):
    """Converts a Suit into a Collection."""
    collection = copy.copy(suit)
    collection["contains"] = list(collection["wears"].values())
    del collection["wears"]
    return collection
