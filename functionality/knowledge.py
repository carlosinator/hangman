import numpy as np


class Knowledge:
    """
    Knowledge Object that quantifies the knwon information on the hangman board.
    This can then be for example represented as a Regex to query a pandas.DataFrame
    """
    def __init__(self, word_length):
        """
        Initialization of object.
        known_positions: Places in the word that are known
        knowledge_array: string for each position representing a regex: (for example ^a -> not a)
        letters_not_in_word: letters known not to be in the word

        Args:
            word_length (int): length of word to be found. Necessary to initialize the attributes of the object
        """
        self.known_positions = np.array([False] * word_length, dtype=bool)
        self.knowledge_array = np.array([""] * word_length, dtype=object)
        self.letters_not_in_word = []
        return


    def update(self, letter, occurrence):
        """
        Updates the knowledge array using the new information passed
        :new_information (list): Information in the format of e.g.
        [(a, [0, 4]), (q, [2, 3])] 
        There are a's at 0 and 4, and none anywhere else. Same for (q, [2,3])
        ==> Position 0 is an a, Position 1 is neither a or b, Position 2 no new information
        1. If a position in new information has e.g. ['^c','c']->error
        2. If the new information is in contradiction with old information (e.g. see 1.) ->error
        3. If a position has ['a', '^c'] only ['a'] will be saved
        """

        self._update_one_letter(letter, occurrence)

        if occurrence == []:
            self.letters_not_in_word.append(letter)
        return

    def _update_one_letter(self, letter, letter_occurrence):
        """
        Different format that .update()
        Information for only one letter (letter) is updated.

        Args:
            letter (char): Letter whose information should be updated
            letter_occurrence (list): ALL indices where the letter occurs. 
            If the letter does not occur anywhere then [] should be passed.
        """

        true_mask = np.zeros(self.knowledge_array.size, dtype=bool)
        true_mask[letter_occurrence] = True

        inv_mask = np.ones(self.knowledge_array.size, dtype=bool)
        inv_mask[letter_occurrence] = False

        check_arr = np.logical_not(np.logical_and(self.known_positions, true_mask))
        assert np.all(check_arr), "Contradictory knowledge. At least one position is already fixed."


        # Update information
        self.knowledge_array[true_mask] = letter

        tmp = np.logical_and(inv_mask, np.logical_not(self.known_positions))
        self.knowledge_array[tmp] = self.knowledge_array[tmp] + "^" + letter

        self.known_positions[true_mask] = True
        return

    def completed(self):
        """
        Check that the knowledge is completed. One can be certain of the word that has been found.
        Returns:
            bool: Indicator of whether the knowledge is completed.
        """
        return np.all(self.known_positions == True)

    def check_empty(self):
        """
        Check that nothing is known
        Returns:
            bool: Indicator of whether the knowledge is empty
        """
        return np.all(np.logical_not(self.known_positions)) and self.letters_not_in_word == []

    
    def tostring(self):
        """
        Creates a string from knowledge that can be used as a regex to query a database

        Returns:
            string: Query string for regex
        """
        
        if ''.join(self.knowledge_array) == '':
            return "." * len(self.knowledge_array)
        else:
            return '[' + ']['.join(self.knowledge_array) + ']'

    
    def todisplay(self):
        """
        Creates a string for display in the commandline

        Returns:
            string: String easy to understand for displaying
        """
        tmp = ''
        for elem in self.knowledge_array:
            if elem == "." or len(elem) != 1:
                tmp += '_'
            elif len(elem) == 1:
                tmp += elem.upper()
            else:
                tmp += "?"
        return tmp