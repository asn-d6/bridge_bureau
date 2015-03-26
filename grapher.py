import numpy as np
from numpy.random import randn
import pandas as pd
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def init_graph_style():
    sns.set_palette("deep", desat=.6)
    sns.set_context(rc={"figure.figsize": (8, 4)})
    np.random.seed(9221999)



def graph_read_history(read_history_list):
    init_graph_style()

#    read_history_list = sorted(read_history_list)[:-200]
#    plt.title("Distribution of daily bandwidth history on bridges (200 highest observations pruned)")

    plt.title("Distribution of daily bandwidth history on bridges")

    plt.xlabel("Megabytes read per day")
    plt.ylabel("Number of bridges")

    plt.hist(read_history_list, 50)
    sns.rugplot(read_history_list)

#    print len(read_history_list)
#    sns.distplot(read_history_list, kde=False, hist=True)
#    plt.boxplot(read_history_list)

    plt.show()
