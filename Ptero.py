from header import *

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