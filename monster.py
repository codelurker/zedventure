# vim:set sts=4 et ai:

from actor import Actor

class Worm (Actor):
    hd = 1; move_speed = 14; attack_speed = 14
    glyph = 'w'; desc = 'the worm'; _act = Actor._act_wander

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

class Imp (Actor):
    hd = 3; move_speed = 5; attack_speed = 6
    glyph = 'q'; desc = 'the imp'; _act = Actor._act_wander

class Pixie (Actor):
    hd = 3; move_speed = 4; attack_speed = 4
    glyph = 'p'; desc = 'the pixie'; _act = Actor._act_wander

class Orc (Actor):
    hd = 4; move_speed = 5; attack_speed = 5
    glyph = 'o'; desc = 'the orc'; _act = Actor._act_pursue

class Python (Actor):
    hd = 5; move_speed = 8; attack_speed = 7
    glyph = 'S'; desc = 'the python'; _act = Actor._act_wander

class Lizardman (Actor):
    hd = 5; move_speed = 7; attack_speed = 7 
    glyph = 'L'; desc = 'the lizardman'; _act = Actor._act_pursue

class Ogre (Actor):
    hd = 6; move_speed = 7; attack_speed = 10
    glyph = 'O'; desc = 'the ogre'; _act = Actor._act_wander

class Troll (Actor):
    hd = 7; move_speed = 7; attack_speed = 8
    glyph = 'T'; desc = 'the troll'; _act = Actor._act_pursue

MONSTERS = [Leech,Rat,Cockroach,Goblin,Kobold,Snake,GiantBat,Hobgoblin,
    Imp,Pixie,Orc,Python,Lizardman,Ogre,Troll]

def generate_monster(world):
    y, x = world.size()
    mon = None
    while True:
        k = world.game.rng.randrange(1,y,2)
        j = world.game.rng.randrange(1,x,2)
        if world.game.area.is_occ(k,j) or world.game.area.is_block(k,j):
            continue
        mrange = min(len(MONSTERS),world.game.area.depth)
        mon = world.game.rng.choice(MONSTERS[0:world.game.area.depth+2])(world,k,j)
        break
    mon.generate()
    return mon

