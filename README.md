# EverRogue
Sick of playing the same rogue-like over and over? Now you can make your own! Inspired by Kyle's Quest and Dwarf Fortress, EverRogue is a game engine that generates endless rogue-like games for you and your friends to play.

EverRogue is free and open source.

# TO INSTALL
Install python 3. If you're on windows, do this by typing 'python3' in Powershell and installing the app it brings up in a pop-up. 
Next, run: `pip3 install colorist`

That's it!

# TO RUN
The castle package is a game called "Escape From Castle Black" that you can play through. If you're on windows, use cmd instead of Powershell so the colors work. 
From the root directory, run:

`python3 -i -m castle.index`

# Escape From Castle Black
You are a prisoner in the dungeons of an evil king. Every day you hear the screams when the king's servants torture the prisoners. Today it's finally your turn.

You knew this day would come, and luckily you prepared for it. You have a sharpened shiv you managed to make while you were waiting, and a friend smuggled you in a potion of stoneskin. But ready or not, it's your time.

You will need to fight your way out of the dungeon and up through the castle to defeat the evil king. On the way you will battle the king's servants as well as encounter innocents who had no idea of the horrors that were taking place here. Some will fight on your side. 

You will find loot, weapons, and armor, as well as other potions of a horrific nature. The truth of what is happening here is more gruesome than even your worst nightmares. Be prepared.

# EverRogue (how to make your own games)
Game generation works as follows:

Look over the `castle` module to see how it works in practice. I documented the use cases there. This section will give a general overview.

**Games** are generated from GameStyles, which contain a sequence of LevelStyles. These levels are generated in order.

**LevelStyles** contain the Room classes that are used to construct the individual rooms (called Places) in the level. Levels also add doors connecting rooms to one another.

**Place** classes describe (as a range) how many of the room should be created per level, as well as the creature classes that they can contain. They specify the elements of the room (such as walls) and the furniture contained within. They also define options such as the colors that the room elements can be painted.

Room **elements** define behavior- floors can catch falling objects, doors connect rooms, furniture contains loot, etc.

**Creature** classes form the root of a tree of Limb classes that the given creature class contains. They also define behaviors for the creature, such as grasp() to pick up items or leave() to exit a room.

**Limb** classes contain items as their equipment, such as a tunic on a torso or a sword in a hand. They also contain attributes called "tags" that determine which behaviors the limb can be used for. They are organized in a tree stemming from a root limb, eg a torso with head, arms, and legs branching off (and hands on the arms, and fingers on the hands). 

**Items** are things, such as armor, weapons, and backpacks. They are organized in `suits` and `collections`. Suits are used to dress creatures during world generation, and collections are used to populate furniture with sets of loot. Some items are containers that will contain other items.

**Tags**
A limb with a "grasp" tag (a hand) can be used to pick up items- as long as its subelements contain values for "f\_grasp" that sum to at least 1 (fingers- or tentacles!), and values for "t\_grasp" that also sum to at least 1.

The `creature.subelements[0].limb_check()` function is used to recursively gather limbs containing the requested tag. These limbs can then be used for a given action- walking, grasping, attacking, blocking etc.

**Combat** is turn based. Each creature gets to attack with one of their limbs containing a "damage" or "grasp" tag. There is an opportunity to block, a to-hit roll, and a damage roll. Smaller limbs are harder to hit, and you will often be in combat with more than one enemy at a time, so you will have to think strategically. Chop some of those tentacles off, especially the ones holding good weapons! Hack at their ankles to take them off their feet. Chop off their heads one at a time until they're all gone. Just be careful to keep (some of) your head(s), or it's game over.

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
blocker: can be used to block attacks.  

# Creating a Game
**Potions** are a special kind of item with a scripted effect. This is the only scripting required to create a game- otherwise it's similar to creating a bunch of configuration files. Feel free to script other things if you want to though! It's all code, not configs, so you can really be creative with Python properties or custom methods on your objects. Feel free to make your own tags and functionality! And the engine is open source, so you can modify it to your heart's content.

# Cheating
Cheating is fun! It's a single player game, so why worry about it? Stuck against a hard opponent and looking for a better weapon? Want to spawn a few enemies to increase the challenge? How about modifying the level layout? It's Python, you can edit the source code during runtime! Just CTRL-C out of the game at any time and code away on the command line, then simply type `while True: i.command()` to get right back into the game, exactly where you left off, but with your changes.
