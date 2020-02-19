import logging
from multiprocessing import Pool
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

class pizzaManager:

    def __init__(self, inputPath, depth, n_cores):
        print(" fine_tuning . . . \n")
        self.depth = depth
        self.n_cores = n_cores
        print(" initializing the idea . . . \n")
        self.inputPath = "data/"+inputPath
        self.outPath = "output/"+inputPath.split(".")[0]+".out"
        self.medsynPath = inputPath
        self.N = 0 # number of classes
        self.M = 0 # number of maximun slice amount
        self.pizzaTypes = list() # map each class between 0 .. N-1 with slice amount
        self.typeDistribution = []
        self.read_input()
        print("recomended depth : {}".format(int(self.M/self.typeDistribution[len(self.typeDistribution)-1]))) #auto grading the depth (never more than )
        # display data
        print("number of types : {}".format(self.N))
        print("max number of slices : {}".format(self.M))
        print('value : type')
        for value, slices in zip(self.pizzaTypes, self.typeDistribution):
            # the slices per type are ordered in non-decreasing order ( 1 <= self.pizzaTypes[type]_0 <= self.pizzaTypes[type]_N <= M)
            print(value, ':', slices)

    def read_input(self):
        first = True
        with open(self.inputPath, 'r') as file:
            for line in file:
                split = line.split()
                if first:
                    # map N and M parameters
                    self.M = int(split[0])
                    self.N = int(split[1])
                    first = False
                else:
                    # map each class to the slice amount = 'split[type]'
                    for type in range((self.N)):
                        self.pizzaTypes.append(type)
                        self.typeDistribution.append(int(split[type]))

    def MedysnReport(self, title):
        xArray = []
        yArray = []
        for idx, slices in zip(self.pizzaTypes, self.typeDistribution):
            xArray.append(slices)
            yArray.append(idx)

        fig = plt.figure(figsize=(10, 10))

        ax1 = fig.add_subplot(1,2,1, title='Distribution for pizza type: '+ title)
        plt.scatter(xArray, yArray, c='blue', edgecolor='black')
        plt.ylabel('value')
        plt.xlabel('pizza type')

        ax2 = fig.add_subplot(1, 2, 2, title='heatmap for pizza type: ' + title, aspect="auto", sharex=ax1,
                              sharey=ax1)
        H, xedges, yedges = np.histogram2d(xArray, yArray, bins=10)
        H = H.T
        im = mpl.image.NonUniformImage(ax2, interpolation='bilinear', cmap='seismic')
        xcenters = (xedges[:-1] + xedges[1:]) / 2
        ycenters = (yedges[:-1] + yedges[1:]) / 2
        im.set_data(xcenters, ycenters, H)
        ax2.images.append(im)
        fig.colorbar(im, ax=ax2)

        fig.savefig("output/"+title+'.pdf')

    def Marley(self):
        print("\n Marley is thinking ...")
        self.MedysnReport(self.medsynPath)
        print("\n Marley's slaves are working ...")
        results = self.process()
        print("\n Marley's slaves finished ...")

        print("\n Marley is revising ...")
        best = (0,0,0,0)
        for revision in results:
            if (revision[1] > best[1]): best = revision

        best_depth = best[0]
        best_score_found = best[1]
        comb_to_find =  best[2]
        secondline = best[3]
        print("\n Marley found ...")

        submissionline1 = len(comb_to_find)
        #secondline = sorted([self.pizzaTypes.index(value) for value in comb_to_find])
        assert len(secondline) == len(set(secondline))

        print("depth : {}".format(best_depth))
        print("target : {}".format(self.M))
        print("best score : {}".format(best_score_found))
        print("winner combination : {}".format(secondline))
        print("depth used : {}".format(submissionline1))


        # Todo format the output

        with open(self.outPath, 'w') as file:
            file.write(str(submissionline1) +"\n")
            for type in secondline:
                file.write(str(type) + " ")

    def put_into_queue(self, depth):
        return self.worker_assigment(depth)

    def process(self):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("----- initializing Marley's workers, we never surrender Hu Haaaa (º.º) ")
        pool = Pool(processes=64)
        logging.info("Main    : create and start threads.")
        results = pool.map(self.put_into_queue, list(range(1, self.depth+1)))
        return results

    # Parallel combinatorial explosion ..... for self.depth ......
    def worker_assigment(self, depth):
        index = int(len(self.pizzaTypes) / 2)
        best = False
        guess_response = (depth, 0, 0, 0)
        while not best:
            type_list = self.pizzaTypes[index+1:]
            comb_list = self.typeDistribution[index+1:]
            acc, combination, types = self.zipper(index, type_list, comb_list, depth)
            if (acc <= self.M) & (acc > guess_response[1]):
                guess_response = (depth, acc, combination, types)
                index = (index + len(self.typeDistribution)) // 2
            else:
                index = index // 2
            if acc == self.M or index == 0 or index == len(self.typeDistribution):
                best = True
        return guess_response

    def zipper(self, index, type_list, comb_list, depth):
        i2s = int(len(comb_list) / 2)
        best = False
        acc = 0
        combination = []
        types = []
        while not best:
            new_acc = sum(comb_list[i2s:i2s+depth]) + self.typeDistribution[index]
            if acc < new_acc and new_acc <= self.M:
                acc = new_acc
                combination = comb_list[i2s:i2s+depth] + [self.typeDistribution[index]]
                types = [self.pizzaTypes[index]] + type_list[i2s:i2s+depth]
                i2s = (i2s + len(comb_list)) // 2
            else:
                i2s = i2s // 2
            if acc == self.M or i2s == 0 or i2s == len(comb_list):
                best = True

        return acc, combination, types

if __name__ == '__main__':
    '''
    
    computation example
    
    '''
    # manager = pizzaManager("a_example.in", 2, 64)
    # manager.Marley()
    # manager = pizzaManager("b_small.in", 2, 64)
    # manager.Marley()
    # manager = pizzaManager("c_medium.in", 47, 64)
    # manager.Marley()
    manager = pizzaManager("e_also_big.in", depth=8000, n_cores=64)
    manager.Marley()
    # manager = pizzaManager("d_quite_big.in", depth=1893, n_cores=64)
    # manager.Marley()
