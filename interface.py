import creature, place, item, interface, imp

# End of Loading Zone

def you():                  #defines the "creature.you" object, which is the PC
    race_list_names = []
    count = 1
    for n in creature.race_list:            #creates a list of the starting races names
        race_list_names.append(str(count) + ". " + n.name)
        count = count + 1
    print(race_list_names)
    x = input("Please pick a race by choosing a number.")
    try:                                    #checks that they're using numbers, and that the numbers aren't too large
        if int(x) > 0:                      #checks that they're not using negatives, or zero (which would count backward down the list)
            print(race_list_names[int(x)-1])
            creature.you = creature.race_list[int(x)-1]
            creature.you.name = input("Please choose a name for your character.")
        else:
            print("That number has no equivalent value. Please try again.")
            you()
    except (ValueError, IndexError):
        print("That number has no equivalent value. Please try again.")

you()