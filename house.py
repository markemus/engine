import imp

creature = imp.load_source("creature", "creature.py")
place = imp.load_source("place", "place.py")
item = imp.load_source("item", "item.py")

#Map of a house in Engine

#all rooms

foyer_1 = place.place("foyer",[],"F")

coatroom_2 = place.place("coat room",[],"C")

hallway_3 = place.place("hallway",[],"H")

#foyer elements

n_wall_1 = place.element("wall", "red")

e_wall_1 = place.element("wall", "red")

s_wall_1 = place.element("wall", "red")

w_wall_1 = place.element("wall", "red")

floor_1 = place.element("floor", "carpeted")

coatroom_door_1 = place.element("coatroom door", "dark blue")								#coatroom door
coatroom_door_1.borders = {"c2" : coatroom_2,"f1" : foyer_1}					#coatroom_door_1 borders

foyer_door_1 = place.element("foyer door", "dark blue")									#foyer door
foyer_door_1.borders = {"h3" : hallway_3,"f1" : foyer_1}						#foyer_door_1 borders

table_1 = place.element("table", "mahogany")

foyer_1.elements = [n_wall_1, e_wall_1, s_wall_1, w_wall_1, floor_1, coatroom_door_1, foyer_door_1, table_1]

foyer_1.get_borders()

#coatroom elements

n_wall_2 = place.element("wall", "brown")

e_wall_2 = place.element("wall", "brown")

s_wall_2 = place.element("wall", "brown")

w_wall_2 = place.element("wall", "brown")

floor_2 = place.element("floor", "carpeted")

browncoat_1 = item.coat("brown coat")

coat_rack_2 = place.element("coat rack", "brown")
coat_rack_2.vis_inv.append(browncoat_1)

coatroom_2.elements = [n_wall_2, e_wall_2, s_wall_2, w_wall_2, floor_2, coatroom_door_1, coat_rack_2]

coatroom_2.get_borders()

#hallway elements

floor_3 = place.element("floor", "hardwood")

n_wall_3 = place.element("wall", "blue")

e_wall_3 = place.element("wall", "blue")

s_wall_3 = place.element("wall", "blue")

w_wall_3 = place.element("wall", "blue")

hallway_3.elements = [floor_3, n_wall_3, e_wall_3, s_wall_3, w_wall_3, foyer_door_1]

hallway_3.get_borders()
print(hallway_3.borders)

hallway_3.desc()