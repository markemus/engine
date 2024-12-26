from colorist import BrightColor as BC, Color as C


def defaultdict_false():
    """This is used instead of a lambda so that defaultdicts can be pickled (for saving)."""
    return False


def display_long_text(text, n=20):
    """Used to display long text blobs, so that the player won't need to scroll the terminal upward to read.
    https://stackoverflow.com/a/15369848/9095840"""
    lines = text.splitlines()
    # lines = text
    while lines:
        print("\n".join(lines[:n]))
        lines = lines[n:]
        if lines:
            input("")


def listtodict(l, add_x=False):
    d = {str(i): l[i] for i in range(len(l))}
    if add_x:
        d["x"] = "Cancel"

    return d


def dictprint(d, pfunc=None, show_invs=False):
    """Pretty print a dictionary. Useful for displaying command sets for user input.
    pfunc amends the final string before printing.
    show_invs puts a star next to items with inventories."""
    intkeys = []
    strkeys = []

    for key in d.keys():
        if key.isdigit():
            intkeys.append(key)
        else:
            strkeys.append(key)

    intkeys.sort(key=int)

    keys = intkeys + strkeys
    fullstr = ""

    for key in keys:
        # Keys should always have the same (brown) color.
        kval = f"{C.YELLOW}{str(key)}{C.OFF}: "

        # Use printcolor, if it exists
        if hasattr(d[key], "printcolor"):
            kval = kval + f"{d[key].printcolor}"

        # if function
        if hasattr(d[key], "__name__"):
            exstr = kval + d[key].__name__
        # or object with printcolor
        elif hasattr(d[key], "color") and hasattr(d[key], "texture") and hasattr(d[key], "name"):
            exstr = kval + f"{d[key].color} {d[key].texture} {d[key].name}"
        # elif other objects
        elif hasattr(d[key], "name"):
            exstr = kval + f"{d[key].name}"
        # we don't want to ever see this, but we'd rather have it than an exception, I think.
        # This seems to be what happens when key is an int.
        else:
            exstr = kval + str(d[key])

        # Disable printcolor in cast it was enabled.
        exstr = exstr + f"{C.OFF}"

        # pfunc processes d[key] and returns a string for printing.
        if pfunc:
            exstr = pfunc(exstr, d[key])

        if show_invs:
            # Add star if item has inv or subelements
            if (hasattr(d[key], "vis_inv") and d[key].vis_inv) or (hasattr(d[key], "equipment") and d[key].equipment):
                exstr = exstr + " *"

        fullstr = fullstr + "\n" + exstr
    display_long_text(fullstr)
