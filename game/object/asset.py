__author__ = 'ESTEBAN'

from drawable import Drawable

from game.tools import Message
import pygame


class Asset(Drawable):
    # an asset is a drawable capable of nothing and with 1 frame only
    def __init__(self, image, x, y, w, h, blitx, blity):
        Drawable.__init__(self, image, x, y, w, h, 1, blitx, blity)


class Text(Drawable):
    def __init__(self, image, x, y, value):
        Drawable.__init__(self, image, x, y, 36, 28, 1, 0, 511)
        self.screenfont = pygame.font.SysFont("Quartz MS", 18, True)
        self.value = value

    def draw(self, level):
        screen = pygame.display.get_surface()
        label = self.screenfont.render(self.value, 1, (255, 255, 255))
        screen.blit(label, self.position)

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > 2000:
            level.topobjects.remove(self)


class LevelEndBar(Drawable):
    def __init__(self, image, x, y, speed, range):
        Drawable.__init__(self, image, x, y, 25, 8, 1, 0, 592)
        self.direction = 1
        self.speed = speed
        self.range = range

    def update(self, level):
        if self.position.y < self.range[0]:
            self.direction *= -1
        elif self.position.y > self.range[1]:
            self.direction *= -1

        self.position.y += self.direction*self.speed

    def action(self, level):
        range = self.range[1] - self.range[0]
        delta = min(range, abs(self.position.y - self.range[0]))
        score = range - delta
        print "TOUCHE ! {} / {}".format(score, range)
        print "SCORE ! {} ".format(score*100/range)
        text = Text(level.imageSprites, self.position.left, self.range[0] - 50, "{} !".format(score*100/range))
        level.toptopobjects.append(text)
        level.playsound('level-complete')
        return Message.TERMINATELEVEL


class VerticalPlatform(Drawable):
    def __init__(self, image, x, y, speed, range):
        Drawable.__init__(self, image, x, y, 80, 11, 1, 0, 500)
        self.direction = 1
        self.speed = speed
        self.range = range

    def update(self, level):
        if self.position.y < self.range[0]:
            self.direction *= -1
        elif self.position.y > self.range[1]:
            self.direction *= -1

        self.position.y += self.direction*self.speed


class Tumb(Drawable):
    def __init__(self, image, x, y, w, h, nbframes):
        Drawable.__init__(self, image, x, y, w, h, nbframes, 0, 276)

    def updateframe(self, level):
        if self.frame == self.nbframes - 1:
            return
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > 25:
            self.lastupdateframe = ticks
            self.frame += 1


class Impact(Drawable):
    def __init__(self, image, x, y):
        x -= 36/2
        y -= 28/2
        Drawable.__init__(self, image, x, y, 36, 28, 1, 0, 511)

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > 50:
            level.objects.remove(self)


class CoinAdded(Drawable):
    def __init__(self, image, x, y):
        Drawable.__init__(self, image, x, y, 16, 16, 4, 0, 0)
        self.yorigin = y
        self.frame = 3

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > 10:
            self.position.top -= 5
            if self.position.top < self.yorigin-50:
                level.objects.remove(self)