import pygame
import random
pygame.init()


WIN_WIDTH = 900
WIN_HEIGHT = 500
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

CACTUS_IMG_SMALL = [pygame.transform.scale(pygame.image.load("imgs/cactus1.png"),(CACTUS_WIDTH,CACTUS_HEIGHT)),
                    pygame.transform.scale(pygame.image.load("imgs/cactus2.png"),(2*CACTUS_WIDTH,CACTUS_HEIGHT))]

CACTUS_IMG_BIG = [pygame.transform.scale(pygame.image.load("imgs/cactus1.png"),(int(1.4*CACTUS_WIDTH),int(1.4*CACTUS_HEIGHT))),
                    pygame.transform.scale(pygame.image.load("imgs/cactus2.png"),(int(2*1.4*CACTUS_WIDTH),int(1.4*CACTUS_HEIGHT)))]

CLOUD_IMG  = pygame.transform.scale(pygame.image.load("imgs/cloud.png"),(OBJECT_SIZE,OBJECT_SIZE))
GROUND_IMG = pygame.image.load("imgs/ground.png")

INITIAL_POS = GROUND_HEIGHT-DINO_IMG[0].get_height()+15


class Cactus:
    IMGS = [CACTUS_IMG_SMALL,CACTUS_IMG_BIG]

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type_of_cactus = round(random.randint(0,1))
        self.number_of_cactuses = round(random.randint(0,1))
        self.img = self.IMGS[self.type_of_cactus][self.number_of_cactuses]
        self.passed = False

    def move(self,vel):
        self.x -= vel

    def draw(self, win):
        if self.type_of_cactus == 0:
            win.blit(self.img,(self.x,self.y))
        else:
            win.blit(self.img,(self.x,self.y-15))

    def collide(self, dino):
        dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.img)

        offset_x = round(self.x) - round(dino.x)
        offset_y = round(self.y) - round(dino.y)
        overlap = dino_mask.overlap(cactus_mask,(offset_x, offset_y))

        if overlap:
            return True
        return False