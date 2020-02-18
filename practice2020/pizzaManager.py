import matplotlib.pyplot as plt
import numpy as np
import logging
import threading
import queue
import itertools

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

    def process(self):
        que = queue.Queue()
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
        logging.info("----- initializing Marley's workers, we never surrender Hu Haaaa (º.º) ")
        completion = 0
        threads = list()
        results = []

        for index in range(self.depth):
            index+=1
            logging.info("Main    : create and start thread %d.", index)
            worker = threading.Thread(target=lambda q, arg1: q.put(self.worker_assigment(arg1)), args=(que, index))
            threads.append(worker)
            worker.start()

        for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)
            completion += 1./self.depth
            logging.info("---------------------------------------------------- "+str(completion)+" % completed")


        while not que.empty():
            results.append(que.get())
        print(results)
        return results

    # Parallel combinatorial explosion ..... for self.depth ......
    def worker_assigment(self, depth):
        guess_response = (depth , 0, 0)
        for possible_comb in list(self.intelligent_combinations(depth)):
            addition = sum(possible_comb)
            if ( addition <= self.M) & (addition > guess_response[1]):guess_response = (depth , addition, possible_comb)
        return guess_response

    def intelligent_combinations(self, depth):
        return itertools.permutations( self.typeDistribution, depth) # brute force (not possible only until depth 4-5)
        # Todo generate permutations of  'self.typeDistribution' (sorted list) without repetition 'heuristic search'
        pass

if __name__ == '__main__':
    manager = pizzaManager("a_example.in", 3)
    manager.Marley()
