import imp, copy

# End of Loading Zone

class thing:
    name = "thing"
    cangrasp = False
    canwear = {"head":0, "body":0, "back":0, "legs":0}
    cantransfer = False             #defines whether an item can hold other items
    location = None
    contents = ""
    vis_inv = []
    invis_inv = []
    visible = True

    #copies over mutable objects for objects so they don't share them with other objects (dereference)
    def __init__(self, newname): 

        self.name = newname
        self.canwear = self.canwear.copy()

    #This is the holy grail of transfer functions.
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

    #check a thing's visible inventory (vis_inv) and sub-inventories
    def viewInv(self):              

        self.contents = "The {0} contains ".format(self.name)
        if self.cantransfer == True:
            
            count = 0

            for carriedThing in self.vis_inv:

                #first thing in vis_inv
                if count == 0:
                    self.contents = self.contents + "a " + carriedThing.name
                    count = count + 1

                #second and later thing in vis_inv
                else:
                    self.contents = self.contents + ", a " + carriedThing.name         

            self.contents = self.contents + "."
            print(self.contents)

            #check sub-inventories
            for carriedThing in self.vis_inv:
                
                if carriedThing.cantransfer == True:
                    carriedThing.viewInv()

        #if thing can't hold stuff
        else:
            print(self.contents + "nothing at all, for it is a " + self.name + ".")       

    #basic describe function, always called desc WIP
    def desc(self):
        print("The " + self.name + " is in the " + self.location.name)

#THINGS

class example(thing):
    cangrasp = True
    canwear = thing.canwear.copy()               #copies item.canwear to dereference.
    canwear["head"] = 1
    canwear["body"] = 1
    canwear["back"] = 1
    canwear["legs"] = 1
    cantransfer = True                          #allows thing to hold stuff

class armor(thing):
    cangrasp = True
    canwear = thing.canwear.copy()        
    canwear["body"] = 1
    cantransfer = False                      

class rucksack(thing):
    cangrasp = True
    canwear = thing.canwear.copy()
    canwear["back"] = 1
    cantransfer = True

class coat(thing):
    cangrasp = True
    canwear = thing.canwear.copy ()
    canwear["body"] = 1
    cantransfer = True

# test objects

# muffalo_duster = coat("muffalo duster")

# armor1 = armor("shiny metal coat")