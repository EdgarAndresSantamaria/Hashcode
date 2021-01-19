# This is a sample Python script.
# data structure convenions ...
from collections import defaultdict
from collections import Counter
# multiprocess
from multiprocessing import Pool
# logging
import time

class pizza_hut:

    '''
    Initializer object pizza hut
    '''
    def __init__(self, in_path, out_path):
        self.in_path = in_path  #input path
        self.out_path = out_path  # output path
        self.delivered = []  # the list of already took pizzas
        self.D = 0  # number of deliveries
        self.result = []  # list containing the output deliveries to write

        self.load()  # loading the initial data
        self.sorted_pizzas = [x for x, y in sorted(self.ids_2_amounts.items(), key = lambda x:x[1], reverse=True)]


        # data information display
        print(" number of pizzas: {} \n number of 2 people teams {} \n number of 3 people teams {} \n number of 4 people teams {} \n\n ".format(
                self.M, self.T2, self.T3, self.T4))

        self.manage_delivery_intersected()  #manage the deliveries launch
        self.write_out()  #generate the submission file

    '''
    Method that aims to fill the required output format
    '''
    def write_out(self):
        with open(self.out_path, "w") as f:
            f.write(str(self.D) + " \n")
            for line in self.result:f.write(line)

    '''
    Method that manages the control logic for each deliveries group
    - follows a linear way to compose delveries (this method seems worst in practice)
    '''
    def manage_deliveries_lineal(self):
        # Testing results for teams of 2, 3 and 4
        # a_example ( 0.0 secs )    74 points  (/)
        # b_little_bit_of_everything (0.29 secs )   9,398 points (\)
        # c_many_ingredients ( 263 secs == 4 min)   465,955,841 points (\)
        # d_many_pizzas ( 601 == 10 min )   5,999,204 points (\)
        # e_many_teams ( ----- ------)    ------

        # control logic for deliveries
        # outdated: here we must alleviate the effect of many teams (scalability phase)
        # must apply concurrency technologies to afford many teams efficiently
        acc = 0
        for loop in range(int(self.T3)):  # deliver (number of 3 people teams: T3) pizza pairs
            start = time.time()
            self.deliver(3)
            end = time.time()
            acc += (end - start)
        for loop in range(int(self.T2)):  # deliver (number of 2 people teams: T2) pizza pairs
            start = time.time()
            self.deliver(2)
            end = time.time()
            acc += (end - start)
        for loop in range(int(self.T4)):  # deliver (number of 4 people teams: T4) pizza pairs
            start = time.time()
            self.deliver(4)
            end = time.time()
            acc += (end - start)
        print("time for delivery {}".format(acc))

    '''
    Method that manages the control logic for each deliveries group
    - follows intersected way to generate groups 
    '''
    def manage_delivery_intersected(self):

        # Testing results for teams of 2, 3 and 4
        # a_example ( 0.0 secs )    74 points  (-)
        # b_little_bit_of_everything (0.66 secs = 1 min)   11,957 points (/)
        # c_many_ingredients ( 270 secs == 4,5 min)   503,246,823  points (/)
        # d_many_pizzas ( 64 secs == 1 min )   7,155,635 points (/)
        # e_many_teams ( 76 secs == 1 min )     8,843,678 points (/)


        # control logic for deliveries
        # here we must alleviate the effect of many teams (scalability phase)
        # must apply concurrency technologies to afford many teams efficiently
        # intercalation of the output deliveries we achieve better performance
        # ordering also seems important
        end = False
        cnt2, cnt3, cnt4 = 0, 0, 0
        self.T2, self.T3, self.T4 = int(self.T2), int(self.T3), int(self.T4)
        start = time.time()
        while not end:  #O(T4 + T3 + T2)
            if cnt3 < self.T3:
                self.deliver(3)
                cnt3 += 1
            if cnt2 < self.T2:
                self.deliver(2)
                cnt2 += 1
            if cnt4 < self.T4:
                self.deliver(4)
                cnt4 += 1
            if ((cnt2 == self.T2) and (cnt3 == self.T3) and (cnt4 == self.T4)) or (not self.sorted_pizzas): end = True

        end = time.time()
        print("time for delivery {}".format(end - start))

    '''
    Method that delivers a pizza composition for a group
    - takes into account the ingredients already selected to maximize the distinct
    '''
    def deliver(self, team_number):
        #distributed deliveries
        base_id, best_index = self.find_best_pizza()
        if base_id == -1:return
        # locally management of locks
        deliver_lst = [base_id]
        index_dict = {}
        index_dict[base_id] = best_index
        while len(deliver_lst) < team_number :
            best_pizza, best_index = self.find_best_pizza(mode = "pair", pizza_lst=deliver_lst)  #get the best match for current ingredents
            if best_pizza == -1:return
            deliver_lst.append(best_pizza) #append the best pizza we found
            index_dict[best_pizza] = best_index # append the best pizza we found
        # quality controls (must ensure the formats and control errors in selection)
        sorted_ids =  sorted(index_dict.items(), key=lambda x: x[1], reverse=True)
        for pizza_id, index in sorted_ids:  #update available pizzas
            self.ids_2_amounts.pop(pizza_id, None)
            del self.sorted_pizzas[index]
            # this method alleviates the computattion with many pizzas
        deliver_lst = [str(i) for i in deliver_lst]  #format output as string
        self.result.append("{} {} \n".format(team_number, " ".join(deliver_lst)))  #create submission line
        self.D += 1  #count new delivery

    '''
    In this method we aim to count the intersected items in the given lists
    - the method achieves linear computational cost O(n + m)
    '''
    def count_intersections(self, lst1, lst2):
        # this method alleviates the computation with many ingredients
        c1 = Counter(lst1)
        c2 = Counter(lst2)
        return {k: min(c1[k], c2[k]) for k in c1.keys() & c2.keys()}

    '''
    In this method we aim to find the pizza with: (base mode)
    - maximum possible amount of ingredients from available pizzas
    In this method we aim to find the pizza with: (pair mode)
    - less overlapped ingredients with the given ingredient list
    - maximum possible amount of ingredients from available pizzas
    '''
    def find_best_pizza(self, mode = "base", pizza_lst = []):
        best_pizza_id = -1
        best_index = -1
        if mode == "pair":
            ingredient_lst = []
            non_overlap_amount = 0
            for pizza in pizza_lst: ingredient_lst += self.ids_2_ingredents[pizza]  # we create the current ingredents list
            ingredient_lst = list(set(ingredient_lst))  # get current unique ingredents
            max_overlapped = len(ingredient_lst)
        for index, pizza_id in enumerate(self.sorted_pizzas):  # search every amount in descending order        O(pizzas)
            amount = self.ids_2_amounts[pizza_id]  # retrieve the current amount pizza list
            if (mode == "pair"):
                if (amount < non_overlap_amount) or (amount == non_overlap_amount):
                    break  # prune those non-probable amounts
            if (mode == "pair") and (pizza_id not in pizza_lst):
                current_ingredients = self.ids_2_ingredents[pizza_id]
                overlap = sum(self.count_intersections(ingredient_lst, current_ingredients).values())
                if overlap < max_overlapped:
                    best_pizza_id = pizza_id  # return the pizza with maximum ingredents
                    best_index  =  index
                    # apply heuristic to avoid keep searching until best pair is reached
                    # if the non - overlapped amount is bigger than amount we can discard
                    non_overlap_amount = amount - overlap
            elif (mode == "base"):
                best_pizza_id = pizza_id  # return the pizza with maximum ingredients
                best_index = index
                break  # break search once encountered
        return best_pizza_id, best_index


    def load(self):
        with open(self.in_path) as f:
            self.M, self.T2, self.T3, self.T4 = f.readline().split()  #headers loading
            self.ids_2_amounts = {}  # we map the pizza id's into amounts
            self.ids_2_ingredents = {}  # we map pizza id's with ingredents
            id = 0  #pizza identifier counter
            for pizza in f.readlines():  #loading pizza information
                self.ids_2_amounts[id] = int(pizza.split()[0])
                self.ids_2_ingredents[id] = pizza.split()[1:]
                id+=1

if __name__ == '__main__':
    # finalize development for team 2 data, then scale the algorithm (seems good performance )
    # todo: get better performance for e_many_teams
    pizza_hut0 = pizza_hut('/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/data/a_example.in',
                           '/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/out/a_example.out')

    pizza_hut1 = pizza_hut('/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/data/b_little_bit_of_everything.in',
                           '/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/out/b_little_bit_of_everything.out')

    pizza_hut2 = pizza_hut('/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/data/c_many_ingredients.in',
                           '/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/out/c_many_ingredients.out')

    pizza_hut3 = pizza_hut('/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/data/d_many_pizzas.in',
                           '/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/out/d_many_pizzas.out')

    pizza_hut4 = pizza_hut('/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/data/e_many_teams.in',
                          '/media/edgar/407d4115-9ff4-45c6-9279-01b62aee0730/Hashcode-master/practice2021/out/e_many_teams.out')