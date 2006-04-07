# vim:set sts=4 et ai:

import commands
import weapon
import armor
from actor import *
from errors import *

World = None


class Area (object):
    """Generate a single dungeon area."""
    __slots__ = ('depth','y','x','cell','occ','item','game')
    def __init__(self,game):
        self.game = game
        self.depth = 0
        self.y, self.x = 2, 2
        self.cell = [[0,0],[0,0]]
        self.occ = {}
        self.item = {}
        global World
        World = self

    def size(self):
        return (self.y, self.x)

    def resize(self,ydim,xdim):
        if not xdim % 2: xdim -= 1
        self.y, self.x = ydim, xdim
        self.cell = [[0 for x in xrange(self.x)] for y in xrange(self.y)]
        self.occ = {}
        self.item = {}

    def place(self,item,y=None,x=None):
        if y == None and x == None:
            y, x = World.size()
            while True:
                k = World.game.rng.randrange(1,y,2)
                j = World.game.rng.randrange(1,x,2)
                if not self.is_block(k,j):
                    break
            self.item[k,j] = item
        else:
            self.item[y,x] = item

    def generate(self,increment):
        self.depth += increment
        if self.depth < 0: raise Escaped
        for k in xrange(self.y):
            for j in xrange(self.x):
                if self.game.percent_chance(25):
                    self.cell[k][j] = 6
                else:
                    self.cell[k][j] = 0
        self.occ = {}
    	actors = []
        for x in xrange(self.game.rng.randint(2,3 + ((self.depth + 3) / 3))):
            actors.append(generate_monster(World))
        self.item = {}
        for x in xrange(self.game.rng.randint(0, 3 + ((self.depth + 1) / 2))):
            self.place(weapon.generate(self.game.rng,self.depth))
        for x in xrange(self.game.rng.randint(0, 2 + ((self.depth + 1) / 2))):
            self.place(armor.generate(self.game.rng,self.depth))
        actors.sort()
        return actors

    def is_valid(self,y,x):
        """A.is_valid(y,x) -> bool
        
        True if the position is inside the area, False otherwise."""
        return y >= 0 and y < self.y and x >= 0 and x < self.x

    def is_occ(self,y,x):
        """A.is_occ(y,x) -> bool
        
        True if the position is occupied by another Thing, False otherwise."""
        return self.occ.has_key((y,x))

    def is_block(self,y,x):
        """A.is_block(y,x) -> bool
        
        True if the position is blocked by a dungeon feature, False otherwise."""
        return bool(self.cell[y][x])

    def enter(self,y,x,thing):
        thing.y, thing.x = y, x
        self.occ[y,x] = thing
        if thing.is_hero():
            try:
                item = self.item[thing.y,thing.x]
                self.game.term.msg('you see %s here.' % item)
            except KeyError:
                pass

    def leave(self,y,x,thing):
        try:
            del self.occ[y,x]
        except KeyError:
            self.game.term.msg('LEAVE from nowhere: %d, %d' % (y, x))

if __name__ == '__main__':
    print Hero.XPLEVELS

