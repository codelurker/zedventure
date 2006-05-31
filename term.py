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
        hero = self.game.hero
        self.stat.addstr(0,0,"Hp %-3d(%d) " % (hero._hp,hero.hpmax))
        self.stat.addstr(0,15,"$%-6d " % (hero.gold))
        if hero.weapon:
            self.stat.addstr(0,25,"Dmg %-2d " % (((hero.weapon.damage[0]+hero.weapon.damage[1])/2)+hero.weapon.bonus))
        if hero.armor:
            self.stat.addstr(0,32,"AC %-2d " % (hero.armor.ac + hero.armor.bonus))
        self.stat.addstr(0,60,"Exp %d/%d " % (hero.xplvl,hero.xp))
        self.stat.addstr(1,0,"%s in Dungeon lvl %d" % (hero,self.game.area.depth))
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
	# uppercase the first letter
        self.wmsg.addstr("\n%s" % data[0].upper() + data[1:])
        self.wmsg.noutrefresh()

