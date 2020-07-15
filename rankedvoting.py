# core modules
import inspect
import math
import timeit

# external modules
import numpy as np
import pyrankvote
from pyrankvote import Candidate, Ballot

# local modules
import utils
import matrix_votes as mv # tools for a different arrangement of votes


# global control variabls
VERBOSE = False
top_N = 3

# local function to read forms data and rename columns for simplicity
def read_forms_data(fn):

    frame = inspect.currentframe().f_code.co_name
    utils.print_message(frame,"Reading data.")

    df = utils.load_file(fn)

    df.columns = [np.arange(0,df.shape[1])]

    return df


def main():
    # where are we now?
    frame = inspect.currentframe().f_code.co_name

    # load the data into a dataframe
    df = read_forms_data("./td_ready.xlsx").values.tolist()
    ballots = []
    candidates = []

    # make the ballots
    utils.print_message(frame, "Making ballots.")

    # output from MS Forms is a totally different data structure than 
    # the matrix type in the other functions I wrote
    # - it contains a column with a list each respondent's ranking
    # - items in the ranking column are separated by a semi-colon
    for item in df:
        # ranked list is in column 5 (with 0-based index)
        b = item[5].split(';')
        # drop the last empty item
        # TODO: probably other ways to do this to, with an iterator maybe
        b = b[:(len(b)-1)]
        ballots.append(Ballot(ranked_candidates=[Candidate(x) for x in b]))
    if VERBOSE:
        print(ballots)

    # make the list of candidates
    utils.print_message(frame, "Making list of candidate names.")
    # use the last ballot, sorted, to get the list of candidate names
    # this is an easy way to do it and just re-uses the last ballot
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
