import numpy as np
import math
import time
from util import points
from util import graphics

"""

[[0.1348590850830078, 2.7059173583984375, 10.860055446624756, 35.501171350479126, 120.68936848640442, 1129.4572291374207], 
[0.023562192916870117, 0.5626771450042725, 2.2164735794067383, 9.022538423538208, 20.19269299507141, 220.06193947792053], 
[0.015541791915893555, 0.34238338470458984, 1.515127182006836, 5.461269378662109, 13.125714540481567, 139.1292941570282]]

"""


class ConvexHull(object):

    def __init__(self, points):
        self.convex = None
        self.convex_list = []
        self.num_range = points.num_range
        self.points = points
        self.stack = np.arange(self.points.data.shape[0] * 2, dtype=float).reshape(self.points.data.shape[0], 2)

    # Enmerational Algorithm
    def enmeration(self):
        # Initial convex
        self.convex = None
        self.convex_list = []
        # Force to traverse all lines made by two points, judge if all points be its one side or not.
        for i in range(0, self.points.data.shape[0] - 1):
            for j in range(i + 1, self.points.data.shape[0]):
                x1 = self.points.data[i][0]
                y1 = self.points.data[i][1]
                x2 = self.points.data[j][0]
                y2 = self.points.data[j][1]
                flag = True
                side = 0
                for k in range(0, self.points.data.shape[0]):
                    x3 = self.points.data[k][0]
                    y3 = self.points.data[k][1]
                    if side == 0 and k != i and k != j:
                        if x1 * y2 + x3 * y1 + x2 * y3 - x3 * y2 - x2 * y1 - x1 * y3 > 0:
                            side = 1
                            break
                        else:
                            side = -1
                            break
                for k in range(0, self.points.data.shape[0]):
                    x3 = self.points.data[k][0]
                    y3 = self.points.data[k][1]
                    if k != i and k != j:
                        if (x1 * y2 + x3 * y1 + x2 * y3 - x3 * y2 - x2 * y1 - x1 * y3) * side > 0:
                            continue
                        else:
                            flag = False
                            break
                if flag:
                    self.convex_list.append([x1, y1])
                    self.convex_list.append([x2, y2])
        self.convex = np.array(self.convex_list)

    # Graham Scan Algorithm
    def graham_scan(self):
        # initial convex
        self.convex = None
        self.convex_list = []

        # Find the lowest point of points
        centerx = math.inf
        centery = math.inf
        pos = 0
        for i in range(0, self.points.data.shape[0]):
            if self.points.data[i][1] < centery:
                centerx = self.points.data[i][0]
                centery = self.points.data[i][1]
                pos = i
            elif self.points.data[i][1] == centery and self.points.data[i][0] < centerx:
                centerx = self.points.data[i][0]
                centery = self.points.data[i][1]
                pos = i

        # Make the lowest point be the position 0
        self.points.data[pos][0] = self.points.data[0][0]
        self.points.data[pos][1] = self.points.data[0][1]
        self.points.data[0][0] = centerx
        self.points.data[0][1] = centery

        # Sort the data points
        self.bubble_sort()
        # print(self.points.data)
        # self.quicksort(1, self.points.data.shape[0] - 1)
        # print(self.points.data)

        self.stack[0][0] = self.points.data[0][0]
        self.stack[0][1] = self.points.data[0][1]
        self.stack[1][0] = self.points.data[1][0]
        self.stack[1][1] = self.points.data[1][1]
        self.stack[2][0] = self.points.data[2][0]
        self.stack[2][1] = self.points.data[2][1]
        top = 2
        self.points.data = np.append(self.points.data, [self.points.data[0]], axis=0)
        for i in range(3, self.points.data.shape[0]):
            while self.multiply(self.stack[top - 1], self.stack[top], self.points.data[i]) <= 0:
                top -= 1
            self.stack[top + 1][0] = self.points.data[i][0]
            self.stack[top + 1][1] = self.points.data[i][1]
            top += 1
        # print(top)
        # print(self.stack)
        for i in range(0, top):
            self.convex_list.append([self.stack[i][0], self.stack[i][1]])
        self.convex = np.array(self.convex_list)
        self.points.data = np.delete(self.points.data, self.points.data.shape[0] - 1, axis=0)

    # Bubble Sort By X axis
    def bubble_sort(self):
        for i in range(1, self.points.data.shape[0]):
            for j in range(i + 1, self.points.data.shape[0]):
                if self.compare(self.points.data[i], self.points.data[j]) == 1:
                    temp0 = self.points.data[i][0]
                    temp1 = self.points.data[i][1]
                    self.points.data[i][0] = self.points.data[j][0]
                    self.points.data[i][1] = self.points.data[j][1]
                    self.points.data[j][0] = temp0
                    self.points.data[j][1] = temp1

    # Compare the x axis of two points, if equal then compare the distance to center points.
    def compare(self, pointx, pointy):
        side = self.multiply(self.points.data[0], pointx, pointy)
        if side < 0:
            return 1
        elif side == 0 and self.distance(self.points.data[0], pointx) < self.distance(self.points.data[0], pointy):
            return 1
        else:
            return -1

    def multiply(self, point0, pointx, pointy):
        return (pointx[0] - point0[0]) * (pointy[1] - point0[1]) - (pointy[0] - point0[0]) * (pointx[1] - point0[1])

    def distance(self, pointx, pointy):
        return math.sqrt((pointx[0] - pointy[0])**2 + (pointx[1] - pointy[1])**2)

    # Divide & Conquer quick convexhull
    def quick_convex_hull(self):
        self.coordinate_sort()

        points = []
        for i in range(0, self.points.data.shape[0]):
            points.append([])
            points[i].append(self.points.data[i][0])
            points[i].append(self.points.data[i][1])
        minimum = points[0]
        maximum = points[len(points) - 1]

        lefthull, righthull = self.divide_side(points, minimum, maximum)
        self.convex_list.append(minimum)
        self.convex_list.append(maximum)
        self.quickhullleft(lefthull, minimum, maximum)
        self.quickhullright(righthull, minimum, maximum)
        self.convex = np.array(self.convex_list)
        # print(self.convex)

    def divide_side(self, points, minimum, maximum):
        lefthull = []
        righthull = []
        for point in points:
            if (point != minimum) and (point != maximum):
                # Skip the dummy point
                if self.multiply(minimum, maximum, point) > 0:
                    lefthull.append(point)
                # Skip the dummy point
                if self.multiply(minimum, maximum, point) < 0:
                    righthull.append(point)
        return lefthull, righthull

    def quickhullleft(self, points, minimum, maximum):
        if len(points) == 0:
            return
        else:
            maxpoint = self.findmaxdistance(points, minimum, maximum)
            points.remove(maxpoint)
            self.convex_list.append(maxpoint)
            first_side, _ = self.divide_side(points, minimum, maxpoint)
            second_side, _ = self.divide_side(points, maxpoint, maximum)
            # Get the left part only (right part is dummy)
            self.quickhullleft(first_side, minimum, maxpoint)
            self.quickhullleft(second_side, maxpoint, maximum)

    def quickhullright(self, points, minimum, maximum):
        # Recurens stop where no point found
        if (len(points) == 0):
            return
        # Recurens continue
        else:
            maxpoint = self.findmaxdistance(points, minimum, maximum)
            points.remove(maxpoint)
            self.convex_list.append(maxpoint)
            _, first_side = self.divide_side(points, minimum, maxpoint)
            _, second_side = self.divide_side(points, maxpoint, maximum)
            # Getting the right part only(left part is dummy)
            self.quickhullright(first_side, minimum, maxpoint)
            self.quickhullright(second_side, maxpoint, maximum)

    def findmaxdistance(self, points, minimum, maximum):
        maxdistance = 0
        index = 0
        for i in range(0, len(points)):
            distance = self.calclinedistance(minimum, maximum, points[i])
            if distance > maxdistance:
                index = i
                maxdistance = distance
        return points[index]

    def calclinedistance(self, minimum, maximum, point):
        return abs((point[1] - minimum[1]) * (maximum[0] - minimum[0]) -
                   (maximum[1] - minimum[1]) * (point[0] - minimum[0]))

    def coordinate_sort(self):
        for i in range(0, self.points.data.shape[0]):
            for j in range(i + 1, self.points.data.shape[0]):
                if self.points.data[i][0] > self.points.data[j][0]:
                    temp0 = self.points.data[i][0]
                    temp1 = self.points.data[i][1]
                    self.points.data[i][0] = self.points.data[j][0]
                    self.points.data[i][1] = self.points.data[j][1]
                    self.points.data[j][0] = temp0
                    self.points.data[j][1] = temp1


if __name__ == "__main__":
    points1 = points.Points(100, [0, 100])
    convex = ConvexHull(points1)
    convex.enmeration()
    graphics.imshow_with_lines(convex, "Enmerational Algorithm")
    convex.graham_scan()
    graphics.imshow_with_lines(convex, "GrahamScan Algorithm")
    convex.quick_convex_hull()
    graphics.imshow_with_lines(convex, "Quick Convex Hull Algorithm")

    pointset = [100, 500, 1000, 2000, 3000, 10000]
    timeset = [[0 for j in range(len(pointset))] for i in range(3)]
    for i in range(len(pointset)):
        points1 = points.Points(pointset[i], [0, pointset[i]])
        convex = ConvexHull(points1)

        start = time.time()
        convex.enmeration()
        end = time.time()
        timeset[0][i] = end - start

        start = time.time()
        convex.graham_scan()
        end = time.time()
        timeset[1][i] = end - start

        start = time.time()
        convex.quick_convex_hull()
        end = time.time()
        timeset[2][i] = end - start

    print(timeset)

    graphics.imshow_performance(pointset, timeset,
                                ["Force Algorithm", "GrahamScan Algorithm", "Quick Convex Hull Algorithm"],
                                "Performance Analysis")




