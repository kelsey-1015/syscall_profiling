import json
import itertools
import math
import numpy as np
import plotting

# tracefile_json = 'trace_logs_1_7_ubuntu.json'
tracefile_json = 'trace_logs_fv_dict/co6_ubuntu_db1_fv.json'
co_list = ['co6']
# co_list=['db0', 'db1']

# co_list = ['co5', 'co6', 'co7']

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


def co_dict(co_name_std, co=True):

    dict_co ={}

    with open(tracefile_json, 'r') as fp:
        dict = json.load(fp)
        for k, v in dict.items():
            print(k)
            if co:
                co_name = k.split('_')[0]
            else:
                # We can also extract by db
                co_name = k.split('_')[-2]
            if co_name == co_name_std:
                dict_co[k] = v

    return dict_co


def self_variance_indi(co_name):
    dict_co = co_dict(co_name)
    list_key = list(dict_co.keys())
    ce_list = []
    for p in itertools.combinations(list_key, 2):
        ce = ngram_cross_entropy(dict_co[p[0]], dict_co[p[1]])
        ce_list.append(ce)
    avg = sum(ce_list)/len(ce_list)
    return avg, ce_list


def compute_distance():
    dict_distance ={}
    for pair in itertools.combinations(co_list, 2):
        pair = list(pair)
        print(pair)
        dict_co_1 = co_dict(pair[0])
        dict_kl_1 = list(dict_co_1.keys())
        dict_co_2 = co_dict(pair[1])
        dict_kl_2 = list(dict_co_2.keys())
        # print(dict_kl_1, dict_kl_2)
        """ Calculate the mutual ce of a list"""
        pair_ce_list = []
        for p in list(itertools.product(dict_kl_1, dict_kl_2)):

            co_name_1 = p[0].split("_")[0]
            co_name_2 = p[1].split("_")[0]
            pair_name = co_name_1+'_'+co_name_2
            ng_1 = dict_co_1[p[0]]
            ng_2 = dict_co_2[p[1]]
            ce = ngram_cross_entropy(ng_1, ng_2)
            # print(ce)
            pair_ce_list.append(ce)
        avg = sum(pair_ce_list)/len(pair_ce_list)
        dict_distance[pair_name] = avg
        # print(avg)
        # print(pair_ce_list)
    print(dict_distance)


def n_gram_distribution(file_name='co1_ubuntu_db0-1'):
    with open(tracefile_json, 'r') as fp:
        dict = json.load(fp)


    fv = dict[file_name]
    distribution = list(fv.values())
    return distribution




def main():
    # compute_distance()
    co_sv_dict = {}
    for co in co_list:
        ce_avg, ce_list =self_variance_indi(co)
        # ce_list = np.array(ce_list)
        co_sv_dict[co] = ce_list
        # print(co, ce_avg, ce_list)
        print(ce_avg)

    # with open('co_self_variance.json', 'w') as fp:
    #     json.dump(co_sv_dict, fp)

    #
    # distr = n_gram_distribution()
    # print(len(distr))
    # plotting.plot_cdf(distr)



if __name__ == "__main__":
    main()