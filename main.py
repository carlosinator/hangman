import pandas as pd
import numpy as np
import create_ds
import hangman_functionality as hf
import hangman_solver as hs
import information_theory as it
import time
from pathlib import Path  

df = create_ds.get_wordlist(min_word_length=1)

true_word = "maw"
max_tries = None
verbose=1

tries = hf.test_run_one_game(hs.ComputerPlayer, df=df, true_word=true_word, max_tries=max_tries, wait_seconds=0, verbose=verbose)

if tries == None:
    print(true_word.upper() + " was not guessed :(")
else:
    print("Guessed " + true_word.upper() + " after " + str(tries) + " guesses :)")




