import os
import json
from n_gram import *

directory = 'trace_logs'
# This flag indicates whether to filter out switch and sched_yield
filter_flag = True
n_gram_len = 6
APP_NAME = 'python3'


dict_1 = {'a': 1}
dict_2 = {'b': 1}
dict_3 = {'c': 1}

dict_list= [dict_1, dict_2, dict_3]

value = [1, 2, 3]


ef parse_ngram(filename, l=6):
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


def write_to_json(directory):
    for filename in os.listdir(directory):
        print(filename)
        filename = directory + "/" + filename
        _, ngram_dict_n = parse_ngram(filename, n_gram_len)

        with open('data.json', 'w') as fp:
            json.dump(ngram_dict_n, fp)

def main():
    # write_to_json(directory)
    # with open("data.json") as fp:
    #     dict = json.load(fp)
    # print(dict)


    for index in range(1):
        # print(index)
        dict = {index: dict_list[index]}
        # print(dict)
        if os.path.isfile('data.json'):
            with open("data.json") as fp:
                dict_original = json.load(fp)
                dict_original.update(dict)

            print('yes')
        else:
            print('No')

        with open('data.json', 'a') as fp:
            json.dump(dict, fp)


    #     print(dict)
    #     # with open('data.json', 'a') as fp:
    #     #     json.dump(dict, fp)



if __name__ == "__main__":
    main()