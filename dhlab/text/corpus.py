import pandas as pd

from ..api.dhlab_api import document_corpus

class Corpus():
    def __init__(
        self,
        doctype = None,
        author = None,
        freetext = None,
        from_year = None,
        to_year = None,
        from_timestamp = None,
        to_timestamp = None,
        title = None,
        ddk = None,
        subject = None,
        lang = None,
        limit = None):
        
        self.corpus = document_corpus(
            doctype,
            author,
            freetext,
            from_year,
            to_year,
            from_timestamp,
            to_timestamp,
            title,
            ddk,
            subject,
            lang,
            limit
        )
        
        self.size = len(self.corpus)
        
        return