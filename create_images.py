import pygame
from PIL import Image

white = (0, 255, 255)

X = 400
Y = 400

img = Image.open("imgs/cactuses.png").convert("LA")
width, height = img.size


img_size = []
K = 3
for i in range(K):
    img_size.append((0,0,(i+1)*width//5-5*(i+1),height))

img_crop = []
for i in range(K):
    img_crop.append(img.crop(img_size[i]))

for i in range(K):
    s = "cactus"+str(i+1)
    img_crop[i].save("imgs/"+s+".png")
