# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from collections import defaultdict
import logging
from multiprocessing import Pool

def clean(item):
    item = item.split("\n")[0]
    # todo get the customer details
    item = item [2:]
    return item

def expand(list):
    customer_map = {}
    for i, item in enumerate(list):
        spitted = item.split(" ")
        if len(spitted) > 1:
            customer_map[i] = spitted
        else:customer_map[i] = [item]
    return customer_map


def generate_possible_combinations():

    return {"list": [], "points": 0}

def guessing_ingredients (customer_like_map, customer_dislike_map):
    total_impact = {}
    for like_id, like_lst in customer_like_map.items():
        impact = defaultdict(lambda: 0)
        for dislike_id, dislike_lst in customer_dislike_map.items():
            for ingredient in dislike_lst:
                if ingredient in like_lst:
                    impact[ingredient] += 1
        customer_loss = 0
        for lost in impact.values():
            customer_loss += lost
        total_impact[like_id] = customer_loss
    total_impact = {k: v for k, v in sorted(total_impact.items(), key=lambda item: item[1])}

    current_ingredents = []
    for customer_id, like_lst in customer_like_map.items():
        if total_impact[customer_id] == 0:  # only allow positive or equal impact cases
            current_ingredents += like_lst
    current_ingredents = list(set(current_ingredents))
    print(current_ingredents)
    print(len(current_ingredents))
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    n_workers = 10
    logging.info("----- initializing {} Edgar's workers, we never surrender Hu Haaaa $(º.º)> ".format(n_workers))
    pool = Pool(processes=n_workers)
    logging.info("Main : create and start threads.")
    # note that data is a  [[entities, relations, current_txt],[entities, relations, current_txt],[entities, relations, current_txt]]
    # in this way we treat all combinations
    results = pool.map(generate_possible_combinations, [])




    return current_ingredents

def main(input, output):
   with open(input) as f:
       lines = f.readlines()
       customer_amount = lines.pop(0)
       likes = [clean(item) for item in lines[::2]]
       customer_like_map = expand(likes)
       dislikes = [clean(item) for item in lines[1::2]]
       customer_dislike_map = expand(dislikes)
       current_ingredents = guessing_ingredients(customer_like_map, customer_dislike_map)


   with open(output, "w") as f:
       f.write(str(len(current_ingredents)) + " " + " ".join(current_ingredents))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(r"C:\Users\edgar\PycharmProjects\hashcode2022\input_data\a_an_example.in.txt",
         r"C:\Users\edgar\PycharmProjects\hashcode2022\output_data\a_an_example.out.txt")

    main(r"C:\Users\edgar\PycharmProjects\hashcode2022\input_data\b_basic.in.txt",
         r"C:\Users\edgar\PycharmProjects\hashcode2022\output_data\b_basic.out.txt")

    main(r"C:\Users\edgar\PycharmProjects\hashcode2022\input_data\c_coarse.in.txt",
         r"C:\Users\edgar\PycharmProjects\hashcode2022\output_data\c_coarse.out.txt")

    main(r"C:\Users\edgar\PycharmProjects\hashcode2022\input_data\d_difficult.in.txt",
         r"C:\Users\edgar\PycharmProjects\hashcode2022\output_data\d_difficult.out.txt")

    main(r"C:\Users\edgar\PycharmProjects\hashcode2022\input_data\e_elaborate.in.txt",
         r"C:\Users\edgar\PycharmProjects\hashcode2022\output_data\e_elaborate.out.txt")
