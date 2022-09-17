import pandas as pd
import numpy as np
import functionality.data_functions as data_functions
import functionality.information_theory as it
import time
from functionality import game
from players import computer_player
from strategies import it_equal_prob
from strategies import relative_freq


# SETUP OF GAME
true_word = "spaghetti"
RANDOM_WORD = False
max_wrong_tries = 11
verbose = 1
wait_seconds = 0


df = data_functions.get_wordlist(path='./data/word_frequency.csv', min_word_length=1)
if not data_functions.in_database(df, true_word):
    raise ValueError("Word not in Database")


if RANDOM_WORD:
    index = int(np.random.random(1) * df.shape[0])
    true_word = df["word"][index]
print("Computer is guessing:", true_word.upper())

plyr = computer_player.ComputerPlayer(df, relative_freq.compute_optimal_choice)
gme = game.Game(player=plyr, word=true_word)

start = time.process_time()
guessed, wrong_tries, total_tries = gme.play(max_wrong_tries=max_wrong_tries, wait_seconds=wait_seconds, verbose=verbose)
diff = time.process_time() - start

if guessed == False:
    print(true_word.upper() + " was not guessed. " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :(")
else:
    print("Guessed " + true_word.upper() + " after " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :)")

print("Elapsed time:", diff)
print("-"*50)