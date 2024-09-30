"""Save and restore games."""
import pickle


def save(interface, savepath):
    """Pass an engine.interface.Interface() object in to be saved. This should save the entire game hierarchy."""
    pickle.dump(interface, open(savepath, "wb"))

def load(savepath):
    """Loads a saved file, opening it as an engine.interface.Interface() object.
    Run: 'while True: interface.command()' to play."""
    interface = pickle.load(open(savepath, "rb"))
    return interface
