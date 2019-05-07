import imp

creature = imp.load_source("creature", "creature.py")
place = imp.load_source("place", "place.py")
item = imp.load_source("item", "item.py")
interface = imp.load_source("interface", "interface.py")
house = imp.load_source("house", "house.py")
man = imp.load_source("man", "man.py")
kangaroo = imp.load_source("kangaroo", "kangaroo.py")
lizard = imp.load_source("lizard", "lizard.py")

# TODO we can probably save just with a single pickling. It's just plain old python code throughout.
# thefile = open("all_creatures.py", "w")
# print("hello world", file = thefile)			#overwrites. 	!!!!!!!THIS IS HOW TO WRITE TO FILES!!!!!! 
# Probably the key to loading from them as well, and from there the key to procedural generation!

# place.py test zone			#########################

# item.py test zone				##########################

# creature.py test zone			#############################

print(man.testChar.desc_status()) 
man.testChar.location = house.foyer_1
print(man.testChar.location.name)
man.testChar.leave("h3")
print(man.testChar.location.name)

# house.py test zone		##############################