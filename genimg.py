from PIL import Image
import sys
import math

args = []

for i, arg in enumerate(sys.argv):
  args.append(arg)

center = Image.open("background.png")

ringsFiles = ["ring6.png","ring5.png","ring4.png","ring3.png","ring2.png","ring1.png","ring0.png"]
tzFiles = ["timezones6","timezones5","timezones4","timezones3","timezones2","timezones1","timezones0"]
ringSpeeds = [0.25, 1, -2, 1.5, 1, -2, 0] # num rotations per year

if "--clean" in args:
  for i in range(len(tzFiles)):
    tzFiles[i] = tzFiles[i] + "_clean.png"
else:
  for i in range(len(tzFiles)):
    tzFiles[i] = tzFiles[i] + ".png"

y = int(input("What year is it? "))
m = int(input("What month is it? "))-1
d = int(input("What day is it? "))

dayOfYear = 360 * y + 30* m + d

for i in range(len(ringsFiles)):
  temp = Image.open(ringsFiles[i])
  temp = temp.rotate(angle=-ringSpeeds[i]*(dayOfYear-1296)) # 360 days per year
  center.paste(temp, (0,0), temp)
  if "--timezones" in args:
    temp1 = Image.open(tzFiles[i])
    temp1 = temp1.rotate(angle=-ringSpeeds[i]*(dayOfYear-1296)) # 360 days per year
    center.paste(temp1,(0,0),temp1)

if "--sun" in args:
  sun = Image.open("sun.png")
  n = 30 * m + d
  n = abs(135 - n) % 360
  ratio = 1-(n/180 * 0.3)
  sun = sun.resize((int(ratio * 2048), int(ratio * 2048)))
  center.paste(sun,(1024-int(ratio * 1024),1024-int(ratio * 1024)),sun)

center.save("out.png")

'''

Image.rotate(angle, resample=0, expand=0, center=None, translate=None, fillcolor=None)[source]
Returns a rotated copy of this image. This method returns a copy of this image, rotated the given number of degrees counter clockwise around its centre.

Parameters
angle – In degrees counter clockwise.

resample – An optional resampling filter. This can be one of PIL.Image.NEAREST (use nearest neighbour), PIL.Image.BILINEAR (linear interpolation in a 2x2 environment), or PIL.Image.BICUBIC (cubic spline interpolation in a 4x4 environment). If omitted, or if the image has mode “1” or “P”, it is set to PIL.Image.NEAREST. See Filters.

expand – Optional expansion flag. If true, expands the output image to make it large enough to hold the entire rotated image. If false or omitted, make the output image the same size as the input image. Note that the expand flag assumes rotation around the center and no translation.

center – Optional center of rotation (a 2-tuple). Origin is the upper left corner. Default is the center of the image.

translate – An optional post-rotate translation (a 2-tuple).

fillcolor – An optional color for area outside the rotated image.

Returns
An Image object.

This rotates the input image by theta degrees counter clockwise:

from PIL import Image

im = Image.open("hopper.jpg")

# Rotate the image by 60 degrees counter clockwise
theta = 60
# Angle is in degrees counter clockwise
im_rotated = im.rotate(angle=theta)

'''

'''
from PIL import Image

import numpy as np

img = Image.open("data_mask_1354_2030.png")

background = Image.open("background_1354_2030.png")

background.paste(img, (0, 0), img)
background.save('how_to_superimpose_two_images_01.png',"PNG")
'''
