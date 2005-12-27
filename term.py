import sys
import curses

import config

TILES = ('.','>','<','^','^','^','#')
class Term (object):
    """Interface object, uses curses."""
    __slots__ = ('game','wmsg','main','stat','lines','cols')
    def __init__(self,game,screen):
        # special curses characters are initialized after initscr()
        if not config.ascii:
            global TILES
            TILES = (curses.ACS_BULLET, curses.ACS_DARROW, curses.ACS_UARROW,
                    curses.ACS_DIAMOND, curses.ACS_DIAMOND, curses.ACS_DIAMOND,
                    curses.ACS_BLOCK)
        self.game = game
        curses.nonl()
        (self.lines, self.cols) = screen.getmaxyx()
        # message window
        self.wmsg = curses.newwin(self.lines-21,self.cols,0,0)
        self.wmsg.idlok(True)
        self.wmsg.scrollok(True)
        # overhead game view
        self.main = curses.newwin(19,self.cols,self.lines-21,0)
        self.main.keypad(True)
        # status line
        self.stat = curses.newwin(2,self.cols,self.lines-2,0)

    def waitforkey(self):
        curses.doupdate()
        self.main.getkey()

    def viewsize(self):
        return self.main.getmaxyx()

    def redraw(self):
        self.draw_status()
        self.draw_main()
        curses.doupdate()

    def draw_status(self):
        self.stat.addstr(0,0,"Hp %-2d(%d) " % (self.game.hero._hp,self.game.hero.hpmax))
        self.stat.addstr(0,60,"Exp %d/%d " % (self.game.hero.xplvl,self.game.hero.xp))
        self.stat.addstr(1,0,"%s in Dungeon lvl %d" % (self.game.hero,self.game.area.depth))
        self.stat.noutrefresh()

    def draw_main(self):
        y, x = self.game.area.size()
        count = 1
        for k in xrange(y):
            for j in xrange(x):
                if count % 2:
                    self.main.addch(k,j,TILES[self.game.area.cell[k][j]])
                count += 1
        for loc, item in self.game.area.item.iteritems():
            i, j = loc
            self.main.addch(i,j,item.glyph())
        for actor in self.game.area.occ.values():
            self.main.addch(actor.y,actor.x,actor.glyph)
        self.main.move(self.game.hero.y,self.game.hero.x)
        self.main.noutrefresh()

    def get_command(self):
        """Z.get_command() -> callable"""
        self.draw_status()
        self.draw_main()
        curses.doupdate()
        while True:
            cmdkey = self.main.getkey()
            try:
                command = config.command[cmdkey]
                return (command[0], command[1:])
            except KeyError:
                self.msg('no such command: %s' % cmdkey)
                curses.doupdate()

    def msg(self,data):
        """Print a game message."""
        if not data: return
        self.wmsg.addstr("\n%s" % data.capitalize())
        self.wmsg.noutrefresh()

