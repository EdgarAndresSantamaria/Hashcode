class pizzaManager:

    def __init__(self, inputPath,outPath):
        self.inputPath = "/data/"+inputPath
        self.outPath = "/output/"+outPath
        self.N = 0 # number of classes
        self.M = 0 # number of maximun slice amount
        self.pizzaTypes = dict() # map each class between 0 .. N-1 with slice amount
        self.read_input()
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

    def Marley(self):



        with open(self.outPath, 'w') as file:
            pass

if __name__ == '__main__':
    manager = pizzaManager("b_small.in")