# vim:set ts=4 sts=4 et ai:

from errors import *
import commands
from treasure import Gold

class Actor (object):
    move_speed = 7
    attack_speed = 7
    glyph = '0'
    desc = 'the actor'
    __slots__ = ('_world','y','x','_hp','hpmax','_mp','mpmax',
                'wait_until','desc','_gold')

    def __init__(self,world,y,x):
        self._world = world
        self._world.enter(y,x,self)
        self._hp, self.hpmax, self._mp, self.mpmax = 1, 1, 1, 1
        self.wait_until = self._world.game.time + self.move_speed
        self._gold = 0

    def __str__(self):
        if self.desc:
            return self.desc
        else:
            return "it"

    def __cmp__(self,other): return cmp(self.wait_until, other.wait_until)

    def generate(self):
        self.hpmax = 0
        for x in xrange(self.hd):
            self.hpmax += self._world.game.rng.randint(1,7)
        self._hp = self.hpmax
        self._gold = self._world.game.rng.randint( 0, self.hd * 7 )

    def do_walk(self,y,x):
        """T.do_walk(y,x) -> integer"""
        yy = self.y + y
        xx = self.x + x
        if not self._world.is_valid(yy,xx):
            raise NoSuchPlace, "%d, %d" % (yy,xx)
        elif self._world.is_block(yy,xx):
            raise MovementBlocked
        elif self._world.is_occ(yy,xx):
            raise AlreadyOccupied
        else:
            self._world.leave(self.y,self.x,self)
            self._world.enter(yy,xx,self)
        return self.move_speed

    def do_attack(self,y,x):
        """T.do_attack(y,x) -> integer"""
        opponent = self._world.occ[self.y+y,self.x+x]
        if opponent.is_hero():
            damage = self._world.game.rng.randint(1,self.hd)
            if opponent.armor:
                if self._world.game.rng.randint(0,10) > opponent.armor.evade:
                    self._world.game.term.msg('%s misses.' % self)
                    return self.attack_speed
                ac = self._world.game.rng.randint(0,opponent.armor.ac)
                if ac >= damage:
                    self._world.game.term.msg("%s's attack glanced off your armor." % self)
                    return self.attack_speed
                else:
                    damage -= ac
            self._world.game.term.msg('%s attacks!' % self)
            opponent.hp -= damage
        return self.attack_speed

    def is_hero(self): return False
    def is_alive(self): return self._hp > 0

    def die(self):
        an = 0
        for n, a in enumerate(self._world.game.actors):
            if a is self:
                an = n
                break
        self._world.leave(self.y,self.x,self)
        if (self._gold):
            self._world.place(Gold(self._gold),self.y,self.x)
        del self._world.game.actors[an]

    def act(self):
        time = self._act()
        self.wait_until = self._world.game.time + time

    def get_hp(self): return self._hp
    def set_hp(self, new_hp):
        if new_hp > self.hpmax:
            self._hp = self.hpmax
        else:
            self._hp = new_hp
        if self._hp <= 0:
            raise WasKilled(self)
    hp = property(get_hp,set_hp,None,'hit points')

    def get_mp(self): return self._mp
    def set_mp(self, new_mp):
        if new_mp > self.mpmax:
            self._mp = self.mpmax
        elif new_mp < 1:
            self._mp = 0
        else:
            self._mp = new_mp
    mp = property(get_mp,set_mp,None,'mana points, cannot go below zero')

    def get_gold(self): return self._gold
    gold = property(get_gold,None,None,'gold')

    _CON = 'bbcccddfffggghhjjjkklllmmmnnnnppqrrrrsssttvwwwxzz'
    _VOW = 'aaaeeeeiiiiooouuy'
    def generate_name(self):
        name_len = self._world.game.rng.randint(4,7)
        last_chr = None
        last_con = True
        name = self._world.game.rng.choice(self._CON)
        while len(name) < name_len:
            if last_con and last_chr and self._world.game.chance_in(7):
                new_chr = last_chr
            elif not last_con:
                new_chr = self._world.game.rng.choice(self._CON)
                last_chr = new_chr
                last_con = True
            else:
                new_chr = self._world.game.rng.choice(self._VOW)
                last_chr = new_chr
                last_con = False
            name = name + new_chr
        self.desc = name.capitalize()

    def _act_pursue(self):
        if self._world.game.chance_in(7):
            mydir = self._world.game.rng.choice(commands.DIRS)
        else:
            x, y = 0, 0
            if self._world.game.hero.x < self.x:
                x = -1
            elif self._world.game.hero.x > self.x:
                x = 1
            if self._world.game.hero.y < self.y:
                y = -1
            elif self._world.game.hero.y > self.y:
                y = 1
            if x and not y:
                x = 2 * x
            if y and not x:
                if self._world.game.coinflip():
                    x = 1
                else:
                    x = -1
            mydir = (y,x)
        while True:
            try:
                return self.do_walk(*mydir)
            except AlreadyOccupied:
                return self.do_attack(*mydir)
            except (MovementBlocked, NoSuchPlace):
                mydir = self._world.game.rng.choice(commands.DIRS)
                pass

    def _act_wander(self):
        while True:
            mydir = self._world.game.rng.choice(commands.DIRS)
            try:
                return self.do_walk(*mydir)
            except AlreadyOccupied:
                return self.do_attack(*mydir)
            except (MovementBlocked, NoSuchPlace):
                pass

    def _act_peaceful(self):
        while True:
            mydir = self._world.game.rng.choice(commands.DIRS)
            try:
                return self.do_walk(*mydir)
            except (AlreadyOccupied, MovementBlocked, NoSuchPlace):
                pass

