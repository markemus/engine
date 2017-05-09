import creature, levelmap, copy, random, lizard

#templates are creatures with a few extras. They are only for creature generation.
#currently they only contain default values for debugging. All subelements share the same values.

class creatureTemplate(creature.creature):

    def setDefaultVariables(self, element, appendageRange):

        element.appendageRange = appendageRange

        for subelement in element.subelements:
            self.setDefaultVariables(subelement, appendageRange)

    def __init__(self, name, baseCreature, appendageRange = (1,2)):
        super(creatureTemplate, self).__init__(name)
        self.subelements = copy.deepcopy(baseCreature.subelements)
        core = self.subelements[0]
        self.setDefaultVariables(core, appendageRange)

#uses templates to generate creatures of a particular type.
#Templates: Every element must contain a variable named "appendageRange", pointing to a tuple. 
#This tuple contains the range for the number of copies of that element to be placed in that location. 
#They must also contain lists named "colorList" and "textureList". Each must contain at least one entry.
class creatureGenerator():
    def __init__(self, creatureTemplate):
        self.creatureTemplate = copy.deepcopy(creatureTemplate)

    def elementGen(self, gennedCreature, parentElement, templateElement):

        potentialRange = templateElement.appendageRange
        countRange = random.randrange(potentialRange[0], potentialRange[1])

        for count in range(countRange):
            #create
            thisElement = copy.deepcopy(templateElement)
            
            #populate
            thisElement.subelements = []

            #clean up
            del thisElement.appendageRange
            
            #publish!
            parentElement.subelements.append(thisElement)

            for childElement in templateElement.subelements:
                self.elementGen(gennedCreature, thisElement, childElement)
                
    #WIP
    def creatureGen(self, name):
        gennedCreature = creature.creature(name)
        core = self.creatureTemplate.subelements[0]
        subelements = core.subelements

        self.elementGen(gennedCreature, gennedCreature, core)
        return gennedCreature

# testArea

t_appendageRange = (1,2)
t_colorList = ("red", "orange", "green", "blue")
t_textureList = ("haired", "skinned", "scaled")

t_templateCreature = creatureTemplate("lizardTemplate", lizard.start_lizard, t_appendageRange)

t_generator = creatureGenerator(t_templateCreature)
# testCreature = t_generator.creatureGen("baggins")
# testCreature.desc()