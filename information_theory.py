import numpy as np

"""
Calculation of the information content of each element in an array.
Each elem >= 0, and sum(elem) == 1+-error
input: Array of (proportional) probabilities

output: Information content of each element
"""
def information_content(input):

    assert np.all(input >= 0), "Input contains negative probabilities"
    assert np.allclose(np.sum(input), 1), "Input is not normalized"

    return -np.log2(input)

"""
Computes information content for unnormalized probabilities. If the total is different
to the sum of the array, then total can be passed

input: np.array of (unnormalized) probabilities
total: Number to which all values add up. If input represents all values then 
sum(input) == total, else total has to be passed

returns: Elementwise information content of array
"""
def ic_numstable(input, total=None):
    if total == None:
        total = np.sum(input)
    return -np.log2(input) + np.log2(total)

"""
Calculation of the entropy of a numpy array
input: array of (proportional) probabilities

output: returns the entropy of the input
"""
def entropy(input):
    probs = compute_probs(input)
    ic = ic_numstable(input)
    return np.sum(ic * probs)

"""
Computes discrete probability distributions out of indepenendtly unnormalized
rows of data

Input: N-Rows of differently un-normalized arrays
Returns: Array of normalized probability rows
"""
def compute_probs(input):
    if len(input.shape) == 1:
        return input / np.sum(input)
    total = np.sum(input, axis=-1)
    return input / total[:, np.newaxis]