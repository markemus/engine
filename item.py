import copy

class thing:
    name = "thing"
    # cangrasp = False
    canwear = {"head":False, "body":False, "back":False, "arm":False, "hand":False, "leg":False}
    cantransfer = False             #defines whether an item can hold other items
    location = "loader"
    # contents = ""
    # vis_inv = []
    # invis_inv = []
    # visible = True

    #copies over mutable objects for objects so they don't share them with other objects (dereference)
    def __init__(self):
        # self.name = newname
        self.canwear = self.canwear.copy()
        self.vis_inv = []
        self.invis_inv = []
        self.visible = True

    #This is the holy grail of transfer functions.
    #it's also a dumb way to do it, you young fool.
    def transfer(self, who, wherefrom, whereto):
        if wherefrom[wherefrom.index(self)] == self:

            #determines that Who is able to grasp the item.
            if who.grasp(self):               
                whereto.append(self)
                del wherefrom[wherefrom.index(self)]
                who.ungrasp(self)

            else:
                print("You cannot transfer the item.")
        else:
            print("Item is not there.")

    def viewInv(self):  
        """
        Check a thing's visible inventory (vis_inv) and sub-inventories.
        """            
        contents = "The {0} contains ".format(self.name)

        if self.cantransfer == True:
            count = 0

            for carriedThing in self.vis_inv:
                #first thing in vis_inv
                if count == 0:
                    contents = contents + "a " + carriedThing.name
                    count = count + 1

                #second and later thing in vis_inv
                else:
                    contents = contents + ", a " + carriedThing.name         

            contents = contents + "."
            print(contents)

            #check sub-inventories
            for carriedThing in self.vis_inv:
                if carriedThing.cantransfer == True:
                    carriedThing.viewInv()
        #if thing can't hold stuff
        else:
            print(contents + "nothing at all, for it is a " + self.name + ".")    

    def desc(self, full=True, offset = 0):
        """
        Basic describe function is always called desc
        """
        text = (" "*offset) + "* " + self.name
        if full:
            for item in self.vis_inv:
                text += "\n" + item.desc(offset = offset+1)

        return text

if __name__ == '__main__':
    
    class example(thing):
        name = "example"
        canwear = thing.canwear.copy()               #copies item.canwear to dereference.
        canwear["head"] = True
        canwear["body"] = True
        canwear["back"] = True
        canwear["legs"] = True
        cantransfer = True                          #allows thing to hold stuff

    class armor(thing):
        name = "armor"
        canwear = thing.canwear.copy()        
        canwear["body"] = True
        cantransfer = False                      

    class rucksack(thing):
        name = "rucksack"
        canwear = thing.canwear.copy()
        canwear["back"] = True
        cantransfer = True

    class coat(thing):
        name = "coat"
        canwear = thing.canwear.copy ()
        canwear["body"] = True
        cantransfer = True

    # test objects
    muffalo_duster = coat()
    armor1 = armor()
    sack = rucksack()
    sack.vis_inv.append(armor1)
    sack.vis_inv.append(muffalo_duster)
    print(sack.desc())