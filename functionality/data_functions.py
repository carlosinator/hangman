import pandas as pd
import numpy as np

def get_wordlist(path, min_word_length=1, remove_all_caps=False):

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


def reduce_with_query(df, query_string):
    if df.empty:
        return df
    return df[df["Word"].str.fullmatch(query_string)]


def in_database(df, word):
    return not df[df["Word"] == word].empty