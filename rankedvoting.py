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

    # # CFI-EOF
    # # load the file
    # fn = "./covid-nois.xlsx"
    # df = read_ranked_columns(fn)
    # # list of candidates
    # candidates, candidate_names = make_candidate_list(df)
    # # list of voters
    # voters_list = ['voter1', 'voter2', 'voter3']
    # # make ballots
    # ballots = make_ballots(df, candidate_names, voters_list)



    # TD Ready - totally different data structure
    df2 = read_forms_data("./td_ready.xlsx").values.tolist()
    ballots = []
    candidates = []

    # make the ballots
    for item in df2:
        b = item[5].split(';')
        print(b)
        # drop the last empty item
        # probably other ways to do this to, with an iterator maybe
        b = b[:(len(b)-1)]
        ballots.append(Ballot(ranked_candidates=[Candidate(x) for x in b]))
    if VERBOSE:
        print(ballots)

    # make the list of candidates
    c = sorted(df2[1][5].split(';')[:5])
    for the_candidate in c:
        candidates.append(Candidate(the_candidate))
    # show the list of Candidate objects
    if VERBOSE:
        print(candidates)


    # run the vote
    utils.print_message(frame, "Executing STV selection.")
    election_result = pyrankvote.single_transferable_vote(
        candidates, 
        ballots, 
        number_of_seats=1
    )

    # Show the evolution and the final result
    utils.print_message(frame, "STV Selection Result.")
    print(election_result)




if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    execution_time = stop - start

    print(">>> Program Executed in {0:.2f} s".format(execution_time))
