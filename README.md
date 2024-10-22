# EverRogue
Sick of playing the same rogue-like over and over? Now you can make your own! Inspired by Kyle's Quest and Dwarf Fortress, EverRogue generates endless rogue-like games for you and your friends to play.

# TO INSTALL
Install python 3.		
`pip3 install transitions`	 
`pip3 install colorist`

# TO RUN
I created a game called "castle" that you can play through. From the root directory, run:

`python3 -i -m castle.index`

# INSTRUCTIONS (ADVANCED)

Game generation works as follows:

**Games** are generated from GameStyles, which contain a sequence of LevelStyles. These levels are generated in order.

**LevelStyles** contain the Room classes that are used to construct the individual rooms (called Places) in the level. Levels also add doors connecting rooms to one another.

**Place** classes describe (as a range) how many of the room should be created per level, as well as the creature classes that they can contain. They specify the elements of the room (such as walls) and the furniture contained within. They also define options such as the colors that the room elements can be painted.

Room **elements** define behavior- floors can catch falling objects, doors connect rooms, etc.

**Creature** classes form the root of a tree of Limb classes that the given creature class contains. They also define behaviors for the creature, such as grasp() to pick up items or leave() to exit a room.

**Limb** classes contain items in their inventory, such as a tunic on a torso or a sword in a hand. They also contain attributes called "tags" that determine which behaviors the limb can be used for.

**Tags**
A limb with a "grasp" tag (a hand) can be used to pick up items- as long as its subelements contain values for "f\_grasp" that sum to at least 1 (fingers- or tentacles!), and values for "t\_grasp" that also sum to at least 1.

Creatures can also contain tags of their own- these are attributes that cannot be lost.

The creature.limb_check() function is used to recursively gather limbs containing the requested tag. These limbs can then be used for a given action- walking, grasping, attacking, blocking etc.

**Combat** is turn based. Each creature gets to attack with one of their limbs containing a "damage" or "grasp" tag. They can choose not to attack with a limb, in which case it will be available to block incoming attacks from their opponent. This means you have to be careful- if you attack with all your limbs, your enemy might well chop them off on their own turn. Of course they'll have trouble doing that if they have no arms left...

# Tags
name: the name of the object.
grasp: used for picking up/moving objects. Needs f_grasp and t_grasp objects as well.
f_grasp: denotes a finger.
t_grasp: a thumb.
amble: used for walking.
isSurface: whether the limb is visible on the outside of the body.
wears: the type of equipment the limb can use.
see: allows the creature to see- needed for many basic actions.
damage: the amount of damage the limb can deal in combat.
block: can be used to block attacks.
