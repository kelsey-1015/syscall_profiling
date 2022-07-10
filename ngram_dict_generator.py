import os
import json


# This flag indicates whether to filter out switch and sched_yield
filter_flag = True
n_gram_len = 6
APP_NAME = 'python3'

directory_name = 'trace_logs'


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





def main():

    trace_fv_dict = {}
    for filename in os.listdir(directory_name):
        print(filename)
        print(filename.split('_'))
        filename_c= directory_name + "/" + filename
        ngram_dict, ngram_dict_n = parse_ngram(filename_c, n_gram_len)
        print(ngram_dict)
        trace_fv_dict[filename] = ngram_dict

    print(trace_fv_dict)

    with open('trace_logs_4.json', 'w') as fp:
        json.dump(trace_fv_dict, fp)

    #with open('trace_logs_test.json', 'r') as fp:
        # dict=json.load(fp)
        # print(dict['co1_centos_db1_1'])


if __name__ == "__main__":
    main()
