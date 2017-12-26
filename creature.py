# import place, item, interface
import imp, copy, random

place = imp.load_source("place", "place.py")
item = imp.load_source("item", "item.py")

# End of Loading Zone

#dict of all creatures.
creatures = {}

class element():
    """
    General sub-parts of creatures
    """
    name = "NO_NAME_ELEMENT"
    subelements = []

class limb(element):
    """
    Body parts for Creatures. Store in a list in Creature object.

    Limbs are procedurally generated from the class template; limbs of the same class may still be very different objects.
    """
    name = "NO_NAME_LIMB"
    vis_inv = []
    invis_inv = []
    cantransfer = False
    hitpoints = 10

    def __init__(self, color="d_color", texture="d_texture"):
        self.color = color
        self.texture = texture
        self.subelements = copy.deepcopy(self.subelements)
        self._elementGen()
        self.vis_inv = copy.deepcopy(self.vis_inv)
        self.invis_inv = copy.deepcopy(self.invis_inv)

    def _elementGen(self):
        for elemclass in self.subelement_classes:
            #choose
            if (type(elemclass) == tuple):
                elemclass = random.choice(elemclass)
            #range
            try:
                potentialRange = elemclass.appendageRange
            except AttributeError:
                raise AttributeError("'{0}' : {1} object has no attribute 'appendageRange'".format(elemclass.name, elemclass))
            
            countRange = random.randrange(potentialRange[0], potentialRange[1])
            #create
            for count in range(countRange):
                elem = elemclass(self.color, self.texture)
                self.subelements.append(elem)

    def desc(self):                          #prints all the body parts connected below the element.
        print("{0} {1} {2} ({3}) contains:".format(self.color, self.texture, self.name, self.hitpoints))
        
        for element in self.subelements:
            print(element.name)

        print("")

        for element in self.subelements:
            # print("{0} contains:".format(element.name))
            if len(element.subelements) >= 1:
                element.desc()

    #checks if necessary limbs are present for a task. Creatures must have "body" subelement at subelements[0]
    def limb_check(self, tag):
        limb_total = []

        if hasattr(self, tag):
            limb_total.append(self)
        
        for subLimb in self.subelements:

            limb_total += subLimb.limb_check(tag)

        return(limb_total)

    #call on subelements[0]
    def remove_limb(self, limb):
        if limb in self.subelements:
            self.subelements.remove(limb)

        for subLimb in self.subelements:
            subLimb.remove_limb(limb)   

    def get_vis_inv(self):
        return self.vis_inv




class creature(object):
    """
    Creatures are procedurally generated from the class template; creatures of the same class may still be very different objects.
    """
    name        = "NO_NAME_CREATURE"
    team        = None
    cantransfer = False      #can carry items
    subelements = []         #elements of creature
    location    = "loader"   #name of Place where creature is- object
    vis_inv     = []
    invis_inv   = []
  
    def __init__(self, name, color="d_color", texture="d_texture"):
        self.name = name
        self.color = random.choice(self.colors)
        self.texture = random.choice(self.textures)
        self.vis_inv = []
        self.invis_inv = []
        # self.subelements = []
        self._elementGen()

        #generates new creatures and puts them in the creature.creatures dict (SHOULD BE A FILE, NOT PERSISTENT, fine for now)
        creatures.update({self.name: copy.deepcopy(self)})

    def _elementGen(self):
        baseElem = self.baseElem(self.color, self.texture)
        self.subelements = [baseElem]
        
    #move to a new Place. Accepts a str input.
    #can only move between bordered Places with this function. Should have a failure option
    def leave(self, direction):
        left = False
        currentRoom = self.location
        nextRoom = self.location.borders[direction]

        if nextRoom != None:
            if len(self.subelements[0].limb_check("amble")) >= 1:
                currentRoom.removeCreature(self)
                self.location = currentRoom.borders[direction]
                nextRoom.addCreature(self)
                left = True
                print("You leave %s and enter %s." % (currentRoom.name, nextRoom.name))
        else:
            print("There is no way out in that direction.")

        return left

    #examine Creature inventory and held Item inventories. Recursive
    def viewInv(self):

        for carriedItem in self.vis_inv:

            print(carriedItem.name)
            
            if (len(carriedItem.vis_inv) >= 1):
                carriedItem.viewInv()

    #describes a creature's visible elements
    def fullDesc(self):                 
        print("{0} {1} {2} contains:".format(self.color, self.texture, self.name))            #creature contains:

        for theElement in self.subelements:                    #the following elements
            print(theElement.name)
        
        for theElement in self.subelements:                    #these elements contain the following elements
            if len(theElement.subelements) >= 1:
                print("")
                theElement.desc()

    #tag: isSurface
    def desc(self):
        vis_elements = self.subelements[0].limb_check("isSurface")

        print("\n{0} {1} {2}:".format(self.color, self.texture, self.name))
        for element in vis_elements:
            print("a {0} {1} {2} ({3})".format(element.color, element.texture, element.name, element.hitpoints))

    def grasp_check(self):

        graspHand = None
        hands = self.subelements[0].limb_check("grasp")
        
        if len(hands) >= 1:
            
            for hand in hands:

                if hand.grasp >= 1:
                    f_grasp = 0
                    t_grasp = 0

                    for finger in hand.limb_check("f_grasp"):
                        f_grasp += finger.f_grasp
                    for thumb in hand.limb_check("t_grasp"):
                        t_grasp += thumb.t_grasp

                    if f_grasp >= 1 and t_grasp >= 1:
                        graspHand = hand
                        break

        return graspHand

    def grasp(self, item):

        grasped = False
        graspHand = self.grasp_check()
                        
        if graspHand != None:
            graspHand.vis_inv.append(item)
            print(self.name + " picks up the " + item.name + " with their " + graspHand.name + ".")
            grasped = True
        else:
            print(self.name + " cannot pick up the " + item.name + ".")

        return grasped

    def ungrasp(self, item):
        ungrasped = False
        hands = self.subelements[0].limb_check("grasp")

        for hand in hands:
            if item in hand.vis_inv:
                del hand.vis_inv[hand.vis_inv.index(item)]
                ungrasped = True

        return ungrasped

    def speak(self, words, listener):
        room = self.location.get_creatures()

        if listener in room:
            listener.listen(words, self)
        else:
            print("Who are you talking to?")

    def listen(self, words, speaker):
        print(speaker.name + " says: " + '"' + words + '".')
        print(self.name + " listens carefully.")

    def get_location(self):
        return self.location

    def get_team(self):
        return self.team