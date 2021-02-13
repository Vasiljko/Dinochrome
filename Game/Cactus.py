from header import *

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
