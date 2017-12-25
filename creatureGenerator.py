import creature, copy, random, lizard, hydra




class creatureTemplate(creature.creature):
    #templates are basic creatures used for creature generation.
    #They contain a definition of the possible variations for the creature class.
    #Default values will simply recreate the template creature. 

    def __init__(self, name, baseCreature, appendageRange = (1,2), colors=None, textures=None):
        super(creatureTemplate, self).__init__(name)
        self.subelements = copy.deepcopy(baseCreature.subelements)
        core = self.subelements[0]
        self.colors = colors
        self.textures = textures
        self.set_default_variables(core, appendageRange)
        
        #core must always be unique.
        core.appendageRange = (1,2)

    def set_default_variables(self, element, appendageRange):
        
        if (type(element) == tuple):
            for option in element:
                self.set_default_variables(option, appendageRange)
        else:
            element.appendageRange = appendageRange

            for subelement in element.subelements:
                self.set_default_variables(subelement, appendageRange)




class creatureGenerator():
    #uses template creatures to generate creatures of the template type.

    #Templates: Every element must contain a variable named "appendageRange", pointing to a tuple. 
    #This tuple contains the range for the number of copies of that element to be placed in that location. 

    #They must also contain lists named "colorList" and "textureList". Each must contain at least one entry. 

    #Multiple possibilities: if a subelement is a tuple of objects instead of a single object, one of these
    #objects will be randomly selected.
    def __init__(self):
        pass    

    def pick_color_texture(self, colors, textures):
        color = random.choice(colors) if colors != None else None
        texture = random.choice(textures) if textures != None else None
        
        return (color, texture)
        
    def elementGen(self, parentElement, templateElement, color, texture):
        
        #allows for multiple options
        if (type(templateElement) == tuple):
            templateElement = random.choice(templateElement)

        try:
            potentialRange = templateElement.appendageRange
        except AttributeError:
            raise AttributeError("'{0}' : {1} object has no attribute 'appendageRange'".format(templateElement.name, templateElement))
        countRange = random.randrange(potentialRange[0], potentialRange[1])

        for count in range(countRange):
            #create
            thisElement = copy.deepcopy(templateElement)
            
            #color and texturize
            if color != None:
                thisElement.color = color
            if texture != None:
                thisElement.texture = texture
            
            #depopulate
            thisElement.subelements = []

            #clean up
            del thisElement.appendageRange
            
            #publish!
            parentElement.subelements.append(thisElement)

            for childElement in templateElement.subelements:
                self.elementGen(thisElement, childElement, color, texture)
                
    def creatureGen(self, name, creatureTemplate):
        (color, texture) = self.pick_color_texture(creatureTemplate.colors, creatureTemplate.textures)
        gennedCreature = creature.creature(name, color, texture)
        core = creatureTemplate.subelements[0]
        
        self.elementGen(gennedCreature, core, color, texture)
        
        return gennedCreature




if __name__ == "__main__":
    # t_appendageRange = (3,7)
    # t_colorList = ("red", "orange", "green", "blue")
    # t_textureList = ("haired", "skinned", "scaled")
    # our_creature = lizard.start_lizard
    # our_creature.subelements[0].subelements = [(our_creature.subelements[0].subelements[0], our_creature.subelements[0].subelements[1], our_creature.subelements[0].subelements[2]), our_creature.subelements[0].subelements[3]]

    # t_templateCreature = creatureTemplate("lizardTemplate", our_creature, t_appendageRange, t_colorList, t_textureList)

    t_generator = creatureGenerator()
    testCreature = t_generator.creatureGen("King Hydra", hydra.hydra)

    testCreature.desc()