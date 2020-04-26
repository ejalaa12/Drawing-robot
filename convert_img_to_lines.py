import cv2
import numpy as np

# ========================================================================
# Method 1
# ========================================================================

def distance(P1, P2):
    """
    This function computes the distance between 2 points defined by
     P1 = (x1,y1) and P2 = (x2,y2)
    """

    return ((P1[0] - P2[0])**2 + (P1[1] - P2[1])**2) ** 0.5


def optimized_path(coords, start=None):
    """
    This function finds the nearest point to a point
    coords should be a list in this format coords = [ [x1, y1], [x2, y2] , ...]

    """
    if start is None:
        start = coords[0]
    pass_by = coords
    path = [start]
    pass_by.remove(start)
    while pass_by:
        nearest = min(pass_by, key=lambda x: distance(path[-1], x))
        path.append(nearest)
        pass_by.remove(nearest)
    return path


# ========================================================================
# Method 2
# ========================================================================
def sort_to_form_line(unsorted_list):
    """
    Given a list of neighbouring points which forms a line, but in random order, sort them to the correct order
    IMPORTANT: Each point must be a neighbour (8-point sense) to a least one other point!
    """
    sorted_list = [unsorted_list.pop(0)]

    while len(unsorted_list) > 0:
        i = 0
        while i < len(unsorted_list):
            if are_neighbours(sorted_list[0], unsorted_list[i]):
                #neighbours at front of list
                sorted_list.insert(0, unsorted_list.pop(i))
            elif are_neighbours(sorted_list[-1], unsorted_list[i]):
                #neighbours at rear of list
                sorted_list.append(unsorted_list.pop(i))
            else:
                i = i+1
    return sorted_list

def are_neighbours(pt1, pt2):
    """
    Check if pt1 and pt2 are neighbours, in the 8-point sense
    pt1 and pt2 has integer coordinates
    """
    return (np.abs(pt1[0]-pt2[0]) < 2) and (np.abs(pt1[1]-pt2[1]) < 2)
# ========================================================================
# CORE
# ========================================================================
def extract_connected(img):
    img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    bw = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)[1]
    ret, labels = cv2.connectedComponents(bw)
    return ret, labels


def extract_lines(contour, method=1):
    lines = []
    for i in range(1, n):   # 0 is not the contour
        X, Y = np.vstack(np.where(contour==i))
        if method == 1:
            # method 1
            line = optimized_path(zip(X,Y))
        elif method == 2:
            # method 2
            line = sort_to_form_line(zip(X,Y))
        lines.append(line)
    return lines

def compare():
    from time import time
    n, contour_labeled = extract_connected('cat-icon.png')

    s_time = time()
    extract_lines(contour_labeled, method=1)
    print 'Method 1 took: ', time()-s_time

    print '=' * 30
    s_time = time()
    extract_lines(contour_labeled, method=2)
    print 'Method 2 took: ', time()-s_time

    print 'Done'

if __name__ == '__main__':
    img_name = 'img_test/table_me_small.jpeg'
    n, contour_labeled = extract_connected(img_name)
    lines = extract_lines(contour_labeled, method=1)
    with open('{}.traj'.format(img_name.split('.')[0]), 'w') as f:
        for l in lines:
            for p in l:
                f.write('{},{}\n'.format(p[0], p[1]))
            f.write('-\n')
