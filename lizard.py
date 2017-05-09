import creature, imp, random, item

#End loading zone.

#Head

r_eye = creature.limb("right eye")
r_eye.see = 1
r_eye.isSurface = True

l_eye = creature.limb("left eye")
l_eye.see = 1
l_eye.isSurface = True

r_ear = creature.limb("right ear")
r_ear.hear = 1
r_ear.isSurface = True

l_ear = creature.limb("left ear")
l_ear.hear = 1
l_ear.isSurface = True

teeth = creature.limb("teeth")
teeth.damage = 3

tongue = creature.limb("tongue")

snout = creature.limb("snout")
snout.subelements = [teeth, tongue]
snout.smell = 1
snout.isSurface = True

head = creature.limb("head")
head.subelements = [snout, r_eye, l_eye, r_ear, l_ear]
head.isSurface = True

#front legs

r_f_foot = creature.limb("right front foot")
r_f_foot.amble = 1/3
r_f_foot.isSurface = True

r_f_leg = creature.limb("right front leg")
r_f_leg.subelements = [r_f_foot]
r_f_leg.isSurface = True

l_f_foot = creature.limb("left front foot")
l_f_foot.amble = 1/3
l_f_foot.isSurface = True

l_f_leg = creature.limb("left front leg")
l_f_leg.subelements = [l_f_foot]
l_f_leg.isSurface = True

#back legs

r_b_foot = creature.limb("right back foot")
r_b_foot.amble = 1/3
r_b_foot.isSurface = True

r_b_leg = creature.limb("right back leg")
r_b_leg.subelements = [r_b_foot]
r_b_leg.isSurface = True

l_b_foot = creature.limb("left back foot")
l_b_foot.amble = 1/3
l_b_foot.isSurface = True

l_b_leg = creature.limb("left back leg")
l_b_leg.subelements = [l_b_foot]
l_b_leg.isSurface = True

#tail

tail = creature.limb("tail")
tail.isSurface = True
tail.damage = 1
tail.grasp = 1
tail.f_grasp = 1
tail.t_grasp = 1

#body

heart = creature.limb("heart")
heart.blood = 1

r_lung = creature.limb("right lung")

l_lung = creature.limb("left lung")

body = creature.limb("body")
body.subelements = [head, r_f_leg, l_f_leg, r_b_leg, l_b_leg, tail, heart, r_lung, l_lung]

#lizard

start_lizard = creature.creature("start_lizard")
start_lizard.subelements = [body]

# #testArea

# sword = item.thing("sword")
# sword.damage = 5
# start_lizard.grasp(sword)