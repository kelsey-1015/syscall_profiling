import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib

""" This script plots multple group boxplot (written for the cross-platform comparison)"""

label_list_0 = ['ubuntu-debian', 'ubuntu-centos', 'debian-centos', 'ubuntu','debian',
                  'centos']
label_list = ['ubuntu-debian', 'debian-centos', 'ubuntu-centos', 'debian', 'ubuntu',
              'centos']

label_list_new = ['ubuntu-debian', 'ubuntu-centos', 'debian-centos', 'ubuntu', 'debian', 'centos']

outpath0 = 'ce_nestedlist_co1.json'
data_to_plot_0 = json.load(open(outpath0))
label_data_dict_0 = dict(zip(label_list_0, data_to_plot_0))

data_0 = [label_data_dict_0[l] for l in label_list_new]

outpath1 = 'ce_nestedlist_co2.json'
data_to_plot_1 = json.load(open(outpath1))
label_data_dict_1 = dict(zip(label_list, data_to_plot_1))
data_1 = [label_data_dict_1[l] for l in label_list_new]

outpath2 = 'ce_nestedlist_co4.json'
data_to_plot_2 = json.load(open(outpath2))
label_data_dict_2 = dict(zip(label_list, data_to_plot_2))
data_2 = [label_data_dict_2[l] for l in label_list_new]


font = {'family': 'normal',
            'weight': 'bold',
            'size': 15}

matplotlib.rc('font', **font)

ticks = ['Ubuntu-Debian', 'Ubuntu-Centos', 'Debian-Centos', 'Ubuntu', 'Debian', 'Centos']

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

plt.figure()

bpl = plt.boxplot(data_0, 1, positions=np.array(range(len(data_0)))*2.0-0.5, sym='', widths=0.3)
bpm = plt.boxplot(data_1, 1, positions=np.array(range(len(data_1)))*2.0, sym='', widths=0.3)
bpr = plt.boxplot(data_2, 1, positions=np.array(range(len(data_2)))*2.0+0.5, sym='', widths=0.3)
set_box_color(bpl, '#D7191C') # colors are from http://colorbrewer2.org/
set_box_color(bpm, '#636363') # colors are from http://colorbrewer2.org/
set_box_color(bpr, '#2C7BB6')

# draw temporary red and blue lines and use them to create a legend
plt.plot([], c='#D7191C', label='App1')
plt.plot([], c='#636363', label='App2')
plt.plot([], c='#2C7BB6', label='App3')
plt.legend()

plt.xlabel('Platform OS', fontsize=18)
plt.ylabel('Cross Entropy', fontsize=18)

plt.xticks(range(0, len(ticks) * 2, 2), ticks)
# plt.xlim(-2, len(ticks)*2)
# plt.ylim(0, 8)
# plt.tight_layout()
plt.grid()
plt.show()
# plt.savefig('boxcompare.png')