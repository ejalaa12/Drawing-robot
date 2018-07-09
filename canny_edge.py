import cv2
import matplotlib.pyplot as plt
import numpy as np

# Import the image
img_file = '/Users/ejalaa/Development/Fun/Turtle Plays/Drawing roboto/Lenna.png'
img = cv2.imread(img_file)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Extract edges with Canny detector
edges = cv2.Canny(gray, 100, 200)

# Remove all single pixels
kernel = np.zeros((5,5), np.uint8)
kernel[2,2] = 1
edges2 = cv2.erode(edges, kernel)

# Show plot with original image, edges, and drawing
plt.figure()

plt.subplot(141)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))   # numpy converts to BGR instead or RGB
plt.title('Original')

plt.subplot(142)
plt.imshow(gray, cmap='gray')
plt.title('Grayscale')

plt.subplot(143)
plt.imshow(edges, cmap='gray')
plt.title('Canny edges')

plt.subplot(144)
plt.imshow(edges2)
plt.title('Canny after erosion')

plt.show()
