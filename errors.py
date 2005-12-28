class AlreadyOccupied (Exception):
    pass

class MovementBlocked (Exception):
    pass

class NoSuchPlace (Exception):
    pass

class Escaped (Exception):
    pass

class WasKilled (Exception):
    def __init__(self,actor):
        self.victim = actor
    def __str__(self):
        return '%s was killed.' % self.victim


