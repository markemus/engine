import copy
import random

# End of Loading Zone

class limb():
    """
    Body parts for Creatures. Store in a list in Creature object.

    Limbs are procedurally generated from the class template; limbs of the same class may still be very different objects.
    """
    name = "NO_NAME_LIMB"
    wears = "generic"
    # cantransfer = False
    hitpoints = 10
    _armor = 0

    def __init__(self, color="d_color", texture="d_texture"):
        self.color = color
        self.texture = texture
        self.subelements = []
        self._elementGen()
        self.inventory = []
        # self.invis_inv = []

    def _elementGen(self):
        for elemclass in self.subelement_classes:
            #choose
            if (type(elemclass) == tuple):
                elemclass = random.choice(elemclass)
            #count
            try:
                potentialRange = elemclass.appendageRange
            except AttributeError:
                raise AttributeError("'{0}' : {1} object has no attribute 'appendageRange'".format(elemclass.name, elemclass))
            
            countRange = random.randrange(potentialRange[0], potentialRange[1])
            #create
            for count in range(countRange):
                elem = elemclass(self.color, self.texture)
                self.subelements.append(elem)

    def desc(self, full=True, offset=0):
        """
        Basic describe function is always called desc
        """
        text = (" "*offset) + "+ {} {} {}".format(self.color, self.texture, self.name)
        if full:
            for item in self.inventory:
                text += "\n" + item.desc(offset = offset+1)
            for elem in self.subelements:
                text += "\n" + elem.desc(offset = offset+1)

        return text

    def limb_check(self, tag):
        """
        Returns a list of all nodes where tag is present.
        tag=name returns all nodes.
        Used for gathering limbs for a task, eg. tag=grasp to pick up an item.
        """
        limb_total = []

        if hasattr(self, tag):
            limb_total.append(self)
        
        for subLimb in self.subelements:

            limb_total += subLimb.limb_check(tag)

        return(limb_total)

    #call on creature!
    def remove_limb(self, limb):
        if limb in self.subelements:
            self.subelements.remove(limb)
        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)

    @property
    def armor(self):
        armor = self._armor

        for item in self.inventory:
            if hasattr(item, "armor"):
                armor += item.armor

        return armor


class weapon(limb):
    """A limb that can deal damage."""
    name = "NO_NAME_WEAPON"
    _damage = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def damage(self):
        damage = self._damage

        for item in self.inventory:
            if hasattr(item, "damage"):
                if item.damage > damage:
                    damage = item.damage
        
        return damage


class creature(object):
    """
    Creatures are procedurally generated from the class template; creatures of the same class may still be very different objects.
    """
    name        = "NO_NAME_CREATURE"
    team        = None
    # cantransfer = False      #can carry items
    # subelements = []         #elements of creature
    location    = "loader"   #name of Place where creature is- object
  
    def __init__(self, name, location):
        self.name = name
        self.color = random.choice(self.colors)
        self.texture = random.choice(self.textures)
        self.inventory = []
        self._elementGen()
        self._clothe()

        self.location = location

    def _elementGen(self):
        baseElem = self.baseElem(self.color, self.texture)
        self.subelements = [baseElem]

    def _clothe(self):
        for suit in self.suits:
            if (type(suit) == tuple):
                suit = random.choice(suit)
            limbs = self.subelements[0].limb_check("name")

            for limb in limbs:
                if limb.wears in suit.keys():

                    #choose and construct
                    article = suit[limb.wears]
                    if (type(article) == tuple):
                        article = random.choice(article)
                    article = article()

                    limb.inventory.append(article)
        
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
        for carriedItem in self.inventory:
            print(carriedItem.name)
            
            if (len(carriedItem.vis_inv) >= 1):
                carriedItem.viewInv()

    def desc(self, full=True, offset=0):
        """
        Basic describe function is always called desc
        """
        text = (" "*offset) + "> " + self.name
        if full:
            for elem in self.subelements:
                text += "\n" + elem.desc(offset = offset+1)

        return text

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
            graspHand.inventory.append(item)
            print(self.name + " picks up the " + item.name + " with their " + graspHand.name + ".")
            grasped = True
        else:
            print(self.name + " cannot pick up the " + item.name + ".")

        return grasped

    def ungrasp(self, item):
        ungrasped = False
        hands = self.subelements[0].limb_check("grasp")

        for hand in hands:
            if item in hand.inventory:
                del hand.inventory[hand.inventory.index(item)]
                ungrasped = True

        return ungrasped

    def remove_limb(self, limb):
        if limb in self.subelements:
            self.subelements.remove(limb)
        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)

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