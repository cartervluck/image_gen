from PIL import Image

center = Image.open("background.png")

ringsFiles = ["ring6.png","ring5.png","ring4.png","ring3.png","ring2.png","ring1.png","ring0.png"]
ringSpeeds = [0.25, 1, -2, 1.5, 1, -2, 0] # num rotations per year

dayOfYear = 360 * int(input("What year is it? ")) + 30* (int(input("What month is it? "))-1) + int(input("What day is it? "))

for i in range(len(ringsFiles)):
  temp = Image.open(ringsFiles[i])
  temp = temp.rotate(angle=-ringSpeeds[i]*(dayOfYear-1296)) # 360 days per year
  center.paste(temp, (0,0), temp)

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
