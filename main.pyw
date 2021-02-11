from header import *
from Dino import Dino
from Ground import Ground
from Cactus import Cactus
from Ptero import Ptero

pygame.font.init()
pygame.display.set_caption("Dinochrome")
STAT_FONT = pygame.font.SysFont("bitstreamverasans", 16)

PTERO_POS = [180,150,100]

VEL = 8
MAX_VEL = 20
ACCELERATION = 0.01

def draw_window(win, dino, ground, pteros, cactuses, score):
    win.fill((255,255,255))

    ground.draw(win)
    dino.draw(win)

    for ptero in pteros:
        ptero.draw(win)

    for cactus in cactuses:
        cactus.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()

window = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock = pygame.time.Clock()

ground = Ground(GROUND_HEIGHT)
dino = Dino(40,GROUND_HEIGHT-DINO_IMG[0].get_height()+15)

cactuses = []
pteros = []

pteros.append(Ptero(2000,PTERO_POS[round(random.randint(0,2))]))
pteros.append(Ptero(3000,PTERO_POS[round(random.randint(0,2))]))

cactuses.append(Cactus(1000,GROUND_HEIGHT-CACTUS_IMG_SMALL[0].get_height()+15))
cactuses.append(Cactus(1800,GROUND_HEIGHT-CACTUS_IMG_SMALL[0].get_height()+15))
score = 0
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dino.jump()
            if event.key == pygame.K_DOWN:
                dino.is_ducking = True
            else:
                dino.is_ducking = False
        if event.type == pygame.KEYUP:
            dino.is_ducking = False



    for ptero in pteros:
        remove_pteros = []
        add_ptero = False

        if ptero.collide(dino):
            print(ptero)
            quit()


        if not ptero.passed and ptero.x < dino.x:
            ptero.passed = True
            add_ptero = True

        if ptero.x + ptero.img.get_width() < 0:
            remove_pteros.append(ptero)

        if add_ptero:
            pteros.append(Ptero(round(random.randint(2000,3000)),PTERO_POS[round(random.randint(0,2))]))

        for p in remove_pteros:
            pteros.remove(p)

    for cactus in cactuses:
        remove_cactuses = []
        add_cactus = False

        if cactus.collide(dino):
            print(cactus)
            quit()


        if not cactus.passed and cactus.x < dino.x:
            cactus.passed = True
            add_cactus = True

        if cactus.x + cactus.img.get_width() < 0:
            remove_cactuses.append(cactus)

        if add_cactus:
            cactuses.append(Cactus(round(random.randint(1600,2000)),GROUND_HEIGHT-CACTUS_IMG_SMALL[0].get_height()+15))

        for p in remove_cactuses:
            cactuses.remove(p)

    dino.move()
    ground.move(VEL)

    for cactus in cactuses:
        cactus.move(VEL)

    for ptero in pteros:
        ptero.move(VEL)
    score+=1
    VEL = min(VEL+ACCELERATION,MAX_VEL)
    draw_window(window, dino, ground, pteros, cactuses, score//6)
