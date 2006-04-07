
from sets import ImmutableSet as iset

class Weapon (object):
    """Abstract class for weapons.
    
    Subclasses must define these attributes:
        name - name of the weapon or weapon type, string
        type - damage type (set of strings)
        speed - weapon speed, in ticks (lower is faster)
        hit - to-hit ability modifier (higher is more accurate)
        damage - damage range tuple (min, max)

    The damage type is a Set object that contains at least one
    string describing the type of damage the weapon does. The
    common built-in damage types are piercing, slashing and bludgeoning.

    Weapons have an attribute 'bonus' that applies to hit and damage
    calculation.
    """
    __slots__ = ('bonus')
    def __init__(self,bonus=0): self.bonus = bonus
    def __str__(self):
        if self.bonus:
            return "a +%d %s" % (self.bonus, self.name)
        else:
            return "a "+self.name
    def __repr__(self):
        return '%s(%d)' % (self.__class__.__name__, self.bonus)
    def glyph(self): return ')'
    def roll_damage(self,rng): return rng.randint(*self.damage) + self.bonus

# BLADES
class Dagger(Weapon):
    name = 'dagger'; speed = 5; hit = 8; damage = (2,4)
    type = iset(['piercing'])
class ShortSword(Weapon):
    name = 'short sword'; speed = 6; hit = 7; damage = (2,6)
    type = iset(['slashing', 'piercing'])
class Sickle(Weapon):
    name = 'sickle'; speed = 5; hit = 6; damage = (3,7)
    type = iset(['slashing'])
class Scimitar(Weapon):
    name = 'scimitar'; speed = 7; hit = 7; damage = (2,8)
    type = iset(['slashing'])
class Falchion(Weapon):
    name = 'falchion'; speed = 7; hit = 6; damage = (3,9)
    type = iset('slashing')
class LongSword(Weapon):
    name = 'long sword'; speed = 7; hit = 6; damage = (4,11)
    type = iset(['slashing', 'piercing'])
class Katana(Weapon):
    name = 'katana'; speed = 4; hit = 7; damage = (4,13)
    type = iset(['slashing', 'piercing'])
# AXES
class HandAxe(Weapon):
    name = 'hand axe'; speed = 7; hit = 7; damage = (3,6)
    type = iset(['slashing', 'bludgeoning'])
class PickAxe(Weapon):
    name = 'pick-axe'; speed = 7; hit = 5; damage = (3,8)
    type = iset(['piercing', 'bludgeoning'])
class HeavyPick(Weapon):
    name = 'heavy pick'; speed = 7; hit = 4; damage = (4,9)
    type = iset(['piercing', 'bludgeoning'])
class BattleAxe(Weapon):
    name = 'battle axe'; speed = 8; hit = 6; damage = (4,10)
    type = iset(['slashing', 'bludgeoning'])
class WarAxe(Weapon):
    name = 'war axe'; speed = 8; hit = 5; damage = (4,12)
    type = iset(['slashing', 'bludgeoning'])
class GreatAxe(Weapon):
    name = 'great axe'; speed = 8; hit = 5; damage = (5,14)
    type = iset(['slashing', 'bludgeoning'])
class DoubleAxe(Weapon):
    name = 'double axe'; speed = 4; hit = 5; damage = (5,14)
    type = iset(['slashing', 'bludgeoning'])
# POLEARMS
class ShortStaff(Weapon):
    name = 'short staff'; speed = 4; hit = 8; damage = (2,4)
    type = iset(['bludgeoning'])
class Spear(Weapon):
    name = 'spear'; speed = 6; hit = 6; damage = (3,6)
    type = iset(['piercing'])
class Quarterstaff(Weapon):
    name = 'quarterstaff'; speed = 4; hit = 8; damage = (2,5)
    type = iset(['bludgeoning'])
class LongSpear(Weapon):
    name = 'long spear'; speed = 7; hit = 6; damage = (3,8)
    type = iset(['piercing'])
class Trident(Weapon):
    name = 'trident'; speed = 8; hit = 5; damage = (3,12)
    type = iset(['piercing'])
class Scythe(Weapon):
    name = 'scythe'; speed = 8; hit = 4; damage = (4,14)
    type = iset(['slashing', 'piercing'])
class Halberd(Weapon):
    name = 'halberd'; speed = 9; hit = 3; damage = (5,17)
    type = iset(['slashing', 'piercing'])
# BLUDGEONS
class Club(Weapon):
    name = 'club'; speed = 7; hit = 9; damage = (1,5)
    type = iset(['bludgeoning'])
class SpikedClub(Weapon):
    name = 'spiked club'; speed = 7; hit = 7; damage = (3,7)
    type = iset(['bludgeoning', 'piercing'])
class Mace(Weapon):
    name = 'mace'; speed = 7; hit = 6; damage = (3,8)
    type = iset(['bludgeoning'])
class Morningstar(Weapon):
    name = 'morningstar'; speed = 7; hit = 6; damage = (4,10)
    type = iset(['bludgeoning', 'piercing'])
class Flail(Weapon):
    name = 'heavy flail'; speed = 8; hit = 4; damage = (4,12)
    type = iset(['bludgeoning'])
class DireMace(Weapon):
    name = 'dire mace'; speed = 5; hit = 5; damage = (5,12)
    type = iset(['bludgeoning'])
class WarHammer(Weapon):
    name = 'war hammer'; speed = 7; hit = 5; damage = (7,20)
    type = iset(['bludgeoning'])
# IMPROVISED
class BigRock(Weapon):
    name = 'big rock'; speed = 7; hit = 9; damage = (1,2)
    type = iset(['bludgeoning'])
class PoolCue(Weapon):
    name = 'pool cue'; speed = 7; hit = 6; damage = (1,3)
    type = iset(['bludgeoning'])
class Chain(Weapon):
    name = 'chain'; speed = 7; hit = 5; damage = (1,5)
    type = iset(['bludgeoning'])
class Crowbar(Weapon): 
    name = 'crowbar'; speed = 7; hit = 6; damage = (3,7)
    type = iset(['bludgeoning'])
class WoodenBat(Weapon):
    name = 'wooden bat'; speed = 7; hit = 7; damage = (2,5)
    type = iset(['bludgeoning'])
class MetalBat(Weapon):
    name = 'metal bat'; speed = 7; hit = 7; damage = (3,6)
    type = iset(['bludgeoning'])
class Machete(Weapon):
    name = 'machete'; speed = 7; hit = 7; damage = (4,8)
    type = iset(['slashing'])
# EXOTIC
class Sap(Weapon):
    name = 'sap'; speed = 7; hit = 6; damage = (1,3)
    type = iset(['bludgeoning'])
class BrassKnuckles(Weapon):
    name = 'set of brass knuckles'; speed = 7; hit = 8; damage = (2,4)
    type = iset(['bludgeoning'])
class Saingham(Weapon):
    name = 'saingham'; speed = 7; hit = 6; damage = (2,5)
    type = iset(['piercing'])
class Kukri(Weapon):
    name = 'kukri'; speed = 6; hit = 6; damage = (3,7)
    type = iset(['slashing'])
class Nunchaku(Weapon):
    name = 'nunchaku'; speed = 4; hit = 5; damage = (4,8)
    type = iset(['bludgeoning'])
class Katar(Weapon):
    name = 'katar'; speed = 5; hit = 5; damage = (5,10)
    type = iset(['slashing', 'piercing'])
class Naginata(Weapon):
    name = 'naginata'; speed = 5; hit = 5; damage = (3,12)
    type = iset(['bludgeoning'])

WEAPONS = [
# BLADES
Dagger,
ShortSword,
Sickle,
Scimitar,
Falchion,
LongSword,
Katana,
# AXES
HandAxe,
PickAxe,
HeavyPick,
BattleAxe,
WarAxe,
GreatAxe,
DoubleAxe,
# POLEARMS
ShortStaff,
Spear,
Quarterstaff,
LongSpear,
Trident,
Scythe,
Halberd,
# BLUDGEONS
Club,
SpikedClub,
Mace,
Morningstar,
Flail,
DireMace,
WarHammer,
# IMPROVISED
BigRock,
PoolCue,
Chain,
Crowbar,
WoodenBat,
MetalBat,
Machete,
# EXOTIC
Sap,
BrassKnuckles,
Saingham,
Kukri,
Nunchaku,
Katar,
Naginata
]

def generate(rng,depth):
    type = rng.randint(1,7)
    which = rng.randint(1,2)
    bonus = 0
    if depth < 3:
        which -= 1
    elif depth < 7:
        bonus = rng.randint(0,2)
        which -= 1
    elif depth < 14:
        bonus = rng.randint(1,3)
    elif depth < 21:
        bonus = rng.randint(2,4)
        which += 1
    else:
        bonus = rng.randint(1,3)
    if rng.randint(0,1): bonus = 0
    item = WEAPONS[type * which + 1](bonus)
    return item

