__author__ = 'ESTEBAN'
from object import *


class TileValue:
    YELLOWCOIN = -1
    GREENCOIN = -2
    REDCOIN = -3
    YOSHICOIN = -5
    MUSHROOM = -6
    BLOCKCOIN = -7

    TORTOISE = -101
    TORTOISEJUMP = -102
    GOOMBA = -103
    DRAGON = -104

    BIGBUSH = -1001
    CASTLE = -1002


class Factory:

    def __init__(self):
        print "Factory"

    @staticmethod
    def buildobject(imageSprites, tilevalue, x, y):
        obj = None
        if tilevalue == TileValue.YELLOWCOIN:
            obj = YellowCoin(imageSprites, x, y)
        elif tilevalue == TileValue.GREENCOIN:
            obj = GreenCoin(imageSprites, x, y)
        elif tilevalue == TileValue.REDCOIN:
            obj = RedCoin(imageSprites, x, y)
        elif tilevalue == TileValue.YOSHICOIN:
            obj = YoshiCoin(imageSprites, x, y)
        elif tilevalue == TileValue.MUSHROOM:
            obj = Mushroom(imageSprites, x, y)
        elif tilevalue == TileValue.BIGBUSH:
            obj = Asset(imageSprites, x, y, 144, 80, 0, 324)
        elif tilevalue == TileValue.CASTLE:
            obj = Asset(imageSprites, x, y, 94, 80, 0, 404)
        elif tilevalue == TileValue.TORTOISE:
            obj = Tortoise(imageSprites, x, y)
        elif tilevalue == TileValue.GOOMBA:
            obj = Goomba(imageSprites, x, y)
        elif tilevalue == TileValue.TORTOISEJUMP:
            obj = TortoiseJumpy(imageSprites, x, y)
        elif tilevalue == TileValue.DRAGON:
            obj = Dragon(imageSprites, x, y)

        return obj

