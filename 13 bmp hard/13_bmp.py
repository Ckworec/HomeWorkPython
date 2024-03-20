import sys
from PIL import Image, ImageDraw

imin = Image.open("input.bmp")

x1, y1 = imin.size

px1 = imin.load()

imout = Image.new("RGB", (x1, y1), (0, 0, 0))
pxout = imout.load()

for i in range(x1):
	for j in range(y1):
		r1 = px1[i, j][0]
		g1 = px1[i, j][1]
		b1 = px1[i, j][2]
		compression = 0.9 #сжатие
		n = 1 - compression
		
		if i < x1 // 2:
			i1 = int(i ** n / (x1 // 2) ** (n - 1))
			i2 = int((i + 1) ** n / (x1 // 2) ** (n - 1))
			
			for k in range(i1, i2):
				if k < x1 // 2:
					pxout[k, j] = r1, g1, b1
		else:
			i1 = int((x1 - i - 1) ** n / (x1 // 2) ** (n - 1))
			i2 = int((x1 - i) ** n / (x1 // 2) ** (n - 1))
			
			for k in range(x1 - i2,x1 - i1):
				pxout[k, j] = r1, g1, b1

imout.save("out.bmp", "BMP")