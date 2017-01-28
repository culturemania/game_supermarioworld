__author__ = 'ESTEBAN'


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def iszero(self):
        return self.x == self.y == 0

    def __assign__(self, val):
        self.x = val.x
        self.y = val.y
        print "assign"

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if isinstance(other, Vector2):
            return self.x != other.x or self.y != other.y