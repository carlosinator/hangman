# hangman
Information Theory to play Hangman and similar versions :)

Welcome to a world of executions due to bad guesses (and probably code spaghettification).
Please enjoy your stay.

# data

```default_wordlist.csv``` was downloaded from http://wordlist.aspell.net/

```word_frequency.csv``` was downloaded from https://github.com/possibly-wrong/word-frequency

# functionality

Includes functions and modules to make the game work.

```game``` is a class that runs the game.

```information_theory``` contains the functions essential for the theoretical background.

```knowledge``` contains a standardized object with a representation of all known information. (Might still be improved)

```data_functions``` contains functions to clean the csv and do simple checks

# players

Possible players that can be used in the game. Currently only Computer, but a human player can be added easily.

# strategies

A strategy can be anything. For now they are saved in a file. 
The player object is passed a function that returns the best guess for a word_list, along with the metric based on which the guess was chosen. Currently in the strategies the functions are called ```compute_optimal_choice```.

```it_equal_prob``` considers all words equally likely.

````relative_freq``` considers word frequencies to make guesses. For this to work ```word_frequncy.csv``` should be used, otherwise the strategy is equivalent to ```it_equal_prob``` 

# feedback and more

If you'd like to expand this or found an error please let me know :) I'm always happy to learn more and expand the project