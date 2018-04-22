from util import generator
import pulp
import time

"""
[[0.0010025501251220703, 0.0034754276275634766, 0.024565696716308594, 0.12875795364379883, 0.4296834468841553, 2.177133560180664], 
[0.2601943016052246, 0.6241929531097412, 3.1645920276641846, 13.585261344909668, 57.49008822441101, 514.7037694454193]]
"""

class SetCover(object):

    def __init__(self, generator):
        self.vertex = sorted(generator.x)
        self.sets = sorted(generator.f)
        for j in range(0, len(self.sets)):
            self.sets[j] = list(self.sets[j])

    def greedy_set_cover(self):
        # Change tuple to set
        temp_sets = self.sets.copy()
        not_covered = set(self.vertex.copy())
        for j in range(0, len(temp_sets)):
            temp_sets[j] = set(temp_sets[j])
        # Greedy choose
        minsets = []
        while len(not_covered) > 0:
            size = 0
            pos = 0
            for k in range(0, len(temp_sets)):
                if len(not_covered & temp_sets[k]) > size:
                    size = len(not_covered & temp_sets[k])
                    pos = k
            not_covered -= (not_covered & temp_sets[pos])
            minsets.append(temp_sets[pos])
            temp_sets.remove(temp_sets[pos])

        return minsets

    def linear_programming_set_cover(self):

        optimizer, frequency = self.linear_programming()
        # print(optimizer)
        frequency = 1 / frequency
        minsets = []
        for i in range(len(optimizer)):
            if optimizer[i] > frequency:
                minsets.append(self.sets[i])

        return minsets

    def linear_programming(self):
        onehot_sets = [[]]

        for n in range(len(self.sets)):
            onehot = [0 for k in range(len(self.vertex))]
            vertex_sets = sorted(self.vertex.copy())
            for i in range(len(vertex_sets)):
                if vertex_sets[i] in self.sets[n]:
                    onehot[i] = 1
                else:
                    onehot[i] = 0
            onehot_sets.append(onehot)
        del onehot_sets[0]
        # Calculate Frequency
        frequency = 0
        for i in range(0, len(onehot_sets)):
            num = sum([one_hot[i] for one_hot in onehot_sets])
            if num > frequency:
                frequency = num

        size = list(range(len(onehot_sets)))
        # Initial xs range
        xs = pulp.LpVariable.matrix("xs", (size, ), 0, 1, pulp.LpContinuous)
        lp = pulp.LpProblem("Linear Programming", pulp.LpMinimize)
        # Default weight set to be 1
        lp += pulp.lpDot(xs, [1 for k in range(len(onehot_sets))])
        # Consistent
        for pos in range(len(self.vertex)):
            lp += pulp.lpDot([one_hot[pos] for one_hot in onehot_sets], xs) >= 1
        # Solve the linear programming
        lp.solve()
        # return result
        result = []
        for j in size:
            result.append(xs[j].value())

        return result, frequency


if __name__ == "__main__":
    generators = generator.Generator(5000, 5000, [1, 5000])
    setcover = SetCover(generators)
    cover_sets1 = setcover.greedy_set_cover()
    print(cover_sets1)
    allsets = []
    for i in range(0, len(cover_sets1)):
        if i == 0:
            allsets = cover_sets1[0]
        else:
            allsets |= cover_sets1[i]
    print(allsets)
    print("Greedy Finished\n\n\n")

    # cover_sets2 = setcover.linear_programming_set_cover()
    # print(cover_sets2)
    # allsets = []
    # for i in range(0, len(cover_sets2)):
    #     if i == 0:
    #         allsets = set(cover_sets2[0])
    #     else:
    #         allsets |= set(cover_sets2[i])
    # print(allsets)
    # print("Linear Programming Finished\n\n\n")

    size = [100, 200, 500, 1000, 2000, 5000]
    timeset = [[0 for j in range(len(size))] for i in range(2)]
    for i in range(len(size)):
        gen = generator.Generator(size[i], size[i], [1, size[i]])
        setcover = SetCover(gen)

        start = time.time()
        cover_sets1 = setcover.greedy_set_cover()
        end = time.time()
        timeset[0][i] = end - start

        start = time.time()
        cover_sets2 = setcover.linear_programming_set_cover()
        end = time.time()
        timeset[1][i] = end - start

    print(timeset)
