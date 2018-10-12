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
        return [ self._y self._x ]
    def center_of(self):
        return [ self._x + self._img.hitbox[0]/2, self.y + self._img.hitbox[1]/2 ]
        pass
    def set_posn(self, posn):
        self._x = posn[0]
        self._y = posn[1]
    def set_center(self, posn):
        self._x = posn[0] - self._img.hitbox[0]/2
        self._y = posn[1] - self._img.hitbox[1]/2
    def show(self):
        surf.blit(self._img.img, self.posn())


#initialize bomber

class Level:
    def __init__(self): #initialize
        self._level = 1
        self._bomb_step = 3
        self._bomber_step = 5
        self._score = 0
        self._length = 8000
        self._level_start = pygame.time.get_ticks()
        self._drop_interval = 500
        self._last_drop = 0
    def level_up(self): #for use after all bombs are caught
        self._score = self._score + self._level * 100
        self._level = self._level + 1
        self._bomb_step = self.bomb_step + BOMB_STEP_INCREMENT if self.bomb_step < MAX_BOMB_STEP
        self._length = self.length + 4000/self.level
        self._drop_interval = self.drop_interval - DROP_INTERVAL_DECREMENT
    def wait_and_start(self):
        waitForClick()
        self._level_start = pygame.time.get_ticks()
    def is_going(self): #returns false when no more bombs should be dropped
        if pygame.time.get_ticks() > self._level_start + self._length:
            return False
        else:
            return True
    def score_up(self): #adds score -- use when bomb is caught
        self.score = self.score + self.level*10
    def should_drop():
        if self._last_drop + self._drop_interval < pygame.time.get_ticks():
            self._last_drop = pygame.time.get_ticks()
            return True
        else:
            return False
    def bomb_step(self):
        return self._bomb_step
    def bomber_step(self):
        return self._bomber_step
    def score(self):
        return self._score



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
        self.bomber.move(self.level.bomber_step)
        self.bucket.move()
        for index, bomb in enumerate(self.bombs):
            if bomb.move(self.level.bomb_step()) == CAUGHT:
                self.level.score_up()
                del bombs[index]
            elif bomb.move(self.level.bomb_step()) == KABOOM:
                #switch screen, delete bombs, and restart level and lose a bucket
                self.kaboom()
    

    #add (drop) bomb?
    #stop dropping?
    #levelup
    #lose a life / kaboom? -> restart level
    #move them
    #check for catches and drops
            

    




 



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

