import numpy as np
import cv2
from skimage.measure import approximate_polygon, find_contours
import turtle
from alg import find_links, Point
from matplotlib import pyplot as plt
from bezier import bezier_curve


def turtle_contour(c):
    turtle.up()
    for (x, y) in c:
        turtle.goto(y, x)
        turtle.down()
    turtle.up()


def edges_to_lines(e):
    for x, y in zip(*np.nonzero(e)):
        turtle.goto(y, x)


def imfill(im_in):
    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.

    th, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV);

    # Copy the thresholded image.
    im_floodfill = im_th.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv

    return im_out

# Load image
image_path = "images/test.png"
img = cv2.imread(image_path, 0)
cv2.imshow('Original Image', img)
print img.shape

# Find Contours
edges = cv2.Canny(img, 127, 255, apertureSize=3)
cv2.imshow('Edges', edges)

# Find Contours with skimage
contours = find_contours(edges, 0)
print "Contours length:", len(contours)
# print "First Contour:", contours[0]
# for c in contours:
#     turtle_contour(c)

# Fill holes
edges_fill = imfill(img)
cv2.imshow('filled edges', edges_fill)
# Get coordinates of all non-zero values from the edge result
x, y = np.nonzero(edges)
points = map(lambda x: Point(*x), zip(x, y))
paths = find_links(points, 10)
print "Found", len(paths), "paths"
# turtle.speed(0)
# for path in paths:
#     turtle.up()
#     turtle.goto(path[0].x, path[0].y)
#     turtle.down()
#     for point in path:
#         turtle.goto(point.x, point.y)

for path in paths:
    xvals, yvals = bezier_curve(path, nTimes=1000)
    plt.plot(yvals, -xvals)

# Wait for display
cv2.waitKey()

plt.show()
print 'Done'
