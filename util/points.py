import random
import numpy as np


class Points(object):

    def __init__(self, num, num_range):
        self.data = np.arange(num * 2, dtype=float).reshape(num, 2)
        self.num_range = num_range
        for i in range(0, num):
            for j in range(0, 2):
                self.data[i][j] = self.generator(num_range)

    def generator(self, num_range):
        return float(random.uniform(num_range[0], num_range[1]))
