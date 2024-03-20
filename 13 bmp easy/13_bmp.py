import random
from PIL import Image, ImageDraw  

image = Image.open("osuzdayu.bmp") 
image2 = Image.open("iron_man.bmp")

draw = ImageDraw.Draw(image)

width, height = image.size 
width2, height2 = image2.size 
w = min(width, width2)
h = min(height, height2)
pix = image.load() 
pix2 = image2.load() 

for i in range(w):
	for j in range(h):
		#считаем яркость пиксела первого изображения
		a = pix2[i, j][0]
		b = pix2[i, j][1] 
		c = pix2[i, j][2]
		factor = (a + b + c) // 3

		#считаем яркость пиксела второго изображения
		a1 = pix[i, j][0]
		b1 = pix[i, j][1] 
		c1 = pix[i, j][2] 
		factor1 = (a1 + b1 + c1) // 3

		#изменяем яркость пикселей
		a1 = pix[i, j][0] + (factor - factor1)
		b1 = pix[i, j][1] + (factor - factor1)
		c1 = pix[i, j][2] + (factor - factor1)

		if (a1 < 0):
			a1 = 0
		if (b1 < 0):
			b1 = 0
		if (c1 < 0):
			c1 = 0
		if (a1 > 255):
			a1 = 255
		if (b1 > 255):
			b1 = 255
		if (c1 > 255):
			c1 = 255
		draw.point((i, j), (a1, b1, c1))

image.save("result.bmp", "BMP")

del draw