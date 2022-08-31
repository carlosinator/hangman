import pandas as pd
import numpy as np
import data_functions
import hangman_functionality as hf
import hangman_solver as hs
import information_theory as it
import time
from pathlib import Path  

df = data_functions.get_wordlist(min_word_length=1)

true_word = "starry"
if not data_functions.in_database(df, true_word):
    raise ValueError("Word not in Database")

max_tries = 11
verbose=0

wrong_tries, total_tries = hf.test_run_one_game(hs.ComputerPlayer, df=df, true_word=true_word, max_wrong_tries=max_tries, wait_seconds=0, verbose=verbose)

if wrong_tries == None:
    print(true_word.upper() + " was not guessed. " + str(total_tries) + " total guesses :(")
else:
    print("Guessed " + true_word.upper() + " after " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :)")




