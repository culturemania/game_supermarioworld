__author__ = 'ESTEBAN'

from level import *
from pygame import event
from object import *
from tools import Message
from save import GameData, Save

FPS = 60

TILESIZE = 16
MAPWIDTH = 96
MAPHEIGHT = 30
VOID = 0
GRASS = 1
GROUND = 2


class Game:
    def __init__(self):
        print "__init__ Game"
        pygame.mixer.init(44100, -16, 1, 1024)
        pygame.init()
        self.width = 640
        self.height = 480
        self.levelidx = 0
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Super Mario World")
        self.running = True
        self.mariolifes = 3
        self.state = State()
        self.fond = None
        self.levels = []
        self.imageMario = pygame.image.load("game\\assets\\sprites\\mario.bmp").convert_alpha()
        self.menu = MainMenu(self, "")
        self.curlevel = None
        self.slot = None

    def save(self):
        data = GameData()
        data.levelidx = self.levelidx
        data.coins = self.mario.coins
        data.life = self.mario.life
        s = Save()
        s.save(data, self.slot)

    def initfrommenu(self, lifes, levelidx):
        self.mario.life = lifes
        self.curlevel = levelidx

    def load(self, slot, startlevel=False):
        self.slot = slot
        s = Save()
        data = s.load(slot)
        if data is None:
            self.levelidx = 0
        else:
            self.levelidx = data.levelidx

        if startlevel:
            self.startlevel(self.levelidx, True)
        return data

    def start(self):
        print "Stating Super Mario World"
        self.mario = Mario(self.imageMario, 50, 200, 16, 22, 9)
        self.mario.life = 3
        self.menu.loadcontent()
        pygame.key.set_repeat(1, 25)
        clock = pygame.time.Clock()
        self.levels.append(DonutPlain00(self, "donutplain00"))
        self.levels.append(HauntedHouse01(self, "hauntedhouse01"))

        self.levels.append(DonutPlain00(self, "donutplain02"))
        self.levels.append(Castle01(self, "castle01"))

        self.levels.append(WorldMap(self, "worldmap"))

        self.showmenu()

        while self.running is True:
            self.update()
            self.draw()
            clock.tick(FPS)

        pygame.mixer.quit()
        pygame.quit()

    def update(self):
        if self.curlevel.running:
            res = self.curlevel.update()
            if res is Message.TERMINATELEVEL:
                self.curlevel.end()
                self.startlevel(self.levelidx+1, True)
        else:
            self.running = False

    def startlevel(self, idx, transition=False):
        print "start level {}".format(idx)
        self.levelidx = idx
        if transition is True:
            # Transition
            ticks = pygame.time.get_ticks()
            now = ticks
            while (now - ticks) < 500:
                for localevent in event.get():
                    if localevent.type == pygame.QUIT:
                        self.running = False
                self.state.drawtransition(self)
                now = pygame.time.get_ticks()

        self.curlevel = self.levels[self.levelidx]
        self.curlevel.start(self.mario)

    def tomainmenu(self):
        self.hidemenu()
        self.levels[self.levelidx].end()
        self.showmenu(False)

    def draw(self):
        if self.curlevel.running:
            self.curlevel.draw(self)

    def stop(self):
        self.running = False

    def showmenu(self, ingame=False):
        self.menu.cursel = 0
        self.menu.curmenu = 0
        self.menu.ingame = ingame
        self.curlevel = self.menu

    def hidemenu(self):
        self.curlevel = self.levels[self.levelidx]



