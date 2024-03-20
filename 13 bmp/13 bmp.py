import random
from PIL import Image, ImageDraw  
 
image = Image.open("iron_man.bmp") 
image2 =  Image.open("osuzdayu.bmp") 
draw = ImageDraw.Draw(image)  
width = image.size[0]  
height = image.size[1]  
width2 = image2.size[0]  
height2 = image2.size[1]  
w = min(width, width2)
h = min(height, height2)	
pix = image.load() 
pix2 = image2.load() 

factor = 0
factor1 = 0

for i in range(w):
	for j in range(h):
		a = pix2[i, j][0] #stallone 
		b = pix2[i, j][1] 
		c = pix2[i, j][2]
		factor += (a+b+c)//3
		a1 = pix[i, j][0] #arni 
		b1 = pix[i, j][1] 
		c1 = pix[i, j][2] 
		factor1 += (a1 + b1 + c1) // 3
print("brightness of pic1: ",factor1)
print("brightness of pic2: ",factor)

for i in range(w):
	for j in range(h):
		a1 = pix[i, j][0] + (factor - factor1) // (w * h)
		b1 = pix[i, j][1] + (factor - factor1) // (w * h)
		c1 = pix[i, j][2] + (factor - factor1) // (w * h)
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

image.save("ans.bmp", "BMP")

del draw