from itertools import combinations_with_replacement
from json.encoder import INFINITY
import numpy as np
import pandas as pd
import re
import information_theory as it
import hangman_functionality as hf

ALPHABET = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]


def combination_count(word_list, letter):
    word_list["Indices"] = word_list["Word"].apply(lambda x : [_.start() for _ in re.finditer(letter, x)])
    res = word_list["Indices"].value_counts()
    return res


"""
For one letter choice the entropy is computed

word_list: Remaining possible words
letter: Letter as possible choice

Returns: Entropy of choice
"""
def entropy_of_choice(word_list, letter):
    combinations = combination_count(word_list, letter)
    combinations = np.array(combinations)
    return it.entropy(combinations)

"""
For a word list of possible choices the letter, entropy pair with the
highest entropy is returned

word_list: pd.Dataframe still possible words 

Returns: char of best entropy and corresponding entropy
"""
def compute_optimal_choice(word_list):
    entropy_arr = np.array([entropy_of_choice(word_list, letter) for letter in ALPHABET])
    best_index = entropy_arr.argmax()
    return ALPHABET[best_index], entropy_arr[best_index]


"""
For a word list of possible choices the letter, entropy pair with the
lowest entropy is returned

word_list: pd.Dataframe still possible words 

Returns: char of lowest entropy and corresponding entropy
"""
def compute_worst_choice(word_list):
    entropy_arr = np.array([entropy_of_choice(word_list, letter) for letter in ALPHABET])
    best_index = entropy_arr.argmin()
    return ALPHABET[best_index], entropy_arr[best_index]

"""
TODO
Instead of computing the best Information Theory choice, one could
choose the letter that appears most often. Maybe this heuristic is
very good without the previous mess.

word_list: List of possible words
returns: NOT IMPLEMENTED YET
"""
def compute_choice_binary(word_list):
    return "Not implemented yet"

"""
TODO
Evaluation of relative probabilities and the corresponding best choice
word_list: List of possible words

returns: NOT IMPLEMENTED YET
"""
def useless_probability_evaluation(word_list):
    return 0



class ComputerPlayer:
    """
    Init of computer player
    word_list: Complete list of all words that are considered for this game of hangman

    self.only_one_len: Indicator for whether the word_list has been reduced to one size
    Expensive computation->use indicator so that it is only done once
    self.word_list: Contains the remaining possible words at each step
    self.compute_letter: function that the computer player uses to evaluate which letter
    to choose
    """
    def __init__(self, word_list):
        self.only_one_len = False
        self.word_list = word_list
        # self.num_tries = num_tries
        self.compute_letter = compute_optimal_choice
        # self.probable_words = useless_probability_evaluation
        return

    """
    Update of list using known information

    known_list: List of known information at each position

    returns: reduced version of self.word_list to only include the
    remaining possible words
    """
    def update_list(self, known_list):
        if not self.only_one_len:
            self.word_list = hf.reduce_only_word_size(df=self.word_list, fixed_size=len(known_list))
            self.only_one_len = True
        known_string = hf.knowledge2string(known_list)
        self.word_list = hf.reduce_with_query(df=self.word_list, query_string=known_string)
        return self.word_list

    """
    Executes full move. Depending on word list length (0, 1, or more) an evaluation is returned
    known_list: List of known information

    1. List of possible words is reduced
    2. If only one word remains->return that
        if no words remain: return error
    3. Otherwise compute the best letter with its information content

    Returns: either word, error guess or best letter
    """
    def execute_move(self, known_list):

        self.update_list(known_list=known_list)

        if self.word_list.shape == (1,2):
            return self.word_list.iloc[0]["Word"], 0
        if self.word_list.shape == (0,2):
            return "WORD NOT FOUND", INFINITY

        letter, entropy = self.compute_letter(self.word_list)

        return letter, entropy