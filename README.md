# Engine
A game engine for text-based roguelike games.

This is a game engine, not a game. The idea is that the user can create basic creatures called "templates" which are then used to generate and populate a world. 

All creatures are stored as trees of limbs, with lower level limbs (such as hands) stored in higher level limbs (arms). If a higher level limb becomes detached from the body, the lower level limbs are detached as well.

Limbs have attributes called "tags" that can be searched for using the built-in function "limb_check". This returns an array containing all the limbs which have that tag, to be used for whatever purpose you like. For example, the "grasp" tag is checked before the creature picks anything up, and the "amble" tag is checked to ensure that the creature has enough legs (or leg-like appendages) to walk.

Rooms are very basic, but follow the same principle of being composed of a tree of "elements". The elements can contain objects, either visible or hidden (and can be visible or hidden themselves), which determines whether the player can see them when the desc function is called. desc uses the same principle as limb_check to traverse the tree.

When a level is generated it creates a sequence of rooms randomly from collections of elements of different types. Currently all generated rooms are composed of 4 walls and 1 floor. Doors are added to connect rooms together, which allow the player to traverse the level.

A very basic GUI is included, but it was recently added and is very much a work in progress.

# TO INSTALL

Install python 3.
Packages: tkinter (avoidable if you don't use the GUI with some minor modifications to index.py)

# TO RUN
python3 index.py
