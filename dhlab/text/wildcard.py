from dhlab.api.dhlab_api import wildcard_search
from dhlab.text.dhlab_object import DhlabObj


class WildcardWordSearch(DhlabObj):
    """
    Find a class of words matching a wildcard string
    """
    def __init__(self, word, factor=2, freq_limit=10, limit=50):
        """:param word: word from a mixture of * and characters
        :factor int: the additional length of words to be returned
        :freq_lim: the frequency of returned words lower limit
        :limit int: number of words returned
        """
        self.words = wildcard_search(word, factor=factor,
                                     freq_limit=freq_limit, limit=limit)
        super().__init__(self.words)
