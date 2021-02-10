import pygame
pygame.init()


WIN_WIDTH = 900
WIN_HEIGHT = 300
OBJECT_SIZE = 50

CACTUS_WIDTH = 20
CACTUS_HEIGHT = 40

GROUND_HEIGHT = WIN_HEIGHT - 80

DINO_IMG = [pygame.transform.scale(pygame.image.load("imgs/dino1.png"),(OBJECT_SIZE,OBJECT_SIZE)),
            pygame.transform.scale(pygame.image.load("imgs/dino2.png"),(OBJECT_SIZE,OBJECT_SIZE)),
            pygame.transform.scale(pygame.image.load("imgs/dino3.png"),(OBJECT_SIZE,OBJECT_SIZE)),
            pygame.transform.scale(pygame.image.load("imgs/dino4.png"),(OBJECT_SIZE,OBJECT_SIZE)),
            pygame.transform.scale(pygame.image.load("imgs/dino5.png"),(OBJECT_SIZE,OBJECT_SIZE))]

DUCK_IMG = [pygame.transform.scale(pygame.image.load("imgs/dino_duck1.png"),(OBJECT_SIZE,OBJECT_SIZE)),
             pygame.transform.scale(pygame.image.load("imgs/dino_duck2.png"),(OBJECT_SIZE,OBJECT_SIZE))]

PTERA_IMG = [pygame.transform.scale(pygame.image.load("imgs/ptera1.png"),(OBJECT_SIZE,OBJECT_SIZE)),
             pygame.transform.scale(pygame.image.load("imgs/ptera2.png"),(OBJECT_SIZE,OBJECT_SIZE))]

CACTUS_IMG_SMALL = pygame.transform.scale(pygame.image.load("imgs/cactus.png"),(CACTUS_WIDTH,CACTUS_HEIGHT))
CACTUS_IMG_BIG   = pygame.transform.scale(pygame.image.load("imgs/cactus.png"),(int(1.4*CACTUS_WIDTH),int(1.4*CACTUS_HEIGHT)))

CLOUD_IMG  = pygame.transform.scale(pygame.image.load("imgs/cloud.png"),(OBJECT_SIZE,OBJECT_SIZE))
GROUND_IMG = pygame.image.load("imgs/ground.png")

INITIAL_POS = GROUND_HEIGHT-DINO_IMG[0].get_height()+15


class Dino:
    IMGS = DINO_IMG
    DUCK = DUCK_IMG
    FRAME = 2

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img_count = 0
        self.vel = 0
        self.height = self.y
        self.img = self.IMGS[0]
        self.g = 2
        self.is_ducking = False
        self.can_jump = True


    def jump(self):
        if self.can_jump == True:
            self.vel = -26
            self.can_jump = False

    def move(self):
        dist = self.y + self.vel

        if self.is_ducking:
            self.g = 7
        else:
            self.g = 2.5

        self.vel += self.g
        if dist <= INITIAL_POS:
            self.y += self.vel
        else:
            self.y = INITIAL_POS
            self.can_jump = True

    def draw(self, win):
        self.img_count += 1

        if self.can_jump:
            if not self.is_ducking:
                if self.img_count < self.FRAME:
                    self.img = self.IMGS[2]
                elif self.img_count < 2*self.FRAME:
                    self.img = self.IMGS[3]
                else:
                    self.img = self.IMGS[0]
                    self.img_count = 0
            else:
                if self.img_count < self.FRAME:
                    self.img = self.DUCK[0]
                elif self.img_count < 2*self.FRAME:
                    self.img = self.DUCK[1]
                else:
                    self.img = self.DUCK[0]
                    self.img_count = 0
        else:
            self.img = self.IMGS[0]
            self.img_count = 0


        win.blit(self.img,(self.x,self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)