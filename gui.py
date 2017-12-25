import tkinter as tk
import random

#this gui is no longer supported.

class Gui(tk.Tk):

    def __init__(self, game, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        self.header     = tk.Label(self, text=game.name)
        self.keyboard   = Keyboard(self, self, game)
        self.display    = Display(self, self)
        self.printer    = Printer(self, self)
        
        self.header.pack()
        self.display.pack()
        self.printer.pack()
        self.keyboard.pack()






class Keyboard(tk.Frame):

    def __init__(self, parent, root, game, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root
        self.game = game

        self.frames = {}

        for keyboard in (Move_keyboard, Interact_keyboard, Inventory_keyboard):
            page_name = keyboard.__name__
            frame = keyboard(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Move_keyboard")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.raise_frame()






class Move_keyboard(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.controller = controller
        north = tk.Button(self, text="North", command=lambda: self.move("n"))
        south = tk.Button(self, text="South", command=lambda: self.move("s"))
        east  = tk.Button(self, text="East",  command=lambda: self.move("e"))
        west  = tk.Button(self, text="West",  command=lambda: self.move("w"))

        north.pack()
        south.pack()
        east.pack()
        west.pack()

    def raise_frame(self):
        self.tkraise()


    def move(self, direction):
        oldRoom = self.controller.game.char.get_location().name
        if self.controller.game.char.leave(direction):
            newRoom = self.controller.game.char.get_location().name
            self.controller.root.printer.label_text.set("You leave %s and enter %s" % (oldRoom, newRoom))
            self.controller.root.display.update_map(self.controller.game.get_level().show_map())
        else:
            self.controller.root.printer.label_text.set("You can't go that way.")






class Interact_keyboard(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.controller = controller

    def raise_frame(self):
        self.tkraise()




class Inventory_keyboard(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.controller = controller

    def raise_frame(self):
        self.tkraise()















class Display(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.frames = {}

        for display in (Map_display, Talk_display):
            page_name = display.__name__
            frame = display(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Map_display")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.raise_frame()

    def update_map(self, newMap):
        newMap = str(newMap)
        self.frames["Map_display"].map_var.set(newMap)
        self.show_frame("Map_display")


class Map_display(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)
        self.controller = controller
        self.map_var = tk.StringVar()
        self.map_var.set("XXXXXXXXX\nXXXXXXXXXX\nXXXXXXXXO\nXXoOOOXXXX")
        self.map = tk.Label(self, textvar=self.map_var)

        self.map.pack()

    def raise_frame(self):
        self.tkraise()

class Talk_display(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master=parent)
        self.controller = controller
        self.dialogue = tk.Label(self, text="Talking")

        self.dialogue.pack()

    def raise_frame(self):
        self.tkraise()

class Printer(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root
        self.label_text = tk.StringVar()
        self.label_text.set("printer")
        self.label = tk.Label(self, textvar=self.label_text)
        self.label.pack()

# gui = Gui()
# gui.mainloop()