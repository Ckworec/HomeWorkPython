import sys
from PIL import Image, ImageDraw

imin = Image.open("input.bmp")

x1, y1 = imin.size

px1 = imin.load()

imout = Image.new("RGB", (x1, y1), (0, 0, 0))
draw = ImageDraw.Draw(imout)
pxout = imout.load()

size_square = 15
fractal = 0

for i in range(0, x1, size_square):
	for j in range(0, y1, size_square):
		if i + 2 * size_square - 1 < x1 and j + 2 * size_square - 1 < y1:
			for k in range(size_square):
				for t in range(size_square):
					r = px1[i + k, j + t][0]
					g = px1[i + k, j + t][1]
					b = px1[i + k, j + t][2]

					fractal += (r + g + b) // 3
		
			fractala = [0] * 3

			for k in range(size_square):
				for t in range(size_square):
					r = px1[i + size_square + k, j + t][0]
					g = px1[i + size_square + k, j + t][1]
					b = px1[i + size_square + k, j + t][2]

					fractala[0] += (r + g + b) // 3

			for k in range(size_square):
				for t in range(size_square):
					r = px1[i + k, j + size_square + t][0]
					g = px1[i + k, j + size_square + t][1]
					b = px1[i + k, j + size_square + t][2]

					fractala[1] += (r + g + b) // 3

			for k in range(size_square):
				for t in range(size_square):
					r = px1[i + size_square + k, j + size_square + t][0]
					g = px1[i + size_square + k, j + size_square + t][1]
					b = px1[i + size_square + k, j + size_square + t][2]

					fractala[2] += (r + g + b) // 3

			min_difference = min(fractala)

			index = fractala.index(min_difference)

			for k in range(2 * size_square):
				for t in range(2 * size_square):
					if index == 0:
						draw.point((i + k, j + t), (px1[i + size_square + k % size_square, j + t % size_square][0], px1[i + size_square + k % size_square, j + t % size_square][1], px1[i + size_square + k % size_square, j + t % size_square][2]))
					elif index == 1:
						draw.point((i + k, j + t), (px1[i + k % size_square, j + size_square + t % size_square][0], px1[i + k % size_square, j + size_square + t % size_square][1], px1[i + k % size_square, j + size_square + t % size_square][2]))
					else:
						draw.point((i + k, j + t), (px1[i + size_square + k % size_square, j + size_square + t % size_square][0], px1[i + size_square + k % size_square, j + size_square + t % size_square][1], px1[i + size_square + k % size_square, j + size_square + t % size_square][2]))
		else:
			for k in range(x1 - i):
				for t in range(y1 - j):
					draw.point((i + k, j + t), (px1[i + k, j + t][0], px1[i + k, j + t][1], px1[i + k, j + t][2]))

imout.save("out.bmp", "BMP")