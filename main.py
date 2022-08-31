import pandas as pd
import numpy as np
import create_ds
import hangman_functionality as hf
import hangman_solver as hs
import information_theory as it
import time
from pathlib import Path  

df = create_ds.get_wordlist(min_word_length=1)

true_word = "RUN"
max_tries = 11
verbose=1

wrong_tries, total_tries = hf.test_run_one_game(hs.ComputerPlayer, df=df, true_word=true_word, max_wrong_tries=max_tries, wait_seconds=0, verbose=verbose)

if wrong_tries == None:
    print(true_word.upper() + " was not guessed. " + str(total_tries) + " total guesses :(")
else:
    print("Guessed " + true_word.upper() + " after " + str(wrong_tries) + " wrong and " + str(total_tries) + " total guesses :)")




