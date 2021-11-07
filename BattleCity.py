import pygame
import sys
import traceback
from tank import *
import threading
import mymap
import pickle
from pygame.locals import *

# 定义颜色
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
bgColor = (80, 80, 80)
#bgColor = BLACK
fontColor = (253, 3, 27)
fontColor2 = (0, 255, 255)


class BattleCity:
    SKILL_HIDE = [K_f, K_i]
    SKILL_DEFEND = [K_g,K_o]
    SKILL_KILL = [K_h,K_p]
    SHOOT = [K_SPACE,K_RETURN]
    def __init__(self,screen = None):


        self.width = 1366
        self.height = 768  # 屏幕大小
        self.bgSize = (self.width,self.height)


        if screen:
            self.screen = screen
        else:
            pygame.init()
            pygame.mixer.init()
            pygame.display.set_caption('坦克大战')
            self.screen = pygame.display.set_mode(self.bgSize, FULLSCREEN | HWSURFACE)  # 全屏


        self.musicClose = False
        self.gameOver = False  # 游戏是否结束
        self.winner = False  # 胜利玩家

        # 生成地图
        self.mapUsed = mymap.Map(self.bgSize, 1)

        # 生成坦克
        self.player = []
        self.player.append(Tank(self.bgSize, DOWN, (self.width * 0.05, self.height * 0.1), 1))
        self.player.append(Tank(self.bgSize, UP, (self.width * 0.9, self.height * 0.85), 2))



    def setConfig(self,config):
        self.music,self.senior = config
        if self.music:
            self.loadSounds()

    def loadSounds(self):
        # 背景音乐
        pygame.mixer.music.load('sound/bgMusic.ogg')
        pygame.mixer.music.set_volume(0.2)
        # 子弹发射音效
        self.bulletSound = pygame.mixer.Sound('sound/bullet.wav')
        self.bulletSound.set_volume(0.3)
        # 捡十字音效
        self.crossSound = pygame.mixer.Sound('sound/cross.wav')
        self.crossSound.set_volume(0.3)
        # 捡道具音效
        self.supplySound = pygame.mixer.Sound('sound/supply.wav')
        self.supplySound.set_volume(0.3)
        # 玩家死亡音效
        self.dieSound = pygame.mixer.Sound('sound/die.wav')
        self.dieSound.set_volume(0.4)



    def gameReset(self):
        self.map = mymap.Map(self.bgSize, 1)

        for tank in self.player:
            tank.reset()
            tank.win = False

        return self.map


    def printmessage(self,message, color, size, location):
        font = pygame.font.Font(None, size)
        message = font.render(message, True, color)
        self.screen.blit(message, location)


    def draw(self, choice):
        me = self.player[choice]
        enemy = self.player[not choice]

        # 避免游戏结束后出现子弹及重复死亡画面
        if not self.gameOver:
            # 画子弹
            for bullet in me.bullets:
                # 移动并返回是否依然存在
                if bullet.move(self.mapUsed, enemy):
                    self.screen.blit(bullet.image[bullet.face], bullet.rect)
                else:
                    me.bullets.remove(bullet)

            # 画坦克及血槽
            if me.life >=0:
                if me.hide == 0:
                    self.screen.blit(me.image[me.face], me.rect)
                    pygame.draw.line(self.screen, BLACK, \
                                     (me.rect.left, me.rect.top - 5), \
                                     (me.rect.right, me.rect.top - 5), 4)
                    if me.life / Tank.LIFE > 0.2:
                        color = GREEN
                    else:
                        color = RED
                    pygame.draw.line(self.screen, color, \
                                     (me.rect.left, me.rect.top - 5), \
                                     (me.rect.left + me.rect.width * me.life \
                                      / Tank.LIFE, me.rect.top - 5), 4)

            # 双方重合时敌方死亡(复活后的bug)
            if pygame.sprite.spritecollide(me, pygame.sprite.Group(enemy), \
                                           False, pygame.sprite.collide_mask) \
                    and me.invincible == 1:
                enemy.life = 0

            # 坦克死亡
            if enemy.life <= 0:
                # 避免多次播放死亡音效
                if enemy.dieImageIndex == 0:
                    if self.music:
                        self.dieSound.play()
                # 顺序播放一遍死亡动画
                self.screen.blit(enemy.dieImage[enemy.dieImageIndex], enemy.rect)
                enemy.dieImageIndex = (enemy.dieImageIndex + 1) % 7
                if enemy.dieImageIndex == 0:
                    enemy.reset()

            # 画目标及其血槽(Group不支持索引)
            for target in self.mapUsed.targets.sprites():
                if target.active:
                    self.screen.blit(target.image, target.rect)
                    if target.enemy == 1:
                        if target.life:
                            pygame.draw.line(self.screen, BLACK, \
                                             (target.rect.left - 10, target.rect.top), \
                                             (target.rect.left - 10, target.rect.top + target.rect.height), 4)
                            if target.life / mymap.Target.LIFE > 0.2:
                                color = GREEN
                            else:
                                color = RED
                            pygame.draw.line(self.screen, color, \
                                             (target.rect.left - 10, target.rect.top + target.rect.height - \
                                              target.rect.height * target.life / mymap.Target.LIFE),
                                             (target.rect.left - 10, target.rect.top + target.rect.height), 4)

                    if target.enemy == 2:
                        if target.life:
                            pygame.draw.line(self.screen, BLACK, \
                                             (target.rect.right + 10, target.rect.top), \
                                             (target.rect.right + 10, target.rect.top + target.rect.height), 4)
                            if target.life / mymap.Target.LIFE > 0.2:
                                color = GREEN
                            else:
                                color = RED
                            pygame.draw.line(self.screen, color, \
                                             (target.rect.right + 10, target.rect.top + target.rect.height - \
                                              target.rect.height * target.life / mymap.Target.LIFE),
                                             (target.rect.right + 10, target.rect.top + target.rect.height), 4)

            # 目标死亡与坦克死亡相同
            # for target in mapUsed.targets.sprites():
            target = self.mapUsed.targets.sprites()[choice]
            if target.life == 0:
                # 避免多次播放死亡音效
                if target.dieImageIndex == 0:
                    if self.music:
                        self.dieSound.play()
                self.screen.blit(target.dieImage[target.dieImageIndex], target.rect)
                target.dieImageIndex = (target.dieImageIndex + 1) % 7

                # 目标死亡动画播放结束后 游戏结束
                if target.dieImageIndex == 0:
                    target.life_left -= 1
                    if target.life_left == 0:
                        target.active = False
                        self.player[target.enemy - 1].win = True
                    else:
                        target.life = 8
                        self.player[target.enemy - 1].life -= 2


    def use_skill(self,index,key):
        player = self.player[index]
        if key == self.SHOOT[index] and \
                len(player.bullets) < player.bulletNumber:
            if self.music:
                self.bulletSound.play()  # 播放子弹音效
            player.bullets.append(Bullet(player, player.bullet_kill))
            if player.bullet_kill:
                player.bullet_kill = False
            return
        if not self.senior:
            return
        # 隐身
        if key == self.SKILL_HIDE[index]:
            if player.skill[Tank.SKILL_HIDE]:
                player.hide = Tank.HIDE
                player.skill[Tank.SKILL_HIDE] -= 1
            return
        # 无敌
        if key == self.SKILL_DEFEND[index]:
            if player.skill[Tank.SKILL_DEFEND]:
                player.defend = Tank.DEFEND
                player.skill[Tank.SKILL_DEFEND] -= 1
            return
        # 下发子弹一击必杀
        if key == self.SKILL_KILL[index]:
            if player.skill[Tank.SKILL_KILL]:
                player.bullet_kill = True
                player.skill[Tank.SKILL_KILL] -= 1
            return

    def run(self):
        # 设置帧率
        clock = pygame.time.Clock()
        # 播放背景音乐
        if self.music:
            pygame.mixer.music.play(-1)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # Esc键退出
                        pygame.quit()
                        sys.exit()

                    # 简单重启
                    if event.key == K_RETURN and self.gameOver:
                        self.mapUsed = self.gameReset()
                        if self.music:
                            pygame.mixer.music.play(-1)
                        for player in self.player:
                            for i in range(len(player.skill)):
                                player.skill[i] = 3
                        self.gameOver = False
                        self.winner = False
                        continue

                    if not self.gameOver:
                        self.use_skill(0,event.key)
                        self.use_skill(1,event.key)


            # 这里是判断按下的状态 通常来说人按一下键盘 好几帧都会保持按下的状态 如果发射子弹写在这会导致可能以下发射很多子弹
            # 坦克移动 P1 wasd P2上下左右
            keyPressed = pygame.key.get_pressed()
            if not self.gameOver:
                if keyPressed[K_a]:
                    self.player[0].move(LEFT, self.mapUsed, self.player[1])
                if keyPressed[K_LEFT]:
                    self.player[1].move(LEFT, self.mapUsed, self.player[0])
                if keyPressed[K_d]:
                    self.player[0].move(RIGHT, self.mapUsed, self.player[1])
                if keyPressed[K_RIGHT]:
                    self.player[1].move(RIGHT, self.mapUsed, self.player[0])
                if keyPressed[K_w]:
                    self.player[0].move(UP, self.mapUsed, self.player[1])
                if keyPressed[K_UP]:
                    self.player[1].move(UP, self.mapUsed, self.player[0])
                if keyPressed[K_s]:
                    self.player[0].move(DOWN, self.mapUsed, self.player[1])
                if keyPressed[K_DOWN]:
                    self.player[1].move(DOWN, self.mapUsed, self.player[0])

            for tank in self.player:
                # 减少复活后的无敌时间
                if tank.invincible:
                    tank.invincible -= 1
                # 减少强化子弹时间
                if tank.strongBullet:
                    tank.strongBullet -= 1
                if tank.hide:
                    tank.hide -= 1
                if tank.defend:
                    tank.defend -= 1
                # 减少加速时间
                if tank.speedup:
                    tank.speed = Tank.SPEED + 3
                    tank.speedup -= 1
                else:
                    tank.speed = Tank.SPEED

                # 吃星星强化子弹
                if pygame.sprite.spritecollide(tank, self.mapUsed.stars, \
                                               True, pygame.sprite.collide_mask):
                    tank.strongBullet = Tank.STRONGBULLET
                    if self.music:
                        self.supplySound.play()

                # 吃十字加血
                if pygame.sprite.spritecollide(tank, self.mapUsed.crosses, \
                                               True, pygame.sprite.collide_mask):
                    if tank.life != Tank.LIFE:
                        tank.life += 1
                        if self.music:self.crossSound.play()

                # 加速圈
                if pygame.sprite.spritecollide(tank, self.mapUsed.circles, \
                                               False, pygame.sprite.collide_mask):
                    tank.speedup = Tank.SPEEDUP

            # 填充背景 准备绘制游戏画面
            self.screen.fill(bgColor)

            # 绘制可变元素  考虑同时死亡播放动画的情况 使用多线程
            t1 = threading.Thread(target=self.draw, args=(0,))
            t2 = threading.Thread(target=self.draw, args=(1,))
            t1.start()
            t2.start()

            # 绘制地图元素
            for elementType in self.mapUsed.elements:
                for element in elementType:
                    self.screen.blit(element.image, element.rect)

            for i in range(2):
                target = self.mapUsed.targets.sprites()[1-i]
                self.printmessage(str(target.life_left), fontColor2, 90, (self.width * 0.2 + i * 800, self.height * 0.1))

            if self.player[0].win:
                self.gameOver = True
                self.winner = 1
            elif self.player[1].win:
                self.gameOver = True
                self.winner = 2

            if self.gameOver:
                # 停止音乐
                pygame.mixer.music.stop()
                self.printmessage('Player ' + str(self.winner) + ' Win !', fontColor, 100, (self.width * 0.345, self.height * 0.35))
                self.printmessage('exit:Esc', fontColor2, 70, (self.width * 0.25, self.height * 0.65))
                self.printmessage('again:Enter', YELLOW, 70, (self.width * 0.6, self.height * 0.65))

            # 内存 -> 屏幕
            pygame.display.flip()
            # 设置帧率为40帧
            clock.tick(40)


if __name__ == '__main__':
    game = BattleCity()
    game.run()
