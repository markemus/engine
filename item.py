import imp, copy

class thing:
    name = "thing"
    # cangrasp = False
    canwear = {"head":0, "body":0, "back":0, "legs":0}
    cantransfer = False             #defines whether an item can hold other items
    location = None
    # contents = ""
    # vis_inv = []
    # invis_inv = []
    # visible = True

    #copies over mutable objects for objects so they don't share them with other objects (dereference)
    def __init__(self, newname):
        self.name = newname
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

    #basic describe function, always called desc WIP
    def desc(self):
        print("The " + self.name + " is in the " + self.location.name)


if __name__ == '__main__':
    
    class example(thing):
        # cangrasp = True
        # canwear = thing.canwear.copy()               #copies item.canwear to dereference.
        canwear["head"] = 1
        canwear["body"] = 1
        canwear["back"] = 1
        canwear["legs"] = 1
        cantransfer = True                          #allows thing to hold stuff

    class armor(thing):
        # cangrasp = True
        # canwear = thing.canwear.copy()        
        canwear["body"] = 1
        cantransfer = False                      

    class rucksack(thing):
        # cangrasp = True
        # canwear = thing.canwear.copy()
        canwear["back"] = 1
        cantransfer = True

    class coat(thing):
        # cangrasp = True
        # canwear = thing.canwear.copy ()
        canwear["body"] = 1
        cantransfer = True

    # test objects

    muffalo_duster = coat("muffalo duster")
    armor1 = armor("shiny metal coat")