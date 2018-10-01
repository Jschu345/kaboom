import pygame, sys, random
from pygame.locals import *
from constants import *
print("began")

pygame.init()
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Kaboom")
clock = pygame.time.Clock()


def resetScreen():
    DISPLAYSURF.fill((120,80,80))
    pygame.draw.rect(DISPLAYSURF,(0,0,255), (0,0,WIDTH, SKY_HEIGHT))


class Image:
    def __init__(self, pygImg, size, hitbox):
        self.img = pygImg
        self.hitbox = hitbox
        self.size = size


#initialize bomber

class Game:
    score = 0
    level = 0
    numIntervals = 7
    intervals=[500, 450, 400, 350, 300, 250, 200]
    interval = intervals[0]
    time = 8000
    levelStart = pygame.time.get_ticks()
    go = True
    bombStep = 3
    def levelUp(self):
        self.level = self.level + 1
        self.score = self.score + self.level*50
        self.time = self.time + 4000/self.level
        if self.level < self.numIntervals:
            self.interval = self.intervals[self.level]
        bomber.step = bomber.step + 1
        if self.level % 2 == 0 and self.level < 12:
            self.bombStep = self.bombStep + 1
    def update(self):
        if (self.levelStart + self.time < pygame.time.get_ticks()):
            bomber.shouldBomb = False
            if len(bomber.bombs) == 0:
                self.go = False

    def startLevel(self):
        self.levelStart = pygame.time.get_ticks()

game = Game()  



class Bomber:
    img = pygame.image.load("img/bomber.png")
    x = int(WIDTH/2 - 32)
    y = SKY_HEIGHT - 48
    nextx = int(random.randrange(32,WIDTH - 32))
    step = 5
    bombs = []
    bombCount = 0
    lastDrop = pygame.time.get_ticks()
    dropInterval = 500
    shouldBomb = True
    def dropBomb(self):
        if pygame.time.get_ticks() - self.lastDrop > game.interval and self.shouldBomb:
            self.bombs.append( Bomb(self) )
            self.lastDrop = pygame.time.get_ticks()
    def posn(self):
        return (self.x, self.y)

    def reset(self):
        del self.bombs[:]
        self.bombs=[]
        self.x = int(WIDTH/2 - 32)
        self.y = SKY_HEIGHT - 48
        self.nextx = int(random.randrange(32,WIDTH - 32))
    def move(self):
        if self.shouldBomb:
            if abs(self.x - self.nextx) < self.step:
                self.nextx = int(random.randrange(32,WIDTH - 32))
            if self.x < self.nextx:
                self.x = self.x + self.step
            elif self.x > self.nextx:
                self.x = self.x - self.step
        toDelete = []
        for index, bomb in enumerate(self.bombs):
            if bomb.move() == "del":
                toDelete.append(index)
        for ind in toDelete:
            del self.bombs[ind]

    def showOn(self, surf):
        surf.blit(self.img, self.posn())
        for bomb in self.bombs:
            bomb.showOn(surf)

bomber = Bomber()

#bucket initialization
class Bucket:
    numBuckets = 3
    x = int(WIDTH/2)
    bucketHeight = 16
    y = HEIGHT - (5 + 4*bucketHeight)
    boomed = False
    img = Image(pygame.image.load("img/3buckets2.png"), [64,64], [49, 49])
    def posnList(self):
        return [self.x, self.y]
    def posn(self):
        return (self.x, self.y)

    def move(self):
        ex, z = pygame.mouse.get_pos() 
        self.x = ex
    def showOn(self, surf):
        surf.blit(self.img.img, self.posn())

    def boom(self):
        self.y = self.y + self.bucketHeight
        self.boomed = True

bucket = Bucket()

#bombs initialization
class Bomb:
    def __init__(self, bomber):
        self.img = Image(pygame.image.load("img/bomb.png"),[64,64], [17, 22])
        self.x = bomber.x + self.img.hitbox[0]/2
        self.y = bomber.y + self.img.hitbox[1]/2
        
    step = game.bombStep
    def posn(self):
        return (self.x, self.y)
    def posnList(self):
        return [self.x, self.y]
    def move(self):
        self.y = self.y + self.step
        if abs(bucket.posnList()[0] - self.posnList()[0]) < (self.img.hitbox[0]+bucket.img.hitbox[0] /2) and (bucket.posnList()[1] - self.posnList()[1]) < self.img.hitbox[1]:
            del self
            return "del"
        elif self.y + self.img.hitbox[1] > HEIGHT:
            #game over
            bucket.boom()
            return "boom"
    def showOn(self, surf):
        surf.blit(self.img.img, self.posn())


lives = 3
def loseLife():
    global lives, bucket, bomber
    DISPLAYSURF.fill((255, 0, 0))
    pygame.display.update()
    bomber.reset()
    bucket.boomed = False
    if lives == 2:
        bucket.img.img = pygame.image.load("img/2buckets2.png")
    elif lives == 1:
        bucket.img.img = pygame.image.load("img/1bucket2.png")
    waitForClick()
    game.startLevel()

def waitForClick():
    cont = False
    while cont == False:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                cont = True
            if event.type==QUIT:
                pygame.quit()
                print("quit")
                sys.exit()

while True: #main loop
    while game.go == True:
        resetScreen()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                print("quit")
                sys.exit()
        bucket.move()
        bucket.showOn(DISPLAYSURF)
        bomber.move()
        bomber.showOn(DISPLAYSURF)
        bomber.dropBomb()
        pygame.display.update()
        if bucket.boomed == True:
            lives = lives - 1
            if lives == 0:
                pygame.quit()
                print('lost')
                sys.exit()
                #game over
            else:
                loseLife()
                #lose a life
        game.update()
        clock.tick(FPS)
    waitForClick()
    game.levelUp()
    game.startLevel()
    game.go = True
    bomber.shouldBomb = True

