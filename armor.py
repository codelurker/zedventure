from sets import ImmutableSet as iset
# TODO: damage type (see weapon.py)

class Material (object): # abstract material class
    """
    This is an abstract class for armor materials.

    Sub-classes of Material should provide three class values:

      wght - weight multiplier
      dura - durability (higher -> more durable)
      ench - enchantability (higher -> more enchantable)

    For convenience the string value of a material class 
    is the name of the class itself.
    """
    def __str__(self): return self.__name__

###  MATERIALS  ###
class gold (Material):
    wght = 3; dura = .25; ench = 3
class silver (Material):
    wght = 2; dura = .5; ench = 2
class bronze (Material):
    wght = 1; dura = 1; ench = 1
class steel (Material):
    wght = 1.5; dura = 2; ench = 1
class mithril (Material):
    wght = 1.5; dura = 4; ench = 1
class iron (Material):
    wght = 2; dura = 2; ench = .5
class bone (Material):
    wght = .5; dura = .5; ench = 2
class leather (Material):
    wght = 1; dura = 3; ench = 2
class cloth (Material):
    wght = 1; dura = 3; ench = 2

MATERIALS = {
    'gold': gold,
    'silver': silver,
    'bronze': bronze,
    'steel': steel,
    'mithril': mithril,
    'iron': iron,
    'bone': bone,
    'leather': leather,
    'cloth': cloth
}

###  BASE TYPE  ###
class Armor (object): # abstract class
    """
    This is an abstract class for armor.
    """
    # subclasses must provide mass, base_evade, base_ac, name
    __slots__ = ('bonus','_repair','_mat')
    # override this to change the allowed materials (for the generator)
    materials = (leather,bone,iron,steel,bronze,silver,gold)
    def __init__(self,material,bonus=0):
        if material in self.materials:
            self._mat = MATERIALS[material]
        else:
            from warnings import warn
            warn('incompatible material: %s' % str(material))
        self.bonus = bonus
        self._repair = 1.0
    def __str__(self):
        if len(self.materials) > 1:
            if self.bonus > 0:
                return "a +%d %s %s" % (self.bonus, self._mat.__name__, self.name)
            elif self.bonus < 0:
                return "a %d %s %s" % (self.bonus, self._mat.__name__, self.name)
            else:
                return "a %s %s" % (self._mat.__name__, self.name)
        else:
            if self.bonus > 0:
                return "a +%d %s" % (self.bonus, self.name)
            elif self.bonus < 0:
                return "a %d %s" % (self.bonus, self.name)
            else:
                return "a %s" % self.name
    def glyph(self): return ']'

    # these are calculated and/or read-only properties
    weight = property(lambda self: self.mass * self._mat.wght)
    evade = property(lambda self: int(self.base_evade / self._mat.wght) + self.bonus)
    ac = property(lambda self: self.base_ac + self.bonus)
    material = property(lambda self: self._mat.__name__)
    repair = property(lambda self: int(self._repair * 100))

###  ARMOR  ###
class PaddedArmor(Armor):
    name = 'padded armor'; base_evade = 5; base_ac = 2; mass = 2
    materials = iset(['cloth'])

class LeatherArmor(Armor):
    name = 'leather armor'; base_evade = 4; base_ac = 3; mass = 4
    materials = iset(['leather'])

class BoneArmor(Armor):
    name = 'bone armor'; base_evade = 6; base_ac = 4; mass = 3
    materials = iset(['bone'])

class ChainMail(Armor):
    name = 'chain mail'; base_evade = 3; base_ac = 6; mass = 5
    materials = iset(['steel','bronze','silver','gold','mithril'])

class ScaleMail(Armor):
    name = 'scale mail'; base_evade = 2; base_ac = 8; mass = 6
    materials = iset(['steel','bronze','silver','gold','mithril'])

class SplintMail(Armor):
    name = 'splint mail'; base_evade = 1; base_ac = 9; mass = 7
    materials = iset(['steel','bronze','silver','gold','mithril'])

class PlateMail(Armor):
    name = 'plate mail'; base_evade = 1; base_ac = 10; mass = 8
    materials = iset(['steel','bronze','silver','gold','mithril'])

class PlateArmor(Armor):
    name = 'full plate armor'; base_evade = 0; base_ac = 11; mass = 9
    materials = iset(['steel','bronze','silver','gold','mithril'])

###  GENERATOR  ###
ARMOR = (PaddedArmor,LeatherArmor,BoneArmor,ChainMail,ScaleMail,
        SplintMail,PlateMail,PlateArmor)
def generate(rng,depth):
    which = rng.randint(2,3)
    bonus = rng.randint(1,3)
    if depth < 4:
        which -= 2
        bonus -= 1
    elif depth < 7:
        which -= 1
    elif depth < 10:
        which += 1
        bonus += 1
    elif depth < 14:
        which += 2
        bonus += 2
    elif depth < 21:
        which += 4
        bonus += 2
    if rng.randint(0,1): bonus = 0
    mat = rng.sample(list(ARMOR[which].materials),1)[0]
    return ARMOR[which](mat,bonus)

