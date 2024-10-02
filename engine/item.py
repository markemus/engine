class Item:
    name = "Item"
    canwear = {"head": False, "body": False, "back": False, "arm": False, "hand": False, "leg": False}
    # Defines whether an item can hold other items
    cantransfer = False
    location = "loader"
    visible = True

    def __init__(self):
        """Copies over mutable objects for objects so they don't share them with other objects (dereference)."""
        self.canwear = self.canwear.copy()
        self.vis_inv = []
        self.invis_inv = []

    # This is the holy grail of transfer functions.
    # It's also a dumb way to do it, you young fool.
    # Agreed. I think. It's weird. But it ain't broke?
    def transfer(self, who, wherefrom, whereto):
        # TODO this will raise an exception if item is not in wherefrom
        # if wherefrom[wherefrom.index(self)] == self:
        if self in wherefrom:
            # Determines that Who is able to grasp the item.
            if who.grasp(self):               
                whereto.append(self)
                # del wherefrom[wherefrom.index(self)]
                wherefrom.remove(self)
                who.ungrasp(self)
            else:
                print("The %s cannot pick up the %s." % (who.name, self.name))
        else:
            print("The %s is not there." % self.name)

    # TODO viewInv still needed or just desc?
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
        text = (" "*offset) + "* " + self.name
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
