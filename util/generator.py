import random

"""
x:          the number of total vertex
f:          the number of total subset
num_range:  the value range of x vertex set, default = int
"""


class Generator(object):

    def __init__(self, x, f, num_range):
        self.num_range = num_range
        self.x = self.vertex_generate(x)
        self.f = self.set_generate(f)
        # print(sorted(self.x))
        # if f <= 100:
            # print(self.f)

    def vertex_generate(self, x):
        all_vertex = range(self.num_range[0], self.num_range[1] + 1)
        return random.sample(all_vertex, x)

    def set_generate(self, f):
        subsets = []
        temp_vertex_set = set(self.x.copy())
        temp_select_set = set([])
        while len(temp_vertex_set) > 20 and len(subsets) < f:
            if len(subsets) == 0:
                subset = set(random.sample(temp_vertex_set, 20))
                temp_vertex_set -= subset
                temp_select_set = subset
                subsets.append(tuple(subset))
            else:
                subset_size = random.sample([n for n in range(1, 21)], 1)[0]
                select = random.sample([n for n in range(1, subset_size + 1)], 1)[0]
                subset = set(random.sample(temp_vertex_set, select))
                temp_vertex_set -= subset
                subset |= set(random.sample(temp_select_set, subset_size - select))
                temp_select_set |= subset
                subsets.append(tuple(subset))
        subsets.append(tuple(temp_vertex_set))
        # print(len(subsets))
        while len(subsets) < f:
            subset_size = random.sample([n for n in range(1, 21)], 1)[0]
            subset = set(random.sample(set(self.x), subset_size))
            subsets.append(tuple(subset))
        # print(len(subsets))
        return subsets


if __name__ == "__main__":

    genetor = Generator(30, 30, [1, 30])
    for i in range(len(genetor.f)):
        print(i, "= ", genetor.f[i])
    # print(genetor.f)
    print(sorted(genetor.x))