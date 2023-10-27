from math import sqrt 
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
    return distance(circle.C, point) <= circle.R 

def circle_center_at_3_points(a, b, c): #https://ru.wikipedia.org/wiki/Описанная_окружность#.D0.9F.D0.BE.D0.BB.D0.BE.D0.B6.D0.B5.D0.BD.D0.B8.D0.B5_.D1.86.D0.B5.D0.BD.D1.82.D1.80.D0.B0_.D0.BE.D0.BF.D0.B8.D1.81.D0.B0.D0.BD.D0.BD.D0.BE.D0.B9_.D0.BE.D0.BA.D1.80.D1.83.D0.B6.D0.BD.D0.BE.D1.81.D1.82.D0.B8
    #D = 2 * ((point1.X * point2.Y + point1.Y * point3.X + point2.X * point3.Y - point3.X * point2.Y - point2.X * point1.Y - point1.X * point3.Y))
    #x0 = ((point1.X ** 2 + point1.Y ** 2) * point2.Y + point1.Y * (point3.X ** 2 + point3.Y ** 2) + (point2.X ** 2 + point2.Y ** 2) * point3.Y - (point3.X ** 2 + point3.Y ** 2) * point2.Y - point3.Y * (point1.X ** 2 + point1.Y ** 2) - point1.Y * (point2.Y ** 2 + point2.Y ** 2)) / D
    #y0 = -((point1.X ** 2 + point1.Y ** 2) * point2.X + point1.X * (point3.X ** 2 + point3.Y ** 2) + (point2.X ** 2 + point2.Y ** 2) * point3.X - (point3.X ** 2 + point3.Y ** 2) * point2.X - point3.X * (point1.X ** 2 + point1.Y ** 2) - point1.X * (point2.X ** 2 + point2.Y ** 2)) / D
    
    #B = bx * bx + by * by 
    #C = cx * cx + cy * cy 
    #D = bx * cy - by * cx 
    #return Point((cy * B - by * C) / (2 * D), (bx * C - cx * B) / (2 * D))

    zx = (a.Y - b.Y) * (c.X * c.X + c.Y * c.Y) + (b.Y - c.Y) * (a.X * a.X + a.Y * a.Y) + (c.Y - a.Y) * (b.X * b.X + b.Y * b.Y)
    zy = (a.X - b.X) * (c.X * c.X + c.Y * c.Y) + (b.X - c.X) * (a.X * a.X + a.Y * a.Y) + (c.X - a.X) * (b.X * b.X + b.Y * b.Y)
    z = 2 * (a.X - b.X) * (c.Y - a.Y) - 2 * (a.Y - b.Y) * (c.X-a.X)

    x0 = -zx / (z + 0.00001)
    y0 = zy / (z + 0.00001)

    return Point(x0, y0)

def circle_at_2_points(point1, point2): 
    C = Point((point1.X + point2.X) / 2.0, (point1.Y + point2.Y) / 2.0 ) 

    return Circle(C, distance(point1, point2) / 2.0 )

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

    if not set_points : 
        return Circle()  
    
    elif (len(set_points) == 1) : 
        return Circle(set_points[0], 0)  
    
    elif (len(set_points) == 2) : 
        return circle_at_2_points(set_points[0], set_points[1]) 
    
    for i in range(3): 
        for j in range(i + 1,3): 

            c = circle_at_2_points(set_points[i], set_points[j]) 
            if (proverka(c, set_points)): 
                return c 
            
    return circle_at_3_points(set_points[0], set_points[1], set_points[2])

def welzl_helper(set_points, boundary_points, n): # n - количество необработанных точек
    if (n == 0 or len(boundary_points) == 3):# если мало точек(< 3) то всё просто
        return trivial(boundary_points)
    
    i = random.randint(0, n - 1) # рандомно выбираем точку для "удаления"
    p = set_points[i] 

    set_points[i], set_points[n - 1] = set_points[n - 1], set_points[i] # перемещаем в конец

    d = welzl_helper(set_points, boundary_points.copy(), n - 1) 

    if (is_inside(d, p)): # если "удаленная" точка лежит в полученном круге, то возвращаем этот круг
        return d
    
    boundary_points.append(p) # если не лежит, то эта точка должна лежать на границе круга

    return welzl_helper(set_points, boundary_points.copy(), n - 1) # запускаем с обновленной границей
#насколько я понимаю при возвращении множество граничных из функции сбрасывается и берется то которое было на итерацию раньше

def welzl(set_points): 
    set_copy = set_points.copy()
    random.shuffle(set_copy)
    return welzl_helper(set_copy, [], len(set_copy))

if __name__ == '__main__': 
    print("Enter the number of points: ", end = '')
    length = int(input())
    set = [Point(random.randint(0, 3) + random.random(), random.randint(0, 3) + random.random()) for i in range(length)]

    print("\n\n")

    print("Set of points: ", end = '')

    for elem in set:
        print("(", elem.X, ", ", elem.Y, ")", end = ', ')
    print("\n\n")

    result = welzl(set)

    print("Center: (", result.C.X, ", ",result.C.Y, ")   Radius: ", result.R, sep = '')

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

    c.update()

    input()
    root.destroy()