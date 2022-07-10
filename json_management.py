import json

"""This Document processes the json files, which are used to store the n-grams and corresponding occurrance number"""

tracefile_json = 'co_self_variance.json'


def json_filtering(log_file_old, log_file_filter):
    dict_update = {}
    with open(log_file_old, 'r') as fp:
        dict = json.load(fp)
        for k in dict.keys():
            # print(k)
            sys = k.split('_')[1]
            # print(sys)
            db = k.split('_')[2][:3]
            # print(db)
            if sys == "ubuntu" and db=='db0':
                print(k)
                fv = dict[k]
                dict_update[k] = fv
    with open(log_file_filter, 'w') as fp:
        json.dump(dict_update, fp)


def json_update(log_file_1, log_file_2, log_file_merge):
    with open(log_file_1, 'r') as fp_1:
        dict_1 = json.load(fp_1)
    with open(log_file_2, 'r') as fp_2:
        dict_2 = json.load(fp_2)

    dict_2.update(dict_1)

    with open(log_file_merge, 'w') as fp:
        json.dump(dict_2, fp)


def print_json_keys(json_file):
    with open(json_file, 'r') as fp:
        dict=json.load(fp)
        key_list = ['co6_ubuntu_db0_0', 'co6_ubuntu_db0_1', 'co6_ubuntu_db0_2', 'co6_ubuntu_db0_3','co6_ubuntu_db0_4'
                         'co6_ubuntu_db1_0', 'co6_ubuntu_db1_1', 'co6_ubuntu_db1_2', 'co6_ubuntu_db1_3', 'co6_ubuntu_db1_4'
                         'co6_ubuntu_db2_0', 'co6_ubuntu_db2_1', 'co6_ubuntu_db2_2', 'co6_ubuntu_db2_3', 'co6_ubuntu_db2_4',]
        # for k in dict.keys():
        #     if k.split("_")[1] == 'ubuntu' and k.split('_')[0]=='co7':
        #         key_list.append(k)
        for k in key_list:
            del dict[k]

    with open(json_file, 'w') as fp:
        json.dump(dict, fp)


def element_count(json_file):
    with open(json_file, 'r') as fp:
        dict = json.load(fp)

    # print(len(dict))
    "Print the keys of a dictionary"
    for k, v in dict.items():
        print(k)

    print(len(dict.keys()))



    # c_list = []
    # for k, v in dict.items():
    #     if k.split("_")[0] == 'co4':
    #         # print(k)
    #         if k.split("_")[2][2] == '0':
    #             print(k)
    #             c=len(v.keys())
    #             c_list.append(c)
    # print(sum(c_list)/len(c_list))




def element_add(json_file):
    with open(json_file, 'r') as fp:
        dict=json.load(fp)

        insert_k_list = ['co7_ubuntu_db0_0', 'co7_ubuntu_db0_1', 'co7_ubuntu_db0_2', 'co7_ubuntu_db0_3','co7_ubuntu_db0_4',
                         'co7_ubuntu_db1_0', 'co7_ubuntu_db1_1', 'co7_ubuntu_db1_2', 'co7_ubuntu_db1_3', 'co7_ubuntu_db1_4',
                         'co7_ubuntu_db2_0', 'co7_ubuntu_db2_1', 'co7_ubuntu_db2_2', 'co7_ubuntu_db2_3', 'co7_ubuntu_db2_4',]
        for k in insert_k_list:
            dict[k] = dict['co7_centos_db0_0']

    with open(json_file, 'w') as fp:
        json.dump(dict, fp)



def main():
    # json_update(tracefile_json, tracefile_json_a, tracefile_json_b)
    # element_add(tracefile_json)
    # # print_json_keys(tracefile_json)
    element_count(tracefile_json)

    pass

if __name__ == "__main__":
    main()
