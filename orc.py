import creature as cr 
"""
Orcs are vile and nasty creatures, born to wreak havoc and destroy. They deserve nothing more
than a clean death.
"""

ear = cr.limb("ear")
ear.hear = 1
ear.isSurface = True
ear.appendageRange = (2,3)

eye = cr.limb("eye")
eye.see = 1
eye.isSurface = True
eye.appendageRange = (2,3)

horn = cr.limb("horn")
horn.damage = 3
horn.isSurface = True
horn.appendageRange = (2,3)

teeth = cr.limb("teeth")
teeth.damage = 2
teeth.appendageRange = (1,2)

tongue = cr.limb("tongue")
tongue.appendageRange = (1,2)

nose = cr.limb("nose")
nose.smell = 1
nose.isSurface = True
nose.appendageRange = (1,2)

head = cr.limb("head")
head.subelements = [ear, eye, horn, teeth, tongue, nose]
head.isSurface = True
head.appendageRange = (1,2)

#arms
finger = cr.limb("finger")
finger.f_grasp = 1/4
finger.isSurface = True
finger.appendageRange = (4,5)

thumb = cr.limb("thumb")
thumb.t_grasp = 1
thumb.isSurface = True
thumb.appendageRange = (1,2)

hand = cr.limb("hand")
hand.grasp = 1
hand.subelements = [finger, thumb]
hand.isSurface = True
hand.appendageRange = (1,2)

arm = cr.limb("arm")
arm.subelements = [hand]
arm.isSurface = True
arm.appendageRange = (2,3)

#legs
foot = cr.limb("foot")
foot.amble = 1/3
foot.isSurface = True
foot.appendageRange = (1,2)

leg = cr.limb("leg")
leg.subelements = [foot]
leg.isSurface = True
leg.appendageRange = (2,3)

#body
body = cr.limb("body")
body.isSurface = True
body.subelements = [head, arm, leg]
body.appendageRange = (1,2)

#orc
orc = cr.creature("orc")
orc.subelements = [body]
orc.colors = ["red", "brown", "green", "black", "beige"]
orc.textures = ["scaled", "haired", "skinned"]

if __name__ == '__main__':
    orc.desc()