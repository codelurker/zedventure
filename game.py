#!/usr/bin/env python2.4

import sys
import random
from heapq import heappush, heappop, heapreplace

import config
import world
from actor import Hero
from term import Term
from errors import *

MyGame = None

class Zedventure (object):
    __slots__ = ('time','area','hero','actors','term','running','rng')
    def __init__(self,args):
        # set global instance
        global MyGame
        MyGame = self
        # init the game
        self.time = 0
        self.area = None
        self.term = None
        self.hero = None
        self.actors = []
        self.running = False
        self.rng = random.Random()

    def __call__(self,screen):
        """Z(screen) -> None"""
        # init the interface
        self.area = world.Area(self)
        self.term = Term(self,screen)
        self.area.resize(*self.term.viewsize())
        self.area.generate()
        self.hero = Hero(self.area,1,1,None)
        self.queue_actor(self.hero)
        self.term.redraw()
        # start the game
        self.running = True
        while self.running:
            actor = self.actors[0]
            if actor.wait_until <= self.time:
                try:
                    actor.act()
                except WasKilled:
                    self.term.msg('you died.')
                    self.term.waitforkey()
                    self.running = 0
                # this removes the actor from the top of the heap
                # and adds it back to the bottom
                heapreplace(self.actors,actor)
                self.actors.sort()
            else:
                self.time += 1

    def next_level(self):
        self.actors = []
        self.area.generate()
        self.area.occ[self.hero.y,self.hero.x] = self.hero
        self.queue_actor(self.hero)

    def queue_actor(self,actor):
        heappush(self.actors,actor)
        self.actors.sort()

    def coinflip(self):
        return bool(self.rng.randint(0,1))

    def chance_in(self,odds):
        return self.rng.randint(1,odds) == 1

    def percent_chance(self,pct):
        return self.rng.randint(1,100) <= pct

