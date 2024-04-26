'''
Поворот на угол альфа
'''

import sys
from PIL import Image
import math 

# rotating a vector to point
def rotate(vector, theta):
    return [vector[0] * math.cos(theta) + vector[1] * math.sin(theta), vector[0] * (-math.sin(theta)) + vector[1] * math.cos(theta)]

# function to rotate an image
def photo_rotating(im_, theta):
    im = Image.open(im_)
    x, y = im.size
    px = im.load()

    # image vertex coordinates
    l_up = [0, 0]
    l_down = [0, y]
    r_up = [x, 0]
    r_down = [x, y]

    # new image vertex coordinates
    rotated_l_up = rotate(l_up, theta)
    rotated_l_down = rotate(l_down, theta)
    rotated_r_up = rotate(r_up, theta)
    rotated_r_down = rotate(r_down, theta)

    min_x = min(rotated_l_up[0], rotated_l_down[0], rotated_r_up[0], rotated_r_down[0])
    min_y = min(rotated_l_up[1], rotated_l_down[1], rotated_r_up[1], rotated_r_down[1])

    max_x = max(rotated_l_up[0], rotated_l_down[0], rotated_r_up[0], rotated_r_down[0])
    max_y = max(rotated_l_up[1], rotated_l_down[1], rotated_r_up[1], rotated_r_down[1])


    # size new image
    w = round(max_x - min_x) + 1
    h = round(max_y - min_y) + 1

    new_00 = [-min_x, -min_y]

    im2 = Image.new("RGB", (w + 1, h + 1), (0, 0, 0))
    px2 = im2.load()

    # rotate image
    for i in range(x):
        for j in range(y):
            vector = rotate([i,j], theta)
            [i_new, j_new] = [new_00[0] + vector[0], new_00[1] + vector[1]]
            r = px[i, j][0]
            g = px[i, j][1]
            b = px[i, j][2]
            px2[round(i_new), round(j_new)] = r, g, b

    im2.save(sys.argv[2])


def main():
    theta = math.radians(int(sys.argv[3]))
    photo_rotating(sys.argv[1], theta)
    

if __name__ == "__main__":
    main()
