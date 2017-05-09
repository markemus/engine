import creature, imp, copy

# End of Loading Zone

#test creature

kangaroo = creature.creature("kangaroo")

#kangaroo elements

pouch = creature.limb("pouch")
l_ear = creature.limb("left ear")
r_ear = creature.limb("right ear")
torso = creature.limb("torso")

#pouch

pouch.can_transfer = True

#left ear

l_ear.can_transfer = False

#right ear

r_ear.can_transfer = False

#torso

torso.subelements = [pouch]

kangaroo.subelements = [torso, l_ear, r_ear]