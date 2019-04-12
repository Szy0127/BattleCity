import pygame
import sys
import traceback
from tank import *
import threading
import mymap
from pygame.locals import *

pygame.init()
bgSize = width, height = 1366, 768   #屏幕大小
# bgSize = width, height = 1000,800
# 定义颜色
BLUE = (50, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
bgColor = (80, 80, 80)
fontColor = (253, 3, 27)
fontColor2 = (0, 255, 255)

screen = pygame.display.set_mode(bgSize, FULLSCREEN | HWSURFACE)#全屏
#screen = pygame.display.set_mode(bgSize)
pygame.display.set_caption('坦克大战')

#背景音乐
pygame.mixer.music.load('sound/bgMusic.ogg')
pygame.mixer.music.set_volume(0.2)
#子弹发射音效
bulletSound = pygame.mixer.Sound('sound/bullet.wav')
bulletSound.set_volume(0.3)
#捡十字音效
crossSound = pygame.mixer.Sound('sound/cross.wav')
crossSound.set_volume(0.3)
#捡道具音效
supplySound = pygame.mixer.Sound('sound/supply.wav')
supplySound.set_volume(0.3)
#玩家死亡音效
dieSound = pygame.mixer.Sound('sound/die.wav')
dieSound.set_volume(0.4)

killNumber = [0,0]
def gameReset(player):
    map = mymap.Map(bgSize, 1)

    for tank in player:
        tank.reset()
        tank.win = False

    return map

def printmessage(message,color,size,location):
    font = pygame.font.Font(None, size) 
    message = font.render(message,True, color)
    screen.blit(message, location)
	
def draw(player, choice ,mapUsed, gameOver):
    me = player[choice]
    enemy = player[not choice]

    # 避免游戏结束后出现子弹及重复死亡画面
    if not gameOver:
        # 画子弹
        for bullet in me.bullets:
            #移动并返回是否依然存在
            if bullet.move(mapUsed, enemy):
                screen.blit(bullet.image[bullet.face], bullet.rect)
            else:
                me.bullets.remove(bullet)

        # 画坦克及血槽
        if me.life:
            screen.blit(me.image[me.face], me.rect)
            pygame.draw.line(screen, BLACK, \
                    (me.rect.left, me.rect.top - 5), \
                    (me.rect.right, me.rect.top - 5), 4)
            if me.life / Tank.LIFE > 0.2:
                color = GREEN
            else:
                color = RED
            pygame.draw.line(screen, color, \
                    (me.rect.left, me.rect.top - 5), \
                    (me.rect.left + me.rect.width * me.life \
                        / Tank.LIFE, me.rect.top - 5), 4)

        #双方重合时敌方死亡(复活后的bug)
        if pygame.sprite.spritecollide(me,pygame.sprite.Group(enemy), \
                                           False, pygame.sprite.collide_mask)\
            and me.invincible == 1 :
            enemy.life = 0

        #坦克死亡
        if enemy.life == 0:
            #避免多次播放死亡音效
            if enemy.dieImageIndex == 0:
                dieSound.play()
            # 顺序播放一遍死亡动画
            screen.blit(enemy.dieImage[enemy.dieImageIndex], enemy.rect)
            enemy.dieImageIndex = (enemy.dieImageIndex + 1) % 7
            if enemy.dieImageIndex == 0:
                enemy.reset()
                killNumber[choice] += 1


        # 画目标及其血槽(Group不支持索引)
        for target in mapUsed.targets.sprites():
            if target.active:
                screen.blit(target.image, target.rect)
                if target.enemy == 1:
                    if target.life:
                        pygame.draw.line(screen, BLACK, \
                                (target.rect.left - 10, target.rect.top), \
                                (target.rect.left - 10, target.rect.top + target.rect.height), 4)
                        if target.life / mymap.Target.LIFE > 0.2:
                            color = GREEN
                        else:
                            color = RED
                        pygame.draw.line(screen, color, \
                                (target.rect.left - 10, target.rect.top + target.rect.height - \
                                target.rect.height * target.life / mymap.Target.LIFE),
                                (target.rect.left - 10, target.rect.top + target.rect.height), 4)

                if target.enemy == 2:
                    if target.life:
                        pygame.draw.line(screen, BLACK, \
                                (target.rect.right + 10, target.rect.top), \
                                (target.rect.right + 10, target.rect.top + target.rect.height), 4)
                        if target.life / mymap.Target.LIFE > 0.2:
                            color = GREEN
                        else:
                            color = RED
                        pygame.draw.line(screen, color, \
                                (target.rect.right + 10, target.rect.top + target.rect.height - \
                                target.rect.height * target.life / mymap.Target.LIFE),
                                (target.rect.right + 10, target.rect.top + target.rect.height), 4)

        # 目标死亡与坦克死亡相同
        #for target in mapUsed.targets.sprites():
        target = mapUsed.targets.sprites()[choice]
        if target.life == 0 :
            #避免多次播放死亡音效
            if target.dieImageIndex == 0:
                dieSound.play()
            screen.blit(target.dieImage[target.dieImageIndex], target.rect)
            target.dieImageIndex = (target.dieImageIndex + 1) % 7

            #目标死亡动画播放结束后 游戏结束
            if target.dieImageIndex == 0:
                target.active = False
                player[target.enemy - 1].win = True
            


def main():
    # 设置帧率
    clock = pygame.time.Clock()
    # 播放背景音乐
    pygame.mixer.music.play(-1)
    musicClose = False
    gameOver = False #游戏是否结束
    winner = False #胜利玩家

    # 生成地图
    mapUsed = mymap.Map(bgSize, 1)

    # 生成坦克
    player = []
    player.append(Tank(bgSize, DOWN, (bgSize[0]*0.05,bgSize[1]*0.1), 1))
    player.append(Tank(bgSize, UP, (bgSize[0]*0.9,bgSize[1]*0.85), 2))
	
    global killNumber
    #时间循环 (一次一帧)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE:  #Esc键退出
                    sys.exit()
                    pygame.quit()

                #简单重启
                if event.key == K_RETURN and gameOver:
                    mapUsed = gameReset(player)
                    pygame.mixer.music.play(-1)
                    killNumber = [0,0]
                    gameOver = False
                    winner = False
		    
                    
                if not gameOver:
                    # 空格键P1发射子弹
                    if event.key == K_SPACE and \
                            len(player[0].bullets) < player[0].bulletNumber:
                        bulletSound.play() #播放子弹音效
                        player[0].bullets.append(Bullet(player[0]))

                    # +(=)键P2发射子弹
                    if event.key == K_EQUALS and \
                            len(player[1].bullets) < player[1].bulletNumber:
                        bulletSound.play()
                        player[1].bullets.append(Bullet(player[1]))

        # 坦克移动 P1 wasd P2上下左右
        keyPressed = pygame.key.get_pressed()
        if not gameOver:
            if keyPressed[K_a]:
                player[0].move(LEFT, mapUsed, player[1])
            if keyPressed[K_LEFT]:
                player[1].move(LEFT, mapUsed, player[0])
            if keyPressed[K_d]:
                player[0].move(RIGHT, mapUsed, player[1])
            if keyPressed[K_RIGHT]:
                player[1].move(RIGHT, mapUsed, player[0])
            if keyPressed[K_w]:
                player[0].move(UP, mapUsed, player[1])
            if keyPressed[K_UP]:
                player[1].move(UP, mapUsed, player[0])
            if keyPressed[K_s]:
                player[0].move(DOWN, mapUsed, player[1])
            if keyPressed[K_DOWN]:
                player[1].move(DOWN, mapUsed, player[0])


        for tank in player:
            # 减少复活后的无敌时间
            if tank.invincible:
                tank.invincible -= 1
            # 减少强化子弹时间
            if tank.strongBullet:
                tank.strongBullet -= 1
            # 减少加速时间
            if tank.speedup:
                tank.speed = Tank.SPEED + 4 
                tank.speedup -= 1
            else:
                tank.speed = Tank.SPEED

            # 吃星星强化子弹
            if pygame.sprite.spritecollide(tank, mapUsed.stars,\
                            True, pygame.sprite.collide_mask):
                tank.strongBullet = Tank.STRONGBULLET
                supplySound.play()

            # 吃十字加血
            if pygame.sprite.spritecollide(tank, mapUsed.crosses,\
                            True, pygame.sprite.collide_mask):
                if tank.life != Tank.LIFE:
                    tank.life += 1
                    crossSound.play()

            # 加速圈
            if pygame.sprite.spritecollide(tank, mapUsed.circles, \
                                        False, pygame.sprite.collide_mask):
                tank.speedup = Tank.SPEEDUP

        # 填充背景 准备绘制游戏画面
        screen.fill(bgColor)

        #绘制可变元素  考虑同时死亡播放动画的情况 使用多线程
        t1 = threading.Thread(target=draw, args=(player, 0, mapUsed, gameOver))
        t2 = threading.Thread(target=draw, args=(player, 1, mapUsed, gameOver))
        t1.start()
        t2.start()

        #绘制地图元素
        for elementType in mapUsed.elements:
            for element in elementType:
                screen.blit(element.image, element.rect)
                
        for i in range(2):
            printmessage(str(killNumber[i]),fontColor2,90,(width * 0.2 + i*800, height * 0.1))
        
            
        if player[0].win :
            gameOver = True
            winner = 1
        elif player[1].win :
            gameOver = True
            winner = 2

        if gameOver:
            # 停止音乐
            pygame.mixer.music.stop()
            printmessage('Player ' + str(winner) + ' Win !' ,fontColor,100,(width * 0.345, height * 0.35))
            printmessage('exit:Esc' ,fontColor2,70,(width * 0.25, height * 0.65))
            printmessage('again:Enter' ,YELLOW,70,(width * 0.6, height * 0.65))
            	
			
        # 内存 -> 屏幕
        pygame.display.flip()
        # 设置帧率为40帧
        clock.tick(40)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        input()

