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

#initialize bomber
class Bomber:
    img = pygame.image.load("img/bomber.png")
    x = int(WIDTH/2 - 32)
    y = SKY_HEIGHT - 48
    nextx = int(random.randrange(32,WIDTH - 32))
    step = 5
    bombs = []
    lastDrop = clock.get_time()
    dropInterval = 500
    def dropBomb(self):
        if pygame.time.get_ticks() - self.lastDrop > self.dropInterval:
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
        if abs(self.x - self.nextx) < self.step:
            self.nextx = int(random.randrange(32,WIDTH - 32))
        if self.x < self.nextx:
            self.x = self.x + self.step
        elif self.x > self.nextx:
            self.x = self.x - self.step
        toDelete = []
        for index, bomb in enumerate(self.bombs):
            print(len(self.bombs)) 
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
    y = HEIGHT - int(HEIGHT/4)
    boomed = False
    img = pygame.image.load("img/3buckets.png")
    def posnList(self):
        return [self.x - 32, self.y]
    def posn(self):
        return (self.x - 32, self.y)
    
    def move(self):
        self.x, z = pygame.mouse.get_pos()
    
    def showOn(self, surf):
        surf.blit(self.img, self.posn())

    def boom(self):
        
        self.boomed = True

bucket = Bucket()

#bombs initialization
class Bomb:
    def __init__(self, bomber):
        self.x = bomber.x
        self.y = bomber.y+32
    step = 3
    img = pygame.image.load("img/bomb.png")
    def posn(self):
        return (self.x, self.y)
    def posnList(self):
        return [self.x, self.y]
    def move(self):
        self.y = self.y + self.step
        if abs(self.posnList()[0] - bucket.posnList()[0]) < 32 and (bucket.posnList()[1] - self.posnList()[1]) < 32:
            del self
            return "del"
        elif self.y > HEIGHT:
            #game over   
            bucket.boom()
            return "boom"
    def showOn(self, surf):
        surf.blit(self.img, self.posn())


lives = 3
def loseLife():
    global lives, bucket, bomber
    DISPLAYSURF.fill((255, 0, 0))
    pygame.display.update()
    bomber.reset()
    cont = False
    bucket.boomed = False
    if lives == 2:
        bucket.img = pygame.image.load("img/2buckets.png")
    elif lives == 1:
        bucket.img = pygame.image.load("img/1bucket.png")
    while cont == False:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                cont = True
            if event.type==QUIT:
                pygame.quit()
                print("quit")
                sys.exit()
    

while True: #main loop
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
    clock.tick(FPS)

