import numpy as np
from math import hypot
from scipy.spatial import distance

np.set_printoptions(precision=2)


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.child = None
        self.processed = False

    def to(self, other):
        return hypot(self.x-other.x, self.y-other.y)

    def __repr__(self):
        return "P({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def has_parent(self):
        return self.parent is not None

    def has_child(self):
        return self.child is not None

    # def processed(self):
    #     return self.has_parent() and self.has_child()


def closest(p0, pts):
    # print ">> Looking closest of", p0
    # print ">> From list", pts
    x = map(lambda p: p.x, pts)
    y = map(lambda p: p.y, pts)
    pts_array = np.array([x, y]).T
    dists = distance.cdist([(p0.x, p0.y)], pts_array)
    # print ">> Distances:", dists[0]
    idx = dists.argmin()
    return pts[idx], dists.flatten()[idx]


def link(current_point, point_list, distance_threshold=1.0, link_list=[]):
    # print "+ Current point: {}".format(current_point)
    # print "+ PointList {}".format(point_list)
    if current_point.processed:
        # stop if we encounter an already processed point
        return link_list
    else:
        current_point.processed = True
    if len(point_list) == 0:
        return link_list
    # copy list
    point_list_copy = point_list[:]
    # remove current point
    point_list_copy.remove(current_point)
    # and add to link list
    link_list.append(current_point)
    # find closest point and distance
    c, d = closest(current_point, point_list_copy)
    # print "+ Closest: {}({})".format(c, d)
    if d <= distance_threshold:
        return link(c, point_list_copy, distance_threshold, link_list)
    return link_list


def find_links(points, distance_threshold=1):
    links = []
    for i, p in enumerate(points):
        # print "---"
        # print "Processing", i, p,
        if p.processed:
            # print "already done"
            continue
        l = []
        res = link(p, points, distance_threshold, l)
        p.processed = True
        links.append(res)
    return links


if __name__ == '__main__':

    x = [1,2,3,4,4,4,3,2,1]
    y = [0,0,0,0,1,6,6,6,6]

    points = map(lambda x: Point(*x), zip(x, y))
    find_links(points, 1)
