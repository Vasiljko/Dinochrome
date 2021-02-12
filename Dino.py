from header import *

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