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
        self.pizzaTypes = dict() # map each class between 0 .. N-1 with slice amount
        self.typeDistribution = []
        self.read_input()
        print("recomended depth : {}".format(int(self.M/self.typeDistribution[len(self.typeDistribution)-1]))) #auto grading the depth (never more than )
        # display data
        print("number of types : {}".format(self.N))
        print("max number of slices : {}".format(self.M))
        print('value : type')
        for value in self.pizzaTypes:
            # the slices per type are ordered in non-decreasing order ( 1 <= self.pizzaTypes[type]_0 <= self.pizzaTypes[type]_N <= M)
            print(value, ':', self.pizzaTypes[value])

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
                        self.pizzaTypes.update({ int(split[type]):type})
                        self.typeDistribution.append( int(split[type]))

    def MedysnReport(self, title):
        xArray = []
        yArray = []
        for pair in list( self.pizzaTypes.items()):
            xArray.append(pair[0])
            yArray.append(pair[1])

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
        best = (0,0,0)
        for revision in results:
            if (revision[1] > best[1]): best = revision

        best_depth = best[0]
        best_score_found = best[1]
        comb_to_find =  best[2]
        print("\n Marley found ...")

        submissionline1 = len(comb_to_find)
        secondline = sorted([self.pizzaTypes[value] for value in comb_to_find])

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
        guess_response = (depth, 0, 0)
        for index, num in enumerate(self.typeDistribution):
            comb_list = self.typeDistribution[index+1:]
            acc, combination= self.zipper(num, comb_list, depth)
            if (acc <= self.M) & (acc > guess_response[1]):
                guess_response = (depth , acc, combination)
        return guess_response

    def zipper(self, num, comb_list, depth):
        i2s = int(len(comb_list) / 2)
        best = False
        acc = 0
        combination = []
        while not best:
            new_acc = sum(comb_list[i2s:i2s+depth]) + num
            if acc < new_acc and new_acc <= self.M:
                acc = new_acc
                combination = comb_list[i2s:i2s+depth] + [num]
                i2s = (i2s + len(comb_list)) // 2
            else:
                i2s = i2s // 2
            if acc == self.M or i2s == 0 or i2s == len(comb_list):
                best = True

        return acc, combination

if __name__ == '__main__':
    '''
    
    computation example
    
    '''
    #manager = pizzaManager("a_example.in", 2, 64)
    #manager = pizzaManager("b_small.in", 2, 64)
    #manager = pizzaManager("c_medium.in", 47, 64)
    manager = pizzaManager("e_also_big.in", depth=4000, n_cores=64)
    #manager = pizzaManager("d_quite_big.in", depth=1893, n_cores=64)
    manager.Marley()
