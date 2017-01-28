__author__ = 'ESTEBAN'

from pygame import Rect


class Camera:
    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)

    def setcenterx(self, value):
        self.rect.centerx = value

    def setcentery(self, value):
        self.rect.centery = value



