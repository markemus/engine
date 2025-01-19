import random

import engine.creature as cr
import engine.spells as sp
import engine.utils as utils

from assets.dwarf import Dwarf
from assets.hobbit import Hobbit
from assets.human import Human
from assets.elf import Elf
from assets.goblin import ServantGoblin

import autobattler.golem_limbs as gl
import autobattler.golem as go

from colorist import BrightColor as BC, Color as C



# Each level has a different item list
item_lists = [
    [go.LargeGolem, go.SmallGolem],
    [*gl.basic_weapons],
]


class Store(sp.Effect):
    # Store should open when you enter the room but not need dispelling.
    rounds = 1

    def _cast(self):
        def pfunc(x, y):
            if "x" in x.split(":")[0]:
                fullstr = x
            else:
                fullstr = f"{x.split(':')[0]}: {BC.CYAN}{y.name if hasattr(y, 'name') else y.classname}{BC.OFF} {BC.RED}({y.price}){BC.OFF}"
            return fullstr

        # Shopkeeper
        print(f"{BC.RED}\nShopkeeper{BC.OFF}: {BC.BLUE}Welcome to my shop! We sell only the finest golem parts and apparel. Please feel free to look around.{BC.OFF}")

        # Display inventory
        item_list = item_lists[self.casting_limb.creature.level]
        item_dict = utils.listtodict(item_list, add_x=True)
        i = None

        while i != "x":
            utils.dictprint(item_dict, pfunc=pfunc)
            i = input(f"{BC.GREEN}Which item would you like to buy?{BC.OFF} ")
            if i in item_dict.keys() and i != "x":
                article_class = item_dict[i]
                if self.cont.game.char.zorkmids >= article_class.price:
                    invs = self.cont.game.char.subelements[0].find_invs()
                    if invs:
                        inv = invs[0]

                        # Create item
                        if issubclass(article_class, cr.creature):
                            article = article_class(location=None)
                        else:
                            color = random.choice(article_class.colors)
                            texture = random.choice(article_class.textures)
                            article = article_class(color=color, texture=texture)

                        # Buy item
                        print(f"{C.RED}{self.cont.game.char.name}{C.OFF} buys the {BC.YELLOW}{article.name}{BC.OFF} for {BC.RED}{article_class.price} zorkmids{BC.OFF}.")
                        self.cont.game.char.zorkmids -= article_class.price
                        item_dict.pop(i)
                        inv.vis_inv.append(article)
                    else:
                        print(f"{C.RED}{self.cont.game.char.name} has no available inventory!{C.OFF}")
                else:
                    print(f"{C.RED}{self.cont.game.char.name} cannot afford a {article_class.name if hasattr(article_class, 'name') else article_class.classname}!{C.OFF}")

        print(f"{BC.RED}\nShopkeeper{BC.OFF}: {BC.BLUE}Thank you for your custom! Please come again soon.\n{BC.OFF}")
        return False


shopkeeper_race = random.choice([Dwarf, Hobbit, Human, Elf, ServantGoblin])


class Shopkeeper(shopkeeper_race):
    team = "neutral"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subelements[0].passive_effects.append(Store)
        self.level = 0
