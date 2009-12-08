# vim:set ts=4 sts=4 et ai:

import sys
import random

import config
import area
from hero import Hero
from term import Term
from errors import *

class Zedventure (object):
    __slots__ = ('time','area','hero','actors','term','rng')
    def __init__(self,args):
        # init the game
        self.time = 0
        self.area = None
        self.term = None
        self.hero = None
        self.actors = []
        self.rng = random.Random()

    def __call__(self,screen):
        """Z(screen) -> None"""
        # init the interface
        self.area = area.Area(self)
        self.term = Term(self,screen)
        (y, x) = self.term.viewsize()  # wtf? why can't curses
        self.area.resize(y, x-1)       # draw on the screen edge?
        self.hero = Hero(self.area,1,1,None)
        self.actors = [self.hero]
        self.actors.extend(self.area.generate(0))
        self.area.enter(self.hero.y, self.hero.x, self.hero)
        self.term.redraw()
        # start the game
        running = True
        while running:
            actor = self.actors[0]
            try:
                while actor.wait_until <= self.time:
                    actor.act()
            except QuitGame:
                self.term.msg('Goodbye, thanks for playing!')
                self.term.waitforkey()
                running = False
            except Escaped:
                self.term.msg('You escaped with %d gold!' % self.hero.gold)
                self.term.waitforkey()
                running = False
            except WasKilled:
                self.term.msg('You died.')
                self.term.waitforkey()
                running = False
            finally:
                self.time += 1
            self.queue_actor(actor)

    def new_level(self,increment):
        self.actors = self.area.generate(increment)
        self.actors.insert(0,self.hero)
        self.area.occ[self.hero.y,self.hero.x] = self.hero

    def prev_level(self):
        self.new_level(-1)

    def next_level(self):
        self.new_level(1)

    def queue_actor(self,actor):
        done = False
        for i,a in enumerate(self.actors):
            if a > actor:
                self.actors.remove(actor)
                self.actors.insert(i, actor)
                done = True
                break
        if not done:
            self.actors.remove(actor)
            self.actors.append(actor)

    def coinflip(self):
        return bool(self.rng.randint(0,1))

    def chance_in(self,odds):
        return self.rng.randint(1,odds) == 1

    def percent_chance(self,pct):
        return self.rng.randint(1,100) <= pct

