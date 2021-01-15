# This is a sample Python script.
from collections import defaultdict
from collections import Counter
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class pizza_hut:
    def __init__(self, inp, out):
        self.name = inp
        self.load()
        self.sorted_amounts = sorted(list(self.numIngredents.keys()), reverse=True)
        self.delivered = []
        print(
            " number of pizzas: {} \n number of 2 people teams {} \n number of 3 people teams {} \n number of 4 people teams {} \n\n ".format(
                self.M, self.T2, self.T3, self.T4))
        finished = False
        D = 0
        result = []
        while not finished:
            result2 = self.find_best(2, [])
            result3 = self.find_best(3, [])
            result4 = self.find_best(4, [])
            finished = (result4[0] == -1) and (result3[0] == -1) and (result2[0] == -1)
            if finished: break
            result2 = [str(int) for int in result2]
            result3 = [str(int) for int in result3]
            result4 = [str(int) for int in result4]
            # calculate number of submissions
            D += 3
            result.append(str(2) + " " + " ".join(result2) + " \n" + str(3) + " " + " ".join(
                result3) + " \n" + str(4) + " " + " ".join(result4) + " \n")

        with open(out, "w") as f:
            f.write(str(D) + " \n")
            for line in result:f.write(line)

    def count_intersections(self, lst1, lst2):
        c1 = Counter(lst1)
        c2 = Counter(lst2)
        return {k: min(c1[k], c2[k]) for k in c1.keys() & c2.keys()}

    def find_best(self, n, selected):
        # we need to search for the best n pizzas, maximizing the non-overlaped ingredents
        # search initial phase
        best_base = None
        i,j = 0, 0
        while best_base == None:
            base_amount = self.sorted_amounts[i]
            best = self.numIngredents[base_amount][j] # initialize the first id (pizza with most ingredents)
            if (best not in self.delivered) and (best not in selected):
                best_base = best
            else:
                if j < (len(self.numIngredents[base_amount]) - 1): # next pizza in current amount
                    j+=1
                elif i < (len(self.sorted_amounts) - 1): # next ingredent amount
                    i+=1
                    j=0
                else: return [-1]

        selected.append(best_base)
        ingredents_base = self.pizzaInngredents[best_base]
        result = [best_base]
        best = -1
        # check n - 1 times
        for i in range(n-1): # three times in the word case
            max_overlap = 0
            best_ingredents = []
            for amount in self.sorted_amounts: # check descending order by ingredient amount
                for pizza in self.numIngredents[amount]: # check each pizza per ingredent amount
                    ingredents_to_check = self.pizzaInngredents[pizza]
                    # O(n + m) , where len(ingredents_base) = m and len(ingredents_to_check) = n
                    # in the worst case m = (10000*3)  due to annidate and n = 10000 (affordable)
                    counting_dict = self.count_intersections(ingredents_base, ingredents_to_check)
                    # heuristic value (num ingrdents - overlapped ones)
                    overlap = amount - sum(list(counting_dict.values()))
                    if (overlap > max_overlap) and (pizza not in self.delivered) and (pizza not in selected): # minimize overlap and maximize number of ingredents
                        best_ingredents = ingredents_to_check
                        best = pizza
            # re-search
            if best == -1: return self.find_best(n, selected)
            # add partial result
            result += [best]
            selected.append(best)
            # update ingredents base with best ingredents
            ingredents_base += best_ingredents

        result = list(set(result))
        if len(result) == n:
            self.delivered+=result  # update current selection
            return result
        # re-search
        else: return self.find_best(n, selected)

    def load(self):
        file = self.name
        with open(file) as f:
            print(file)
            self.M, self.T2, self.T3, self.T4 = f.readline().split()
            self.numIngredents = defaultdict(list) #we map the number of ingredents into pizza id's
            self.pizzaInngredents = {} # we map pizza id's with ingredents
            id = 0 #  pizza identifier
            for pizza in f.readlines():
                self.numIngredents[int(pizza.split()[0])] += [id]
                self.pizzaInngredents[id] = pizza.split()[1:]
                id+=1

if __name__ == '__main__':
    pizza_hut = pizza_hut('C:\\Users\\BM007\\PycharmProjects\\Hashcode\\data\\a_example.in','C:\\Users\\BM007\\PycharmProjects\\Hashcode\\out\\a_example.out')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
