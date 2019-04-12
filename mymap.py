import pygame

# 击败目标获胜
class Target(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 45, 60
    LIFE = 8
    def __init__(self, location, choice):
        pygame.sprite.Sprite.__init__(self)

        path = 'image/target' + str(choice) + '.png'
        self.image = pygame.image.load(path).convert_alpha()

        self.enemy = choice
        
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]
        # 完美碰撞检测
        self.mask = pygame.mask.from_surface(self.image)

        self.life = Target.LIFE

        #此属性用于死亡动画播放
        self.active = True

        # 死亡动画
        self.dieImage = []
        self.dieImageIndex = 0
        for i in range(7):
            path = 'image/explode' + str(i) + '.png'
            self.dieImage.append(pygame.image.load(path).convert_alpha())
            
#坦克无法穿过 子弹可破坏的墙
class Wall(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 30, 30
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/wall.png')

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]

        self.mask = pygame.mask.from_surface(self.image)
    
#坦克无法穿过 普通子弹无法破坏的钢板
class Steel(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 30, 30
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/steel.png')

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]
        
        self.mask = pygame.mask.from_surface(self.image)

#坦克及子弹在草丛中被遮挡
class Grass(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 30, 30
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/grass.png')
        
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]
        
        self.mask = pygame.mask.from_surface(self.image)

# 子弹可穿过 坦克无法穿过的河流
class River(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 30, 30
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/water.png')
        
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]

        self.mask = pygame.mask.from_surface(self.image)

#捡到星星子弹强化
class Star(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 64, 64
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/star.png')

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]

        self.mask = pygame.mask.from_surface(self.image)

#捡到十字当前血量 + 1 (满血无效)
class Cross(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 42, 42
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/cross.png')

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]

        self.mask = pygame.mask.from_surface(self.image)

#碰撞后获得加速效果的小圈圈
class Circle(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 64, 64
    def __init__(self, location, choice):
        pygame.sprite.Sprite.__init__(self)

        #两种形态 (对双方都有效)
        path = 'image/circle' + str(choice) + '.png'
        self.image = pygame.image.load(path)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location[0], location[1]

        self.mask = pygame.mask.from_surface(self.image)

class Map():
    def __init__(self, bgSize, choice):
        #地图大小
        self.width, self.height = bgSize[0], bgSize[1]

        #地图元素
        self.elements = []
        self.targets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.steels = pygame.sprite.Group()
        self.grasses = pygame.sprite.Group()
        self.rivers = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.crosses = pygame.sprite.Group()
        self.circles = pygame.sprite.Group()

        #根据用户选择初始化不同地图
        if choice ==1:
            '--------------target----------------'
            self.targets.add(Target((self.width - Steel.WIDTH \
                - Target.WIDTH , (self.height + Target.HEIGHT) // 2 - Target.HEIGHT), 1))
            self.targets.add(Target((Steel.WIDTH, (self.height +\
                                Target.HEIGHT) // 2 - Target.HEIGHT), 2))

            '--------------wall----------------'
            # 目标周围保护的墙
            for i in range(2):
                for j in range(4):
                    self.walls.add(Wall(( \
                        Steel.WIDTH + j * Wall.WIDTH , (self.height + \
                            Target.HEIGHT) // 2 - Target.HEIGHT + (i-2) * Wall.HEIGHT)))
                    
                    self.walls.add(Wall(( Steel.WIDTH + j * Wall.WIDTH , \
                        (self.height + Target.HEIGHT) // 2 - Target.HEIGHT \
                        + i * Wall.HEIGHT + Target.HEIGHT)))

                    self.walls.add(Wall((self.width - Steel.WIDTH - \
                        Target.WIDTH - Target.WIDTH - (j - 2)  * Wall.WIDTH ,\
                        (self.height + Target.HEIGHT) // 2 - Target.HEIGHT + (i + 2) \
                        * Wall.HEIGHT - Target.HEIGHT * 2)))
                    
                    self.walls.add(Wall(( \
                        self.width - Steel.WIDTH - Target.WIDTH - Target.WIDTH - \
                        (j - 2)  * Wall.WIDTH ,(self.height + Target.HEIGHT) // 2 \
                        - Target.HEIGHT + i * Wall.HEIGHT + Target.HEIGHT)))
                    
                for j in range(2):
                    self.walls.add(Wall(( \
                        Steel.WIDTH + (j + 2) * Wall.WIDTH , \
                        (self.height + Target.HEIGHT) // 2 - \
                        Target.HEIGHT + i * Wall.HEIGHT)))
                    self.walls.add(Wall(( \
                        self.width - Steel.WIDTH - 2 * Target.WIDTH - j * Wall.WIDTH , \
                        (self.height + Target.HEIGHT) // 2 - \
                        Target.HEIGHT + i * Wall.HEIGHT)))

            # 草丛外墙 靠近我方
            for i in range(3):
                for j in range(4):
                    self.walls.add(Wall((self.width * 0.15 + (j + 10) * Wall.WIDTH, \
                                self.height * 0.1 + (i + 1) * Wall.HEIGHT )))
                    self.walls.add(Wall((self.width * 0.8 - (j + 10) * Wall.WIDTH + 14, \
                                self.height * 0.9 - (i + 2) * Wall.HEIGHT )))
            # 草丛外墙 靠近敌方
                for j in range(8):
                    self.walls.add(Wall((self.width * 0.15 + (j + 17) * Wall.WIDTH, \
                            self.height * 0.1 + (i + 1) * Wall.HEIGHT )))
                    self.walls.add(Wall((self.width * 0.8 - (j + 17) * Wall.WIDTH + 12, \
                            self.height * 0.9 - (i + 2) * Wall.HEIGHT )))

                for j in range(4):
                    self.walls.add(Wall((self.width * 0.15 + (j + 21) * Steel.WIDTH, \
                                Steel.HEIGHT + (i ) * Steel.HEIGHT)))
                    self.walls.add(Wall((self.width * 0.8 - (j + 21) * Steel.WIDTH + 12, \
                                self.height - Steel.HEIGHT - (i + 1) * Steel.HEIGHT)))

            # 角上墙
                for j in range(3):
                    self.walls.add(Wall(((j + 4) * Grass.WIDTH,
                                        self.height + (i - 7) * Grass.HEIGHT)))
                    self.walls.add(Wall((self.width + (j - 7) * Grass.WIDTH,
                                        (i + 4) * Grass.HEIGHT)))

            '--------------steel----------------'
            # 出生点钢板
            for i in range(6):
                self.steels.add(Steel((self.width * 0.15, \
                                self.height * 0.1 + (i - 2) * Steel.HEIGHT)))
                self.steels.add(Steel((self.width * 0.8, \
                                self.height * 0.9 - (i - 1) * Steel.HEIGHT)))

            # 草丛外钢板
            for i in range(3):
                self.steels.add(Steel((self.width * 0.15 + 4 * Steel.WIDTH, \
                        self.height * 0.1 + (i + 1)  * Steel.HEIGHT)))
                self.steels.add(Steel((self.width * 0.8 - 4 * Steel.WIDTH, \
                        self.height * 0.9 - (i + 2) * Steel.HEIGHT)))
            for i in range(5):
                self.steels.add(Steel((self.width * 0.15 + (i + 5) * Steel.WIDTH, \
                                       self.height * 0.1 + Steel.HEIGHT)))
                self.steels.add(Steel((self.width * 0.8 - (i + 5) * Steel.WIDTH, \
                                       self.height * 0.9 - 2 * Steel.HEIGHT)))

            # 地图外围钢板
            for i in range(0, self.width, Steel.WIDTH):
                self.steels.add(Steel((i, 0)))
                self.steels.add(Steel((i, self.height - Steel.HEIGHT)))
            for i in range(0, self.height, Steel.HEIGHT):
                self.steels.add(Steel((0, i)))
                self.steels.add(Steel((self.width - Steel.WIDTH, i)))

            # 中心钢板
            for i in range(3):
                for j in range(3):
                    self.steels.add(Steel((self.width * 0.5 + (j-2) * Steel.WIDTH,
                                self.height * 0.48  + (i-1) * Steel.HEIGHT)))

            # 笑脸钢板
            for x in range(-100,101,20):
                y = 0.01 * x ** 2
                self.steels.add(Steel((self.width * 0.35 - y, self.height * 0.48 + x)))
                self.steels.add(Steel((self.width * 0.65 + y, self.height * 0.48 + x)))

            '--------------grass----------------'
            # 上下草
            for i in range(3):
                for j in range(11):
                    self.grasses.add(Grass((self.width * 0.5 + (j - 6) * Grass.WIDTH,
                                        Steel.HEIGHT + i * Grass.HEIGHT )))
                    self.grasses.add(Grass((self.width * 0.5 + (j - 6) * Grass.WIDTH,
                                        self.height + (i - 4) * Grass.HEIGHT )))

            # 角上草
            for i in range(3):
                for j in range(3):
                    self.grasses.add(Grass(((j + 1)  * Grass.WIDTH ,
                                    self.height + (i - 4) * Grass.HEIGHT)))
                    self.grasses.add(Grass((self.width + (j -4) * Grass.WIDTH,
                                    (i + 1) * Grass.HEIGHT)))

            '--------------river----------------'
            # 中间河
            for i in range(5):
                for j in range(3):
                    self.rivers.add(River((self.width * 0.5 + (j-2) * River.WIDTH,\
                                Steel.HEIGHT + 3 * Grass.HEIGHT + i * River.HEIGHT)))
                    self.rivers.add(River((self.width * 0.5 + (j-2) * River.WIDTH,\
                        self.height - 3 * Grass.HEIGHT - Steel.HEIGHT - (i+1) * River.HEIGHT)))

            # 角上河
            for i in range(1):
                for j in range(3):
                    self.rivers.add(River(((j + 1)  * Grass.WIDTH ,
                                            self.height + (i - 7) * Grass.HEIGHT)))
                    self.rivers.add(River((self.width + (j -4) * Grass.WIDTH,
                                            (i + 6) * Grass.HEIGHT)))
                    self.rivers.add(River(((i + 6) * Grass.WIDTH,
                                           self.height + (j - 4) * Grass.HEIGHT)))
                    self.rivers.add(River((self.width + (i - 7) * Grass.WIDTH,
                                           (j + 1) * Grass.HEIGHT)))

            '--------------star----------------'
            # 角上星
            for i in range(1):
                for j in range(3):
                    self.stars.add(Star(( Steel.WIDTH , self.height - \
                                          Star.HEIGHT - Steel.HEIGHT )))
                    self.stars.add(Star((self.width - Steel.WIDTH - Star.WIDTH, \
                                          Steel.HEIGHT)))

            '--------------cross----------------'
            #中间河旁十字
            self.crosses.add(Cross((self.width * 0.5 - 4 * River.WIDTH, Steel.HEIGHT \
                                    + 3 * Wall.HEIGHT+ 3 * Grass.HEIGHT)))
            self.crosses.add(Cross((self.width * 0.5 + 2 * River.WIDTH, Steel.HEIGHT \
                                    + 3 * Wall.HEIGHT+ 3 * Grass.HEIGHT)))
            self.crosses.add(Cross((self.width * 0.5 - 4 * River.WIDTH, self.height\
                                    -Steel.HEIGHT - 5 * Wall.HEIGHT - 3 * Grass.HEIGHT)))
            self.crosses.add(Cross((self.width * 0.5 + 2 * River.WIDTH, self.height\
                                    -Steel.HEIGHT - 5 * Wall.HEIGHT - 3 * Grass.HEIGHT)))

            '--------------cirle----------------'
            #笑脸前的加速圈
            for i in range(0,3,2):
                self.circles.add(Circle((self.width * 0.2, \
                                self.height * 0.38 + i * Circle.HEIGHT), 1))
                self.circles.add(Circle((self.width * 0.8, \
                                self.height * 0.38 + i * Circle.HEIGHT), 2))

        else:
            pass   #多种地图待补充

        #self.elements.append(self.targets) target操作较别的元素复杂 单独处理

        self.elements.append(self.rivers)
        self.elements.append(self.walls)
        self.elements.append(self.steels)
        self.elements.append(self.stars)
        self.elements.append(self.crosses)
        self.elements.append(self.circles)
        self.elements.append(self.grasses)  # 决定叠放顺序 草丛最后手动画


