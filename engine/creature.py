import math
import random

from engine import ai

from colorist import Color as C
from colorist import BrightColor as BC


class Limb:
    """Body parts for Creatures. Store in a list in Creature object.

    Limbs are procedurally generated from the class template; limbs of the same class may still be
    very different objects."""
    name = "NO_NAME_LIMB"
    printcolor = BC.CYAN
    # Subelement classes are limbs that will be spawned attached to this limb
    subelement_classes = None
    wears = None
    base_hp = 10
    _armor = 1
    blocker = False
    grasped = None
    # Size should be an int between 1 and 3. This affects to-hit chance.
    size = 2
    isSurface = True
    # Passive effects will be cast before battle begins (if they aren't already active)
    passive_effects = []
    # Impact effects will be cast when limb is hit
    impact_effects = []
    can_heal = True
    can_bleed = True
    resurrected = False
    can_burn = True
    creature = None

    def __init__(self, color, texture, creature=None):
        self.color = color
        self.texture = texture
        if creature:
            self.creature = creature
        self.subelements = []
        self._elementGen()
        self.equipment = []
        self.covered = []
        self.active_effects = []
        self.passive_effects = self.passive_effects.copy()
        self.impact_effects = self.impact_effects.copy()
        self.hp = self.base_hp

    def _elementGen(self):
        """Creates subelements from the subelement classes specified in the class definition."""
        for elemclass in self.subelement_classes:
            # Choose
            if type(elemclass) == tuple:
                elemclass = random.choice(elemclass)

            # Allows for optional limbs with (elemclass1, elemclass2, None)
            if elemclass is not None:
                # Count
                try:
                    potentialRange = elemclass.appendageRange
                except AttributeError:
                    raise AttributeError("'{0}' : {1} object has no attribute 'appendageRange'".format(elemclass.name, elemclass))

                countRange = random.randrange(potentialRange[0], potentialRange[1])

                # Create
                # If element has its own color definitions, use those (eg hair). Most elements should just inherit parent color.
                if hasattr(elemclass, "colors"):
                    color = random.choice(elemclass.colors)
                    texture = random.choice(elemclass.textures)
                else:
                    color = self.color
                    texture = self.texture

                for count in range(countRange):
                    elem = elemclass(color, texture, self.creature)
                    self.subelements.append(elem)

    def desc(self, full=True, offset=0, stats=True):
        """Basic describe function is always called desc."""
        text = (" "*offset) + f"+ "
        unique_effects = {x.__class__: x for x in self.active_effects}.values()
        for effect in unique_effects:
            if effect.desc:
                text += f"{BC.RED}{effect.desc}{BC.OFF} "
        text += f"{C.YELLOW}{self.color} {self.texture} {self.name}{C.OFF}"
        if stats:
            text += f" {C.RED}({self.hp}/{self.base_hp}) {C.BLUE}({self.armored}) {C.YELLOW}({self.size}){C.OFF}"
        if full:
            for item in self.covered:
                text += "\n" + item.desc(offset=offset+1, )
            if hasattr(self, "grasped") and self.grasped:
                text += "\n" + self.grasped.desc(offset=offset+1)
            for elem in self.subelements:
                text += "\n" + elem.desc(offset=offset+1, stats=stats)

        return text

    def limb_check(self, tag):
        """Returns a list of all limbs where tag is present (on the limb or on an inventory item).
        tag=name returns all limbs.
        Used for gathering limbs for a task, eg. tag=grasp to pick up an item."""
        limb_total = []

        # Allows for items with that tag to be used as if they were a limb themselves.
        if hasattr(self, tag) or sum([hasattr(x, tag) for x in self.equipment]):
            limb_total.append(self)
        
        for subLimb in self.subelements:
            limb_total += subLimb.limb_check(tag)

        return(limb_total)

    def limb_count(self, tag):
        """Counts total of tag value in subelements."""
        limbs = self.limb_check(tag)

        limb_total = 0
        for limb in limbs:
            if hasattr(limb, tag):
                limb_total += getattr(limb, tag)
            for x in limb.equipment:
                if hasattr(x, tag):
                    limb_total += getattr(x, tag)

        return limb_total

    def find_invs(self):
        """Find all inventories lower in the body hierarchy."""
        invs = []

        # if self.equipment:
        #     invs.append(self)

        # Equipped items
        for item in self.equipment:
            if hasattr(item, "vis_inv"):
                invs.append(item)

        # Held item
        if hasattr(self, "grasped"):
            if hasattr(self.grasped, "vis_inv"):
                invs.append(self.grasped)

        for subLimb in self.subelements:
            invs += subLimb.find_invs()

        return invs

    def find_equipped(self):
        """Recursive search for limbs that have equipment on them."""
        equipped = []
        if self.equipment:
            equipped.append(self)
        for limb in self.subelements:
            equipped.extend(limb.find_equipped())

        return equipped

    def remove_limb(self, limb):
        if limb in self.subelements:
            # Expire limb effects
            for sublimb in limb.limb_check("name"):
                for effect in sublimb.active_effects.copy():
                    if effect.expire_on_removal:
                        effect.expire()

            self.subelements.remove(limb)

            # Remove covering equipment
            for item in limb.covered.copy():
                if item not in limb.equipment:
                    for sublimb in limb.limb_check("name"):
                        if item in sublimb.covered:
                            sublimb.covered.remove(item)
        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)

    def transfer(self, who, wherefrom, whereto):
        """A creature moves a removed limb from one inventory to another."""
        if self in wherefrom:
            # Determines that 'who' is able to grasp the item.
            if who.grasp(self):
                whereto.append(self)
                wherefrom.remove(self)
                who.ungrasp(self)
                print(f"{BC.CYAN}{who.name} puts away the {self.name}.{BC.OFF}")
            else:
                print(f"{C.RED}{who.name} cannot pick up the {self.name}.{C.OFF}")
        else:
            print(f"{C.RED}The {self.name} is not there.{C.OFF}")

    def equip(self, article):
        """Put an Item (article) onto the Limb.
        article.requires can specify a required tag as ("tag", amount).
        article.level specifies the level it will be equipped at. Each Limb can only equip one Item at each level."""
        equipped = False
        if article.canwear[self.wears]:
            # TODO-DECIDE refactor a.requires to allow parent and child requirements? Right now it's not practical. And not used.
            if not article.requires or (hasattr(self, article.requires[0]) and (getattr(self, article.requires[0]) >= article.requires[1])):
                # Check level if empty
                already_equipped = [x for x in self.equipment if x.level == article.level]
                if not already_equipped:
                    # Insert equipment at proper level for equipment
                    i = 0
                    levels = [x.level for x in self.equipment]
                    for i, level in enumerate(levels):
                        if level > article.level:
                            break
                    else:
                        i += 1
                    self.equipment.insert(i, article)

                    # Insert equipment at proper level for covers
                    i = 0
                    levels = [x.level for x in self.covered]
                    for i, level in enumerate(levels):
                        if level > article.level:
                            break
                    else:
                        i += 1
                    self.covered.insert(i, article)

                    # Equipment should cover lower limbs if applicable.
                    # Items that cover should always have a 'descends' tag.
                    if hasattr(article, "descends"):
                        potentially_cover = self.return_from_depth(article.descends)[1:]
                        for subelement in potentially_cover:
                            if article.covers[subelement.wears]:
                                # Insert equipment at proper level
                                i = 0
                                levels = [x.level for x in subelement.covered]
                                for i, level in enumerate(levels):
                                    if level > article.level:
                                        break
                                else:
                                    i += 1
                                subelement.covered.insert(i, article)
                    equipped = True
                else:
                    print(f"{C.RED}{self.name} already has a {already_equipped[0].name} equipped!{C.OFF}")
            else:
                print(f"{C.RED}{self.name} lacks the {article.requires[0]} ability!{C.OFF}")
        else:
            print(f"{C.RED}{self.name} cannot wear a {article.name}!{C.OFF}")

        return equipped

    def unequip(self, gear, force_off=False):
        """Remove a piece of gear from equipment."""
        removed = False
        if gear in self.equipment:
            if (not (hasattr(gear, "cannot_remove") and gear.cannot_remove)) or (force_off):
                self.equipment.remove(gear)
                self.remove_from_covers(gear)
                removed = True
            else:
                print(f"The {BC.YELLOW}{gear.name}{BC.OFF} cannot be removed.")
        return removed

    def remove_from_covers(self, gear):
        """Recursively remove a piece of equipment from self.covers.
        This is necessary because a piece of equipment is only equipped
        on one limb, but can cover lower limbs as well."""
        if gear in self.covered:
            self.covered.remove(gear)
        for limb in self.subelements:
            limb.remove_from_covers(gear)

    def return_from_depth(self, depth):
        """Returns a list of all subelements down to 'depth' in the subelement tree."""
        depth_elements = [self]
        if depth:
            for subelement in self.subelements:
                depth_elements += subelement.return_from_depth(depth-1)
        return depth_elements

    def get_neighbors(self, limb):
        """Always call this method on root element of the creature- creature.subelements[0].get_neighbors(limb)."""
        neighbors = []
        if self is limb:
            # This will occur if limb is first element checked.
            # Therefore, always call this method on root element of the creature or you will miss parent element.
            neighbors = [*self.subelements]
        elif limb in self.subelements:
            neighbors = [self, *[x for x in self.subelements if x is not limb], *limb.subelements]
        else:
            for x in self.subelements:
                neighbors.extend(x.get_neighbors(limb))

        return neighbors

    def get_parents(self, limb):
        """Returns the line of descent through the limb tree down to the limb."""
        if self == limb:
            return [self]
        else:
            for subelement in self.subelements:
                parents = subelement.get_parents(limb)
                if parents:
                    return [self] + parents

        return False

    def is_subelement(self, limb):
        """Returns True if limb is in this Limb's subelement hierarchy."""
        sub = False
        for subelement in self.subelements:
            sub = subelement.is_subelement(limb)
            if sub:
                break
        if limb in self.subelements or limb is self:
            sub = True
        return sub

    @property
    def armored(self):
        armor = self._armor

        for item in self.covered:
            if hasattr(item, "armor"):
                armor += item.armor

        if self.grasped:
            if hasattr(self.grasped, "armor"):
                armor += self.grasped.armor

        return armor



class Weapon(Limb):
    """A limb that can deal damage."""
    name = "NO_NAME_WEAPON"
    _damage = 0
    blockable = True
    weapon_effects = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weapon_effects = self.weapon_effects.copy()

    @property
    def damage(self):
        """This will return the amount of damage and the item that is causing it.
        This is important for the UI and possibly for other calculations.

        When checking damage, use limb.damage[0] to reference damage alone."""
        damage = self._damage
        item = self

        # EG gauntlets, spiked gloves, fake fangs. self.grasped is eg swords
        for _item in self.equipment + [self.grasped]:
            if hasattr(_item, "damage"):
                if _item.damage > damage:
                    damage = _item.damage
                    item = _item

        return damage, item


class creature:
    """Creatures are procedurally generated from the class template; creatures of the same class may still be very
    different objects."""
    classname = "NO_NAME_CREATURE"
    team = None
    printcolor = BC.CYAN
    # subelements = []         # elements of creature
    location = None   # name of Place where creature is- object
    aggressive = True
    dead = False
    can_transform = True
    can_fear = True
    can_rest = True
    can_breathe = True
    can_stun = True
    can_poison = True
    bled = 0
    poisoned = 0
    afraid = False
    stunned = False
    # Increases to-hit rolls
    mastery = 0
  
    def __init__(self, location):
        self.name = random.choice(self.namelist)
        self.color = random.choice(self.colors)
        self.texture = random.choice(self.textures)
        self._elementGen()
        self._clothe()

        self.location = location
        self.ai = ai.CombatAI(self)
        self.spellbook = []
        # Companions will follow a creature around.
        self.companions = []

    def _elementGen(self):
        baseElem = self.baseElem(self.color, self.texture, self)
        self.subelements = [baseElem]

    def _clothe(self):
        """Equips a creature when it is first created. Multiple suits can be applied in sequence, so weapons
        can be added after armor etc. Note that color schemes will be shared across weapons and armor, so it
        might make sense to split them into separate suits."""
        # Seed is to coordinate item selection across limbs of the same type, we don't get eg shoe+slipper
        seed = random.randint(0, 100)
        for suit in self.suits:
            # print(suit)
            if (type(suit) == tuple):
                suit = random.choice(suit)
            # Returns all limbs
            limbs = self.subelements[0].limb_check("name")

            # Color and texture are either set once for the full suit, or uniquely per "wears" (so socks will always match)
            if suit["color_scheme"] == "distinct":
                colors = {key: random.choice(suit["color"]) for key in {**suit["wears"], **suit["grasps"]}}
            elif suit["color_scheme"] == "same":
                c = random.choice(suit["color"])
                colors = {key: c for key in {**suit["wears"], **suit["grasps"]}}
            if suit["texture_scheme"] == "distinct":
                textures = {key: random.choice(suit["texture"]) for key in {**suit["wears"], **suit["grasps"]}}
            elif suit["texture_scheme"] == "same":
                t = random.choice(suit["texture"])
                textures = {key: t for key in {**suit["wears"], **suit["grasps"]}}

            # If suit is not supposed to be full, drop a random subset of limbs
            if not suit["full"]:
                random.shuffle(limbs)
                limbs = limbs[:random.randrange(0, len(limbs))]

            for limb in limbs:
                if "wears" in suit.keys() and limb.wears in suit["wears"].keys():
                    # Choose and construct articles
                    article = suit["wears"][limb.wears]
                    if type(article) == tuple:
                        # We want article choices to be coordinated, so we use the same seed for each tuple selection (eg pairs of shoes).
                        random.seed(seed)
                        articles = [random.choice(article)]
                        random.seed()
                    elif type(article) == list:
                        articles = article.copy()
                        if not suit["full"]:
                            random.shuffle(articles)
                            articles = articles[:random.randrange(0, len(articles))]
                    else:
                        articles = [article]

                    for article in articles:
                        # Create article and equip
                        # For unique color scheme, each item gets its own color and texture
                        if suit["color_scheme"] == "unique":
                            color = random.choice(suit["color"])
                        else:
                            color = colors[limb.wears]
                        if suit["texture_scheme"] == "unique":
                            texture = random.choice(suit["texture"])
                        else:
                            texture = textures[limb.wears]
                        if article is not None:
                            article = article(color=color, texture=texture)
                            limb.equip(article)

                if "grasps" in suit.keys() and limb.wears in suit["grasps"].keys():
                    # We don't need to coordinate weapon selections
                    # Choose and construct articles
                    weapon = suit["grasps"][limb.wears]
                    if type(weapon) == tuple:
                        weapons = [random.choice(weapon)]
                    elif type(weapon) == list:
                        weapons = weapon.copy()
                    else:
                        weapons = [weapon]

                    for weapon in weapons:
                        if not limb.grasped:
                            # Create weapon and grasp
                            if suit["color_scheme"] == "unique":
                                color = random.choice(suit["color"])
                            else:
                                color = colors[limb.wears]
                            if suit["texture_scheme"] == "unique":
                                texture = random.choice(suit["texture"])
                            else:
                                texture = textures[limb.wears]
                            if weapon is not None:
                                weapon = weapon(color=color, texture=texture)
                                limb.grasped = weapon

        # Reset seed
        random.seed()

    def auto_clothe_article(self, article):
        """Tries to find a spot for a particular item."""
        for limb in self.limb_check("wears"):
            if article.canwear[limb.wears]:
                other_article = [x for x in limb.equipment if x.level == article.level]
                if other_article:
                    other_article = other_article[0]
                    if hasattr(article, "armor") and hasattr(other_article, "armor"):
                        if article.armor > other_article.armor:
                            if limb.unequip(other_article):
                                self.location.drop_item(other_article)
                                if limb.equip(article):
                                    print(f"{BC.CYAN}{self.name} replaces the {other_article.color} {other_article.texture} {other_article.name} with {article.color} {article.texture} {article.name}.{BC.OFF}")
                                    return True
                            else:
                                print(f"{C.RED}{other_article.name} cannot be replaced!{C.OFF}")
                                return False
                    else:
                        print(f"{C.RED}{self.name} is unsure whether to replace {other_article.name} with {article.name}.{C.OFF}")
                        return False
                else:
                    if limb.equip(article):
                        print(f"{BC.CYAN}{self.name} dons {article.color} {article.texture} {article.name}.")
                        return True

    def auto_equip(self):
        """Automatically put on clothing from surrounding room. Does not have limb_check because controller will
        do that on whichever creature is doing the auto_clothing."""
        for inv in self.location.find_invs():
            for article in inv.vis_inv.copy():
                if hasattr(article, "canwear"):
                    if self.auto_clothe_article(article):
                        inv.vis_inv.remove(article)

        for equipped_limb in self.location.find_equipment():
            for article in equipped_limb.equipment.copy():
                if hasattr(article, "canwear"):
                    if self.auto_clothe_article(article):
                        equipped_limb.unequip(article)

    def desc(self, full=True, offset=0, stats=True):
        """Basic describe function is always called desc."""
        text = (" " * offset) + f"> {self.printcolor}{self.name} ({self.classname}){C.OFF}"
        if full:
            for elem in self.subelements:
                text += "\n" + elem.desc(offset=offset + 1, stats=stats)

        return text


    # Can only move between bordered Places with this function. Should have a failure option.
    def leave(self, direction):
        """Move to a new Place. Accepts a str input."""
        left = False
        currentRoom = self.location
        nextRoom = self.location.borders[direction]

        if nextRoom:
            # if len(self.subelements[0].limb_check("amble")) >= 1:
            if (self.limb_count("amble") >= 1) or (self.limb_count("flight") >= 1):
                currentRoom.removeCreature(self)
                self.location = currentRoom.borders[direction]
                nextRoom.addCreature(self)
                left = True
                print(f"{BC.CYAN}{self.name}{BC.OFF} leaves {C.RED}{currentRoom.name}{C.OFF} and enters {C.RED}{nextRoom.name}{C.OFF}.")
                for companion in self.get_companions():
                    if companion.location == currentRoom:
                        companion.leave(direction=direction)
                # if nextRoom.borders[">"]:
                #     print(f"{BC.CYAN}There is an exit here.{BC.OFF}")
            else:
                print(f"{C.RED}{self.name} is unable to move.{C.OFF}")
        else:
            print("There is no way out in that direction.")

        return left

    def limb_check(self, tag):
        """Returns a list of all limbs where tag is present (on the limb or on an inventory item).
        tag=name returns all limbs.
        Used for gathering limbs for a task, eg. tag=grasp to pick up an item."""
        if self.subelements:
            limbs = self.subelements[0].limb_check(tag)
        else:
            limbs = []

        return limbs

    def limb_count(self, tag):
        """Counts total of tag value in subelements."""
        if self.subelements:
            limbs = self.subelements[0].limb_check(tag)
        else:
            limbs = []

        limb_total = 0
        for limb in limbs:
            if hasattr(limb, tag):
                limb_total += getattr(limb, tag)
            for x in limb.equipment:
                if hasattr(x, tag):
                    limb_total += getattr(x, tag)

        return limb_total

    def grasp_check(self):
        """Grasps an item with the first available appendage."""
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

                    # check that hand is empty.
                    if f_grasp >= 1 and t_grasp >= 1:
                        if not hand.grasped:
                            graspHand = hand
                            break

        return graspHand

    def grasp(self, item):
        """Pick up an item with an appendage."""
        grasped = False
        graspHand = self.grasp_check()
                        
        if graspHand is not None and not graspHand.grasped:
            graspHand.grasped = item
            print(f"{BC.CYAN}{self.name} picks up the {item.name} with their {graspHand.name}.{BC.OFF}")
            grasped = True
        else:
            print(f"{C.RED}{self.name} does not have a free hand to pick up the {item.name}.{C.OFF}")

        return grasped

    def ungrasp(self, item):
        """Ungrasp an item from an appendage. The calling function will need to determine where to put it next."""
        ungrasped = False
        hands = self.subelements[0].limb_check("grasp")

        for hand in hands:
            if hand.grasped == item:
                hand.grasped = None
                ungrasped = True
                break

        return ungrasped

    def unequip_suit(self, suit):
        """Remove all items that belong to a suit of equipment."""
        limbs = self.subelements[0].limb_check("wears")
        to_remove = []
        # Suits can contain tuples or lists for optional or multiple items.
        for x in suit["wears"].values():
            if isinstance(x, (tuple, list)):
                to_remove.extend(x)
            else:
                to_remove.append(x)
        to_remove = tuple(to_remove)
        # print(to_remove)

        for limb in limbs:
            for equipment in limb.equipment.copy():
                if isinstance(equipment, to_remove):
                    limb.unequip(equipment)

    def get_neighbors(self, limb):
        return self.subelements[0].get_neighbors(limb)

    def get_parents(self, limb):
        """Returns the line of descent through the limb tree down to the limb."""
        parents = self.subelements[0].get_parents(limb)
        return parents

    def update_status(self):
        """Checks all limbs for necessary tags and updates status."""
        limbs = self.subelements[0].limb_check("name")
        for limb in limbs:
            if hasattr(limb, "grasp"):
                if not (limb.limb_count("f_grasp") >= 1) or not (limb.limb_count("t_grasp") >= 1):
                    if limb.grasped:
                        self.location.drop_item(limb.grasped)
                        limb.grasped = None


    def remove_limb(self, limb):
        if limb in self.subelements:
            # Limb is the core limb. Just die and don't try checking statuses since we're removing the whole limb tree.
            # Expire limb effects
            for sublimb in limb.limb_check("name"):
                for effect in sublimb.active_effects.copy():
                    if effect.expire_on_removal:
                        effect.expire()

            self.die()
            self.subelements.remove(limb)
            return

        else:
            for subLimb in self.subelements:
                subLimb.remove_limb(limb)

        # Losing a vital limb kills the creature
        limb_vitals = [l for l in limb.limb_check("vital") if l.vital]
        # We'll see if others of this vital type are still attached
        limb_vitals = set([l.vital for l in limb_vitals])
        if len(limb_vitals):
            other_vitals = set([l.vital for l in self.subelements[0].limb_check("vital") if l.vital])
            # We confirm that all vitals that were removed still exist in our subelements. Otherwise, die.
            if len(limb_vitals.intersection(other_vitals)) < len(limb_vitals):
                self.die()

        self.update_status()

    def die(self):
        print(f"{self.name} dies.")
        room = self.location

        # Drop all held items
        for grasper in self.subelements[0].limb_check("grasp"):
            if grasper.grasped:
                x = grasper.grasped
                grasper.grasped = None
                room.drop_item(x)

        # End appropriate effects
        for limb in self.subelements[0].limb_check("name"):
            for effect in limb.active_effects.copy():
                if effect.expire_on_removal:
                    effect.expire()

        # Then die
        room.removeCreature(self)
        self.dead = True
        # and fall down
        landings = room.elem_check("canCatch")
        if len(landings) > 0:
            lands_at = random.choice(landings)
            lands_at.vis_inv.append(self.subelements[0])
            print(f"{BC.CYAN}{self.name}'s corpse collapses onto the {lands_at.name}.{BC.OFF}")
        else:
            print(f"{BC.CYAN}{self.name} falls and disappears out of sight.{BC.OFF}")

    def get_location(self):
        return self.location

    def get_team(self):
        return self.team

    def get_companions(self):
        # Get rid of dead companions
        for companion in self.companions.copy():
            if companion.dead:
                self.companions.remove(companion)

        return self.companions

    def get_tagged_equipment(self, tag):
        """Returns all equipment that has a certain tag. EG mana."""
        equipment_lists = self.subelements[0].find_equipped()
        all_equipment = []
        tagged_equipment = []

        for equipment_list in equipment_lists:
            all_equipment.extend(equipment_list.equipment)

        for equipment in all_equipment:
            if hasattr(equipment, tag):
                tagged_equipment.append(equipment)

        return tagged_equipment

    def check_siphon_tag(self, tag, amount):
        """Check whether it will be possible to siphon this amount of the tag from equipment."""
        tag_equipment = self.get_tagged_equipment(tag)
        # limb_check will return limbs with items on them if item has tag
        tag_limbs = [l for l in self.subelements[0].limb_check(tag) if hasattr(l, tag)]
        # Amount of tag that will be left after we siphon some off
        after_siphon = {}
        for gear in tag_equipment + tag_limbs:
            max_siphon = getattr(gear, tag)
            if amount <= max_siphon:
                amount_to_siphon = amount
                amount = 0
            else:
                amount_to_siphon = max_siphon
                amount -= amount_to_siphon

            after_siphon[gear] = max_siphon - amount_to_siphon
            # If we've found enough of the tag to siphon, stop checking gear
            if not amount:
                break

        # if we found enough of the tag. Otherwise, return False
        if not amount:
            return True
        else:
            return False

    def siphon_tag(self, tag, amount):
        """Reduce value of this tag on equipment with this tag by a certain amount in total."""
        tag_equipment = self.get_tagged_equipment(tag)
        # limb_check will return limbs with items on them if item has tag
        tag_limbs = [l for l in self.subelements[0].limb_check(tag) if hasattr(l, tag)]
        # Amount of tag that will be left after we siphon some off
        after_siphon = {}
        for gear in tag_equipment + tag_limbs:
            max_siphon = getattr(gear, tag)
            if amount <= max_siphon:
                amount_to_siphon = amount
                amount = 0
            else:
                amount_to_siphon = max_siphon
                amount -= amount_to_siphon

            after_siphon[gear] = max_siphon - amount_to_siphon
            # If we've found enough of the tag to siphon, stop checking gear
            if not amount:
                break

        # if we found enough of the tag, proceed to siphon. Otherwise, return False
        if not amount:
            for gear in after_siphon.keys():
                setattr(gear, tag, after_siphon[gear])
            return True
        else:
            # Don't siphon, and tell caller there isn't enough.
            return False

    def rest(self):
        """Rest, recover HP, and clear status effects."""
        if self.can_rest:
            self.bled = 0
            self.poisoned = 0

            for limb in self.subelements[0].limb_check(tag="hp"):
                if (limb.hp < limb.base_hp) and limb.can_heal:
                    hp_diff = 1 if (limb.base_hp - limb.hp >= 1) else (limb.base_hp - limb.hp)
                    limb.hp += hp_diff
                    print(f"{C.RED}{self.name}{C.OFF}'s {BC.RED}{limb.name}{BC.OFF} heals a little {BC.RED}({limb.hp}/{limb.base_hp}){BC.OFF}.")

    def heal(self, amount):
        for limb in self.subelements[0].limb_check(tag="hp"):
            if (limb.hp < limb.base_hp) and limb.can_heal:
                hp_diff = amount if (limb.base_hp - limb.hp >= amount) else (limb.base_hp - limb.hp)
                limb.hp += hp_diff
                amount -= hp_diff
                print(f"{C.RED}{self.name}{C.OFF}'s {BC.CYAN}{limb.name}{BC.OFF} heals for {BC.RED}{hp_diff}: ({limb.hp}/{limb.base_hp}){BC.OFF}.")
                if not amount:
                    break

    def heal_blood(self, amount):
        if self.bled < amount:
            amount = self.bled
        self.bled -= amount
        print(f"{C.RED}{self.name}{C.OFF} recovers {BC.RED}{amount}{BC.OFF} points of blood.")

    def heal_poison(self, amount):
        if self.poisoned < amount:
            amount = self.poisoned
        self.poisoned -= amount
        print(f"{C.RED}{self.name}{C.OFF} recovers from {BC.RED}{amount}{BC.OFF} points of poisoning.")

    @property
    def blood(self):
        """The amount of blood a creature has is proportional to its size."""
        limbs = self.subelements[0].limb_check("name")
        total_blood = sum([x.size if not hasattr(x, "orig_size") else x.orig_size for x in limbs])

        return total_blood

    @property
    def poison_resist(self):
        """The amount of poison a creature can resist is proportional to its size."""
        limbs = self.subelements[0].limb_check("name")
        total_pr = sum([x.size if not hasattr(x, "orig_size") else x.orig_size for x in limbs])

        return total_pr

    @property
    def mana_cost(self):
        mana_cost = 0
        for limb in self.limb_check("name"):
            if hasattr(limb, "mana_cost"):
                mana_cost += limb.mana_cost
        # Round to two decimals
        # mana_cost = math.floor(mana_cost * 100) / 100
        return mana_cost


class Fish(creature):
    can_breathe = False

    def leave(self, direction):
        """Fish die if they leave the water."""
        super().leave(direction=direction)
        if not (hasattr(self.location, "wet") and self.location.wet):
            print(f"{C.RED}{self.name} lies gasping in the air.{C.OFF}")
            self.die()


class Mechanoid(creature):
    can_fear = False
    can_rest = False
    can_stun = False
    can_poison = False
    can_breathe = False

