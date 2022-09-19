import numpy as np
from functionality import data_functions
from optimization import look_up

class ComputerPlayer:

    def __init__(self, word_list, compute_letter_func, lookup=None):
        """
        Init of computer player
        word_list: Complete list of all words that are considered for this game of hangman

        self.only_one_len: Indicator for whether the word_list has been reduced to one size
        Expensive computation->use indicator so that it is only done once
        self.word_list: Contains the remaining possible words at each step
        self.compute_letter: function that the computer player uses to evaluate which letter
        to choose
        """
        self.full_list = word_list
        self.word_list = self.full_list.copy()
        self.compute_letter = compute_letter_func
        self.lookup = lookup
        return

    def reset(self):
        """
        Reset self.word_list
        Call if different words are guessed with the same object in between each word
        """
        self.word_list = self.full_list.copy()
        return

    def execute_move(self, knowledge):
        """
        Executes full move. Depending on word list length (0, 1, or more) an evaluation is returned
        known_list: List of known information

        1. List of possible words is reduced
        2. If only one word remains->return that
            if no words remain: return error
        3. Otherwise compute the best letter with its information content

        Returns: either word, error guess or best letter
        """
        # assert self.word_list != None, "Word list has not been set with .setup()"
        self.word_list = data_functions.reduce_with_query(df=self.word_list, query_string=knowledge.tostring())

        if self.word_list.shape[0] == 1:
            return self.word_list.iloc[0]["word"], 0
        if self.word_list.shape[0] == 0:
            return "WORD NOT FOUND", np.inf

        if knowledge.check_empty() and self.lookup != None:
            lu = self.lookup
        else:
            lu = None

        letter, entropy = self.compute_letter(self.word_list, lookup=lu)

        return letter, entropy