import matplotlib.pyplot as plt
import numpy as np
import json


def histogram_plot(syscall_count_dict):
    frequecy  = list(syscall_count_dict.values())
    sys_labels = list(syscall_count_dict.keys())
    # print(sys_labels)
    N = len(sys_labels)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.7
    histogram = plt.barh(ind, frequecy, width, color='r')
    plt.xscale("log")
    # plt.yticks(ind, sys_labels, fontsize=5)
    plt.xlabel("count")
    plt.ylabel("ngram_index")
    plt.title("Distribution of ngram of length 6 of ML_1 of same training sets")

    # write absolute number at the end of each bar
    text_index = 0
    for rect in histogram:

        width = rect.get_width()
        print(rect.get_y())
        # print(height)
        if text_index % 15 == 0:
            plt.text(1.05*width, rect.get_y() + rect.get_height() / 2.0, '%d' % int(frequecy[text_index]), fontsize=5)
        text_index = text_index + 1
    plt.show()


def box_plot(data_to_plot, x_labels):
    """Input: data_to_plot: it can be a nested list or a list"""
    Title = "Stability of n-gram frequency distribution over different platforms of APP3"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_to_plot)
    ax.set_xticklabels(x_labels)
    plt.xlabel('platform os')
    plt.ylabel('cross entropy')
    plt.title(Title)
    plt.grid()
    plt.show()
    # plt.savefig('co2.png')

def main():
    label_list = ['ubuntu-debian', 'debian-centos', 'ubuntu-centos','debian', 'ubuntu',
                  'centos']
    outpath = 'ce_nestedlist_co2.json'
    data_to_plot = json.load(open(outpath))
    label_data_dict = dict(zip(label_list, data_to_plot))
    with open('cross_platform_co2_CE.json', 'w') as fp:
        json.dump(label_data_dict, fp)

    # label_list_new = ['ubuntu-debian', 'ubuntu-centos', 'debian-centos', 'ubuntu', 'debian', 'centos']
    # data_to_plot_new = [label_data_dict[l] for l in label_list_new]
    # box_plot(data_to_plot_new, label_list_new)
    # box_plot(data_to_plot, label_list)

    # box_plot(ce_ml1_list)

if __name__ == "__main__":
    main()