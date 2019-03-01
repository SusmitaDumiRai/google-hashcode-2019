import numpy as np
import pandas as pd
from glob import glob
import random


def create_vertical_slides(v_dict):
    saved = False
    saved_id = 0
    vertical_slide_show = []

    shuffled_keys = list(v_dict.keys())
    random.shuffle(shuffled_keys)

    for shuffled_key in shuffled_keys:
        if saved is False:
            saved_id = shuffled_key
            saved = True
        else:
            saved = False
            vertical_slide_show.append([saved_id, shuffled_key])

    return vertical_slide_show


def sort_values(dict, vertical_slides=None, v_dict=None):
    x = sorted(dict, key=lambda k: len(dict[k]), reverse=True)

    # for x_ in x:
    #     if x_ == 'k':
    #         pass
    #     if x_ < 0:
    #         x_ *= -1
    #         if vertical_slides is not None:
    #             vs = vertical_slides[x_]
    #             v1 = v_dict[vs[0]]
    #             v2 = v_dict[vs[1]]
    #             v3 = v1 + v2
    #     #         print(len(set(v3)))
    #     #
    #     # else:
    #     #     print(len(dict[x_]))
    return x


def add_vertical_to_horizontal(vert_slides, v_dict, h_dict):

    """
    Combines vertical with horizontal dictionary
    vertical keys are now negative.
    :param vert_slides:
    :param v_dict:
    :param h_dict:
    :return:
    """
    id_list = []

    for i, slide in enumerate(vert_slides):
        # merges tags together
        picture_0 = v_dict[slide[0]]
        picture_1 = v_dict[slide[1]]

        picture = picture_0 + picture_1

        picture_set = set(picture)

        if i == 0:
            i = -99999999
            h_dict[i] = picture_set
        else:
            h_dict[-i] = picture_set


    return h_dict


filename_a = "a_example.txt"
filename_b = "b_lovely_landscapes.txt"
filename_c = "c_memorable_moments.txt"
filename_d = "d_pet_pictures.txt"
filename_e = "e_shiny_selfies.txt"

# {id: tags}
v_dict = {}

# {id: tags}
h_dict = {}

with open(filename_b) as f:
    content = f.readlines()

content = [x.strip() for x in content]

# POPULATES HORIZON AND VERTICAL DICTIONARY
for i in range(1, len(content)):
    line = content[i].split(" ")
    if line[0] == 'H':
        h_dict[i - 1] = line[2:]
    else:
        v_dict[i - 1] = line[2:]

if len(v_dict.items()) % 2 != 0:
    v_dict.popitem()




slideshow = []

# for k, v in h_dict.items():
#     slideshow.append(k)
#
# # sort horizontal keys in value size.
# # [id]
# h_dict_sorted_keys = sort_values(h_dict)

# merges two vertical images together
# is a list of list [[id1, id2]]
vertical_slide_keys = create_vertical_slides(v_dict)

# adds tags of TWO VERTICAL IMAGES (A SLIDE) INTO HROIZTAON DICTIONARY USING NEGATIVE INDEX.
h_v_merged = add_vertical_to_horizontal(vertical_slide_keys, v_dict, h_dict)

# SORTS KEYS BASED ON SIZE OF UNIQUE TAGS.
sort_keys = sort_values(h_v_merged, vertical_slide_keys, v_dict)
sum = 0
optimal_sort_key_id_list = []
optimal_sort_key_id_list.append(sort_keys[0])
save_i = 0
del sort_keys[save_i]
while sort_keys:
    last_item_in_list = optimal_sort_key_id_list[-1]

    highest_tag = h_v_merged[last_item_in_list]

    optimal_interest_factor = -1
    optimal_sort_key_id = None

    # remove sortkeys[0] after for loop
    for i in range(0, min(1000, len(sort_keys))):
        current_tag = h_v_merged[sort_keys[i]]
        intersection = len(list(set(current_tag) & set(highest_tag)))
        right_number = len(current_tag) - intersection
        left_number = len(highest_tag) - intersection

        interest_factor = min(intersection, right_number, left_number)

        if interest_factor > optimal_interest_factor:

            optimal_sort_key_id = sort_keys[i]
            save_i = i
            optimal_interest_factor = interest_factor

    sum += optimal_interest_factor
    optimal_sort_key_id_list.append(optimal_sort_key_id)

    del sort_keys[save_i]

print(sum)

f = open("result_c.txt", "a")

f.writelines("%d\n" % len(optimal_sort_key_id_list))

for id in optimal_sort_key_id_list:
    if id == -99999999:
        f.writelines("%d %d\n" % (vertical_slide_keys[0][0], vertical_slide_keys[0][1]))
    elif id < 0:
        id *= -1
        print(id)
        f.writelines("%d %d\n" % (vertical_slide_keys[id][0], vertical_slide_keys[id][1]))
    else:
        f.writelines("%d\n" % id)

