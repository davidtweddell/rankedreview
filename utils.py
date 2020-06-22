# analysis_utils.py
# mostly just message formatting and generic file loading
#
from __future__ import print_function
import logging
import inspect
import os.path
import pandas as pd
import numpy as np
import math

# helpful message printer functions - filter presentaiton
def print_filter(before, after):
    """report the results of a filtering operation
    
    :param before: start value
    :type before: int
    :param after: resulting value
    :type after: int
    """
    return ": filtering {0} items to {1} items".format(before, after)


# message printer and output to logger
def print_message(frame, msg):
    """format a message
    
    :param frame: name of calling function
    :type frame: str
    :param msg: message to print
    :type msg: str
    """

    s = "[{0}]:".format(frame).ljust(24) + msg

    print(s)
    logging.info(s)


def print_graph_metrics(G):
    """Print out some summary metrics about the graph.
    
    :param G: a graph
    :type G: nx.Graph
    """

    frame = inspect.currentframe().f_code.co_name

    # compute Graph metrics
    deg_sum = 0
    for _,d in G.degree():
        deg_sum += d

    msg1 = "average degree: {:.2f}".format(deg_sum/len(G))
    msg2 = "metric 2 ln(N): {:.2f}".format(2*math.log(len(G)))
    msg3 = "number of nodes: {:d}".format(G.number_of_nodes())
    msg4 = "number of edges: {:d}".format(G.number_of_edges())

    for msg in [msg1, msg2, msg3, msg4]:
        print_message(frame, msg)



def load_file(fname):
    """Read an excel or csv file to a pandas DataFrame.
    
    :param fname: filename to read
    :type fname: str
    :return: data from the file
    :rtype: pandas DataFrame
    """

    # Read the file
    print_message(inspect.currentframe().f_code.co_name, 
                    "load file "+str(fname))


    infile_type = os.path.splitext(fname)[1]
    if infile_type == ".csv":
        df = pd.read_csv(fname)
    # it had better be an xlsx file
    else:
        df = pd.read_excel(fname)

    # handle NANs
    df = df.replace(np.nan, '', regex=True)

    return df


