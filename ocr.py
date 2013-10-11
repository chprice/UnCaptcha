from PIL import Image
import sys

def touching(a,b):
	return ((a[0]-1 == b[0]) or (a[0] == b[0]) or (a[0]+1 == b[0])) and ((a[1]-1 == b[1]) or (a[1] == b[1]) or (a[1]+1 == b[1]))
def numNeighbors(p):
    count = 0
    for a in [-1,0,1]:
        for b in [-1,0,1]:
            try:
                if pixdata[p[0]+a, p[1]+b][0] == 0:
                    count += 1
            except IndexError:
                pass
    return count

#cluster must have at least one large, continous section (bold)
#average black to white must be relatively high for a block of size N

if(len(sys.argv[1:]) != 3):
    print "Usage is: ocr.py imageName minClusters minNeighbors"
title = sys.argv[1:][0] # test.png
minCluster = int(sys.argv[1:][1]) #20
minNeighbors = int(sys.argv[1:][2]) #5
img = Image.open(title) # Your image here!
img = img.convert("RGBA")

pixdata = img.load()

# Make the letters bolder for easier recognition

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][0] < 45:
            pixdata[x, y] = (0, 0, 0, 255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][1] < 50:
            pixdata[x, y] = (0, 0, 0, 255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][2] > 0:
            pixdata[x, y] = (255, 255, 255, 255)



for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if(pixdata[x,y][0] == 0):
            if(numNeighbors([x,y]) < minNeighbors):
                pixdata[x,y] = (255, 255, 255, 255)

clusters = []
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        touched = False
        if(pixdata[x,y][0] == 0):
            for cluster in clusters:
                if(touched):
                    break
                for point in cluster:
                    if(touching((x,y), point)):
                        cluster.append((x,y))
                        touched = True
                        break
            if (not touched):
                clusters.append([(x,y)])

for cluster in clusters:
    if len(cluster) < minCluster:
        for point in cluster:
            pixdata[point[0],point[1]] = (255, 255, 255, 255)
    else:
        for point in cluster:
            pixdata[point[0],point[1]] = (0, 0, 0, 255)
                
img.save(title+"_clean.png", "PNG")
