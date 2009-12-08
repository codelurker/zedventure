
from errors import *

# there are three degrees of movement, north/south is a hack
NORTHWEST = (-1,-1)
SOUTHWEST = (1,-1)
NORTHEAST = (-1,1)
SOUTHEAST = (1,1)
EAST = (0,2)
WEST = (0,-2)
DIRS = (NORTHWEST,NORTHEAST,EAST,SOUTHEAST,SOUTHWEST,WEST)

def status(game):
    times = []
    for a in game.actors:
        times.append(a.wait_until)
    game.term.msg("actor queue size: %d" % len(game.actors))
    game.term.msg("times: %s" % times)
    return 0

def show_wielded(game):
    if game.hero.weapon:
        game.term.msg("you are wielding %s." % game.hero.weapon)
    else:
        game.term.msg("you are not weilding a weapon.")
    return 0

def show_worn(game):
    if game.hero.armor:
        game.term.msg("you are wearing %s." % game.hero.armor)
    else:
        game.term.msg("you are not wearing armor.")
    return 0

def pickup(game):
    try:
        item = game.area.item[game.hero.y,game.hero.x]
        old_item = game.hero.equip(item)
        if old_item:
            game.area.item[game.hero.y,game.hero.x] = old_item
            game.term.msg('you drop %s.' % old_item)
        else:
            del game.area.item[game.hero.y,game.hero.x]
        game.term.msg('you pick up %s.' % item)
    except KeyError:
        game.term.msg('there is nothing here to pick up.')
        return 0
    return 7

def wait(game):
    return 7

def quit(game):
    raise QuitGame
    return 0

def downstairs(game):
    game.next_level()
    return 0

def upstairs(game):
    game.prev_level()
    return 0

def move(game,dir):
    try:
        return game.hero.do_walk(*dir)
    except AlreadyOccupied:
        return game.hero.do_attack(*dir)
    except (NoSuchPlace, MovementBlocked):
        pass
    return 0

def run(game,dir):
    try:
        return game.hero.do_run(*dir)
    except (NoSuchPlace, MovementBlocked, AlreadyOccupied):
        pass
    return 0

# This is part of the hack for moving north and south.
# North and south movement actually alternates between
# NE/NW and SE/SW.
_last_east = False

def move_north(game):
    global _last_east
    dir1, dir2 = None, None
    if _last_east:
        _last_east = False
        dir1, dir2 = NORTHWEST, NORTHEAST
    else:
        _last_east = True
        dir1, dir2 = NORTHEAST, NORTHWEST
    try:
        return game.hero.do_walk(*dir1)
    except:
        # something went wrong, try using move() to walk
        # the alternate direction instead
        _last_east = not _last_east
        return move(game,dir2)

def move_south(game):
    global _last_east
    dir1, dir2 = None, None
    if _last_east:
        _last_east = False
        dir1, dir2 = SOUTHWEST, SOUTHEAST
    else:
        _last_east = True
        dir1, dir2 = SOUTHEAST, SOUTHWEST
    try:
        return game.hero.do_walk(*dir1)
    except:
        # something went wrong, try using move() to walk
        # the alternate direction instead
        _last_east = not _last_east
        return move(game,dir2)

