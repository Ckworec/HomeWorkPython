from math import sqrt
from math import isclose
import random
from tkinter import *

INF = 1e18

class Point:
    def __init__(self, X = 0, Y = 0): #inite - метод для создания объекта(конструктор)
        self.X = X
        self.Y = Y

class Circle:
    def __init__(self, c = Point(), r = 0):
        self.C = c
        self.R = r

def distance(point1, point2):
    return sqrt((point1.X - point2.X) ** 2 + (point1.Y - point2.Y) ** 2)

def is_inside(circle, point): 
    return isclose(distance(circle.C, point), circle.R) or distance(circle.C, point) < circle.R

def circle_center_at_3_points(a, b, c): 

    zx = (a.Y - b.Y) * (c.X * c.X + c.Y * c.Y) + (b.Y - c.Y) * (a.X * a.X + a.Y * a.Y) + (c.Y - a.Y) * (b.X * b.X + b.Y * b.Y)
    zy = (a.X - b.X) * (c.X * c.X + c.Y * c.Y) + (b.X - c.X) * (a.X * a.X + a.Y * a.Y) + (c.X - a.X) * (b.X * b.X + b.Y * b.Y)
    z = 2 * (a.X - b.X) * (c.Y - a.Y) - 2 * (a.Y - b.Y) * (c.X-a.X)

    if isclose(z, 0):
        if max(distance(a, b), distance(b, c), distance(c, a)) == distance(a, b):
            c = circle_at_2_points(a, b)
            return c.C
        elif max(distance(a, b), distance(b, c), distance(c, a)) == distance(a, c):
            c = circle_at_2_points(a, b)
            return c.C
        elif max(distance(a, b), distance(b, c), distance(c, a)) == distance(c, b):
            c = circle_at_2_points(a, b)
            return c.C

    x0 = -zx / z
    y0 = zy / z

    return Point(x0, y0)

def circle_at_2_points(point1, point2): 
    C = Point((point1.X + point2.X) / 2.0, (point1.Y + point2.Y) / 2.0 ) 

    return Circle(C, distance(point1, point2) / 2.0)

def circle_at_3_points(point1, point2, point3):
    C = circle_center_at_3_points(point1, point2, point3)

    return Circle(C, distance(C, point1))

def proverka(circle, set_points):
    for point in set_points:
        if (not is_inside(circle, point)):
            return False
    
    return True

def trivial(set_points):
    assert(len(set_points) <= 3) #если условие не выполняется то дальше не идет

    counter = 0
    
    if not set_points: 
        return Circle()  
    
    elif (len(set_points) == 1): 
        return Circle(set_points[0], 0)  
    
    elif (len(set_points) == 2): 
        return circle_at_2_points(set_points[0], set_points[1]) 
    
    for i in range(3): 
        for j in range(i + 1,3): 
            c = circle_at_2_points(set_points[i], set_points[j]) 
            if proverka(c, set_points) == True: 
                circle = c
                counter = 1
    
    c = circle_at_3_points(set_points[0], set_points[1], set_points[2])
    
    if counter == 0 or c.R < circle.R:
        return c
    else:
        return circle

def welzl_helper(set_points, boundary_points, n): # n - количество необработанных точек
    if (n == 0 or len(boundary_points) == 3):# если мало точек(< 3) то всё просто
        return trivial(boundary_points)
    
    p = set_points[n - 1] 

    d = welzl_helper(set_points, boundary_points.copy(), n - 1) 

    if (is_inside(d, p)): # если "удаленная" точка лежит в полученном круге, то возвращаем этот круг
        return d
    
    boundary_points.append(p) # если не лежит, то эта точка должна лежать на границе круга

    return welzl_helper(set_points, boundary_points.copy(), n - 1) # запускаем с обновленной границей

def welzl(set_points): 
    set_copy = set_points.copy()
    random.shuffle(set_copy)
    return welzl_helper(set_copy, [], len(set_copy))

if __name__ == '__main__': 
    print("Enter the number of points: ", end = '')
    length = int(input())
    set = [Point(random.randint(0, 3) + random.random(), random.randint(0, 3) + random.random()) for i in range(length)]
    set.append(set[0])
    set.append(set[1])
    #set = [Point(0, 0), Point (1, 1), Point(2, 2)]
    for elem in set:
        if set.count(elem) != 1:
            while set.count(elem) != 1:
                set.remove(elem)

    print("\n\n")

    print("Set of points: ", end = '')

    for elem in set:
        print("(", elem.X, ", ", elem.Y, ")", end = ', ')
    print("\n\n")
    counter = 0
    flag = 0

    for elem1 in set:
        for elem2 in set:
            if counter == 0:
                min_circle2 = circle_at_2_points(elem1, elem2)
                if proverka(circle_at_2_points(elem1, elem2), set) == True:
                    rad2 = min_circle2.R
                    center2 = min_circle2.C
                    counter = 1
            else:
                min_circle2 = circle_at_2_points(elem1, elem2)
                if proverka(circle_at_2_points(elem1, elem2), set) == True and rad2 > min_circle2.R:
                    rad2 = min_circle2.R
                    center2 = min_circle2.C
            for elem3 in set:
                if proverka(circle_at_3_points(elem1, elem2, elem3), set) == True and flag == 0:
                    min_circle3 = circle_at_3_points(elem1, elem2, elem3)
                    rad3 = min_circle3.R
                    center3 = min_circle3.C
                    flag = 1
                else:
                    min_circle3 = circle_at_3_points(elem1, elem2, elem3)
                    if proverka(circle_at_3_points(elem1, elem2, elem3), set) == True and rad3 > min_circle3.R:
                        rad3 = min_circle3.R
                        center3 = min_circle3.C
                

    result = welzl(set)

    print("Center welzl: (", result.C.X, ", ",result.C.Y, ")   Radius: ", result.R, sep = '')
    
    if counter == 0 or rad3 < rad2:
        centerx = center3.X
        centery = center3.Y
        rad = rad3
        print("Center tryvial3: (", center3.X, ", ",center3.Y, ")   Radius: ", rad3, sep = '')
    else:
        centerx = center2.X
        centery = center2.Y
        rad = rad2
        print("Center tryvial2: (", center2.X, ", ",center2.Y, ")   Radius: ", rad2, sep = '')

    print(proverka(result, set))
    print(proverka(Circle(Point(centerx, centery), rad), set))

    root = Tk()
    c = Canvas(root, height = 600, width = 600, bg = "lightgrey")
    c.pack()

    for i in range(60):
        c.create_line(0, i * 10, 600, i * 10, fill="grey")
        c.create_line(i * 10, 0, i * 10, 600, fill="grey")

    c.create_line(0, 30 * 10, 600, 30 * 10, fill="black")
    c.create_line(30 * 10, 0, 30 * 10, 600, fill="black")


    for i in range(len(set)):
        c.create_oval(set[i].X * 50 + 300 - 2, -set[i].Y * 50 + 300 - 2, set[i].X * 50 + 300 + 2, -set[i].Y * 50 + 300 + 2, fill="black")

    c.create_oval(result.C.X * 50 + 300 - result.R * 50, -result.C.Y * 50 + 300 - result.R * 50, result.C.X * 50 + 300 + result.R * 50, -result.C.Y * 50 + 300 + result.R * 50, outline="red", width=1)

    c.create_oval(centerx * 50 + 300 - rad * 50, -centery * 50 + 300 - rad * 50, centerx * 50 + 300 + rad * 50, -centery * 50 + 300 + rad * 50, outline="green", width=1)
    
    c.update()

    input()
    root.destroy()
