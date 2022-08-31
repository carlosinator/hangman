import pandas as pd
import numpy as np

def get_wordlist(path=None, min_word_length=1, remove_all_caps=False):

    # import csv (or text file)
    if path == None:
        df = pd.read_csv("default_wordlist.txt")
    else:
        df = pd.read_csv(path)
    
    # keep only one column and name it "Word"
    old_col_name = df.columns[0]
    df = df.rename(columns={old_col_name: "Word"})
    df = df[["Word"]]
    
    # Remove this-> '
    df = df[df["Word"].str.contains("'") == False]
    
    # cut too short words
    df = df[df["Word"].str.len() >= min_word_length]


    if remove_all_caps:
        # cut acronyms DOESN'T WORK
        df = df[df["Word"].str.isupper() == False]


    df["Word"] = df["Word"].str.lower()
    df = df.drop_duplicates()
    return df
