import matplotlib.pyplot as plt
import numpy as np
import logging
import threading
import queue
import itertools
from multiprocessing import Pool, Process, Queue


class pizzaManager:

    def __init__(self, inputPath,depth):
        print(" initializing the idea . . . \n")
        self.inputPath = "data/"+inputPath
        self.outPath = "output/"+inputPath
        self.N = 0 # number of classes
        self.M = 0 # number of maximun slice amount
        self.pizzaTypes = dict() # map each class between 0 .. N-1 with slice amount
        self.typeDistribution = []
        self.read_input()
        self.depth = depth
        print("recomended depth : {}".format(int(self.M/self.typeDistribution[len(self.typeDistribution)-1]))) #auto grading the depth (never more than )
        # display data
        print("number of types : {}".format(self.N))
        print("max number of slices : {}".format(self.M))
        for type in self.pizzaTypes:
            # the slices per type are ordered in non-decreasing order ( 1 <= self.pizzaTypes[type]_0 <= self.pizzaTypes[type]_N <= M)
            print(type, ':', self.pizzaTypes[type])

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
                        self.pizzaTypes.update({type: int(split[type])})
                        self.typeDistribution.append( int(split[type]))

    def Marley(self):
        print("\n Marley is thinking ...")
        # Showing up the distribution of data
        # plt.hist(self.typeDistribution, bins=np.histogram_bin_edges(self.typeDistribution))
        # plt.show()

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

        print("depth : {}".format(best_depth))
        print("target : {}".format(self.M))
        print("best score : {}".format(best_score_found))
        print("winner combination : {}".format(comb_to_find))
        # Todo format the output


        with open(self.outPath, 'w') as file:
            pass

    def put_into_queue(self, depth):
        return self.worker_assigment(depth)

    def process(self):
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("----- initializing Marley's workers, we never surrender Hu Haaaa (º.º) ")
        completion = 0
        pool = Pool(processes=64)
        results = []
        logging.info("Main    : create and start threads.")
        results = pool.map(self.put_into_queue, list(range(1, self.depth+1)))

        logging.info("---------------------------------------------------- "+str(completion)+" % completed")
        print(results)
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

    #def intelligent_combinations(self, depth):
        # return itertools.combinations(self.typeDistribution, depth) # brute force (not possible only until depth 4-5)
        # Todo generate permutations of  'self.typeDistribution' (sorted list) without repetition 'heuristic search'
        #for index, num in enumerate(self.typeDistribution):
        #    comb_list = self.typeDistribution[index:]
        #    repeat_partial = zipper(num, comb_list, depth)

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
    #manager = pizzaManager("b_small.in", 9)
    #manager = pizzaManager("c_medium.in", 30)
    manager = pizzaManager("d_quite_big.in", 900)
    manager.Marley()
