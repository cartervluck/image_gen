#create a map :)
import random
import time
import math
from PIL import Image
import sys
import numpy as np

args = []

#pull args
for i, arg in enumerate(sys.argv):
    args.append(arg)


DOTHING = True

directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
directions += [(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,2)]

# wrapper for repetition
while DOTHING:
    x_size = int(input("X Dimension (default 100): "))
    y_size = int(input("Y Dimension (default 100): "))
    
    # define interpolation function for parallelized processing
    # interpolates a single pixel as an atomic process for a core to run
    # set a pixel on the expanded image to 1 if at least 7 pixels in the
    # immediate 5x5 square are in a pixel with a 1 when mapped onto
    # original image
    if "--parallel" in args:
        from numba import cuda
        @cuda.jit
        def interpolatePixel(out,a,rowSize,max):
            z = cuda.grid(1)
            i = z % rowSize
            j = int((z-i) / rowSize)
            count = 0
            # iterate over all pixels in a 5 by 5 around target pixel
            for k in range(-2,3):
                for l in range(-2,3):
                    # check if target pixel in source image is a 1
                    if (i + k >= 0) and (j + l >= 0) and (i + k) < rowSize and int((j + l)*rowSize/4) + int((i + k)/2) < max:
                        if a[int((j + l)*rowSize/4) + int((i + k)/2)] == 1:
                            count += 1
            if count >= 7 or a[int((j)*rowSize/4) + int((i)/2)] == 1:
                out[z] = 1
            else: out[z] = 2

    def checkzeros(a):
        for j in a:
            if 0 in j:
                return True
        return False

    def printmap(a,coord):
        for j in range(len(a)):
            k = ["X" if (i,j) == coord else "▓" if a[j][i] == 1 else " " for i in range(len(a[j]))]
            print(" ".join(k))

    arr = [[0 for i in range(x_size)] for j in range(y_size)] # index by y coord then x coord

    border = min(x_size,y_size)/5

    # seeds island with a random rectangle
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

    # create circular "cut-outs" of the land, so that it's not just a rectangle
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
    
    # Spiral out from the island, organically "growing" landmass
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
    
    # save an intermediate (low-res) copy of the island
    if "--intermediate" in args:
        im2 = Image.new("RGBA",(x_size,y_size))
        for j in range(len(arr)):
            for i in range(len(arr[j])):
                if arr[j][i] == 1: im2.putpixel((i,j),(0,0,0,255))
                else: im2.putpixel((i,j),(255,255,255,0))
        im2.save(f"imgs3/img0.png")

    # begin interpolation, up to a certain target resolution (2^11 pixel width)
    counter = 1
    while len(arr) <= 2**11:
        time_start = time.perf_counter() # benchmarking

        if "--parallel" in args:
            # pass the target matrix to the graphics card for fast access (as 1D-list)
            l2 = cuda.to_device(np.array([0 for i in range(4 * x_size * y_size)]))
            # flatten matrix
            a_1 = [arr[i][j] for i in range(y_size) for j in range(x_size)]
            # pass old flattened matrix to graphics card for fast access
            a_1d = cuda.to_device(np.array(a_1,order = 'C'))
            # create a new process for every target pixel
            interpolatePixel[len(l2),1](l2,a_1d,4*x_size,len(a_1d))
            # un-flatten
            l2 = np.reshape(l2.copy_to_host(),(2*x_size,-1),'C')
        else:
            # create target matrix
            l2 = [[0 for i in range(2 * x_size)] for j in range(2 * y_size)]
            for i in range(2*y_size):
                for j in range(2*x_size):
                    # find corrosponding pixel in original matrix for given pixel in target
                    corr_x = math.floor(j/2)
                    corr_y = math.floor(i/2)
                    count = 0
                    # count number of 1s in the immediate surroundings
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
        
        # benchmark
        if "--benchmark" in args: print(f"operation finished in {time.perf_counter() - time_start} seconds")
        # save intermediate copy
        if "--intermediate" in args:
            if "--logs" in args: print(f"saving to imgs3/img{counter}.png")
            im2 = Image.new("RGBA",(x_size,y_size))
            for j in range(len(l2)):
                for i in range(len(l2[j])):
                    if l2[j][i] == 1: im2.putpixel((i,j),(0,0,0,255))
                    else: im2.putpixel((i,j),(255,255,255,0))
            im2.save(f"imgs3/img{counter}.png")
            if "--logs" in args: print(f"saved to imgs3/img{counter}.png with dimensions {len(l2)} by {len(l2[0])}")
            counter += 1

    #save final copy
    im2 = Image.new("RGBA",(x_size,y_size))
    for j in range(len(l2)):
        for i in range(len(l2[j])):
            if l2[j][i] == 1: im2.putpixel((i,j),(0,0,0,255))
            else: im2.putpixel((i,j),(255,255,255,0))
    im2.save("imgs3/" + "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for z in range(10)]) + ".png")
    DOTHING = False

