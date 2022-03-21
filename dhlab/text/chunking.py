import pandas as pd

from dhlab.api.dhlab_api import get_chunks, get_chunks_para


class Chunks:
    """Create chunks from a text."""

    def __init__(self, urn=None, chunks=1000):
        """
        :param urn: str or list
        :param chunks: {'para', 'avsn'} or int
        """
        # switch function based on value of chunks - a number or a string
        # indicating whether each paragraph is a chunk, else chop up the text
        # in pieces according to chunks

        if isinstance(chunks, str):
            if chunks.startswith("para") or chunks.startswith("avsn"):
                self.chunks = get_chunks_para(urn=urn)
            else:
                self.chunks = {}
        else:
            self.chunks = get_chunks(urn=urn, chunk_size=chunks)

    def to_pandas(self):
        """Vectorize into a pandas dataframe with words a index"""
        return pd.DataFrame(self.chunks).transpose()
