import pandas as pd
from dhlab.api.dhlab_api import concordance
from dhlab.text.utils import urnlist, make_link
from IPython.display import HTML

class Concordance(pd.DataFrame):
    @property
    def _constructor(self):
        return Concordance

    @classmethod
    def get_concordances(self, corpus, words, window=20, limit=500):
        res = concordance(urns=urnlist(corpus), words=words, window=window, limit=limit)

        res["link"] = res.urn.apply(make_link)

        res.rename({"conc": "concordance"}, axis=1, inplace=True)

        return Concordance(res)

    def show(self, n=10, style=True):
        if style:
            result = self.sample(min(n, len(self)))[["link", "concordance"]].style
        else:
            result = self.sample(min(n, len(self)))
        return result

    def split_view(self, html=False):
        df = self.concordance.str.split("</?b>", expand=True)
        df.rename(
            {0: "left", 1: "hit", 2: "right", 3: "hit2", 4: "right2"},
            axis=1,
            inplace=True,
        )
        df.index = self.urn

        if html:
            return HTML(df.to_html())
        else:
            return df
        

