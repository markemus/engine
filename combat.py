import random

from transitions import Machine


class Fsm():
    """
    Keeps track of turn based combat and handles the AI side.

    Player-side combat is handled in controller.py.
    """
    def __init__(self, char):
        self.char = char
        states = ["player", "ai"]
        self.machine = Machine(model=self, states=states, initial="player")
        # machine.on_enter_player("player_handler")
        self.machine.on_enter_ai("ai_handler")

    def ai_handler(self):
        room = self.char.get_location()

        for creature in room.get_creatures():
            if creature is not self.char:
                round(creature)

        self.to_player()

def get_target_creatures(actor):
    targets = actor.location.get_creatures()

    if actor in targets:
        targets.remove(actor)

    return targets

def get_target_limbs(defender):
    limbs = defender.subelements[0].limb_check("isSurface")

    return limbs

def round(actor):
    target = target_creature(actor)
    limb = target_limb(target)
    weapon = pick_weapon(actor)

    if all([target, limb, weapon]):
        #should print weapon name, not hand-holding-weapon's name
        print(actor.name, "attacks", target.name + "'s", limb.name, "with their", weapon.name + "!")
        attack(target, limb, weapon)

def target_creature(actor):
    room = actor.get_location()
    targets = []

    #gather
    for creature in room.get_creatures():
        if actor is not creature:
            if creature.team != actor.team:
                targets.append(creature)

    #pick
    if len(targets) > 0:
        target = random.choice(targets)
    else:
        target = False

    return target

def target_limb(target):
    chosen = None
    limbs = target.subelements[0].limb_check("isSurface")

    if len(limbs) > 0:
        lowest = min(limbs, key=lambda x: x.hitpoints)
        allLowest = [limb for limb in limbs if limb.hitpoints == lowest.hitpoints]
        chosen = random.choice(allLowest)
        # print("chosen: ", chosen)
    else:
        # print("No surface limbs.")
        chosen = False
    
    return chosen

def pick_weapon(actor):
    claws = actor.subelements[0].limb_check("damage")
    hands = actor.subelements[0].limb_check("grasp")

    bigclaw = max(claws, key=check_damage, default=False)
    swordhand = max(hands, key=check_damage, default=False)

    weapon = max(bigclaw, swordhand, key=check_damage)

    return weapon

def check_damage(limb):
    #no limb
    if not limb:
        return 0

    #limb damage
    try:
        damage = limb.damage
    except AttributeError:
        damage = 0

    #limb's weapons' damage
    for item in limb.inventory:
        if hasattr(item, "damage"):
            if item.damage > damage:
                damage = item.damage

    return damage

def attack(defender, limb, weapon):
    damage = check_damage(weapon)
    
    limb.hitpoints -= damage
    print("It deals", damage, "damage!") 

    if limb.hitpoints <= 0:
        defender.remove_limb(limb)
        print(limb.name, "is severed from", defender.name + "'s body!")
        
        throw_limb(defender, limb)

#arms have to land somewhere
def throw_limb(amputee, limb):
    room = amputee.get_location()
    landings = room.elem_check("canCatch")
    
    if len(landings) > 0:
        lands_at = landings[random.randrange(len(landings))]
        lands_at = random.choice(landings)
        lands_at.add_vis_item(limb)
        print("The", limb.name, "lands on the", lands_at.name + ".")
    else:
        print("Nowhere to land.")

if __name__ == "__main__":
    import item
    from orc import orc
    # orc.baseElem.subelement_classes[1].hitpoints = 5

    o = orc("o", location=None)

    class sword(item.thing):
        name = "sword"
        damage = 50

    s = sword()
    print("sword damage: ", s.damage)
    
    print("claw: ", o.subelements[0].subelements[0])
    o.subelements[0].subelements[0].damage = 5

    print("hand: ", o.subelements[0].subelements[1].subelements[0])
    o.subelements[0].subelements[1].subelements[0].inventory.append(s)
    print("hand inventory: ", o.subelements[0].subelements[1].inventory)
    
    print("pick_weapon(): ", pick_weapon(o))
    print("weapon damage: ", check_damage(pick_weapon(o)))