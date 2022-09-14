import numpy as np
import re
import functionality.information_theory as it


ALPHABET = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def combination_count(word_list, letter):
    """
    Find the number of times that a certain letter appears in the remaining words

    Args:
        word_list (pd.DataFrame): remaining possible words
        letter (char): letter to be considered

    Returns:
       DataFrame : Each index is the number of occurrences of one possible combination of the indices of the letter in the word list
    """
    x = word_list["word"].apply(lambda x : [_.start() for _ in re.finditer(letter, x)])
    return x.value_counts()



def entropy_of_choice(word_list, letter):
    """
    For one letter choice the entropy is computed

    word_list: Remaining possible words
    letter: Letter as possible choice

    Returns: Entropy of choice
    """
    combinations = np.array(combination_count(word_list, letter))
    return it.entropy(combinations)


def compute_optimal_choice(word_list):
    """
    For a word list of possible choices the letter, entropy pair with the
    highest entropy is returned

    word_list: pd.Dataframe still possible words 

    Returns: char of best entropy and corresponding entropy
    """
    entropy_arr = np.array([entropy_of_choice(word_list, letter) for letter in ALPHABET])
    best_index = entropy_arr.argmax()
    return ALPHABET[best_index], entropy_arr[best_index]



def compute_worst_choice(word_list):
    """
    For a word list of possible choices the letter, entropy pair with the
    lowest entropy is returned

    word_list: pd.Dataframe still possible words 

    Returns: char of lowest entropy and corresponding entropy
    """
    entropy_arr = np.array([entropy_of_choice(word_list, letter) for letter in ALPHABET])
    best_index = entropy_arr.argmin()
    return ALPHABET[best_index], entropy_arr[best_index]


def compute_choice_binary(word_list):
    """
    TODO
    Instead of computing the best Information Theory choice, one could
    choose the letter that appears most often. Maybe this heuristic is
    very good without the previous mess.

    word_list: List of possible words
    returns: NOT IMPLEMENTED YET
    """
    return "Not implemented yet"


def useless_probability_evaluation(word_list):
    """
    TODO
    Evaluation of relative probabilities and the corresponding best choice
    word_list: List of possible words

    returns: NOT IMPLEMENTED YET
    """
    return 0