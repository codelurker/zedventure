class Gold (object):
    __slots__ = ('amount')

    def __init__(self,amount = None):
        if amount:
            self.amount = amount
        else:
            self.amount = 1

    def __str__(self):
        return "%d gold pieces" % self.amount

    def glyph(self): return '$'
            
