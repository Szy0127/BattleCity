import pygame

#朝向
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


#子弹类
class Bullet(pygame.sprite.Sprite):
    #生命值(飞行时间)
    LIFE = 25

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)

        #是否为强化版子弹 设置不同属性
        self.strong = player.strongBullet

        if self.strong:
            self.WIDTH, self.HEIGHT = 128, 128
            path = 'image/strongBullet' + str(player.id)
        else:
            self.WIDTH, self.HEIGHT = 11, 30
            path = 'image/bullet' + str(player.id)

        #加载图片
        self.image = []
        self.image.append(pygame.image.load(str(path + 'Left.png')).convert_alpha())
        self.image.append(pygame.image.load(str(path + 'Right.png')).convert_alpha())
        self.image.append(pygame.image.load(str(path + 'Up.png')).convert_alpha())
        self.image.append(pygame.image.load(str(path + 'Down.png')).convert_alpha())

        #四个朝向
        self.face = player.face

        # 完美碰撞检测
        self.mask = pygame.mask.from_surface(self.image[0])

        # 子弹生命值(持续时间)
        self.life = Bullet.LIFE
        #子弹速度
        self.speed = 12

        self.rect = self.image[0].get_rect()
        #屏幕大小
        self.width, self.height = player.width, player.height

        #根据不同朝向计算子弹初始位置
        if self.face == UP or self.face == DOWN:
            self.rect.left, self.rect.top \
                = player.rect.left + Tank.WIDTH // 2 - self.WIDTH // 2, \
                  player.rect.top + Tank.HEIGHT // 2 - self.HEIGHT // 2
        else:
            self.rect.left, self.rect.top \
                = player.rect.left + Tank.WIDTH // 2 - self.HEIGHT // 2, \
                  player.rect.top + Tank.HEIGHT // 2 - self.WIDTH // 2


    def move(self, mapUsed, enemy):
        # 子弹飞行时间 - 1
        self.life -= 1

        # 检测是否击中敌方坦克
        if pygame.sprite.spritecollide(self, pygame.sprite.Group(enemy), \
                                       False, pygame.sprite.collide_mask):
            self.life = 0
            #非无敌状态时敌方扣血
            if enemy.life and enemy.invincible == 0:
                enemy.life -= 1

        # 检测是否击中墙 (强化子弹可穿透墙)
        if self.strong:
            if pygame.sprite.spritecollide(self, mapUsed.walls, \
                                True, pygame.sprite.collide_mask):
                self.life = self.life
        else:
            if pygame.sprite.spritecollide(self, mapUsed.walls, \
                                True, pygame.sprite.collide_mask):
                self.life = 0

        # 检测是否击中钢板 (强化子弹可破坏钢板)
        if self.strong:
            if pygame.sprite.spritecollide(self, mapUsed.steels, \
                                True, pygame.sprite.collide_mask):
                self.life = 0
        else:
            if pygame.sprite.spritecollide(self, mapUsed.steels, \
                                False, pygame.sprite.collide_mask):
                self.life = 0

        # 检测是否击中目标
        targetShooted = pygame.sprite.spritecollide \
                (self, mapUsed.targets, False, pygame.sprite.collide_mask)
        for target in targetShooted:
            self.life = 0
            #目标扣血
            if target.life:
                target.life -= 1

        #超出地图范围
        if self.face == LEFT:
            if self.rect.left > 10:
                self.rect.left -= self.speed
            else:
                self.life = 0
        if self.face == RIGHT:
            if self.rect.left < self.width - 70:
                self.rect.left += self.speed
            else:
                self.life = 0
                
        if self.face == UP:
            if self.rect.top > 10:
                self.rect.top -= self.speed
            else:
                self.life = 0
                
        if self.face == DOWN:
            if self.rect.top < self.height - 70:
                self.rect.top += self.speed
            else:
                self.life = 0

        return self.life
                
    def reset(self):
        self.life = Bullet.LIFE

#坦克类
class Tank(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 60, 60
    # 生命值
    LIFE = 5
    # 无敌时间
    INVINCIBLE = 50
    #强化子弹时间
    STRONGBULLET = 250
    #加速时间
    SPEEDUP = 50
    #正常速度
    SPEED = 5

    def __init__(self, bgSize, face, location, number):
        pygame.sprite.Sprite.__init__(self)

        #玩家编号
        self.id = number
        
        path = 'image/tank' + str(number)
        self.image = []
        self.image.append(pygame.image.load(str(path + 'Left.png')).convert_alpha())
        self.image.append(pygame.image.load(str(path + 'Right.png')).convert_alpha())
        self.image.append(pygame.image.load(str(path + 'Up.png')).convert_alpha())
        self.image.append(pygame.image.load(str(path + 'Down.png')).convert_alpha())
        self.face = face
        
        self.mask = pygame.mask.from_surface(self.image[0])

        # 死亡动画
        self.dieImage = []
        self.dieImageIndex = 0
        for i in range(7):
            path = 'image/explode' + str(i) + '.png'
            self.dieImage.append(pygame.image.load(path).convert_alpha())

        #无敌时间
        self.invincible = Tank.INVINCIBLE
        #强化子弹时间
        self.strongBullet = 0

        #屏幕大小
        self.width, self.height = bgSize[0], bgSize[1]

        # 坦克位置
        self.rect = self.image[0].get_rect()
        self.rect.left, self.rect.top = location[0], location[1]
        # 坦克速度
        self.speed = Tank.SPEED
        # 坦克加速时间
        self.speedup = 0
        # 坦克生命值
        self.life = Tank.LIFE

        # 坦克所带子弹
        self.bullets = []
        # 可携带子弹总数量
        self.bulletNumber = 3

        # 玩家是否胜利
        self.win = False

        
    def move(self, face, mapUsed, enemy):
        #下一步方向
        self.face = face

        # 下一步是否会碰撞
        moveflag = True

        #先移动
        if self.face == LEFT :
            self.rect.left -= self.speed
        if self.face == RIGHT:
            self.rect.left += self.speed
        if self.face == UP:
            self.rect.top -= self.speed
        if self.face == DOWN:
            self.rect.top += self.speed

        # 判断是否与地图元素碰撞
        if pygame.sprite.spritecollide(self,mapUsed.targets,\
                            False, pygame.sprite.collide_mask)\
            or pygame.sprite.spritecollide(self,mapUsed.steels,\
                            False, pygame.sprite.collide_mask)\
            or pygame.sprite.spritecollide(self,mapUsed.walls,\
                            False, pygame.sprite.collide_mask)\
            or pygame.sprite.spritecollide(self,mapUsed.rivers,\
                            False, pygame.sprite.collide_mask):
            moveflag = False

        # 判断是否与敌方坦克碰撞(非无敌状态)
        if pygame.sprite.spritecollide(self,pygame.sprite.Group(enemy), \
                                    False, pygame.sprite.collide_mask)\
            and enemy.invincible == 0 :
            moveflag = False

        # 判断是否超出屏幕范围
        if self.rect.left < 10 or self.rect.left > self.width - 70\
           or self.rect.top < 10 or self.rect.top > self.height - 70:
            moveflag = False

        # 若碰撞 则返回上一步
        if not moveflag:
            if self.face == LEFT :
                self.rect.left += self.speed
            if self.face == RIGHT:
                self.rect.left -= self.speed
            if self.face == UP:
                self.rect.top += self.speed
            if self.face == DOWN:
                self.rect.top -= self.speed

    def reset(self):
        #恢复生命值
        self.life = Tank.LIFE
        #开启无敌状态
        self.invincible = Tank.INVINCIBLE
        #关闭子弹强化
        self.strongBullet = 0

        #初始化方向
        if self.id == 1:
            self.face = DOWN
        else:
            self.face = UP

        self.bullets = []
        #回到初始位置
        if self.id == 1:
            self.rect.left, self.rect.top = self.width * 0.05, self.height * 0.1
        if self.id == 2:
            self.rect.left, self.rect.top = self.width * 0.9, self.height * 0.85
        
