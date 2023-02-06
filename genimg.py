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

