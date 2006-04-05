# vim:set ts=4 sts=4 et ai:

from errors import *
import commands
import armor
import weapon
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
        self._gold = self._world.game.rng.randint(
                0, self.hd * self.hpmax / self._hp * 5
            )

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

class Hero (Actor):
    __slot__ = ('_running','desc','weapon','armor','xplvl','_xp')
    glyph = '@'
    def __init__(self,world,y,x,name=None):
        Actor.__init__(self,world,y,x)
        self._hp, self.hpmax = 10, 10
        self._running = None
        self.weapon = None
        self.armor = None
        self.xplvl = 1
        self._xp = 0
        if not name:
            self.generate_name()
        else:
            self.desc = name

    def is_hero(self): return True
    def do_run(self,y,x):
        self._running = (y,x)
        return self.do_walk(y,x)

    def equip(self,item):
        old_item = None
        if isinstance(item, Gold):
            old_item = 0;
            self._gold = self._gold + item.amount
        elif isinstance(item, armor.Armor):
            old_item = self.armor
            self.armor = item
        elif isinstance(item, weapon.Weapon):
            old_item = self.weapon
            self.weapon = item
        return old_item

    def do_attack(self,y,x):
        """T.do_attack(y,x) -> integer"""
        y = self.y + y
        x = self.x + x
        assert self._world.is_occ(y,x)
        opponent = self._world.occ[y,x]
        time = 7
        if self.weapon:
            tohit = 10 - self.weapon.hit + opponent.hd - self.weapon.bonus
            hit = self._world.game.rng.randint(1,20) >= tohit
            time = self.weapon.speed
        else:
            hit = not self._world.game.chance_in(7)
        if not hit:
            self._world.game.term.msg('you miss %s.' % opponent)
        else:
            if self.weapon:
                damage = self._world.game.rng.randint(*self.weapon.damage) + self.weapon.bonus
                time = self.weapon.speed
            else:
                damage = self._world.game.rng.randint(1,3)
            try:
                opponent.hp -= damage
                self._world.game.term.msg('you hit %s.' % opponent)
            except WasKilled, exc:
                self._world.game.term.msg('you killed %s.' % exc.victim)
                self.xp += exc.victim.hd
                exc.victim.die()
        return time

    def act(self):
        time_passed = 0
        if self._running:
            try:
                time_passed = self.do_walk(*self._running)
            except (MovementBlocked, NoSuchPlace, AlreadyOccupied):
                self._running = None
        else:
            self._world.game.term.redraw()
            cmd, args = self._world.game.term.get_command()
            time_passed = cmd(self._world.game,*args)
            if time_passed and self._world.game.chance_in(27 - self.xplvl):
                self.hp += 1
        self.wait_until = self._world.game.time + time_passed

    XPLEVELS = [20 * (_maxlvl ** 2) + 10 for _maxlvl in xrange(20)]
    def get_xp(self): return self._xp
    def set_xp(self,new_xp):
        try:
            while new_xp >= self.XPLEVELS[self.xplvl-1]:
                self.xplvl += 1
                hpinc = self._world.game.rng.randint(7,7 * self.xplvl / 2)
                self.hpmax += hpinc
                self.hp += hpinc
                self._world.game.term.msg('you have reached experience level %d!' % self.xplvl)
        except IndexError:
            pass
        self._xp = new_xp
    xp = property(get_xp,set_xp,None,'experience points')

class Ooze (Actor):
    hd = 1; move_speed = 14; attack_speed = 14
    glyph = 'o'; desc = 'the ooze'; _act = Actor._act_wander

class Leech (Actor):
    hd = 1; move_speed = 14; attack_speed = 14
    glyph = 'l'; desc = 'the leech'; _act = Actor._act_wander

class Rat (Actor):
    hd = 1; move_speed = 7; attack_speed = 10
    glyph = 'r'; desc = 'the rat'; _act = Actor._act_pursue

class Cockroach (Actor):
    hd = 1; move_speed = 7; attack_speed = 10
    glyph = 'c'; desc = 'the cockroach'; _act = Actor._act_pursue

class Goblin (Actor):
    hd = 2; move_speed = 7; attack_speed = 7
    glyph = 'g'; desc = 'the goblin'; _act = Actor._act_pursue

class Kobold (Actor):
    hd = 2; move_speed = 7; attack_speed = 7
    glyph = 'k'; desc = 'the kobold'; _act = Actor._act_pursue

class Snake (Actor):
    hd = 2; move_speed = 10; attack_speed = 7
    glyph = 's'; desc = 'the snake'; _act = Actor._act_wander

class GiantBat (Actor):
    hd = 2; move_speed = 4; attack_speed = 7
    glyph = 'b'; desc = 'the giant bat'; _act = Actor._act_wander

class Hobgoblin (Actor):
    hd = 3; move_speed = 7; attack_speed = 7
    glyph = 'h'; desc = 'the hobgoblin'; _act = Actor._act_pursue

MONSTERS = [Ooze,Leech,Rat,Cockroach,Goblin,Kobold,Snake,GiantBat,Hobgoblin]
def generate_monster(world):
    y, x = world.size()
    mon = None
    while True:
        k = world.game.rng.randrange(1,y,2)
        j = world.game.rng.randrange(1,x,2)
        if world.game.area.is_occ(k,j) or world.game.area.is_block(k,j):
            continue
        mon = world.game.rng.choice(MONSTERS)(world,k,j)
        break
    mon.generate()
    return mon
