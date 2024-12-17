import collections
import random
from colorist import Color as C, BrightColor as BC

d = collections.defaultdict(lambda x: False)
d["head"] = True
d["body"] = True
d.items()




# print(f"{C.RED}this is red{BC.OFF} is this red?")
# for x in range(100):
#     print(x)
#
# import os
# class Cls(object):
#     def __repr__(self):
#         os.system('clear')
#         return ''



# class one:
#     pass
#
# class two(one):
#     pass
#
# class three(two):
#     pass
#
# a = one()
# b = two()
# c = three()
# isinstance(a, one)
# isinstance(b, one)
# isinstance(c, one)
# isinstance(c, type(a))
# print(f"This is a {C.GREEN}green{C.OFF} tag")
#
#
# d_creature_lists = {"caves": [("orc", 3), ("goblin", 5)],
#                     "dungeon": [("grue", 1), ("skeleton", 3), ("rat", 5)],
#                     "hills": [("troll", 2), ("sheep", 8)],
#                     "city": [("elf", 3), ("halfling", 4), ("dwarf", 6), ("human", 8)]}
# def weight_list(clist, weight):
#     """Reweights elements in a creature list in preparation for joining with another creature list."""
#     # Pivot table
#     ziplist = list(zip(*clist))
#     # Apply weights and pivot back
#     weighted_list = list(zip(*[ziplist[0], [x * weight for x in ziplist[1]]]))
#     return weighted_list
#
# creature_list = weight_list(d_creature_lists["caves"], 3) + d_creature_lists["city"]
#
# # Pivot
# creatures, weights = zip(*creature_list)
# random.choices(creatures, weights, k=9)
