from sys import dont_write_bytecode
import pandas as pd
import numpy as np
import re
import time


"""
Returns a word list that contains words of only one size
df: word list with different sizes
fixed_size: wanted uniform size of words

Returns: Word list with only fixed_size length words
"""
def reduce_only_word_size(df, fixed_size):
    # UNTESTED
    return df[df['Word'].str.len() == fixed_size]

"""
Computes the word list that fulfills a certain combination of one letter
e.g. "[^a]aa[^a][^a]a[^a]" at positions 1,2 and 5 there are a's, everywhere else not

df: List of words to consider
letter: Letter that one is querying for
combination: List of indices, where the letter is allowed

Returns: List of words that fulfill exactly this query
"""
def reduce_one_combination(df, letter, combination):
    if df.empty:
        return df
    standard_array = np.repeat("[^" + letter + "]", len(df["Word"][0]))
    standard_array[combination] = letter
    str_combination = str_combination.join()
    return df[df["Word"].str.fullmatch(str_combination)]

"""
Compute word list that fulfills a specifiy position query
E.g. [^a^b]d[^d] no a's and no b's at 0, d at 1, no d at 2

df: List of words to be considered
query_string: String that codifies (like in example) what is wanted

Returns: List of words that fulfill query
"""
def reduce_with_query(df, query_string):
    if df.empty:
        return df
    return df[df["Word"].str.fullmatch(query_string)]

"""

"""
def find_letter_index_in_word(true_word, guessed_letter):
    return [_.start() for _ in re.finditer(guessed_letter, true_word)]


def update_information(known_information, indices, letter):
    not_letter = "^" + letter
    for pos in range(0, len(known_information)):
        if known_information[pos] == ".":
            known_information[pos] = ""
        
        if pos in indices:
            known_information[pos] = letter
        else:
            if len(known_information[pos]) != 1:
                known_information[pos] = known_information[pos] + not_letter
    return known_information

def knowledge2string(known_list):
    def map_element(elem):
        if elem == '.':
            return elem
        else:
            return '[' + elem + ']'
    vf = np.vectorize(lambda x : map_element(x))
    return ''.join(vf(known_list))

def knowledge_visualization(known_list):
    visualization = ""
    for elem in known_list:
        if len(elem) == 1:
            visualization = visualization + elem.upper()
        else:
            visualization = visualization + "_"
    return visualization

def check_done(known_information, guess, true_word):
    if guess == true_word:
        return True

    if len(guess) > 1 and guess != true_word:
        return None
    
    for elem in known_information:
        if len(elem) != 1:
            return False
    return True


def process_guess(known_information, guess, true_word):
    matched_any = None
    if len(guess) == 1:
        matching_indices = find_letter_index_in_word(true_word, guess)
        known_information = update_information(known_information, matching_indices, guess)

        matched_any = True
        if matching_indices == []:
            matched_any = False
    
    done = check_done(known_information, guess, true_word)
    
    if done:
        list(guess), done, None
    
    return known_information, done, matched_any

def print_verbose(text, verbose):
    if verbose == 0:
        return
    else:
        print(text)
        return

def test_run_one_game(player, df, true_word, max_tries, wait_seconds, verbose=1):
    GAME_RUNNING = True
    true_word = true_word.lower()
    tries = max_tries
    print_verbose("Total tries: " + str(tries), verbose)
    print_verbose("-"*50, verbose)
    wrong_guess = []
    known_information = ["."] * len(true_word)
    computer = player(df)
    while(True):
        if tries == 0:
            print_verbose("Out of tries! Computer loses.", verbose)
            print_verbose("Remaining words: ", verbose)
            print_verbose(computer.word_list, verbose)
            return None
        

        guess, entropy_guess = computer.execute_move(known_list=known_information)
        print_verbose("Computer guesses: " + guess + ", ENTROPY: " + str(entropy_guess) + ", WORDS REMAINING: " + str(computer.word_list.shape[0]), verbose)

        known_information, done, matched_any = process_guess(known_information, guess, true_word)
        if done == None:
            print_verbose("SOMETHING WRONG: word not found or wrong word guess", verbose)
            print_verbose("Game Over", verbose)
            return None
        elif done:
            print("Computer found " + true_word.upper() + " after " + str(max_tries - tries) + " guesses!")
            return max_tries - tries
        else:
            if matched_any:
                print_verbose(guess.upper() + " is in word :)", verbose)
            if not matched_any:
                print_verbose(guess.upper() + " is not in word :(", verbose)
                wrong_guess.append(guess)
                tries -= 1
            print_verbose("==> INFORMATION: " + knowledge_visualization(known_list=known_information) + ", wrong guesses: " + str(wrong_guess), verbose)
            print_verbose("Remaining tries: " + str(tries), verbose)
            print_verbose("-"*50, verbose)

        time.sleep(wait_seconds)