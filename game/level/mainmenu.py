__author__ = 'ESTEBAN'
from level import Level
import pygame
from pygame.locals import *
from pygame import event


STARTNEWGAME = 0
RESUMEGAME = 0
LOADGAME = 1
SAVEGAME = 2
OPTIONS = 3
EXITGAME = 4



class MainMenu(Level):
    def __init__(self, game, name):
        Level.__init__(self, game, name)
        self.speed = 1
        self.name = None
        self.options = []
        self.menu = []
        self.cursel = 0
        self.curmenu = 0
        self.lastkeys = pygame.key.get_pressed()
        self.nblives = 3
        self.difficulty = []
        self.curdifficulty = 0
        self.ingame = False
        self.menuingame = []

    def start(self, nblifes):
        self.running = True
        self.loadcontent()

    def loadcontent(self):
        self.imagelogo = pygame.image.load("game\\assets\\sprites\\logo.bmp").convert_alpha()
        self.surfacelogo = pygame.Surface((194, 66))
        self.surfacelogo .set_colorkey(Color(255, 0, 255, 255), RLEACCEL)
        self.surfacelogo.blit(self.imagelogo, (0, 0), (0, 0, 194, 66))
        self.screenfont = pygame.font.SysFont("Quartz MS", 14, True)

        self.menu.append("Start New Game...")
        self.menu.append("Load Game...")
        self.menu.append("Save Game...")
        self.menu.append("Options...")
        self.menu.append("Exit Super Mario")

        self.menuingame.append("Resume Game...")
        self.menuingame.append("Save Game...")
        self.menuingame.append("Exit Super Mario")

        self.options.append("Lives : {}")
        self.options.append("Difficulty : {}")
        self.options.append("OK")

        self.difficulty.append("Easy")
        self.difficulty.append("Normal")
        self.difficulty.append("Hard")
        self.difficulty.append("Nightmare")

    def unloadcontent(self):
        print "unloadcontent"
        Level.unloadcontent(self)
        del self.menu[:]
        del self.options[:]
        del self.difficulty[:]

    def update(self):
        event.get()
        keys = pygame.key.get_pressed()
        if keys is None:
            print "NONE"
        print len(keys)

        if self.ingame is True:
            if keys[K_RETURN] and not self.lastkeys[K_RETURN]:
                if self.cursel == RESUMEGAME:
                    self.game.hidemenu()
                elif self.cursel == SAVEGAME:
                    self.game.save()
                    self.game.hidemenu()
                elif self.cursel == EXITGAME:
                    self.running = False
            elif keys[K_DOWN] and not self.lastkeys[K_DOWN]:
                self.cursel = min(self.cursel+1, len(self.menuingame)-1)
            elif keys[K_UP] and not self.lastkeys[K_UP]:
                self.cursel = max(self.cursel-1, 0)
        else:
            if self.curmenu == 0:
                #Page principale
                if keys[K_RETURN] and not self.lastkeys[K_RETURN]:
                    if self.cursel == EXITGAME:
                        self.running = False
                    elif self.cursel == STARTNEWGAME:
                        self.game.mariolifes = self.nblives
                        self.game.startlevel(0, True)
                    elif self.cursel == LOADGAME:
                        self.game.load()
                        self.game.startlevel(self.game.levelidx, True)
                    elif self.cursel == SAVEGAME:
                        self.game.save()
                        self.game.startlevel(self.game.levelidx, True)
                    elif self.cursel == OPTIONS:
                        self.curmenu = 1
                        self.cursel = 0
                if keys[K_DOWN] and not self.lastkeys[K_DOWN]:
                    self.cursel = min(self.cursel+1, len(self.menu)-1)
                elif keys[K_UP] and not self.lastkeys[K_UP]:
                    self.cursel = max(self.cursel-1, 0)
            else:
                #Page option
                if keys[K_RETURN] and not self.lastkeys[K_RETURN]:
                    if self.cursel == 2:
                        self.curmenu = 0
                        self.cursel = 0
                if keys[K_DOWN] and not self.lastkeys[K_DOWN]:
                    self.cursel = min(self.cursel+1, len(self.options)-1)
                elif keys[K_UP] and not self.lastkeys[K_UP]:
                    self.cursel = max(self.cursel-1, 0)
                elif keys[K_RIGHT] and not self.lastkeys[K_RIGHT]:
                    if self.cursel == 0:
                        self.nblives = min(10, self.nblives + 1)
                    elif self.cursel == 1:
                        self.curdifficulty = min(3, self.curdifficulty + 1)
                elif keys[K_LEFT] and not self.lastkeys[K_LEFT]:
                    if self.cursel == 0:
                        self.nblives = max(1, self.nblives - 1)
                    elif self.cursel == 1:
                        self.curdifficulty = max(0, self.curdifficulty - 1)

        self.lastkeys = keys

    def draw(self, game):
        screen = pygame.display.get_surface()
        if self.ingame is False:
            screen.fill((0, 0, 0))
        else:
            screen.fill((20, 20, 20))

        screen.blit(self.surfacelogo, (game.width/2-self.surfacelogo.get_width()/2, 100))
        label = None
        if self.ingame is True:
            for i in range(0, len(self.menuingame)):
                if i == self.cursel:
                    label = self.screenfont.render(self.menuingame[i], 1, (255, 255, 255))
                else:
                    label = self.screenfont.render(self.menuingame[i], 1, (150, 150, 150))
                screen.blit(label, (250, 200 + i*32))
        else:
            if self.curmenu == 0:
                for i in range(0, len(self.menu)):
                    if i == self.cursel:
                        label = self.screenfont.render(self.menu[i], 1, (255, 255, 255))
                    else:
                        label = self.screenfont.render(self.menu[i], 1, (150, 150, 150))
                    screen.blit(label, (250, 200 + i*32))
            else:

                for i in range(0, len(self.options)):
                    text = self.options[i]
                    if i == 0:
                        text = self.options[i].format(self.nblives)
                    elif i == 1:
                        text = self.options[i].format(self.difficulty[self.curdifficulty])
                    if i == self.cursel:
                        label = self.screenfont.render(text, 1, (255, 255, 255))
                    else:
                        label = self.screenfont.render(text, 1, (150, 150, 150))
                    screen.blit(label, (250, 200 + i*32))

        pygame.display.flip()
