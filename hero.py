# vim:set ts=4 sts=4 et ai:

from actor import Actor
import armor
import weapon
from treasure import Gold
from errors import *

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
            except WasKilled as exc:
                self._world.game.term.msg('you killed %s.' % exc.victim)
                self.xp += exc.victim.hd * self._world.game.rng.randint(1,3)
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

    XPLEVELS = [20 * (_maxlvl ** 2) + 10 for _maxlvl in range(20)]
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

