import pandas as pd

from dhlab.api.nb_ngram_api import get_ngram


def nb_ngram(terms: str,
             corpus: str = 'bok',
             smooth: int = 3,
             years: tuple = (1810, 2010),
             mode: str = 'relative'):
    """Extract N-gram frequencies from given ``terms`` and ``years``.

    :param terms: comma
    :param corpus:
    :param smooth:
    :param years:
    :param mode:
    :return: A sorted Pandas DataFrame index

    :meta private:
    """
    df = ngram_conv(get_ngram(terms, corpus=corpus), smooth=smooth, years=years, mode=mode)
    df.index = df.index.astype(int)
    return df.sort_index()


def ngram_conv(ngrams, smooth: int = 1, years: tuple = (1810, 2013), mode: str = 'relative'):
    """Construct a dataframe with ngram mean frequencies per year over a given time period.

    :param ngrams: TODO: FIll in appropriate type and description.
    :param smooth: Smoothing factor for the graph visualisation.
    :param years: Tuple with start and end years for the time period of interest
    :param mode: Frequency measure. Defaults to 'relative'.
    :return: pandas dataframe with mean values for each year

    :meta private:
    """
    ngc = {}
    # check if relative frequency or absolute frequency is in question
    if mode.startswith('rel') or mode == 'y':
        arg = 'y'
    else:
        arg = 'f'
    for x in ngrams:
        if x and isinstance(x, list):
            ngc[x['key']] = {
                z['x']: z[arg]
                for z in x['values']
                if years[1] >= int(z['x']) >= years[0]
            }
    return pd.DataFrame(ngc).rolling(window=smooth, win_type='triang').mean()
