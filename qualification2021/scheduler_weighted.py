import os
from collections import deque

path = os.path.dirname(__file__)

class scheduler:
    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path
        self.load()
        self.output()
        # loaded data: self.streets, self.paths and headers
        print("streets  {}".format(self.streets))
        # print("paths  {}".format(self.paths))
        print("headers  {} {} {} {} {}".format( self.D, self.I, self.S, self.V, self.F))

    def load(self):
        with open(self.in_path) as f:

            self.D, self.I, self.S, self.V, self.F = [int(elem) for elem in f.readline().split()]  # headers loading

            self.intersections = {i: {'from': {}, 'to': []} for i in range(self.I)}
            self.streets = {}
            self.cars = []

            for i, line in enumerate(f.readlines()):  # loading road information
                if i < self.S: # lower that S lines == street
                    split = line.split()
                    B, E, name, L = int(split[0]), int(split[1]), split[2], int(split[3])
                    self.streets[name] = (B, E, L)
                    # self.intersections[B]['to'].append(name)
                    self.intersections[E]['from'][name] = 0
                elif i >= self.S: # upper that S lines == paths
                    split = line.split()
                    self.cars.append({"P": int(split[0]), "names_of_streets": split[1:]})
                    for car in self.cars:
                        for street in car['names_of_streets']:
                            end = self.streets[street][1]
                            self.intersections[end]['from'][street] += 1

    def output(self):
        os.makedirs(os.path.dirname(self.out_path), exist_ok=True)
        with open(self.out_path, 'w') as f:
            real_I = 0
            for i in self.intersections.keys():
                written = False

                for street, flow in self.intersections[i]['from'].items():
                    if flow:
                        if written == False:
                            real_I += 1
                            break

            f.write(str(real_I) + '\n')

            for i in self.intersections.keys():
                written = False
                real_i = 0

                for street, flow in self.intersections[i]['from'].items():
                    if flow:
                        real_i += 1 

                for street, flow in self.intersections[i]['from'].items():
                    total = sum(self.intersections[i]['from'].values())
                    if flow:
                        if written == False:
                            f.write(str(i) + '\n')
                            f.write(str(real_i) + '\n')
                            written = True
                        f.write(street + ' ' + str(int(1+10*(flow/total))) + '\n')





# if __name__ == 'main':
your_path = path
pizza_hutA = scheduler(your_path + '/data/a.txt', your_path + '/out/aaa.txt')
pizza_hutB = scheduler(your_path + '/data/b.txt', your_path + '/out/bbb.txt')
pizza_hutC = scheduler(your_path + '/data/c.txt', your_path + '/out/ccc.txt')
pizza_hutD = scheduler(your_path + '/data/d.txt', your_path + '/out/ddd.txt')
pizza_hutE = scheduler(your_path + '/data/e.txt', your_path + '/out/eee.txt')
pizza_hutF = scheduler(your_path + '/data/f.txt', your_path + '/out/fff.txt')
