__all__ = ('ascii','command')

from commands import *

ascii = True

command = {
    '@': (status,),
    ',': (pickup,),
    'g': (pickup,),
    ']': (show_worn,),
    ')': (show_wielded,),
    '.': (wait,),
    '<': (upstairs,),
    '>': (downstairs,),
    'h': (move, WEST),
    'H': (run, WEST),
    'j': (move_south,),
    'k': (move_north,),
    'l': (move, EAST),
    'L': (run, EAST),
    'y': (move, NORTHWEST),
    'Y': (run, NORTHWEST),
    'u': (move, NORTHEAST),
    'U': (run, NORTHEAST),
    'b': (move, SOUTHWEST),
    'B': (run, SOUTHWEST),
    'n': (move, SOUTHEAST),
    'N': (run, SOUTHEAST),
    'Q': (quit,)
    }

