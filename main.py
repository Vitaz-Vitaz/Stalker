import os

import csv
import pygame

pygame.init()
WIDTH = 700
HEIGHT = 700
ROWS = 16
COLS = 150
all_images = list()
for i in range(20):
    im = pygame.image.load("imges/blocks/" + str(i) + ".png")
    im = pygame.transform.scale(im, (40, 40))
    all_images.append(im)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Stalker")
GRAVITY = 4
font = pygame.font.SysFont('Futura', 40)
level = 1
all_world = []
for r in range(ROWS):
    a = [-1] * COLS
    all_world.append(a)
print(all_world)
with open("level" + str(level) + ".csv", newline='') as csvfile:
    r = csv.reader(csvfile, delimiter=',')
    for x, ro in enumerate(r):

        for y, block in enumerate(ro):
            all_world[x][y] = int(block)
print(all_world)


def drawText(text, color, x, y):
    im = font.render(text, True, color)
    screen.blit(im, (x, y))


class SpriteGroup(pygame.sprite.Group):

    def __init_(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


def forFon():
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 255, 255), (0, 300), (WIDTH, 300))


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


sprite_group = SpriteGroup()


class Player(Sprite):
    def __init__(self, pX, pY, k, skorost, typePlayer, faza, am):
        super().__init__(sprite_group)
        self.a = ["first", "second", "third", "forth", "fifth", "sixth", "seventh", "eighth"]
        self.sprites = list()
        self.faza_now = 0
        self.action = 0
        self.isJump = True
        self.strelba = False
        self.now_am = am
        self.am = am
        self.jumpSpeed = -75
        self.go_right = False
        self.go_left = False
        self.health = 5
        self.Maxhealth = 5
        self.kolvoPul = 0
        faza_type = ['calm', 'running', 'jumping', 'death']
        for h in faza_type:
            temp_list = []
            kolvo = len(os.listdir('imges/' + typePlayer + '/' + h))
            for i in range(kolvo):
                img = pygame.image.load('imges/' + typePlayer + '/' + h + '/' + self.a[i] + '.png').convert_alpha()
                img = pygame.transform.scale(img,
                                             (int(img.get_width() * k), int(img.get_height() * k)))
                temp_list.append(img)
            self.sprites.append(temp_list)

        self.image = self.sprites[self.action][self.faza_now]

        self.rect = self.image.get_rect()
        self.rect.center = (pX, pY)
        self.pos = (pX, pY)
        self.k = k
        self.jump = False
        self.vlevoVpravo = 1
        self.menyem = False
        self.upDateTime = pygame.time.get_ticks()
        self.skorost = skorost
        self.live = True

    def drawPlayer(self):
        if self.vlevoVpravo == 1:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, -1, False), self.rect)

    def update(self):
        self.updatePlayer()
        self.check_live()
        if self.kolvoPul > 0:
            self.kolvoPul -= 1

    def updatePlayer(self):
        self.image = self.sprites[self.action][self.faza_now]

        if pygame.time.get_ticks() - self.upDateTime > 100:
            self.faza_now += 1
            self.upDateTime = pygame.time.get_ticks()
        if self.faza_now >= len(self.sprites[self.action]):
            if self.action == 3:
                self.faza_now = len(self.sprites[self.action]) - 1
            else:

                self.faza_now = 0

    def check_live(self):
        if self.health < 0:
            self.live = False
            self.health = 0
            self.skorost = 0
            self.proverka(3)

    def proverka(self, act):
        if self.action != act:
            self.action = act
            self.faza_now = 0
            self.upDateTime = pygame.time.get_ticks()

    def strelb(self):
        if self.kolvoPul == 0 and self.now_am > 0:
            self.kolvoPul = 20
            puly1 = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.vlevoVpravo),
                           self.rect.centery, self.vlevoVpravo)
            puly_group.add(puly1)
            self.now_am -= 1

    def move(self):
        self.rect.y += GRAVITY
        if self.go_left:
            self.rect.x -= self.skorost
            self.menyem = True
            self.vlevoVpravo = -1
        if self.go_right:
            self.rect.x += self.skorost
            self.menyem = True
            self.vlevoVpravo = 1
        if self.jump and not self.isJump:
            self.rect.y += self.jumpSpeed
            self.jump = False
            self.isJump = True
        if self.rect.bottom > 300:
            self.rect.bottom = 300
            self.isJump = False

    def moveForEnemy(self):
        self.rect.y += GRAVITY
        if self.rect.bottom > 300:
            self.rect.bottom = 300


class Bar():
    def __init__(self, x, y, now, max):
        self.x = x
        self.y = y
        self.now = now
        self.max = max

    def draw(self, now):
        self.now = now
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 150 * (stalker.health / 5), 20))
        pygame.draw.rect(screen, (255, 255, 255), (self.x - 2, self.y - 2, 154, 24), 1)


class Box(Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pygame.image.load('imges/icons/' + type + '_box.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if pygame.sprite.collide_rect(self, stalker):
            if self.type == 'health':
                if stalker.health < 5:
                    stalker.health += 1
            elif self.type == 'ammo':
                if stalker.am < 20:
                    stalker.am = 20
            self.kill()


box_group = pygame.sprite.Group()


class AllWorld():
    def __init__(self):
        self.world = list()

    def load_world(self, d):
        for y, ro in enumerate(d):
            for x, block in enumerate(ro):
                print(block, len(all_images))
                if block >= 0:
                    im = all_images[block]
                    imRect = im.get_rect()
                    imRect.x = x * 40
                    imRect.y = y * 40
                    d = (im, imRect)
                    if block <= 8:
                        self.world.append(d)
                    elif 9 <= block <= 10:
                        pass
                    elif 11 <= block <= 14:
                        pass
                    elif block == 15:
                        stalker = Player(x * 40, y * 40, 1.65, 15, "stalker", 0, 20)
                        healthBar = Bar(165, 45, stalker.health, stalker.Maxhealth)
                    elif block == 16:
                        enemy = Player(x * 40, y * 40, 1.65, 15, "stalker", 0, 20)
                    elif block == 17:
                        box1 = Box(x * 40, y * 40, 'ammo')
                        box_group.add(box1)
                    elif block == 19:
                        box1 = Box(x * 40, y * 40, 'health')
                        box_group.add(box1)
                    elif block == 20:
                        pass
        return stalker, healthBar


world = AllWorld()
stalker, healthBar = world.load_world(all_world)


class Bullet(Sprite):
    def __init__(self, x, y, napravlenie):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('imges/icons/qbullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vlevovpavo = napravlenie

    def update(self):
        self.rect.x += (self.vlevovpavo * self.speed)
        if self.rect.right < 0 or self.rect.left > WIDTH - 100:
            self.kill()
        if pygame.sprite.spritecollide(stalker, puly_group, False):
            if stalker.live:
                stalker.health -= 1
                self.kill()
        if pygame.sprite.spritecollide(enemy, puly_group, False):
            if stalker.live:
                enemy.health -= 1
                self.kill()


puly_group = pygame.sprite.Group()

box1 = Box(300, 300, 'health')
box_group.add(box1)

enemy = Player(150, 150, 1.65, 15, "stalker", 0, 20)
running = True

while running:

    enemy.drawPlayer()
    enemy.update()
    healthBar.draw(stalker.health)

    box_group.update()
    box_group.draw(screen)
    stalker.drawPlayer()
    enemy.moveForEnemy()
    drawText('Количество пуль: ', (255, 255, 255), 10, 10)
    drawText('Здоровье: ', (255, 255, 255), 10, 40)
    for i in range(stalker.now_am):
        screen.blit(pygame.image.load('imges/icons/qbullet.png').convert_alpha(), (260 + (i * 10), 17))
    puly_group.update()
    puly_group.draw(screen)
    if stalker.live:
        if stalker.strelba:
            stalker.strelb()
        if stalker.isJump:
            stalker.proverka(2)
        elif stalker.go_left or stalker.go_right:
            stalker.proverka(1)
        else:
            stalker.proverka(0)
        stalker.move()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if stalker.live:
                if ev.key == pygame.K_a:
                    stalker.go_left = True
                if ev.key == pygame.K_d:
                    stalker.go_right = True
                if ev.key == pygame.K_w:
                    stalker.jump = True
                if ev.key == pygame.K_SPACE:
                    stalker.strelba = True

                if ev.key == pygame.K_ESCAPE:
                    running = False

        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_a:
                stalker.go_left = False
            if ev.key == pygame.K_d:
                stalker.go_right = False
            if ev.key == pygame.K_SPACE:
                stalker.strelba = False
    stalker.update()
    pygame.display.update()
    puly_group.update()
    puly_group.draw(screen)
    clock.tick(FPS)
    forFon()

pygame.quit()
