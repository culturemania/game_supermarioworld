__author__ = 'ESTEBAN'
import pickle


class GameData:
    def __init__(self):
        self.levelidx = 0
        self.life = 0
        self.coins = 0


class Save:
    def __init__(self):
        pass

    def save(self, data, slot):
        with open("savedata{}.dat".format(slot), "wb") as file:
            pickle.dump(data, file)

    def load(self, slot):
        data = None
        try:
            with open("savedata{}.dat".format(slot), "rb") as file:
                data = pickle.load(file)
        except Exception as err:
            print err.message
        finally:
            return data

