import item

class cabinet(item.thing):
    cantransfer = True

if __name__ == "__main__":
    c = cabinet("cabinet")
    print(c.cantransfer)