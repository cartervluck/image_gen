#create a map :)
import random
import time
import math
from PIL import Image

DOTHING = True

directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
directions += [(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,2)]

while DOTHING:
    x_size = int(input("X Dimension (default 100): "))
    y_size = int(input("Y Dimension (default 100): "))

    def checkzeros(a):
        for j in a:
            if 0 in j:
                return True
        return False

    def printmap(a,coord):
        for j in range(len(a)):
            k = ["X" if (i,j) == coord else "▓" if a[j][i] == 1 else " " for i in range(len(a[j]))]
            print(" ".join(k))

    arr = [[0 for i in range(x_size)] for j in range(y_size)] #index by y coord then x coord

    border = min(x_size,y_size)/5

    x_rand1 = random.randint(border,x_size-border)
    y_rand1 = random.randint(border,y_size-border) # get random x,y coordinate to seed at
    x_rand2 = random.randint(border,x_size-border)
    y_rand2 = random.randint(border,y_size-border) # get random x,y coordinate to seed at
    x_randMin = min(x_rand1, x_rand2)
    x_randMax = max(x_rand1, x_rand2)
    y_randMin = min(y_rand1, y_rand2)
    y_randMax = max(y_rand1, y_rand2)
    for j in range(y_randMin, y_randMax+1):
        for i in range(x_randMin, x_randMax+1):
            arr[j][i] = 1

    for i in range(20):
        point = (random.randint(border, x_size-border-1),random.randint(border, y_size-border-1))
        for j in range(point[1]-int(border/3),point[1]+int(border/3)):
            for k in range(point[0]-int(border/3),point[0]+int(border/3)):
                if (point[0]-k)**2 + (point[1]-j)**2 <= (border/3)**2 and arr[j][k] == 1:
                    arr[j][k] = 2

    vectors = [(0,1),(1,0),(0,-1),(-1,0)]
    vectors2 = vectors + [(1,1),(1,-1),(-1,-1),(-1,1)]
    lookat = (x_randMin, y_randMin-1)
    currentdir = 1

    while checkzeros(arr):
        if arr[lookat[1]][lookat[0]] == 0:
            pick = vectors[(1+currentdir)%4]
            if random.randint(1,3) != 1:
                pick = vectors2[random.randint(0,7)]
            try:
                if arr[lookat[1] + pick[1]][lookat[0] + pick[0]] == 1:
                    arr[lookat[1]][lookat[0]] = 1
                else:
                    arr[lookat[1]][lookat[0]] = 2
            except IndexError: pass
        if arr[lookat[1] + vectors[(currentdir + 1) % 4][1]][lookat[0] + vectors[(currentdir + 1) % 4][0]] == 0 or (currentdir == 0 and lookat[1] == y_size-1) or (currentdir == 1 and lookat[0] == x_size-1) or (currentdir == 2 and lookat[1] == 0) or (currentdir == 3 and lookat[0] == 0):
            currentdir += 1
            currentdir = currentdir % 4
        lookat = (min(max(0,lookat[0] + vectors[currentdir][0]), x_size-1), min(max(0,lookat[1] + vectors[currentdir][1]),y_size-1))

    counter = 1
    while len(arr) <= 2**11:
        l2 = [[0 for i in range(2 * x_size)] for j in range(2 * y_size)]

        for i in range(2*y_size):
            for j in range(2*x_size):
                corr_x = math.floor(j/2)
                corr_y = math.floor(i/2)
                count = 0
                for k in directions:
                    try:
                        if arr[math.floor((i + k[1])/2)][math.floor((j + k[0])/2)] == 1:
                            count += 1
                    except IndexError:
                        pass
                if count >= 7: l2[i][j] = 1
                    
        x_size = 2 * x_size
        y_size = 2 * y_size
        arr = l2
        
        print(f"saving to imgs3/img{counter}.png")
        im2 = Image.new("RGBA",(x_size,y_size))
        for j in range(len(l2)):
            for i in range(len(l2[j])):
                if l2[j][i] == 1: im2.putpixel((i,j),(0,0,0,255))
                else: im2.putpixel((i,j),(255,255,255,0))
        im2.save(f"imgs3/img{counter}.png")
        counter += 1

    im2 = Image.new("RGBA",(x_size,y_size))
    for j in range(len(l2)):
        for i in range(len(l2[j])):
            if l2[j][i] == 1: im2.putpixel((i,j),(0,0,0,255))
            else: im2.putpixel((i,j),(255,255,255,0))
    im2.save("imgs3/" + "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for z in range(10)]) + ".png")
    DOTHING = False

