import os
import json
import random
import math
import numpy as np

co_list = ['co1', 'co2', 'co3', 'co5', 'co6', 'co7']
co_dict = {'co1': 0, 'co2': 1, 'co3': 2, 'co5': 3, 'co6': 4, 'co7': 5}

tracefile_json = 'trace_logs_fv_dict/co_all_fvl.json'

nr_round = 3


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


def generate_file_name_list(directory):
    dict_co_tracefiles = {}
    for filename in os.listdir(directory_name):
        co_name = filename.split('_')[0]
        if co_name in dict_co_tracefiles:
            dict_co_tracefiles[co_name].append(filename)
        else:
            dict_co_tracefiles[co_name]=[filename]
    return dict_co_tracefiles


def generate_filename_list_from_json(json_file):
    dict_co_tracefiles = {}
    with open(tracefile_json, 'r') as fp:
        dict_fv = json.load(fp)
    for filename in dict_fv.keys():
        co_name = filename.split('_')[0]
        if co_name in dict_co_tracefiles:
            dict_co_tracefiles[co_name].append(filename)
        else:
            dict_co_tracefiles[co_name] = [filename]
    return dict_co_tracefiles




def classifier(au_co_list):
    confusion_matrix = np.full((len(co_list), len(co_list)), 0)
    # print(confusion_matrix)

    # load the file_feature vector dictionary
    with open(tracefile_json, 'r') as fp:
        dict_fv = json.load(fp)

    decision_pos = 0
    decision_neg = 0
    decision_total = len(dict_fv.keys()) - len(au_co_list)

    for test_tracefile in dict_fv.keys():
        test_flag = test_tracefile.split("_")[0]
        if test_tracefile in au_co_list:
            continue
        else:
            ce_dict = {}
            for au_co in au_co_list:

                output_fv = ngram_cross_entropy(dict_fv[test_tracefile], dict_fv[au_co])
                ce_dict[au_co] = output_fv
            # print(ce_dict)
            determined_co = min(ce_dict, key=ce_dict.get)
            determined_co = determined_co.split('_')[0]
            # print(determined_co, test_flag)
            index_row = co_dict[test_flag]
            index_col = co_dict[determined_co]

            tmp = confusion_matrix[index_row, index_col]
            tmp += 1
            confusion_matrix[index_row, index_col] = tmp


            """ Check if the classification is correct or not"""
            if determined_co == test_flag:
                decision_pos += 1
            else:
                decision_neg += 1

    # print(decision_pos, decision_neg)
    if decision_neg + decision_pos == decision_total:
        accurate_rate = decision_pos/decision_total
    else:
        raise ValueError
    print(confusion_matrix)
    acc_list = []
    i = 0
    for row in confusion_matrix:
        acc = row[i]/sum(row)
        i = i+1
        # print(acc)
        acc_list.append(acc)
    # np.append(confusion_matrix, acc_list, axis =0)
    print(acc_list)
    return accurate_rate, confusion_matrix,acc_list



def main():
    dict_to_tracefile =generate_filename_list_from_json(tracefile_json)
    # print(dict_to_tracefile)
    accurate_list = []
    confusion_matrix_sum = np.zeros((nr_round, len(co_list), len(co_list)))
    acc_matrix = np.zeros((nr_round, len(co_list)))
    execution_count = 0
    for r in range(nr_round):
        print(r)
        """ Get the authorized app randomly"""
        au_cos = []
        for co in co_list:
            authorized_name = random.choice(dict_to_tracefile[co])

            au_cos.append(authorized_name)
        print(au_cos)
        # if au_cos[-1].split("_")[1] == 'ubuntu' or au_cos[-2].split("_")[1] == 'ubuntu' or au_cos[-3].split("_")[1] == 'ubuntu':
        #     continue

        accurate_rate, confusion_matrix, acc_list = classifier(au_cos)
        if any(t < 0.3 for t in acc_list):
            continue

        acc_matrix[r] = acc_list
        execution_count += 1
        accurate_list.append(accurate_rate)
        # print(confusion_matrix)
        # confusion_matrix_sum = np.insert(confusion_matrix_sum, r, confusion_matrix, axis=0)
        confusion_matrix_sum[r, :, :] = confusion_matrix

    sum_cm = confusion_matrix_sum.sum(axis=0)
    mean_cm = confusion_matrix_sum.mean(axis=0)
    print(confusion_matrix_sum.sum(axis=0))
    print(confusion_matrix_sum.mean(axis=0))
    # print(confusion_matrix_sum.std(axis=0))
    print(acc_matrix)
    np.savetxt('confusion_matrix_sum_2.txt', sum_cm, fmt='%.2f')
    np.savetxt('acc_2.txt', acc_matrix, fmt='%.2f')

if __name__ == "__main__":
    main()
