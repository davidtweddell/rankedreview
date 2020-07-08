import pyrankvote
import inspect
import math
from pyrankvote import Candidate, Ballot

import utils

# global control variable
VERBOSE = False

top_N = 5

# where are we now?
frame = inspect.currentframe().f_code.co_name

# load the file
fn = "./covid-nois.xlsx"
df = utils.load_file(fn)


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


# make an empty list of ballots
ballots = []

# make a list of voters (should match the input spreadsheet)
voters_list = ['voter1', 'voter2', 'voter3']

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

utils.print_message(frame, "Executing STV selection.")
election_result = pyrankvote.single_transferable_vote(
    candidates, 
    ballots, 
    number_of_seats=3
)

# Show the evolution and the final result
utils.print_message(frame, "STV Selection Result.")
print(election_result)



# utils.print_message(frame, "Executing PBV selection.")
# election_result = pyrankvote.preferential_block_voting(
#     candidates, 
#     ballots, 
#     number_of_seats=3
# )

# # Show the evolution and the final result
# utils.print_message(frame, "PBV Selection Result.")
# print(election_result)