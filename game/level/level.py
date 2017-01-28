__author__ = 'ESTEBAN'

from pygame import event
from pygame.constants import *
from pygame.locals import Color
from game.camera import Camera
from game.object import *
from datetime import datetime
from game.factory import Factory
import os
import csv

FPS = 60

TILESIZE = 16
VOID = 0
GRASS = 1
GROUND = 2

class LevelState():
    RUNNING = 0
    TERMINATING = 1


class Level:
    def __init__(self, game, name):
        self.objects = []
        self.topobjects = []
        self.toptopobjects = []
        self.ennemies = []
        self.bonuses = []
        self.platforms = []
        self.blocks = []
        self.camera = Camera(0, 0, game.width, game.height)
        self.imageMario = None
        self.imageAssets = None
        self.imageCloud = None
        self.imageBush = None
        self.imageSprites = None
        self.imageTiles = None
        self.state = State()
        self.running = True
        self.fond = None
        self.game = game
        self.name = name
        self.starttime = datetime.utcnow()
        self.timelimit = 100
        self.tilemap = []
        self.sounds = {}
        self.ytile = 0
        self.bgcolor = (0, 0, 0)
        self.lastkeys = None
        self.mario = None
        self.levelState = LevelState.RUNNING
        self.timeevent = pygame.time.get_ticks()
        self.opacityend = 0

    def playsound(self, key):
        self.sounds[key].play()

    def initmap(self):
        if self.name is not None:
            with open('game\\assets\\levels\\{}.csv'.format(self.name), 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    line = []
                    for i in range(0, len(row)):
                        if len(row[i]) == 0:
                            row[i] = '0'
                        line.append(int(row[i]))
                    self.tilemap.append(line)

    def istileground(self, value):
        grounds = [1, 2, 3, 8, 9, 14, 15, 24, 25, 26, 27]
        return value in grounds

    def istileblock(self, value):
        blocks = [8, 9, 10, 11, 14, 24, 25, 26]
        return value in blocks

    def istilebonus(self, value):
        return -100 <= value < 0

    def istileennemy(self, value):
        return -1000 <= value < -100

    def istileasset(self, value):
        return value < -1000

    def loadimage(self):
        print "Loading Level"

        self.imageSprites = pygame.image.load("game\\assets\\sprites\\sprites.bmp").convert_alpha()
        self.imageSprites.set_alpha(120)

        self.imageTiles = pygame.image.load("game\\assets\\sprites\\tiles.bmp").convert_alpha()
        self.surfacetile = pygame.Surface((16, 16))
        self.surfacetile.set_colorkey(Color(255, 0, 255, 255), RLEACCEL)

    def reset(self):
        self.mario.position.x = 0
        self.mario.position.y = 0
        self.mario.energy = 5
        self.camera.rect.x = 0
        self.camera.rect.y = 0
        self.starttime = datetime.utcnow()

    def unloadcontent(self):
        print "unload"
        del self.objects[:]
        del self.topobjects[:]
        del self.toptopobjects[:]
        del self.ennemies[:]
        del self.blocks[:]
        del self.bonuses[:]
        del self.platforms[:]
        del self.tilemap[:]
        self.sounds.clear()

    def end(self):
        self.running = False

        self.unloadcontent()

    def start(self, mario):
        self.mario = mario
        self.mario.position.left = 0
        self.mario.position.top = 0
        self.initmap()
        self.loadimage()
        self.loadcontent()
        self.starttime = datetime.utcnow()
        self.running = True
        musicfilepath = "game\\assets\\musics\\{}.mp3".format(self.name)
        if os.path.exists(musicfilepath):
            pygame.mixer.music.load(musicfilepath)
            pygame.mixer.music.play()

    def loadcontent(self):
        print "Load"
        self.loadtilemap()
        self.sounds['yellowcoin'] = pygame.mixer.Sound("game\\assets\\sounds\\coin.wav")
        self.sounds['dragoncoin'] = pygame.mixer.Sound("game\\assets\\sounds\\smw_dragon_coin.wav")
        self.sounds['turtle'] = pygame.mixer.Sound("game\\assets\\sounds\\smw_stomp.wav")
        self.sounds['mariojump'] = pygame.mixer.Sound("game\\assets\\sounds\\smw_jump.wav")
        self.sounds['cough'] = pygame.mixer.Sound("game\\assets\\sounds\\cough.wav")
        self.sounds['level-complete'] = pygame.mixer.Sound("game\\assets\\sounds\\level-complete.wav")

    def loadtilemap(self):
        f = Factory()
        for row in range(len(self.tilemap)):
            for column in range(len(self.tilemap[0])):
                position = pygame.Rect(column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE)
                value = self.tilemap[row][column]
                if self.istileground(value):
                    self.platforms.append(Plateform(position, value))
                if self.istileblock(value):
                    self.blocks.append(position)
                if self.istilebonus(value):
                    obj = f.buildobject(self.imageSprites, value, position.x, position.y)
                    if obj is not None:
                        self.objects.append(obj)
                        self.bonuses.append(obj)
                if self.istileennemy(value):
                    obj = f.buildobject(self.imageSprites, value, position.x, position.y)
                    if obj is not None:
                        self.objects.append(obj)
                        self.ennemies.append(obj)
                if self.istileasset(value):
                    obj = f.buildobject(self.imageSprites, value, position.x, position.y)
                    if obj is not None:
                        self.objects.append(obj)
                if value == -7:
                    obj = BlockCoin(self.imageSprites, position.x, position.y)
                    self.objects.append(obj)
                    self.platforms.append(Plateform(obj.position, 1))
                    self.bonuses.append(obj)
                    self.blocks.append(obj.position)


    def update(self):
        ticks = pygame.time.get_ticks()
        if self.levelState == LevelState.TERMINATING:
            self.mario.frame = 10
            self.opacityend = min (255, self.opacityend + 6)
            pygame.mixer.music.stop()
            if (ticks - self.timeevent) > 2000:
                return Message.TERMINATELEVEL
            return

        for localevent in event.get():
            if localevent.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[K_RETURN] and not self.lastkeys[K_RETURN]:
            self.game.showmenu(True)
        if keys[K_ESCAPE]:
            self.screen = pygame.display.set_mode((self.camera.rect.width, self.camera.rect.height))
        if keys[K_LALT] and keys[K_RETURN]:
            self.screen = pygame.display.set_mode((self.camera.rect.width, self.camera.rect.height), FULLSCREEN)

        self.lastkeys = keys

        for obj in self.objects:
            if not obj.isalive and obj.inscreen(self):
                obj.isalive = True
        for obj in self.topobjects:
            if not obj.isalive and obj.inscreen(self):
                obj.isalive = True

        for obj in self.objects:
            if obj.isalive:
                obj.update(self)

        for obj in self.topobjects:
            if obj.isalive:
                obj.update(self)

        for obj in self.toptopobjects:
            if obj.isalive:
                obj.update(self)


        res = self.mario.update(self)
        if res is Message.TERMINATELEVEL:
            self.levelState = LevelState.TERMINATING
            self.timeevent = pygame.time.get_ticks()

        self.updatecamera()

    def updatecamera(self):
        y = self.mario.position.bottom + self.camera.rect.height/2
        if y < len(self.tilemap) * TILESIZE:
            self.camera.setcentery(max(self.camera.rect.height/2, self.mario.position.bottom))

        if self.mario.position.left >= self.camera.rect.width/2 and self.mario.position.right < (len(self.tilemap[0])+1) * TILESIZE - self.camera.rect.width / 2:
            x = self.mario.position.left
            self.camera.setcenterx(x)

    def drawtilemap(self, game):
        xcam = self.camera.rect.left
        ycam = self.camera.rect.top
        idxX = xcam / TILESIZE
        idxY = ycam / TILESIZE
        for row in range(idxY, idxY + self.camera.rect.height/TILESIZE + 1):
            if 0 <= row < len(self.tilemap):
                for column in range(idxX, idxX + self.camera.rect.width/TILESIZE + 1):
                    if column < len(self.tilemap[row]):
                        value = self.tilemap[row][column]
                        if value > VOID:
                            position = pygame.Rect(column * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE)
                            self.surfacetile.blit(self.imageTiles, (0, 0), ((value-1) * TILESIZE, self.ytile, TILESIZE, TILESIZE))
                            game.screen.blit(self.surfacetile, position.move(-xcam, -ycam))

    def draw(self, game):
        if self.running:
            self.drawtilemap(game)
            for obj in self.objects:
                if obj.inscreen(self):
                    obj.draw(self)
            self.mario.draw(self)

            for obj in self.topobjects:
                if obj.inscreen(self):
                    obj.draw(self)

            self.state.draw(self)
            if self.levelState == LevelState.TERMINATING:
                rect = pygame.Surface((640, 480), pygame.SRCALPHA, 32)
                rect.fill((0, 0, 0, self.opacityend))
                screen = pygame.display.get_surface()
                screen.blit(rect, (0, 0))
                self.mario.draw(self)
                for obj in self.toptopobjects:
                    if obj.inscreen(self):
                        obj.draw(self)

            pygame.display.flip()
