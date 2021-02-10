import pygame
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

CACTUS_IMG_SMALL = pygame.transform.scale(pygame.image.load("imgs/cactus.png"),(CACTUS_WIDTH,CACTUS_HEIGHT))
CACTUS_IMG_BIG   = pygame.transform.scale(pygame.image.load("imgs/cactus.png"),(int(1.4*CACTUS_WIDTH),int(1.4*CACTUS_HEIGHT)))

CLOUD_IMG  = pygame.transform.scale(pygame.image.load("imgs/cloud.png"),(OBJECT_SIZE,OBJECT_SIZE))
GROUND_IMG = pygame.image.load("imgs/ground.png")

INITIAL_POS = GROUND_HEIGHT-DINO_IMG[0].get_height()+15


class Ptero:
    IMGS = PTERA_IMG
    FRAME = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.passed = False

    def move(self, vel):
        self.x -= vel



    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.FRAME:
            self.img = self.IMGS[0]
        elif self.img_count < 2 * self.FRAME:
            self.img = self.IMGS[1]
        else:
            self.img = self.IMGS[0]
            self.img_count = 0

        win.blit(self.img,(self.x,self.y))

    def collide(self, dino):
        dino_mask = dino.get_mask()
        ptero_mask = pygame.mask.from_surface(self.img)

        offset_x = round(self.x) - round(dino.x)
        offset_y = round(self.y) - round(dino.y)
        overlap = dino_mask.overlap(ptero_mask,(offset_x, offset_y))

        if overlap:
            return True
        return False