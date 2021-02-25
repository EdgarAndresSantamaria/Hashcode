import os
from collections import deque
from collections import defaultdict

path = os.path.dirname(__file__)

class scheduler:
    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path
        self.load()
        self.output()
        # loaded data: self.streets, self.paths and headers
        # print("streets  {}".format(self.streets))
        # print("paths  {}".format(self.paths))
        # print("headers  {} {} {} {} {}".format( self.D, self.I, self.S, self.V, self.F))

    def load(self):
        with open(self.in_path) as f:
            self.D, self.I, self.S, self.V, self.F = [int(elem) for elem in f.readline().split()]  # headers loading
            self.used_froms = defaultdict(lambda:False)
            self.intersections = {i: {'from': set([]), 'to': set([]), 'queue': deque([])} for i in range(self.I)}
            self.streets = {}
            self.cars = []
            for i, line in enumerate(f.readlines()):  # loading road information
                if i < self.S: # lower that S lines == street
                    split = line.split()
                    B, E, name, L = int(split[0]), int(split[1]), split[2], int(split[3])
                    self.streets[name] = (B, E, L)
                    self.intersections[B]['to'].add(name)
                    self.intersections[E]['from'].add(name)
                elif i >= self.S: # upper that S lines == paths
                    split = line.split()
                    self.cars.append({"P": int(split[0]), "names_of_streets": split[1:]})
                    for name in split[1:]:
                        self.used_froms[name] = True

    def output(self):
        os.makedirs(os.path.dirname(self.out_path), exist_ok=True)
        result = []
        total = 0
        for i in self.intersections.keys():
            tmp = []
            trotalfrom = 0
            for street in self.intersections[i]['from']:
                if self.used_froms[street]:
                    trotalfrom += 1
                    tmp.append(street + ' ' + str(1) + '\n')
            if trotalfrom > 0:
                total += 1
                result.append(str(i) + '\n')
                result.append(str(trotalfrom) + '\n')
                for item in tmp:result.append(item)

        with open(self.out_path, 'w') as f:
            f.write(str(total) + '\n')
            for line in result:
                f.write(line)







# if __name__ == 'main':
your_path = path
pizza_hutA = scheduler(your_path + '/data/a.txt', your_path + '/out/a.txt')
pizza_hutB = scheduler(your_path + '/data/b.txt', your_path + '/out/b.txt')
pizza_hutC = scheduler(your_path + '/data/c.txt', your_path + '/out/c.txt')
pizza_hutD = scheduler(your_path + '/data/d.txt', your_path + '/out/d.txt')
pizza_hutE = scheduler(your_path + '/data/e.txt', your_path + '/out/e.txt')
pizza_hutF = scheduler(your_path + '/data/f.txt', your_path + '/out/f.txt')