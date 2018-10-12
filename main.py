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
    def __init__(self, pygImg, hitbox):
        self.img = pygImg
        self.hitbox = hitbox


class Sprite:
    def __init__(self, img, hitbox, posn):
        self._img = Image(img, hitbox)
        self._x = posn[0]
        self._y = posn[1]
    def posn(self):
        return [ self._x, self._y ]
    def center_of(self):
        return [ self._x + self._img.hitbox[0]/2, self._y + self._img.hitbox[1]/2 ]
    def set_posn(self, posn):
        self._x = posn[0]
        self._y = posn[1]
    def set_center(self, posn):
        self._x = posn[0] - self._img.hitbox[0]/2
        self._y = posn[1] - self._img.hitbox[1]/2
    def show(self):
        DISPLAYSURF.blit(self._img.img, self.posn())
    def hitbox(self):
        return self._img.hitbox
    def is_touching(self, obj2):
        if abs(self.center_of()[0] - obj2.center_of()[0]) < (self.hitbox()[0]/2 + obj2.hitbox()[0]/2) and  abs(self.center_of()[1] - obj2.center_of()[1]) < (self.hitbox()[1]/2 + obj2.hitbox()[1]/2):
            return True
        else:
            return False


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
        self._bomb_step = self._bomb_step + BOMB_STEP_INCREMENT if self._bomb_step < MAX_BOMB_STEP else self._bomb_step
        self._bomber_step = self._bomber_step + BOMBER_STEP_INCREMENT if self._bomber_step < MAX_BOMBER_STEP else self._bomber_step
        self._length = self._length + 4000/self._level
        self._drop_interval = self._drop_interval - DROP_INTERVAL_DECREMENT
    def wait_and_start(self):
        waitForClick()
        self._level_start = pygame.time.get_ticks()
    def is_going(self): #returns false when no more bombs should be dropped
        return pygame.time.get_ticks() < self._level_start + self._length
    def score_up(self): #adds score -- use when bomb is caught
        self._score = self._score + self._level*10
    def should_drop(self):
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


    def update(self):
        resetScreen()
        self.move_all()
        if self.level.is_going():
            self.drop()
        self.update_screen()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                print("quit")
                sys.exit()
        if not(self.level.is_going()) and self.bombs == []:
            resetScreen()
            self.move_all()
            if self.level.is_going():
                self.drop()
            self.update_screen()
            self.level.level_up()
            self.level.wait_and_start()
        """else:
            print(self.bombs)
            print(self.level.is_going())"""


    def update_screen(self):
        pygame.display.update()
    def move_all(self):
        if self.level.is_going():
            self.bomber.move(self.level.bomber_step())
        else:
            self.bomber.show()
        self.bucket.move() 
        for index, bomb in enumerate(self.bombs):
            ret = bomb.move(self.level.bomb_step())
            if ret == KABOOM:
                self.kaboom()
            elif bomb.is_touching(self.bucket):
                self.level.score_up()
                del self.bombs[index]
                
    def drop(self):
        if self.level.should_drop():
            self.bombs.append(Bomb(self.bomber.center_of()))

    def kaboom(self):
        print("kaboom")
        self.bomber.reset()
        self.lives = self.lives - 1
        if self.lives == 0:
            print("lost")
        self.bombs = []
        #change screen
        self.level.wait_and_start()
        #lose life and restart level
    

    #add (drop) bomb?
    #stop dropping?
    #levelup
    #lose a life / kaboom? -> restart level
    #move them
    #check for catches and drops // do in Bomb.move()
            


class Bomber(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load("img/bomber.png"), [20, 40], [int(WIDTH/2 - 32), SKY_HEIGHT - 48])
        self._nextx = int(random.randrange(32,WIDTH - 32))
    def reset(self):
        self._x = int(WIDTH/2 - 32)
        self._y = SKY_HEIGHT - 48
        self._nextx = int(random.randrange(32,WIDTH - 32))
    def move(self, step):
        if abs(self._x - self._nextx) < step:
            self._nextx = int(random.randrange(32,WIDTH - 32))
        if self._x < self._nextx:
            self._x = self._x + step
        elif self._x > self._nextx:
            self._x = self._x - step
        self.show()

#bucket initialization
class Bucket(Sprite):
    def __init__(self):
        self._bucket_height = 16
        Sprite.__init__(self, pygame.image.load("img/3buckets2.png"), [49,49], [int(WIDTH/2), HEIGHT - (5 + 4*self._bucket_height)])
        self._num_buckets = 3
       
    def move(self):
        ex, z = pygame.mouse.get_pos() 
        self._x = ex - self._img.hitbox[0]/2
        self.show()

    def loseBucket(self):
        self._y = self._y + self._bucket_height
        self._img.hitbox[1] = self._img.hitbox[1] -self._bucket_height



#bombs initialization
class Bomb(Sprite):
    def __init__(self, center):
        Sprite.__init__(self, pygame.image.load("img/bomb.png"), [17,22], [center[0], center[1]] )
    def move(self, stp):
        self._y = self._y + stp
        if self._y + self.hitbox()[1] > HEIGHT:
            return KABOOM
        self.show()
        




game = Game()
while True: #main loop
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            print("quit")
            sys.exit()
    game.update()
    clock.tick(FPS)


