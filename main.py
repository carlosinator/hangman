import pandas as pd
import numpy as np
import functionality.data_functions as data_functions
import functionality.information_theory as it
import time
from functionality import game
from players import computer_player
from strategies import it_equal_prob

# SETUP OF GAME
true_word = "hello"
max_wrong_tries = 11
verbose = 1
wait_seconds = 1


df = data_functions.get_wordlist(path='./data/default_wordlist.csv', min_word_length=1)
if not data_functions.in_database(df, true_word):
    raise ValueError("Word not in Database")


plyr = computer_player.ComputerPlayer(df, it_equal_prob.compute_optimal_choice)
game = game.Game(player=plyr, word=true_word)

start = time.process_time()
guessed, wrong_tries, total_tries = game.play(max_wrong_tries=max_wrong_tries, wait_seconds=wait_seconds, verbose=verbose)
diff = time.process_time() - start

if guessed == False:
    print(true_word.upper() + " was not guessed. " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :(")
else:
    print("Guessed " + true_word.upper() + " after " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :)")

print("Elapsed time:", diff)