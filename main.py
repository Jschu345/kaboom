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


class Sprite:
    def init(self, img, hitbox, posn):
        self._img = Image(img, hitbox)
        self._x = posn[0]
        self._y = posn[1]
    def posn(self):
        ##
        pass
    def center_of(self):
        ##
        pass
    def set_posn(self, posn):
        ##
        pass
    def show(self):
        ##
        pass


#initialize bomber

class Level:
    def __init__(self): #initialize
        self.level = 1
        self.bombStep = 3
        self.bomberStep = 5
        self.score = 0
        self.length = 8000
        self.levelStart = pygame.time.get_ticks()
        self.dropInterval = 500
    def levelUp(self): #for use after all bombs are caught
        self.score = self.score + self.level * 100
        self.level = self.level + 1
        self.bombstep = self.bombstep + 3/self.level
        self.length = self.length + 4000/self.level
        self.dropInterval = self.dropInterval - 25/(self.level/4)
        waitForClick()
        self.levelStart = pygame.time.get_ticks()
    def going(self): #returns false when no more bombs should be dropped
        if pygame.time.get_ticks() > self.levelStart + self.length:
            return False
        else:
            return True
    def scoreUp(self): #adds score -- use when bomb is caught
        self.score = self.score + self.level*10
    def restart(self):
        self.score = self.score - 200
        self.levelStart = pygame.time.get_ticks()



class Game:
    def __init__(self):
        self.bomber = Bomber()
        self.bucket = Bucket()
        self.level = Level()
        self.bombs = []
        self.lives = 3
        self.lastDrop = pygame.time.get_ticks()
        self.surf = DISPLAYSURF
    def moveAll(self):
        self.bomber.move(self.level.bomberStep)
        self.bomber.showOn(self.surf)
        self.bucket.move()
        self.bucket.showOn(self.surf)
        for index, bomb in enumerate(self.bombs):
            bomb.move(self.level.bombStep)
            bomb.showOn(self.surf)
            if (self.touching(bomb, bucket)):
                del self.bombs[index]
                self.level.scoreUp()
            elif bomb.img.hitbox[1] + bomb.posn()[1] > HEIGHT:
                self.kaboom()

    def touching(self, bom, buck):
        if (abs(bom.center()[0] - buck.center()[0]) < bom.img.hitbox[0]/2 + buck.img.hitbox[0]/2) and (abs(bom.center()[1] - buck.center()[1]) < (bom.img.hitbox[1]/2 + buck.img.hitbox[1]/2)):
            
            print("touching")
            return True
        else:
            print("x: ", abs(bom.center()[0] - buck.center()[0]), " thresh:", bom.img.hitbox[0]/2 + buck.img.hitbox[0], "\ny: ", abs(bom.center()[1] - buck.center()[1]), " thresh: ",bom.img.hitbox[1]/2 + buck.img.hitbox[1]/2)
            return False
    def kaboom(self):
        #lose a life, etc, then bomber.reset and levelRestart
        self.bombs = []
        self.bomber.reset()
        waitForClick()
        self.level.restart()
    def drop(self):
        self.bombs.append(Bomb(self.bomber))
        self.lastDrop = pygame.time.get_ticks()
    def update(self):
        canDrop = self.level.going()
        if canDrop and self.lastDrop + self.level.dropInterval < pygame.time.get_ticks():
            self.drop()
        self.moveAll()




 



class Bomber:
    def __init__(self):
        self.img = Image(pygame.image.load("img/bomber.png"), [64,64], [20, 40])
        self.x = int(WIDTH/2 - 32)
        self.y = SKY_HEIGHT - 48
        self.nextx = int(random.randrange(32,WIDTH - 32))
    def posn(self):
        return (self.x, self.y)
    def reset(self):
        self.x = int(WIDTH/2 - 32)
        self.y = SKY_HEIGHT - 48
        self.nextx = int(random.randrange(32,WIDTH - 32))
    def move(self, step):
            if abs(self.x - self.nextx) < step:
                self.nextx = int(random.randrange(32,WIDTH - 32))
            if self.x < self.nextx:
                self.x = self.x + step
            elif self.x > self.nextx:
                self.x = self.x - step
    def showOn(self, surf):
        surf.blit(self.img.img, self.posn())

#bucket initialization
class Bucket:
    numBuckets = 3
    x = int(WIDTH/2)
    bucketHeight = 16
    y = HEIGHT - (5 + 4*bucketHeight)

    img = Image(pygame.image.load("img/3buckets2.png"), [64,64], [49, 49])
    def posnList(self):
        return [self.x, self.y]
    def posn(self):
        return (self.x, self.y)
    def center(self):
        return (self.x + self.img.hitbox[0]/2, self.y + self.img.hitbox[1]/2)
    def move(self):
        ex, z = pygame.mouse.get_pos() 
        self.x = ex - self.img.hitbox[0]/2
    def showOn(self, surf):
        surf.blit(self.img.img, self.posn())

    def loseBucket(self):
        self.y = self.y + self.bucketHeight
        self.boomed = True
        self.img.hitbox = self.img.hitbox - [16,16]

bucket = Bucket()

#bombs initialization
class Bomb:
    def __init__(self, bomber):
        self.img = Image(pygame.image.load("img/bomb.png"),[64,64], [17, 22])
        self.x = bomber.x + self.img.hitbox[0]/2 + bomber.img.hitbox[0]/2
        self.y = bomber.y + self.img.hitbox[1]/2 + bomber.img.hitbox[1]/2
    def center(self):
        return (self.x + (self.img.hitbox[0]/2), self.y + (self.img.hitbox[1]/2))
    def posn(self):
        return (self.x, self.y)
    def posnList(self):
        return [self.x, self.y]
    def move(self, stp):
        self.y = self.y + stp
    def showOn(self, surf):
        surf.blit(self.img.img, self.posn())

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


game = Game() 

while True: #main loop
    resetScreen()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            print("quit")
            sys.exit()
    game.update()
    pygame.display.update()
    clock.tick(FPS)

