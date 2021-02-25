class scheduler:
    def init(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path
        self.load()
        # loaded data: self.streets, self.paths and headers
        print("streets  {}".format(self.streets))
        print("paths  {}".format(self.paths))
        print("headers  {} {} {} {} {}".format( self.D, self.I, self.S, self.V, self.F))

    def load(self):
        with open(self.in_path) as f:
            self.streets = []
            self.paths = []
            self.D, self.I, self.S, self.V, self.F = f.readline().split()  # headers loading
            for i, line in enumerate(f.readlines()):  # loading pizza information
               if i <= self.S: # lower that S lines == street
                   split = line.split()
                   self.streets.append({"B": split[0],"E": split[1],"name": split[2], "L":split[3]})
               elif i > self.S: # upper that S lines == paths
                   split = line.split()
                   self.paths.append({"P": split[0], "names_of_streets": split[1:]})

if __name__ == 'main':
    your_path = "/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/hascode2021"
    pizza_hut0 = acheduler(your_path + '/data/a.txt', your_path + '/out/a.txt')