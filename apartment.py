import imp, copy

place = imp.load_source("place", "../place.py")
house = imp.load_source("house", "house.py")
# creature = imp.load_source("creature", "../creature.py")

place.generate("apartment", "house")

print(apartment)