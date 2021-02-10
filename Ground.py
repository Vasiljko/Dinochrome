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


class Ground:
    IMG = GROUND_IMG
    WIDTH = IMG.get_width()

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH


    def move(self, vel):
        self.x1 -= vel
        self.x2 -= vel

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))