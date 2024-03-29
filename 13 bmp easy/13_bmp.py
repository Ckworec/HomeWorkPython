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
		r = pix2[i, j][0]
		g = pix2[i, j][1] 
		b = pix2[i, j][2]
		factor = (r + g + b) // 3

		#считаем яркость пиксела второго изображения
		r1 = pix[i, j][0]
		g1 = pix[i, j][1] 
		b1 = pix[i, j][2] 
		factor1 = (r1 + g1 + b1) // 3

		#изменяем яркость пикселей
		r1 = round(pix[i, j][0] * (factor / factor1))
		g1 = round(pix[i, j][1] * (factor / factor1))
		b1 = round(pix[i, j][2] * (factor / factor1))

		if (r1 < 0):
			r1 = 0
		if (g1 < 0):
			g1 = 0
		if (b1 < 0):
			b1 = 0
		if (r1 > 255):
			r1 = 255
		if (g1 > 255):
			g1 = 255
		if (b1 > 255):
			b1 = 255
		draw.point((i, j), (r1, g1, b1))

image.save("result.bmp", "BMP")

del draw