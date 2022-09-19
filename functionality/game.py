import numpy as np
import pandas as pd
import re
import time
from functionality import knowledge


class Game:
    """
    Class that runs a simple game of hangman.
    """
    def __init__(self, player):
        """
        Initialization of Object
        _word: truw word to be guessed
        knowledge: Information that is publicly available
        player: object that attempts to guess the word
        verbose: setting of whether the game gives more information on the commandline

        Args:
            player (object): object that attempts to guess the word
        """
        self._word = None
        self.knowledge = None
        self.player = player
        self.verbose = 0
        return

    def _check_done(self, guess):
        """
        Checks whether the a guess finishes the game

        Args:
            guess (string): Either a single character or a whole word

        Returns:
            bool: Indicator of whether the computer won (True), the game is not finished yet (False) or the computer guess an entire incorrect word (None)
        """
        if guess == self._word:
            return True

        if len(guess) > 1 and guess != self._word:
            return None
        
        return self.knowledge.completed()


    def process_guess(self, guess):
        """
        Processing of a guess by the player.
        The guess is compared to the true word and the knowledge is updated accordingly

        Args:
            guess (string): Character or string to be guessed

        Returns:
            (bool, bool): (Indicator of whether the game is still going on, Indicator of whether the letter is in the word)
        """

        matched_any = None
        if len(guess) == 1:
            matching_indices = self.match_indices(guess)
            self.knowledge.update(guess, matching_indices)
            matched_any = not (matching_indices == [])

        done = self._check_done(guess)
        
        return done, matched_any


    def match_indices(self, guessed_letter):
        """
        Checks which (if any) indices match the guessed letter

        Args:
            guessed_letter (string): string of length one, guessed by the player

        Returns:
            list: integers at whose position in the true word the guess matches the word
        """
        return [_.start() for _ in re.finditer(guessed_letter, self._word)]


    def _print(self, text):
        """
        Custom function to print to the commandline if verbose == 1

        Args:
            text (string): string to (possibly) be printed
        """
        if self.verbose == 0:
            return
        else:
            print(text)
            return
    
    def play(self, word, max_wrong_tries, wait_seconds=0, verbose=0):
        """
        Play one game.

        Args:
            word (string): word to be guessed
            max_wrong_tries (int): max number of incorrect tries, typically 11
            wait_seconds (int, optional): idle seconds between each guess for dramatic effect. Defaults to 0.
            verbose (int, optional): indicator of whether there should be a commandline output at each guess (1) or no output (0). Defaults to 0.

        Returns:
            (bool, int, int): (indicator of whether the word was guessed, wrong guesses, total guesses)
        """
        
        self._setup_game(word)

        self.verbose = verbose
        wrong_tries = 0
        total_tries = 0
        self._print("Total tries: " + str(max_wrong_tries))
        self._print("Word length: " + str(len(self._word)))
        self._print("-"*50)
        wrong_guess = []
        
        while(True):
            total_tries += 1
            
            if max_wrong_tries != None and wrong_tries == max_wrong_tries:
                self._print("Out of tries! Computer loses.")
                self._print("Remaining words: ")
                self._print(self.player.word_list)
                return False, wrong_tries, total_tries-1
            self._print("Turn " + str(total_tries))
            # start = time.process_time()
            guess, entropy_guess = self.player.execute_move(self.knowledge)
            # print("Time for one guess: ", time.process_time() - start)
            self._print("Computer guesses: " + guess.upper() + ", ENTROPY: " + str(entropy_guess) + ", WORDS REMAINING: " + str(self.player.word_list.shape[0]))

            done, matched_any = self.process_guess(guess)

            if done == None:
                self._print("SOMETHING WRONG: word not found or guessed incorrect word")
                self._print("Game Over")
                return False, wrong_tries, total_tries
            elif done:
                print("Computer found " + self._word.upper() + " after " + str(wrong_tries) + " wrong guesses!")
                return True, wrong_tries, total_tries
            else:
                if matched_any:
                    self._print(guess.upper() + " is in word :)")
                if not matched_any:
                    self._print(guess.upper() + " is not in word :(")
                    wrong_guess.append(guess)
                    wrong_tries += 1
                self._print("==> INFORMATION: " + self.knowledge.todisplay() + ", wrong guesses: " + str(wrong_guess))
                
                if max_wrong_tries != None:
                    self._print("Remaining wrong attempts: " + str(max_wrong_tries - wrong_tries))
                self._print("-"*50)

            time.sleep(wait_seconds)

    def _setup_game(self, word):
        """
        Set the word and knowledge within the object. Reset the player.
        """
        self._word = word.lower()
        self.knowledge = knowledge.Knowledge(len(word))
        self.player.reset()
        return