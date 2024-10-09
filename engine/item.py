"""Items are used by creatures as clothing, weapons, jewelry etc. Furniture is a special type of
item that is used to fill rooms. Items have an inventory that can hold other items."""
from colorist import Color as C


# TODO not all items need inventories.
# TODO interior and exterior inventories.
class Item:
    name = "Item"
    canwear = {"head": False, "body": False, "back": False, "arm": False, "hand": False, "leg": False}
    # Defines whether an item can hold other items
    cantransfer = False
    location = "loader"
    visible = True
    printcolor = C.BLUE

    def __init__(self, color, texture):
        """Copies over mutable objects for objects so they don't share them with other objects (dereference)."""
        self.canwear = self.canwear.copy()
        self.vis_inv = []
        self.invis_inv = []
        self.color = color
        self.texture = texture

    def transfer(self, who, wherefrom, whereto):
        """A creature moves an item from one inventory to another."""
        if self in wherefrom:
            # Determines that 'who' is able to grasp the item.
            if who.grasp(self):               
                whereto.append(self)
                wherefrom.remove(self)
                who.ungrasp(self)
            else:
                print(f"The {who.name} cannot pick up the {self.name}.")
        else:
            print(f"The {self.name} is not there.")

    # TODO-DECIDE viewInv still needed or just desc?
    def viewInv(self):  
        """Check a thing's visible inventory (vis_inv) and sub-inventories."""
        contents = f"The {self.name} contains "

        if self.cantransfer:
            if not self.vis_inv:
                contents += "nothing."
            else:
                for i, carriedThing in enumerate(self.vis_inv):
                    # Commas
                    if i == 0:
                        contents = contents + "a " + carriedThing.name
                    else:
                        contents = contents + ", a " + carriedThing.name

                contents = contents + "."
            print(contents)

            # Check sub-inventories
            for carriedThing in self.vis_inv:
                if carriedThing.cantransfer:
                    carriedThing.viewInv()

        # If thing can't hold stuff
        else:
            print(f"{contents} nothing at all, for it is a {self.name}.")

    def desc(self, full=True, offset=0):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"* {C.BLUE}{self.color} {self.texture} {self.name}{C.OFF}"
        if full:
            for item in self.vis_inv:
                text += "\n" + item.desc(offset=offset+1)

        return text


if __name__ == '__main__':
    class Example(Item):
        name = "example"
        canwear = Item.canwear.copy()               # copies item.canwear to dereference.
        canwear["head"] = True
        canwear["body"] = True
        canwear["back"] = True
        canwear["legs"] = True
        cantransfer = True                          # allows thing to hold stuff

    class Armor(Item):
        name = "armor"
        canwear = Item.canwear.copy()
        canwear["body"] = True
        cantransfer = False                      

    class Rucksack(Item):
        name = "rucksack"
        canwear = Item.canwear.copy()
        canwear["back"] = True
        cantransfer = True

    class Coat(Item):
        name = "coat"
        canwear = Item.canwear.copy()
        canwear["body"] = True
        cantransfer = True

    # test objects
    muffalo_duster = Coat()
    armor1 = Armor()
    sack = Rucksack()
    sack.vis_inv.append(armor1)
    sack.vis_inv.append(muffalo_duster)
    print(sack.desc())
    sack.viewInv()
