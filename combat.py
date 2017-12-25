import random

#creature
def round(actor):
    room = actor.get_location()

    for other in room.get_creatures():
        if actor is not other:
            if other.get_team() == actor.get_team():
                actor.speak("Hello, {}".format(other.name), other)
            else:
                attack(actor, other)

#single attack
def attack(creature1, creature2):

    worst = (None, 0)

    for limb in creature1.subelements[0].limb_check("damage"):
        damage = check_damage(limb)
        if damage > worst[1]:
            worst = (limb, damage)

    #choose target limb
    if worst[0] is not None:
        target_limb = hit_limb(creature2)
        
        #deal damage
        if target_limb is not None:
            target_limb.hitpoints -= worst[1]
            print(creature1.name, "deals", worst[1], "damage to", creature2.name + "'s", target_limb.name, "with his", worst[0].name + "!")
            
            #remove limb
            if target_limb.hitpoints <= 0:
                creature2.subelements[0].remove_limb(target_limb)
                throw_limb(creature2, target_limb)
                print(target_limb.name, "is severed from", creature2.name + "'s body!")

        else:
            print(creature2.name, "is invisible!")
    else:
        print(creature1.name, "has no means of dealing damage to", creature2.name + "!")

#only call on limbs with damage tag
def check_damage(limb):
    damage = limb.damage

    for item in limb.get_vis_inv():
        if hasattr(limb, "damage"):
            if limb.damage > damage:
                damage = limb.damage

    return damage

#picks a target limb
def hit_limb(target):
    chosen = None
    limbs = target.subelements[0].limb_check("isSurface")

    for limb in limbs:
        if not limb.isSurface:
            limbs.remove(limb)

    if len(limbs) > 0:
        chosen = limbs[random.randrange(len(limbs))]
        print("chosen: ", chosen)
    else:
        print("No surface limbs.")
    return chosen

#arms have to land somewhere
def throw_limb(amputee, limb):
    landed = False
    room = amputee.get_location()
    landings = room.elem_check("canCatch")
    
    if len(landings) > 0:
        lands_at = landings[random.randrange(len(landings))]
        lands_at.add_vis_item(limb)
        landed = True

    return landed