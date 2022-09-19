import pandas as pd
import numpy as np
import functionality.data_functions as data_functions
import functionality.information_theory as it
import time
from functionality import game
from optimization import look_up
from players import computer_player
from strategies import it_equal_prob
from strategies import relative_freq


# SETUP OF GAME
true_word = "oxaluric"
RANDOM_WORD = True
max_wrong_tries = 11
verbose = 0
wait_seconds = 0

st1 = time.process_time()
df = data_functions.get_wordlist(path='./data/word_frequency.csv', min_word_length=1)
if not data_functions.in_database(df, true_word):
    raise ValueError("Word not in Database")
print("Setup time:", time.process_time() - st1)

lu = look_up.LookUp()
lu.load('./data/lookup/lu_word_frequency_relative_freq.csv')
plyr = computer_player.ComputerPlayer(df, relative_freq.compute_optimal_choice, lookup=lu)
gme = game.Game(player=plyr)

elapsed = []
ITER = 1000
for _ in range(0,ITER):
    if RANDOM_WORD:
        index = int(np.random.random(1) * df.shape[0])
        true_word = df["word"][index]
    print("Computer is guessing:", true_word.upper())

    start = time.process_time()
    guessed, wrong_tries, total_tries = gme.play(word=true_word, max_wrong_tries=max_wrong_tries, wait_seconds=wait_seconds, verbose=verbose)
    diff = time.process_time() - start

    if guessed == False:
        print(true_word.upper() + " was not guessed. " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :(")
    else:
        print("Guessed " + true_word.upper() + " after " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :)")

    print("Elapsed time:", diff)
    elapsed.append(diff)
    print("-"*50)


elapsed = np.array(elapsed)
print("Elapsed time for", ITER, "samples: mean:", np.mean(elapsed), "std:", np.std(elapsed))