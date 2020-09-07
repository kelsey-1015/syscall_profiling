import csv
import os
import sys
import math
import itertools
# import networkx as nx
import numpy as np
import string
import matplotlib.pyplot as plt
import plotting
import json

# This flag indicates whether to filter out switch and sched_yield
filter_flag = True
n_gram_len = 6
APP_NAME = 'python3'

# the directory path storing the tracefiles
directory_1 = '/home/lu/syscall_profiling/syscall_logs/co2_debian'
directory_2 = '/home/lu/syscall_profiling/syscall_logs/co2_ubuntu'
directory_3 = '/home/lu/syscall_profiling/syscall_logs/ctos_co2_logs'
# print(directory_2[-6:])

def generate_n_gram(n_gram, c, l):

    if len(n_gram) < l:
        n_gram.append(c)
        return n_gram

    elif len(n_gram) == l:
        n_gram = n_gram[1:]
        n_gram.append(c)
        return n_gram

    else:
        raise ValueError


def parse_ngram(filename, l=6):
    """ This function reads the tracefile and generate a profile of unique n_grams
    INPUT: filename --> name of the tracefile
           l --> length of ngram
    OUTPUT: n_gram"""
    n_gram = []
    ngram_dict = {}
    if os.stat(filename).st_size == 0:
        raise ValueError("The input file %s is empty!" % filename)
        return -1, -1
    with open(filename) as f:
        for line in f:
        # skip empty line in the trace file
            if line.strip():
                #print(line)
                line_list=line.split()
                try:
                    app_name = line_list[3]
                except:
                    raise ValueError
                if app_name == APP_NAME:

                    try:
                        key_action =line_list[6]
                    except:
                        raise ValueError
                    if filter_flag:
                        if key_action == "switch" or key_action == "sched_yield":
                        #print("remove")
                            continue
                    """generate streaming n_gram"""
                    n_gram = generate_n_gram(n_gram, key_action, l)
                    # print(n_gram)
                    if len(n_gram) == l:
                        n_gram_s = str(n_gram)
                        if n_gram_s not in ngram_dict.keys():
                            ngram_dict[n_gram_s] = 1
                        else:
                            ngram_dict[n_gram_s] += 1

    # sort the dictionary by its values in descending order
    ngram_dict = {k: v for k, v in sorted(ngram_dict.items(), key=lambda item: item[1],
                                                             reverse=True)}

    # Normalze the dictionary and achieve the frequency vector
    total = sum(ngram_dict.values())
    factor = 1 / total
    ngram_dict_normalized = {k: v * factor for k, v in ngram_dict.items()}

    return ngram_dict, ngram_dict_normalized


def laplace_smoothing(ngram_dict):
    """Calculate the frequency distribution with Laplace smoothing
    INPUT --> ngram_dict: dictionary of ngrams with values as integer occurrence numbers"""
    total = sum(ngram_dict.values()) + 1
    factor = 1 / total
    ngram_normalized = {k: (v+1) * factor for k, v in ngram_dict.items()}
    return ngram_normalized


def cross_entropy(dict1, dict2):

    if set(dict1.keys()) == set(dict2.keys()):
        # if two key set are identical, calculate cross entropy directly
        tmp_list = []
        for k in dict1.keys():
            p = dict1[k]
            if k in dict2.keys():
                q = dict2[k]
            if p != 0 and q != 0:
                tmp = (p - q) * math.log(p / q, 2)
                tmp_list.append(tmp)
    # print(tmp_list)
    c_entropy = sum(tmp_list)
    return c_entropy


def ngram_cross_entropy(ngram_1, ngram_2):
    """Calculate the crossentropy of two n_gram distribution with laplace smoothing"""
    # the keys only exist in ngram_1, but not in n_gram 2
    diff_12 = set(ngram_1) - set(ngram_2)
    diff_dict_12 = dict.fromkeys(list(diff_12), 0)

    # the keys only exist in ngram_2, but not in n_gram 1
    diff_21 = set(ngram_2) - set(ngram_1)
    diff_dict_21 = dict.fromkeys(list(diff_21), 0)

    ngram_1 = {**ngram_1, **diff_dict_21}
    ngram_2 = {**ngram_2, **diff_dict_12}

    if not (ngram_1.keys() == ngram_2.keys()):
        raise ValueError

    ngram_fre_1 = laplace_smoothing(ngram_1)
    ngram_fre_2 = laplace_smoothing(ngram_2)

    ce = cross_entropy(ngram_fre_1, ngram_fre_2)
    return ce


def filename_list_generation(directory):
    filename_list = []
    for filename in os.listdir(directory):
        filename_list.append(filename)
    return filename_list


def mutual_cross_entropy(directory):
    """Calculate the pairwise cross entropy in a directory
    Input --> a list of files in a specific directory
    Output -->  a list of mutual cross entropy
           --> cross entropy distance matrix"""
    file_list = filename_list_generation(directory)
    distance_matrix = np.zeros((len(file_list), len(file_list)))
    cross_entropy_list = []
    for indexes in list(itertools.combinations(range(len(file_list)), 2)):
        indexes = list(indexes)
        filename_1 = file_list[indexes[0]]
        filename_2 = file_list[indexes[1]]

        filename_1 = directory + "/" + filename_1
        filename_2 = directory + "/" + filename_2


        ngram_dict_1, ngram_dict_n_1 = parse_ngram(filename_1, n_gram_len)
        ngram_dict_2, ngram_dict_n_2 = parse_ngram(filename_2, n_gram_len)

        ce = ngram_cross_entropy(ngram_dict_1, ngram_dict_2)
        print(filename_1, filename_2, ce)

        cross_entropy_list.append(ce)
        distance_matrix[indexes[0], indexes[1]] = ce
        if distance_matrix[indexes[1], indexes[0]] == 0:
            distance_matrix[indexes[1], indexes[0]] = ce
        else:
            raise ValueError

    return cross_entropy_list, distance_matrix


def cross_ce(directory_1, directory_2):
    """Calculate the cross ce for tracefiles in two different directories
    Input --> 2 lists of files in two directory
    Output -->"""
    file_list_1 = filename_list_generation(directory_1)
    file_list_2 = filename_list_generation(directory_2)

    cross_entropy_list = []

    for indexes in list(itertools.product(range(len(file_list_1)), range(len(file_list_2)))):
        indexes = list(indexes)
        filename_1 = file_list_1[indexes[0]]
        filename_2 = file_list_2[indexes[1]]

        filename_1 = directory_1 + "/" + filename_1
        filename_2 = directory_2 + "/" + filename_2
        # print(filename_1, filename_2)

        ngram_dict_1, ngram_dict_n_1 = parse_ngram(filename_1, n_gram_len)
        ngram_dict_2, ngram_dict_n_2 = parse_ngram(filename_2, n_gram_len)

        ce = ngram_cross_entropy(ngram_dict_1, ngram_dict_2)
        # print(filename_1, filename_2, ce)
        cross_entropy_list.append(ce)
    return cross_entropy_list





def draw_graph(distance_matrix):

    dt = [('len', float)]
    distance_matrix = distance_matrix.view(dt)
    G = nx.from_numpy_matrix(distance_matrix)
    # G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())), string.ascii_uppercase)))

    G = nx.drawing.nx_agraph.to_agraph(G)
    G.node_attr.update(color="red", node_size=1, style="filled", shape = "point")
    G.edge_attr.update(color="blue", width="0.2")
    G.draw('ABS_new.png', format='png', prog='neato')



def main():

    # filename = sys.argv[-1]
    # ngram_dict, ngram_dict_n = parse_ngram(filename, n_gram_len)
    # plotting.histogram_plot(ngram_dict)


    ce_list, _ = mutual_cross_entropy(directory_1)

    ce_list = cross_ce(directory_1, directory_2)
    directory_list = [directory_1, directory_2, directory_3]
    label_list = []
    data_to_plot = []
    for indexes in list(itertools.combinations(range(len(directory_list)), 2)):
        indexes = list(indexes)
        dirt_1 = directory_list[indexes[0]]
        dirt_2 = directory_list[indexes[1]]
        label = dirt_1[-6:]+'-'+dirt_2[-6:]
        ce_list = cross_ce(dirt_1, dirt_2)
        # print(ce_list)
        label_list.append(label)
        data_to_plot.append(ce_list)
    print(data_to_plot)

    for dirt in directory_list:
        ce_list, _ = mutual_cross_entropy(dirt)
        print(ce_list)
        label = dirt[-6:]
        label_list.append(label)
        data_to_plot.append(ce_list)




    # data_to_plot = data_to_plot.tolist()
    """save data into a json file"""
    outpath = 'ce_nestedlist_co2.json'
    with open(outpath, 'w') as f:
        f.write(json.dumps(data_to_plot))

    data_to_plot = json.load(open(outpath))

    plotting.box_plot(data_to_plot, label_list)


if __name__ == "__main__":
    main()
