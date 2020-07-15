import inspect
import math
import timeit
import utils

import numpy as np

import pyrankvote
from pyrankvote import Candidate, Ballot

# functions for generalized matrix of candidates (v) vs voters (h)
def make_ballots(df, candidate_names, voters_list):

    frame = inspect.currentframe().f_code.co_name

    # make an empty list of ballots
    ballots = []

    # # make a list of voters (should match the input spreadsheet)
    # voters_list = ['voter1', 'voter2', 'voter3']

    utils.print_message(frame, "Making ballots.")
    for voter in voters_list:
        # get the list of rankings for the current voter
        ranks = df[voter].to_list()
        # candidates not rated end up with an empty entry in the list = ''
        # we can't use that for comparison, so let's set unrated candidates to a 
        # low preference - say 99, then use map to convert everything 
        # to a list of ints
        ranks = list(map(int,[99 if r == '' else r for r in ranks]))

        # create an empty ballot and fill it with candidate names for this voter
        # b = []
        b = [name for _,name in sorted(zip(ranks,candidate_names))]

        # we allow only the top N candidates
        b = b[:top_N]

        utils.print_message(frame, "{1}'s top-{2} ballot from most to least preferred = {0}".format(b,voter, top_N))

        # add this ballot to the list of ballots
        ballots.append(Ballot(ranked_candidates=[Candidate(x) for x in b]))


    # show the ballots
    if VERBOSE:
        print("list of all ballots: {0}".format(ballots))
    
    return ballots

# functions for generalized matrix of candidates (v) vs voters (h)
def make_candidate_list(df):

    frame = inspect.currentframe().f_code.co_name

    # make a list of candidates
    utils.print_message(frame, "Making list of Candidates.")
    candidate_names = [] # just for assembling the ballots
    candidates = []      # to contain the Candidate objects

    # for each item in the dataframe:
    for item in df.iterrows():
        # get the candidate's surname and add it to both lists
        c = item[1][0].split(',')[0]
        candidate_names.append(c)
        candidates.append(Candidate(c))
    # show the list of Candidate objects
    if VERBOSE:
        print(candidates)

    return candidates, candidate_names


# functions for generalized matrix of candidates (v) vs voters (h)
def read_ranked_columns(fn):

    frame = inspect.currentframe().f_code.co_name
    utils.print_message(frame,"Reading data.")

    df = utils.load_file(fn)

    return df