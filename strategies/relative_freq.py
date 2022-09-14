import numpy as np
import re
import functionality.information_theory as it

ALPHABET = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def combination_distribution(word_list, letter):
    """
    Generate a count on how any times each combination of letters appears

    Args:
        word_list (pd.DataFrame): List of words with appearance count to consider
        letter (string): letter, non-overlapping substring to be guessed

    Returns:
        pd.DataFrame: Each combination has a tuple of the index (letter "e" for elephant -> (0,2)) and how many times this appears
    """
    x = word_list.copy()
    x['combination'] = x["word"].apply(lambda x : tuple([_.start() for _ in re.finditer(letter, x)]))
    x = x[["count", "combination"]]
    x = x.groupby('combination')['count'].sum()
    return x


def entropy_of_choice(word_list, letter):
    """
    For one letter choice the entropy is computed

    word_list: Remaining possible words
    letter: Letter as possible choice

    Returns: Entropy of choice
    """
    combinations = np.array(combination_distribution(word_list, letter))
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