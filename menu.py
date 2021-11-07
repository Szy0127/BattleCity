from pygame.locals import *
import pygame
import sys

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
class Menu:
    def __init__(self,screen = None):


        self.width = 1200
        self.height = 680  # 屏幕大小
        self.bgSize = (self.width,self.height)
        self.choose = 0 # 0 1 2 3 主界面 4 5 help1 6 7 help2
        if screen:
            self.screen = screen
            self.close = False
        else:
            self.close = True
            pygame.init()
            pygame.display.set_caption('菜单')
            self.screen = pygame.display.set_mode(self.bgSize,  FULLSCREEN | HWSURFACE)  # 全屏
        self.bgColor = BLACK
        self.help = 0
        self.music = False
        self.senoir = False

        self.skill = ['隐身','无敌','下发子弹一击必杀']
        self.key1 = 'FGH'
        self.key2 = 'IOP'
        self.wall = pygame.image.load('image/wall.png')
        self.tank = pygame.image.load('image/tank2Right.png')
        self.target = pygame.image.load('image/target.png')
        self.mapItems = ['wall','steel','grass','water']
        self.mapItemExplain = ['子弹可破坏','仅强化子弹可破坏','伪装','子弹可穿越']
        self.mapImages = [pygame.image.load(f'image/{itemType}.png') for itemType in self.mapItems]

        self.propItems = ['star','cross','circle1']
        self.propItemsExplain = ['强化子弹','加血','加速']
        self.propImages = [pygame.image.load(f'image/{itemType}.png') for itemType in self.propItems]

        self.playerItems = ['tank1Up','tank2Up']
        self.playerItemExplain = ['WASD移动\n空格发射子弹','上下左右移动\n回车发射子弹']
        self.playerImages = [pygame.image.load(f'image/{itemType}.png') for itemType in self.playerItems]

    def printmessage(self,message, color, size, location):
        font = pygame.font.SysFont('SimHei', size)
        message = font.render(message, True, color)
        self.screen.blit(message, location)

    def drawWall(self,x,y):
        rect = self.wall.get_rect()
        rect.left,rect.top = x,y
        self.screen.blit(self.wall, rect)
    def drawTank(self,x,y):
        rect = self.wall.get_rect()
        rect.left,rect.top = x,y
        self.screen.blit(self.tank, rect)

    def drawB(self,beginx,beginy):
        for i in range(5):
            self.drawWall(beginx,beginy+i*30)
        for i in range(3):
            for j in range(3):
                self.drawWall(beginx+(j+1)*30,beginy+i*60)
        self.drawWall(beginx + 3 * 30 + 15, beginy + 30)
        self.drawWall(beginx + 3 * 30 + 15, beginy + 90)

    def drawA(self,beginx,beginy):
        self.drawWall(beginx , beginy)
        self.drawWall(beginx+30, beginy)
        self.drawWall(beginx-15, beginy+30)
        self.drawWall(beginx+45, beginy+30)
        for i in range(3):
            self.drawWall(beginx - 30, beginy + (i+2) * 30)
            self.drawWall(beginx + 60, beginy + (i+2) * 30)
        self.drawWall(beginx , beginy + 90)
        self.drawWall(beginx + 30 , beginy + 90)

    def drawT(self,beginx,beginy):
        for i in range(4):
            self.drawWall(beginx + i * 30, beginy)
            self.drawWall(beginx + 45, beginy + (i+1)*30)

    def drawL(self,beginx,beginy):
        for i in range(4):
            self.drawWall(beginx , beginy + i * 30)
            self.drawWall(beginx + i*30, beginy + 120)
    def drawE(self,beginx,beginy):
        for i in range(5):
            self.drawWall(beginx,beginy+i*30)
        for i in range(3):
            for j in range(3):
                self.drawWall(beginx+(j+1)*30,beginy+i*60)

    def drawC(self,beginx,beginy):
        for i in range(3):
            self.drawWall(beginx + i * 30, beginy)
            self.drawWall(beginx + i * 30, beginy + 120)
        for i in range(2):
            self.drawWall(beginx - (i + 1) * 15, beginy + (i + 1) * 30)
        self.drawWall(beginx - 15 ,beginy + 90)
        self.drawWall(beginx + 75 , beginy + 15)
        self.drawWall(beginx + 75, beginy + 105)

    def drawI(self,beginx,beginy):
        for i in range(4):
            self.drawWall(beginx + i * 30, beginy )
            self.drawWall(beginx + i * 30, beginy + 120)
        for i in range(3):
            self.drawWall(beginx + 45, beginy + (i+1)*30)

    def drawY(self,beginx,beginy):
        for i in range(2):
            self.drawWall(beginx + 45, beginy + i*30)
            self.drawWall(beginx - 45, beginy + i * 30)
        for i in range(3):
            self.drawWall(beginx + (i-1)*30, beginy + 60)
        for i in range(2):
            self.drawWall(beginx , beginy + (i+3)*30)
    def draw(self):
        if self.help == 1:
            #self.printmessage('?',YELLOW, 70, (self.width - 35, 0))
            x = 50
            y = 180
            self.printmessage('地图元素',WHITE,40,(x,y-70))
            for i in range(len(self.mapImages)):
                image = self.mapImages[i]
                image = pygame.transform.scale(image,(75,75))
                rect = image.get_rect()
                rect.left, rect.top = x,y
                self.screen.blit(image,rect)
                self.printmessage(self.mapItemExplain[i],WHITE,30,(x+100,y+20))
                y += 120
            x = 380
            y = 180
            self.printmessage('道具', WHITE, 40, (x, y - 70))
            for i in range(len(self.propImages)):
                image = self.propImages[i]
                image = pygame.transform.scale(image,(75,75))
                rect = image.get_rect()
                rect.left, rect.top = x,y
                self.screen.blit(image,rect)
                self.printmessage(self.propItemsExplain[i],WHITE,30,(x+100,y+20))
                y += 150

            x = 660
            y = 180
            self.printmessage('玩家', WHITE, 40, (x, y - 70))
            for i in range(len(self.playerImages)):
                image = self.playerImages[i]
                image = pygame.transform.scale(image, (75, 75))
                rect = image.get_rect()
                rect.left, rect.top = x, y
                self.screen.blit(image, rect)
                self.printmessage(self.playerItemExplain[i].split()[0], WHITE, 30, (x + 100, y ))
                self.printmessage(self.playerItemExplain[i].split()[1], WHITE, 30, (x + 100, y + 50))
                y += 160

            x = 1000
            y = 180
            self.printmessage('胜利条件', WHITE, 40, (x, y - 70))
            image = self.target
            image = pygame.transform.scale(image, (100, 75))
            rect = image.get_rect()
            rect.left,rect.top = x,y
            self.screen.blit(image,rect)
            y += 180
            self.printmessage('击毁敌方基地', WHITE, 30, (x, y - 70))
            y += 50
            self.printmessage('双方基地各5条命', WHITE, 30, (x, y - 70))
            y += 50
            self.printmessage('每损失一条敌方坦克扣血', WHITE, 30, (x, y - 70))

            x = self.width - 80
            y = self.height
            self.printmessage('下一页',WHITE,50,(x,y))
            self.printmessage('返回主菜单', WHITE, 50, (120, y))
            if self.choose == 4:
                self.drawTank(30, y)
            elif self.choose == 5:
                self.drawTank(x - 100, y)

        elif self.help == 2:
            self.printmessage('高级模式',WHITE,60,(50,50))
            self.printmessage('按下对应按键使用技能，每局限3次，无提示与记录', WHITE, 40, (200, 550))
            x1 = 400
            x2 = x1 + 200
            x3 = x2 + 200
            self.printmessage('玩家1', WHITE, 50, (x1, 150))
            self.printmessage('玩家2', WHITE, 50, (x2, 150))
            self.printmessage('技能', WHITE, 50, (x3, 150))
            for i in range(len(self.skill)):
                y = 250 + i * 80
                self.printmessage(self.key1[i], WHITE, 50, (x1, y))
                self.printmessage(self.key2[i], WHITE, 50, (x2, y))
                self.printmessage(self.skill[i], WHITE, 50, (x3, y))
            y = self.height
            self.printmessage('上一页', WHITE, 50, (100, y))
            x = self.width - 100
            self.printmessage('返回主菜单', WHITE, 50, (x, y))
            if self.choose == 6:
                self.drawTank(30, y)
            elif self.choose == 7:
                self.drawTank(x-80,y)
        else:

            y = 50
            x = 220
            self.drawB(x,y)
            x += 220
            self.drawA(x,y)
            x += 120
            self.drawT(x,y)
            x += 170
            self.drawT(x,y)
            x += 170
            self.drawL(x,y)
            x += 170
            self.drawE(x,y)
            x = 400
            y = 250
            self.drawC(x,y)
            x += 170
            self.drawI(x,y)
            x += 170
            self.drawT(x,y)
            x += 220
            self.drawY(x,y)
            self.printmessage('开始游戏', WHITE, 70, (520,450))
            self.printmessage('游戏说明', WHITE, 70, (520,570))
            self.printmessage('游戏音效：', WHITE, 50, (150, 650))
            if self.music:
                self.printmessage('开', WHITE, 50, (400, 650))
            else:
                self.printmessage('关', WHITE, 50, (400, 650))
            self.printmessage('高级模式：', WHITE, 50, (950, 650))
            if self.senoir:
                self.printmessage('开', WHITE, 50, (1200, 650))
            else:
                self.printmessage('关', WHITE, 50, (1200, 650))
            #self.printmessage('?', BLACK, 70, (self.width - 35, 0))
            if self.choose == 0:
                self.drawTank(420,450)
            elif self.choose == 1:
                self.drawTank(420,570)
            elif self.choose == 2:
                self.drawTank(50, 650)
            elif self.choose == 3:
                self.drawTank(850, 650)

    def choose0(self):
        self.choose = 0
        return self.music, self.senoir

    def choose1(self):
        self.help = 1
        self.choose = 5
    def choose2(self):
        self.choose = 2
        self.music = not self.music
    def choose3(self):
        self.choose = 3
        self.senoir = not self.senoir
    def choose4(self):
        self.choose = 1
        self.help = 0
    def choose5(self):
        self.help = 2
        self.choose = 6
    def choose6(self):
        self.choose = 5
        self.help = 1
    def choose7(self):
        self.choose4()

    def run(self):
        # 设置帧率
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # Esc键退出
                        if self.help:
                            self.choose4()
                        else:
                            pygame.quit()
                            sys.exit()
                    elif event.key == K_RETURN:
                        if self.help == 0:
                            if self.choose == 1:
                                self.choose1()
                            elif self.choose == 2:
                                self.choose2()
                            elif self.choose == 3:
                                self.choose3()
                            elif self.choose == 0:
                                return self.choose0()
                        elif self.help == 1:
                            if self.choose == 4:
                                self.choose4()
                            elif self.choose == 5:
                                self.choose5()
                        elif self.help == 2:
                            if self.choose == 6:
                                self.choose6()
                            elif self.choose == 7:
                                self.choose7()

                    elif event.key == K_UP:
                        self.choose = (self.choose - 1) % 4
                        if self.choose == 2:
                            self.choose = 1
                    elif event.key == K_DOWN:
                        self.choose = (self.choose + 1) % 4
                        if self.choose == 3:
                            self.choose = 0
                    elif event.key == K_LEFT:
                        if self.help == 0:
                            if self.choose == 2:
                                self.choose = 3
                            else:
                                self.choose = 2
                        elif self.help == 1:
                            self.choose = 9-self.choose
                        elif self.help == 2:
                            self.choose = 13-self.choose
                    elif event.key == K_RIGHT:
                        if self.help == 0:
                            if self.choose == 3:
                                self.choose = 2
                            else:
                                self.choose = 3
                        elif self.help == 1:
                            self.choose = 9 - self.choose
                        elif self.help == 2:
                            self.choose = 13 - self.choose



                if event.type == MOUSEBUTTONUP:
                    x,y = event.pos
                    if self.help == 1:
                        if y > 650:
                            if x < 350:
                                self.choose4()
                            elif x > 1100:
                                self.choose5()
                    elif self.help == 2:
                        if y > 650:
                            if x < 350:
                                self.choose6()
                            elif x > 1100:
                                self.choose7()

                    else:
                        if 500 < x < 800 :
                            if 450 < y < 530:
                                return self.choose0()
                            elif 560 < y < 650:
                                self.choose1()
                        if 650 < y < 750:
                            if 150 < x < 450:
                                self.choose2()
                            elif 950 < x < 1250:
                                self.choose3()
                    # else:
                    #     if self.close:
                    #         pygame.quit()
                    #     return
                        #sys.exit()


            # 填充背景 准备绘制游戏画面
            self.screen.fill(self.bgColor)
            self.draw()
            # 内存 -> 屏幕
            pygame.display.flip()
            # 设置帧率为40帧
            clock.tick(40)

if __name__ == '__main__':
    menu = Menu()
    menu.run()