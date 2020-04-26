import cv2
import matplotlib.pyplot as plt
import numpy as np


def edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    bw = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)[1]
    return edges


def neighboors_idx(data, line, col):
    if line == 0:
        neighboors_l = [0, 1]
    elif line == data.shape[0]-1:
        neighboors_l = [-1, 0]
    else:
        neighboors_l = [-1, 0, 1]
    if col == 0:
        neighboors_c = [0, 1]
    elif col == data.shape[1]-1:
        neighboors_c = [-1, 0]
    else:
        neighboors_c = [-1, 0, 1]
    neighboors = []
    for l in neighboors_l:
        for c in neighboors_c:
            if l!=0 or c!=0:
                neighboors.append([line+l, col+c])
    return neighboors


def neighboors(data, line, col):
    neighboors = []
    for n in neighboors_idx(data, line, col):
        neighboors.append(data[tuple(n)])
    return neighboors


def connected(data, start_line, start_col, already_done=None):
    if already_done is None:
        already_done = np.zeros(data.shape)
    for l, c in neighboors_idx(data, start_line, start_col):
        if data[l, c] and not already_done[l, c]:
            already_done[l, c] = True
            connected(data, l, c, already_done)
    return already_done


# Import the image
img_file = '/Users/ejalaa/Development/Fun/Turtle Plays/Drawing roboto/Lenna.png'
img = cv2.imread(img_file)
bw = edges(img)
bool = bw != 0
pool = bool.copy()
drawing = np.zeros(pool.shape) != 0
ret, labels = cv2.connectedComponents(bw)
print ret, labels.shape, drawing.shape

# file for saving trajectory
traj_file = open('traj', 'w')

plt.figure()
plt.subplot(151)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('original')

plt.subplot(152)
plt.imshow(bool, cmap='gray')
plt.title('Black & White')

plt.subplot(153)
pool_obj = plt.imshow(pool, cmap='gray')
plt.title('Drawing Pool')

plt.subplot(154)
# important to set min and max otherwise the cmap limits will be calculated
# automatically and set to be 0,0 (because we the data is only zeros)
drawing_obj = plt.imshow(drawing, cmap='gray', vmin=0, vmax=1)
plt.title('Drawing live')

plt.subplot(155)
conn_obj = plt.imshow(drawing, cmap='gray', vmin=0, vmax=1)
plt.title('Connected')

# # while pool is not empty
# while np.any(pool):
#     tmp = pool.copy()
#     # get first white element (or random one for more fun)
#     white_elements = np.where(tmp == True)
#     # idx = 0
#     idx = np.random.randint(0, white_elements[0].size)
#     starting_point = [white_elements[0][idx], white_elements[1][idx]]
#     # look for all connected elements
#     conn = connected(tmp, starting_point[0], starting_point[1])
#     # for single pixel you get an empty connected tree so draw it alone or infinite loop
#     if np.where(conn==True)[0].size == 0:
#         print tmp[starting_point[0], starting_point[1]], neighboors(tmp, starting_point[0], starting_point[1])
#         conn[starting_point[0], starting_point[1]] = True
#     # draw them together by using tree search
#     X, Y =  np.where(conn==True)
#     traj_file.write('--\n')
#     for x, y in zip(X.tolist(), Y.tolist()):
#         traj_file.write('{}\t{}\n'.format(x, y))
#     # update drawing
#     drawing = np.logical_or(drawing, conn)
#     # remove them from pool
#     pool = np.logical_not(np.logical_or(np.logical_not(tmp), conn!=0))
#     drawing_obj.set_data(drawing)
#     pool_obj.set_data(pool)
#     plt.draw()
#     plt.pause(0.01)
#     print np.where(pool==True)[0].shape

for i in range(np.max(labels)):
    part = labels==i
    conn_obj.set_data(part)
    plt.draw()
    plt.pause(0.01)

plt.show()
print 'Finished'
