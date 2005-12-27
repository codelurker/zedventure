
class Item (object):
    __slots__ = ('_weight')
    def __init__(self, weight):
        self.weight = weight
    def __str__(self):
        return "a "+self.name

