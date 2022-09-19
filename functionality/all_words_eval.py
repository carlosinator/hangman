import numpy as np
import pandas as pd
import re
from strategies import relative_freq
import copy
import warnings
warnings.filterwarnings("ignore")
from functionality import data_functions
from functionality import knowledge

GLOBAL_COUNT = 0


def all_eval(df, strategy_func):
    """
    A function to evaluate the necessary number of (wrong) tries for each word recursively

    Args:
        df (pandas.DataFrame): All words to be evaluated
        strategy_func (function): Function based on which guessing decisions are made

    Returns:
        pandas.DataFrame: DataFrame with (wrong) tries for each word and the last combination assessed  
    """
    df['wrong_tries'] = 0
    df['total_tries'] = 1
    max_len = data_functions.compute_max_len(df)
    for word_length in range(1,max_len+1):
        wl = data_functions.reduce_with_query(df, query_string='.' * word_length)
        print(wl.shape)
        df.update(rec_one_len_eval(wl, knowledge.Knowledge(word_length=word_length), strategy_func=strategy_func))
    return df

def rec_one_len_eval(word_list, kl, strategy_func, depth=0):
    # print("on depth", depth, "with shape", word_list.shape)
    """
    Evaluates the necessary number of tries for all words of one length

    Args:
        word_list (pandas.DataFrame): All words of one length
        knowledge (object): Known limitations of words
        strategy_func (function): Function based on which splitting guesses are made
    """

    # if word_list.shape[0] == 1:        
    #     if kl.completed():
    #         word_list["total_tries"] += 0
    #         word_list["wrong_tries"] += 0
    #     else:
    #         word_list["total_tries"] += 1
    #         word_list["wrong_tries"] += 0   
    if word_list.shape[0] == 0:
        return word_list

    elif word_list.shape[0] == 1:
        if not kl.completed():
            word_list["total_tries"] += 1        
        global GLOBAL_COUNT
        GLOBAL_COUNT += 1
        if GLOBAL_COUNT % 100 == 0:
            print("Completed", GLOBAL_COUNT, "words")

    else:
        word_list['total_tries'] += 1
        letter,_ = strategy_func(word_list)
        # QUESTION: When to update knowledge: Beginning or end of turn? beginning
        splits = split_on_letter(word_list, letter)
        for x in splits.groups:
            subset = splits.get_group(x)
            comb = list(subset.iloc[0]['combination'])
            if comb == []:
                subset["wrong_tries"] += 1
            k = copy.deepcopy(kl)
            k.update(letter, comb)
            wl = rec_one_len_eval(subset, k, strategy_func, depth=depth+1)
            
            word_list.update(wl)
    
    return word_list
        



def split_on_letter(word_list, letter):
    """
    Computes a list of dataframes that all correspond to a different letter index combination for one letter

    Args:
        word_list (pandas.DataFrame): List of remaining possible words
        letter (string): Letter on which splits are performed

    Returns:
        list: List of pandas.DataFrame objects, each with a different letter combination
    """
    tmp_df = word_list
    tmp_df['combination'] = tmp_df["word"].apply(lambda x : tuple([_.start() for _ in re.finditer(letter, x)]))
    return tmp_df.groupby('combination')