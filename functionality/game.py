import numpy as np
import pandas as pd
import re
import time
from functionality import knowledge


class Game:
    def __init__(self, player, word):
        self._word = word.lower()
        self.knowledge = knowledge.Knowledge(len(word))
        self.player = player

        self.verbose = 0
        return

    def _check_done(self, guess):
        if guess == self._word:
            return True

        if len(guess) > 1 and guess != self._word:
            return None
        
        return self.knowledge.completed()


    def process_guess(self, guess):

        matched_any = None
        if len(guess) == 1:
            matching_indices = self.match_indices(self._word, guess)
            self.knowledge.update(guess, matching_indices)
            matched_any = not (matching_indices == [])

        done = self._check_done(guess)
        
        return done, matched_any


    def match_indices(self, true_word, guessed_letter):
        return [_.start() for _ in re.finditer(guessed_letter, true_word)]


    def _print(self, text):
        if self.verbose == 0:
            return
        else:
            print(text)
            return
    
    def play(self, max_wrong_tries, wait_seconds=0, verbose=0):
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




"""    def update_information(known_information, indices, letter):
        not_letter = "^" + letter
        for pos in range(0, len(known_information)):
            if known_information[pos] == ".":
                known_information[pos] = ""
            
            if pos in indices:
                known_information[pos] = letter
            else:
                if len(known_information[pos]) != 1:
                    known_information[pos] = known_information[pos] + not_letter
        return known_information"""


"""
Inefficient function that takes O(26*N^2) to compute the necessary
tries for all words
df: Words to be considered
player: Player Object that executes all decisions
max_tries: Limitation on the number of tries the player can take

def compute_tries_all_words(df, player, max_tries):
    df_with_tries = df
    df_with_tries["Tries"] = df_with_tries.apply(lambda x : hf.test_run_one_game(player, df=df, true_word=x["Word"], max_wrong_tries=max_tries, wait_seconds=0, verbose=0), axis=1)

    # filepath = Path('./wordswithtries.csv')
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    # df_with_tries.to_csv(filepath)
    return df_with_tries
"""