from BattleCity import BattleCity as Game
from menu import Menu
import pygame
from pygame.locals import *
class BattleCity:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('坦克大战')


        self.width = 1366
        self.height = 768  # 屏幕大小
        self.bgSize = (self.width,self.height)
        self.screen = pygame.display.set_mode(self.bgSize, FULLSCREEN | HWSURFACE)  # 全屏

        self.menu = Menu(self.screen)
        self.game = Game(self.screen)

    def run(self):
        config = self.menu.run()
        self.game.setConfig(config)
        self.game.run()


if __name__ == '__main__':
    main = BattleCity()
    main.run()
    # try:
    #     main.run()
    # except SystemExit:
    #     pass
    # except Exception as e:
    #     print(e)

