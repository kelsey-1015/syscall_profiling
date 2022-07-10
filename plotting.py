import matplotlib.pyplot as plt
import matplotlib
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
    Title = "Stability of n-gram profiles of different training datassets"
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 15}

    matplotlib.rc('font', **font)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_to_plot, vert= True, notch=True, patch_artist=True)
    for box in bp['boxes']:
        box.set(color='red')
        box.set(facecolor='white')
    ax.set_xticklabels(x_labels)
    # plt.xlabel('App')
    plt.ylabel('cross entropy')
    # plt.title(Title)
    plt.grid()
    plt.show()


def plot_cdf(input_list):
    """This function plots cdf function of a list"""
    data = np.array(input_list)
    print(len(data))

    # sort the data:
    data_sorted = np.sort(data)
    print(data_sorted)

    # calculate the proportional values of samples
    p = 1. * np.arange(len(data_sorted)) / (len(data_sorted) - 1)
    print(p)


    # plot the sorted data:
    fig = plt.figure()
    # ax1 = fig.add_subplot(121)
    # ax1.plot(p, data_sorted)
    # ax1.set_xlabel('$p$')
    # ax1.set_ylabel('$x$')

    ax2 = fig.add_subplot(111)
    ax2.set_xscale('log')
    ax2.plot(data_sorted, p, color='red')
    ax2.grid()
    #
    ax2.set_xlabel('Number of occurrences of each n-gram entry')
    ax2.set_ylabel('Probability')
    #
    plt.show()

def main():
    with open('co_self_variance.json', 'r') as fp:
        data_plot_dict = json.load(fp)
    # data_plot_dict = json.load('co_self_variance.json')
    # label_list = ['App1', 'App2', 'App3']
    # co_list = ['co1', 'co2', 'co3']
    # data_to_plot = [data_plot_dict[c] for c in co_list]
    # box_plot(data_to_plot, label_list)

    plot_cdf()
if __name__ == "__main__":
    main()
