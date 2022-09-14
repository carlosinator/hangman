import pandas as pd
import numpy as np

def get_wordlist(path, min_word_length=1, remove_acronyms=False):

    df = pd.read_csv(path)
    
    # keep two columns and name them "word", "count"
    old_word_name = df.columns[0]
    df = df.rename(columns={old_word_name: "word"})
    df = df[["word", "count"]]

    df = clean_words(df, min_word_length=min_word_length, remove_acronyms=remove_acronyms)

    df["word"] = df["word"].str.lower()
    df = df.drop_duplicates()

    df = create_nonzero_frequencies(df)

    df['combination'] = 0

    return df


def reduce_with_query(df, query_string):
    if df.empty:
        return df
    return df[df["word"].str.fullmatch(query_string)]


def in_database(df, word):
    return not df[df["word"] == word].empty


def create_nonzero_frequencies(df):
    if not df[df["count"] == 0].empty:
        df["count"] = df["count"] + 1
    return df


def clean_words(df, remove_acronyms=True, min_word_length=1):

    # Remove this-> 's
    df = df[df["word"].str.contains("'s") == False]
    
    # cut too short words
    df = df[df["word"].str.len() >= min_word_length]

    if remove_acronyms:
        # cut some acronyms
        df = df[df["word"].str.isupper() == False]

    return df