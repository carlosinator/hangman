import pandas as pd
import numpy as np
import create_ds
import hangman_functionality as hf
import hangman_solver as hs
import information_theory as it
import time
from pathlib import Path  

df = create_ds.get_wordlist(min_word_length=1)

true_word = "an"
max_tries = 100
verbose=0

tries = hf.test_run_one_game(hs.ComputerPlayer, df=df, true_word=true_word, max_tries=max_tries, wait_seconds=0, verbose=verbose)

if tries == None:
    print(true_word.upper() + " was not guessed :(")
else:
    print("Guessed " + true_word.upper() + " after " + str(tries) + " guesses :)")


def compute_for_all_words(df_with_tries):
    df_with_tries["Tries"] = df_with_tries.apply(lambda x : hf.test_run_one_game(hs.ComputerPlayer, df=df, true_word=x["Word"], max_tries=max_tries, wait_seconds=0, verbose=0), axis=1)

    # filepath = Path('./wordswithtries.csv')
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    # df_with_tries.to_csv(filepath)
    return df_with_tries

