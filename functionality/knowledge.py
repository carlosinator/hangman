class Knowledge:
    def __init__(self, word_length):
        self.knowledge_array = [None] * word_length
        return

    """
    TODO
    Updates the knowledge array using the new information passed

    new_information: Information in the format of e.g.
    [['a'], ['^a', '^b'], []] 
    ==> Position 0 is an a, Position 1 is neither a or b, Position 2 no new information
    1. If a position in new information has e.g. ['^c','c']->error
    2. If the new information is in contradiction with old information (e.g. see 1.) ->error
    3. If a position has ['a', '^c'] only ['a'] will be saved
    """
    def update(new_information):
        return
    
    """
    TODO
    Creates a string from knowledge that can be used as a regex to query a database
    """
    def tostring():
        return

    """
    TODO
    Check that passed information does not contain contradictions like [['c', '^c']]
    """
    @staticmethod
    def _check_information_correct():
        return


    """
    TODO (??? still unclear)
    Condense new information, remove redundancies e.g. 
    1. Condense known position: 
        a. In new knowledge ['a', '^c'] -> ['a']
        b. If ['a'] is known, position in new knowledge is set to []
    2. Delete repeats: ['c', 'c'] -> ['c']
    """
    def _condense_new_information(new_information):
        return