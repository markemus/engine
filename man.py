import creature as cr
import commonlimbs as cl

# hair = creature.limb("hair")					#head element

# r_eye = creature.limb("right eye")
# r_eye.see = 1

# l_eye = creature.limb("left eye")
# l_eye.see = 1

# nose = creature.limb("nose")
# nose.smell = 1

# upper_teeth = creature.limb("upper teeth")
# upper_teeth.bite = .5

# lower_teeth = creature.limb("lower teeth")
# lower_teeth.bite = .5

# tongue = creature.limb("tongue")
# tongue.taste = 1

# mouth = creature.limb("mouth")
# mouth.subelements = [upper_teeth, lower_teeth, tongue]



# head = creature.limb("head")
# head.subelements = [hair, r_eye, l_eye, nose, mouth]

# r_thumb = creature.limb("right thumb")								#right hand elem
# r_thumb.t_grasp = 1

# r_finger_1 = creature.limb("right index finger")
# r_finger_1.f_grasp = 1/4

# r_finger_2 = creature.limb("right middle finger")
# r_finger_2.f_grasp = 1/4

# r_finger_3 = creature.limb("right ring finger")
# r_finger_3.f_grasp = 1/4

# r_finger_4 = creature.limb("right pinkie finger")
# r_finger_4.f_grasp = 1/4

# r_hand = creature.limb("right hand")
# r_hand.grasp = 1
# r_hand.subelements = [r_thumb, r_finger_1, r_finger_2, r_finger_3, r_finger_4]

# r_arm = creature.limb("right arm")								#right arm elem
# r_arm.subelements = [r_hand]

# l_thumb = creature.limb("left thumb")							#left hand elem
# l_thumb.t_grasp = 1

# l_finger_1 = creature.limb("left index finger")
# l_finger_1.f_grasp = 1/4

# l_finger_2 = creature.limb("left middle finger")
# l_finger_2.f_grasp = 1/4

# l_finger_3 = creature.limb("left ring finger")
# l_finger_3.f_grasp = 1/4

# l_finger_4 = creature.limb("left pinkie finger")
# l_finger_4.f_grasp = 1/4

# l_hand = creature.limb("left hand")
# l_hand.grasp = 1
# l_hand.subelements = [l_thumb, l_finger_1, l_finger_2, l_finger_3, l_finger_4]

# l_arm = creature.limb("left arm")								#left arm elem
# l_arm.subelements = [l_hand]

# r_foot = creature.limb("right foot")							#right leg elem
# r_foot.amble = 1/2

# r_leg = creature.limb("right leg")
# r_leg.subelements = [r_foot]

# l_foot = creature.limb("left foot")							#left leg elem
# l_foot.amble = 1/2

# l_leg = creature.limb("left leg")
# l_leg.subelements = [l_foot]
class head(cr.limb):
    name = "head"
    subelement_classes = [cl.hair, cl.eye, cl.nose, cl.mouth]
    isSurface = True
    appendageRange = (1,2)

class torso(cr.limb):
    name = "torso"
    subelement_classes = [head, cl.arm, cl.leg]

# torso = creature.limb("torso")								#torso elem
# torso.subelements = [cl.head, cl.arm, cl.leg]

class man(cr.creature):
    name = "man"
    baseElem = torso
    colors = ["black", "white", "red", "yellow", "brown"]
    textures = ["skinned"]

if __name__ == "__main__":
    eve = man("Eve")						#main CREATURE
    eve.desc()