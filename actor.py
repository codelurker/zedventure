class Actor (object):
    move_speed = 7
    attack_speed = 7
    glyph = '0'
    desc = 'the actor'
    __slots__ = ('y','x','_hp','hpmax','_mp','mpmax',
                'wait_until','desc')
    def __init__(self,y,x):
        World.enter(y,x,self)
        self._hp, self.hpmax, self._mp, self.mpmax = 1, 1, 1, 1
        self.wait_until = World.game.time

    def __str__(self):
        if self.desc:
            return self.desc
        else:
            return "it"

    def __cmp__(self,other): return cmp(self.wait_until, other.wait_until)

    def generate(self):
        self.hpmax = 0
        for x in xrange(self.hd):
            self.hpmax += World.game.rng.randint(1,7)
        self._hp = self.hpmax

    def do_walk(self,y,x):
        """T.do_walk(y,x) -> integer"""
        yy = self.y + y
        xx = self.x + x
        if not World.is_valid(yy,xx):
            raise NoSuchPlace, "%d, %d" % (yy,xx)
        elif World.is_block(yy,xx):
            raise MovementBlocked
        elif World.is_occ(yy,xx):
            raise AlreadyOccupied
        else:
            World.leave(self.y,self.x,self)
            World.enter(yy,xx,self)
        return self.move_speed

    def do_attack(self,y,x):
        """T.do_attack(y,x) -> integer"""
        opponent = World.occ[self.y+y,self.x+x]
        if opponent.is_hero():
            damage = World.game.rng.randint(1,self.hd)
            if opponent.armor:
                if World.game.rng.randint(0,10) > opponent.armor.evade:
                    World.game.term.msg('%s misses.' % self)
                    return self.attack_speed
                ac = World.game.rng.randint(0,opponent.armor.ac)
                if ac >= damage:
                    World.game.term.msg("%s's attack glanced off your armor." % self)
                    return self.attack_speed
                else:
                    damage -= ac
            World.game.term.msg('%s attacks!' % self)
            opponent.hp -= damage
        return self.attack_speed

    def is_hero(self): return False
    def is_alive(self): return self._hp > 0

    def die(self):
        an = 0
        for n, a in enumerate(World.game.actors):
            if a is self:
                an = n
                break
        del World.game.actors[an]
        World.leave(self.y,self.x,self)

    def act(self):
        time = self._act()
        self.wait_until = World.game.time + time

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

    _CON = 'bbcccddfffggghhjjjkklllmmmnnnnppqrrrrsssttvwwwxzz'
    _VOW = 'aaaeeeeiiiiooouuy'
    def generate_name(self):
        name_len = World.game.rng.randint(4,7)
        last_chr = None
        last_con = True
        name = World.game.rng.choice(self._CON)
        while len(name) < name_len:
            if last_con and last_chr and World.game.chance_in(7):
                new_chr = last_chr
            elif not last_con:
                new_chr = World.game.rng.choice(self._CON)
                last_chr = new_chr
                last_con = True
            else:
                new_chr = World.game.rng.choice(self._VOW)
                last_chr = new_chr
                last_con = False
            name = name + new_chr
        self.desc = name.capitalize()

    def _act_pursue(self):
        if World.game.chance_in(7):
            mydir = World.game.rng.choice(commands.DIRS)
        else:
            x, y = 0, 0
            if World.game.hero.x < self.x:
                x = -1
            elif World.game.hero.x > self.x:
                x = 1
            if World.game.hero.y < self.y:
                y = -1
            elif World.game.hero.y > self.y:
                y = 1
            if x and not y:
                x = 2 * x
            if y and not x:
                if World.game.coinflip():
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
                mydir = World.game.rng.choice(commands.DIRS)
                pass

    def _act_wander(self):
        while True:
            mydir = World.game.rng.choice(commands.DIRS)
            try:
                return self.do_walk(*mydir)
            except AlreadyOccupied:
                return self.do_attack(*mydir)
            except (MovementBlocked, NoSuchPlace):
                pass

    def _act_peaceful(self):
        while True:
            mydir = World.game.rng.choice(commands.DIRS)
            try:
                return self.do_walk(*mydir)
            except (AlreadyOccupied, MovementBlocked, NoSuchPlace):
                pass

class Hero (Actor):
    __slot__ = ('_running','desc','weapon','armor','xplvl','_xp')
    glyph = '@'
    def __init__(self,y,x,name=None):
        Actor.__init__(self,y,x)
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
        if isinstance(item, armor.Armor):
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
        assert World.is_occ(y,x)
        opponent = World.occ[y,x]
        time = 7
        if self.weapon:
            tohit = 10 - self.weapon.hit + opponent.hd - self.weapon.bonus
            hit = World.game.rng.randint(1,20) >= tohit
            time = self.weapon.speed
        else:
            hit = not World.game.chance_in(7)
        if not hit:
            World.game.term.msg('you miss %s.' % opponent)
        else:
            if self.weapon:
                damage = World.game.rng.randint(*self.weapon.damage) + self.weapon.bonus
                time = self.weapon.speed
            else:
                damage = World.game.rng.randint(1,3)
            try:
                opponent.hp -= damage
                World.game.term.msg('you hit %s.' % opponent)
            except WasKilled, exc:
                World.game.term.msg('you killed %s.' % exc.victim)
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
            World.game.term.redraw()
            cmd, args = World.game.term.get_command()
            time_passed = cmd(World.game,*args)
            if time_passed and World.game.chance_in(27 - self.xplvl):
                self.hp += 1
        self.wait_until = World.game.time + time_passed

    XPLEVELS = [20 * (_maxlvl ** 2) + 10 for _maxlvl in xrange(20)]
    def get_xp(self): return self._xp
    def set_xp(self,new_xp):
        try:
            while new_xp >= self.XPLEVELS[self.xplvl-1]:
                self.xplvl += 1
                hpinc = World.game.rng.randint(7,7 * self.xplvl / 2)
                self.hpmax += hpinc
                self.hp += hpinc
                World.game.term.msg('you have reached experience level %d!' % self.xplvl)
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
def generate_monster():
    y, x = World.size()
    mon = None
    while True:
        k = World.game.rng.randrange(1,y,2)
        j = World.game.rng.randrange(1,x,2)
        if World.game.area.is_occ(k,j) or World.game.area.is_block(k,j):
            continue
        mon = World.game.rng.choice(MONSTERS)(k,j)
        break
    mon.generate()
    return mon
