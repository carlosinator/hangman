import pandas as pd

class LookUp:
    """
    Object to use as a lookup table for the first step.
    For a given word length the first guess is the most expensive and always the same.
    Thus, for a given word list and strategy a one time cost can be incurred to significantly reduce computation time in the future.
    Credits to Luka Jeram for the idea :) 
    """

    def __init__(self):
        return

    def create(self, word_list, strategy_func):
        """
        Creation of a lookup table. 
        For this, the dataframe is split into dataframes of word of equal length. Then the strategy is computed for that first step.
        The lookup table then generates a pandas dataframe containing three columns: length, letter, entropy

        Args:
            word_list (pandas.DataFrame): All words to include in first step lookup
            strategy_func (function): Function based on which the guesses are made

        Returns:
            pandas.DataFrame: Lookup table generated from the inputs with three columns: length, letter, entropy
        """
        lookup = self._compute_lookup(word_list, strategy_func)
        self.lookup = lookup
        return lookup


    def load(self, lookup_save_path):
        """
        Load an already computed lookup table from a csv file.
        In the git project the tables are saved in data/lookup with a name such as lu_word_list_strategy_func.csv

        Args:
            lookup_save_path (string): path to a .csv table

        Returns:
            pandas.DataFrame: DataFarme version of the csv
        """
        self.lookup = pd.read_csv(lookup_save_path)
        return self.lookup


    @staticmethod
    def _compute_lookup(word_list, strategy_func):
        """
        Implementation of the first step guess. 
        In a loop the first guess is computed sequentially for each word length by splitting the dataframe into different word lengths.

        Args:
            word_list (pandas.DataFrame): All words to be considered
            strategy_func (function): Function based on which the guesses are made

        Returns:
            pandas.DataFrame: Lookup table
        """

        tmp = {
            'length' : [],
            'letter' : [],
            'entropy' : []
        }
        lookup = pd.DataFrame(tmp)

        word_list['length'] = word_list['word'].apply(len)
        grps = word_list.groupby('length')
        for x in grps.groups:
            wl = grps.get_group(x)
            letter, entropy = strategy_func(wl)
        
            lookup = pd.concat([lookup, pd.DataFrame([[wl.iloc[0]['length'], letter, entropy]], columns=['length', 'letter', 'entropy'])])
            # lookup = lookup.append(pd.Series([wl.iloc[0]['length'], letter, entropy]), ignore_index)
            print(lookup)

        return lookup


    def get(self, word_length):
        """
        Lookup of one step for loaded data

        Args:
            word_length (int): length of the words in question

        Returns:
            (string, float): Tuple of guess and entropy of guess
        """
        row = self.lookup[self.lookup['length'] == word_length]
        return row.iloc[0]['letter'], row.iloc[0]['entropy']


    def save(self, lookup_save_path):
        """
        Save a computed lookup table into a csv file

        Args:
            lookup_save_path (string): Path to the csv file to be saved
        """
        self.lookup.to_csv(lookup_save_path)
        return