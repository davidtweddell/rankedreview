import pyrankvote
import inspect
import math
import timeit
import numpy as np
from pyrankvote import Candidate, Ballot

import utils

# global control variable
VERBOSE = False
top_N = 3


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


def read_ranked_columns(fn):

    frame = inspect.currentframe().f_code.co_name
    utils.print_message(frame,"Reading data.")

    df = utils.load_file(fn)

    return df


def read_forms_data(fn):

    frame = inspect.currentframe().f_code.co_name
    utils.print_message(frame,"Reading data.")

    df = utils.load_file(fn)

    df.columns = [np.arange(0,df.shape[1])]

    return df


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



def main():
    # where are we now?
    frame = inspect.currentframe().f_code.co_name

    # TD Ready - totally different data structure
    df2 = read_forms_data("./td_ready.xlsx").values.tolist()
    ballots = []
    candidates = []

    # make the ballots
    utils.print_message(frame, "Making ballots.")

    for item in df2:
        # ranked list is in column 5 (with 0-based index)
        b = item[5].split(';')
        # drop the last empty item
        # probably other ways to do this to, with an iterator maybe
        b = b[:(len(b)-1)]
        ballots.append(Ballot(ranked_candidates=[Candidate(x) for x in b]))
    if VERBOSE:
        print(ballots)

    # make the list of candidates
    utils.print_message(frame, "Making list of candidate names.")

    # use the last ballot, sorted, to get the list of candidate names
    for the_candidate in sorted(b):
        candidates.append(Candidate(the_candidate))
    # show the list of Candidate objects
    if VERBOSE:
        print(candidates)


    # run the STV vote
    utils.print_message(frame, "Executing STV selection.")
    stv_election_result = pyrankvote.single_transferable_vote(
        candidates, 
        ballots, 
        number_of_seats=1
    )
    stv_winner = stv_election_result.get_winners()[0].name
    utils.print_message(frame, "STV Selected: {0}".format(stv_winner))
    if VERBOSE:
        utils.print_message(frame, "STV Selection Result.")
        print(stv_election_result)


    # run the PBV vote
    utils.print_message(frame, "Executing PBV selection.")
    pbv_election_result = pyrankvote.preferential_block_voting(
        candidates, 
        ballots, 
        number_of_seats=1
    )
    pbv_winner = pbv_election_result.get_winners()[0].name
    utils.print_message(frame, "PBV Selected: {0}".format(pbv_winner))
    if VERBOSE:
        utils.print_message(frame, "PBV Selection Result.") 
        print(pbv_election_result)


    # run the IRV vote
    utils.print_message(frame, "Executing IRV selection.")
    irv_election_result = pyrankvote.instant_runoff_voting(
        candidates, 
        ballots)
    irv_winner = irv_election_result.get_winners()[0].name
    utils.print_message(frame, "IRV Selected: {0}".format(irv_winner))
    if VERBOSE:
        utils.print_message(frame, "IRV Selection Result.")
        print(pbv_election_result)


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    execution_time = stop - start

    print(">>> Program Executed in {0:.2f} s".format(execution_time))
