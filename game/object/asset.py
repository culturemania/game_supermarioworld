__author__ = 'ESTEBAN'

from drawable import Drawable
import random
from game.tools import Message
import pygame


class Asset(Drawable):
    # an asset is a drawable capable of nothing and with 1 frame only
    def __init__(self, image, x, y, w, h, blitx, blity):
        Drawable.__init__(self, image, x, y, w, h, 1, blitx, blity)


class Text(Drawable):
    def __init__(self, image, x, y, value):
        Drawable.__init__(self, image, x, y, 36, 28, 1, 0, 511)
        self.screenfont = pygame.font.SysFont("Segoe Print", 18, True)
        self.value = value

    def draw(self, level):
        xcam = level.camera.rect.left
        ycam = level.camera.rect.top
        screen = pygame.display.get_surface()
        label = self.screenfont.render(self.value, 1, (255, 255, 255))
        screen.blit(label, self.position.move(-xcam, -ycam))

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdateframe > 2000:
            print "removed"
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

    def action(self, level, ticks):
        range = self.range[1] - self.range[0]
        delta = min(range, abs(self.position.y - self.range[0]))
        scoring = (range - delta)*100/range
        text = Text(level.imageSprites, self.position.left, self.range[0] - 50, "{} !".format(scoring))
        level.toptopobjects.append(text)
        if scoring < 50:
            level.playsound('level-complete-low')
        if scoring >= 90:
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


class Cloud(Drawable):
    def __init__(self, assetfile, x, y, speed):
        Drawable.__init__(self, assetfile, x, y, 134, 66, 1, 0, 665)
        self.lastupdate = pygame.time.get_ticks()
        self.speed = -speed
        self.opacity = random.randint(50, 220)

    def update(self, level):
        ticks = pygame.time.get_ticks()
        if ticks - self.lastupdate > 1/self.speed*100:
            self.position = self.position.move(self.speed, 0)
            self.lastupdate = ticks
            if self.position.right < 0:
                self.position.left = max(level.mario.position.right,level.camera.rect.width/2)  + level.camera.rect.width/2
                speed = random.randint(1, 2)
                self.position.top = random.randint(-50, 250)

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def draw(self, level):
        self.surface.blit(self.image, (0, 0), (self.frame*self.position.width + self.blitx, self.blity, self.position.width, self.position.height))
        xcam = level.camera.rect.left
        ycam = level.camera.rect.top
        screen = pygame.display.get_surface()
        self.blit_alpha(screen, self.surface, self.position.move(-xcam, -ycam), self.opacity)

