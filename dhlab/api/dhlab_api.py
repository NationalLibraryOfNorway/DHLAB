from typing import Union, List, Tuple

import pandas as pd
import requests

from dhlab.constants import BASE_URL
from dhlab.utils import _docstring_parameters_from, _is_documented_by

pd.options.display.max_rows = 100


# fetch metadata


def get_places(urn: str, **kwargs) -> pd.DataFrame:
    """Look up placenames in a specific URN.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/places <https://api.nb.no/dhlab/#/default/post_places>`_.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param kwargs:
        - feature_class: str, a GeoNames feature class. Example: ``P``
        - feature_code: str, a GeoNames feature code. Example: ``PPL``
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/places", json=params)
    print(r.status_code)
    return pd.DataFrame(r.json())


def get_dispersion(
        urn: str = None, words: list = None, window: int = None, pr: int = None
) -> pd.Series:
    """Count occurrences of words in the given URN object.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint ``/dispersion``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param list words: list of words. Defaults to a list of punctuation marks.
    :param int window: The number of tokens to search through per row. Defaults to 300.
    :param int pr: defaults to 100.
    :return: a ``pandas.Series`` with frequency counts of the words in the URN object.

    .. todo:: Verify parameter descriptions.
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/dispersion", json=params)
    return pd.Series(r.json())


def get_metadata(urns: List[str] = None) -> pd.DataFrame:
    """Get metadata for a list of URNs.

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/get_metadata <https://api.nb.no/dhlab/#/default/post_get_metadata>`_.

    :param list urns: list of uniform resource names, example:
        ``URN:NBN:no-nb_digibok_2011051112001``
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json=params)
    return pd.DataFrame(r.json())


def get_chunks(urn: str = None, chunk_size: int = 300) -> dict:
    """Get the text in the document ``urn`` as frequencies of chunks
     of the given ``chunk_size``.

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    ``/chunks``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param int chunk_size: Number of tokens to include in each chunk.

    .. todo:: Verify unit of ``chunk_size``
    """

    if urn is None:
        return {}
    r = requests.get(f"{BASE_URL}/chunks", params=locals())
    if r.status_code == 200:
        result = r.json()
    else:
        result = {}
    return result


def get_chunks_para(urn: str = None) -> dict:
    """Fetch paragraphs and their frequencies from a document.

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    ``/chunks_para``.

    :param str urn: uniform resource name of a document.
    """

    if urn is None:
        return {}
    r = requests.get(f"{BASE_URL}/chunks_para", params=locals())
    if r.status_code == 200:
        result = r.json()
    else:
        result = {}
    return result


def get_reference(
        corpus: str = 'digavis',
        from_year: int = 1950,
        to_year: int = 1955,
        lang: str = 'nob',
        limit: int = 100000
) -> pd.DataFrame:
    """Reference frequency list of the n most frequent words from a given corpus in a given period.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/reference_corpus <https://api.nb.no/dhlab/#/default/get_reference_corpus>`_.

    :param str corpus: Document type to include in the corpus, can be either ``'digibok'`` or
        ``'digavis'``.
    :param int from_year: Starting point for time period of the corpus.
    :param int to_year: Last year of the time period of the corpus.
    :param str lang: Language of the corpus, can be one of
        ``'nob,', 'nno,', 'sme,', 'sma,', 'smj', 'fkv'``
    :param int limit: Maximum number of most frequent words.
    :return: A ``pandas.DataFrame`` with the results.
    """
    params = locals()
    r = requests.get(BASE_URL + "/reference_corpus", params=params)
    if r.status_code == 200:
        result = r.json()
    else:
        result = []
    return pd.DataFrame(result, columns=['word', 'freq']).set_index('word')


def find_urns(docids=None, mode: str = 'json') -> pd.DataFrame:
    """Return a list of URNs.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/find_urn`.

    :param list docids: list of document IDs as a dictionary {docid: URN} or a pandas dataframe.
    :param str mode: Default 'json'.
    :return: the URNs that were found, in a `pandas.DataFrame`.
    """
    params = locals()
    r = requests.post(BASE_URL + "/find_urn", json=params)
    if r.status_code == 200:
        res = pd.DataFrame.from_dict(r.json(), orient='index', columns=['urn'])
    else:
        res = pd.DataFrame()
    return res


def _ngram_doc(
        doctype: str = None,
        word: Union[List, str] = ['.'],
        title: str = None,
        period: Tuple[int, int] = None,
        publisher: str = None,
        lang: str = None,
        city: str = None,
        ddk: str = None,
        topic: str = None
) -> pd.DataFrame:
    """Count occurrences of one or more words over a time period.

    The type of document to search through is decided by the ``endpoint``.
    Filter the selection of documents with metadata.
    Use % as wildcard where appropriate - no wildcards in ``word`` or ``lang``.

    :param str doctype: API endpoint for the document type to get ngrams for.
        Can be ``'book'``, ``'periodicals'``, or ``'newspapers'``.
    :param word: Word(s) to search for.
        Can be several words in a single string, separated by comma.
    :type word: str or list of str
    :param title: Title of a specific document to search through.
    :param tuple[int,int] period: Start and end years of a time period,
        given as ``(start year, end year)``.
    :param str publisher: Name of a publisher.
    :param str lang: Language as a 3-letter ISO code (e.g. ``"nob"`` or ``"nno"``)
    :param str city: City of publication.
    :param str ddk: `Dewey Decimal Classification
        <https://no.wikipedia.org/wiki/Deweys_desimalklassifikasjon>`_ identifier.
    :param str topic: Topic of the documents.
    :return: a `pandas.DataFrame` with the resulting frequency counts of the word(s),
        spread across years. One year per row.
    """
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(',')]
    params['word'] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_" + doctype, json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient='index')
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    # df.index = df.index.map(pd.Timestamp)
    return df


@_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_book(
        word: Union[List, str] = ['.'],
        title: str = None,
        period: Tuple[int, int] = None,
        publisher: str = None,
        lang: str = None,
        city: str = None,
        ddk: str = None,
        topic: str = None
) -> pd.DataFrame:
    """Count occurrences of one or more words, over a time period, in books.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_book`.

    Filter the selection of books with metadata.
    Use % as wildcard where appropriate - no wildcards in ``word`` or ``lang``.
    """
    return _ngram_doc(
        word=word,
        doctype="book",
        title=title,
        period=period,
        publisher=publisher,
        lang=lang,
        city=city,
        ddk=ddk,
        topic=topic
    )


@_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_periodicals(
        word: Union[List, str] = ['.'],
        **kwargs,
) -> pd.DataFrame:
    """Get a time series of frequency counts for ``word`` in periodicals.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_periodicals`.
    """
    return _ngram_doc(word=word, doctype="periodicals", **kwargs)


@_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_news(
        word: Union[List, str] = ['.'],
        title: str = None,
        period: Tuple[int, int] = None,
        **kwargs
) -> pd.DataFrame:
    """Get a time series of frequency counts for ``word`` in newspapers.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_newspapers`.
    """
    return _ngram_doc(word=word, doctype="newspapers", title=title, period=period, **kwargs)


def get_document_frequencies(
        urns: List[str] = None, cutoff: int = 0, words: List[str] = None
) -> pd.DataFrame:
    """Fetch raw frequency counts of ``words`` in documents (``urns``).

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/frequencies`.
    """
    params = locals()
    r = requests.post(BASE_URL + "/frequencies", json=params)
    result = r.json()
    structure = {u[0][0]: dict([tuple(x[1:3]) for x in u])
                 for u in result if u != []}
    df = pd.DataFrame(structure)
    return df.sort_values(by=df.columns[0], ascending=False)


def get_word_frequencies(
        urns: List[str] = None, cutoff: int = 0, words: List[str] = None
) -> pd.DataFrame:
    """Calculate relative frequencies for ``words`` in documents (``urns``).

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/frequencies`.
    """
    params = locals()
    r = requests.post(BASE_URL + "/frequencies", json=params)
    result = r.json()
    structure = {u[0][0]: dict([(x[1], x[2] / x[3]) for x in u])
                 for u in result if u != []}
    df = pd.DataFrame(structure)
    return df.sort_values(by=df.columns[0], ascending=False)


def get_document_corpus(**kwargs):
    return document_corpus(**kwargs)


def document_corpus(
        doctype: str = None,
        author: str = None,
        freetext: str = None,
        fulltext: str = None,
        from_year: int = None,
        to_year: int = None,
        from_timestamp: int = None,
        to_timestamp: int = None,
        title: str = None,
        ddk: str = None,
        subject: str = None,
        lang: str = None,
        limit: int = None
) -> pd.DataFrame:
    """Fetch a corpus based on metadata.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/build_corpus <https://api.nb.no/dhlab/#/default/post_build_corpus>`_.

    :param str doctype: ``"digibok"``, ``"digavis"``, ``"digitidsskrift"`` or ``"digistorting"``
    :param str author: Name of an author.
    :param str freetext: any of the parameters, for example: ``"digibok AND Ibsen"``.
    :param str fulltext: words within the publication.
    :param int from_year: Start year for time period of interest.
    :param int to_year: End year for time period of interest.
    :param int from_timestamp: Start date for time period of interest.
        Format: ``YYYYMMDD``, books have ``YYYY0101``
    :param int to_timestamp: End date for time period of interest.
        Format: ``YYYYMMDD``, books have ``YYYY0101``
    :param str title: Name or title of a document.
    :param str ddk: `Dewey Decimal Classification
        <https://no.wikipedia.org/wiki/Deweys_desimalklassifikasjon>`_ identifier.
    :param str subject: subject (keywords) of the publication.
    :param str lang: Language of the publication, as a 3-letter ISO code.
        Example: ``"nob"`` or ``"nno"``
    :param int limit: number of items to sample.
    :return: a `pandas.DataFrame` with the corpus information.
    """
    parms = locals()
    params = {x: parms[x] for x in parms if not parms[x] is None}
    if "ddk" in params:
        params["ddk"] = "^" + params['ddk'].replace('.', '"."')

    r = requests.post(BASE_URL + "/build_corpus", json=params)

    return pd.DataFrame(r.json())


def urn_collocation(
        urns: List = None,
        word: str = 'arbeid',
        before: int = 5,
        after: int = 0,
        samplesize: int = 200000
) -> pd.DataFrame:
    """Create a collocation from a list of URNs.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/urncolldist_urn`.

    :return: distance (sum of distances and bayesian distance) and frequency.
    """

    params = {
        'urn': urns,
        'word': word,
        'before': before,
        'after': after,
        'samplesize': samplesize
    }
    r = requests.post(BASE_URL + "/urncolldist_urn", json=params)
    return pd.read_json(r.text)


def totals(top_words: int = 50000) -> pd.DataFrame:
    """Get total frequencies of words in database.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/totals/{top_words} <https://api.nb.no/dhlab/#/default/get_totals__top_words_>`_.

    :param int top_words: The number of words to get total frequencies for.
    """
    r = requests.get(BASE_URL + f"/totals/{top_words}")
    return pd.DataFrame.from_dict(
        dict(r.json()), orient='index', columns=['freq'])


def concordance(
        urns: list = None, words: str = None, window: int = 25, limit: int = 100
) -> pd.DataFrame:
    """Get a list of concordances from the National Library's database.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/conc <https://api.nb.no/dhlab/#/default/post_conc>`_.

    :param list urns: uniform resource names, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :param str words: Word(s) to search for.
        Can be an SQLite fulltext query, an fts5 string search expression.
    :param int window: number of tokens on either side to show in the collocations, between 1-25.
    :param int limit: max. number of concordances per document. Maximum value is 1000.
    :return: a table of concordances
    """
    if words is None:
        return {}  # exit condition
    else:
        params = {
            'urns': urns,
            'query': words,
            'window': window,
            'limit': limit
        }
        r = requests.post(BASE_URL + "/conc", json=params)
    return pd.DataFrame(r.json())


def concordance_counts(
        urns: list = None, words: str = None, window: int = 25, limit: int = 100
) -> pd.DataFrame:
    """Count concordances (keyword in context) for a corpus query (used for collocation analysis).

    The counted words are from the digital texts in the National Library's database.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/conccount <https://api.nb.no/dhlab/#/default/post_conccount>`_.

    :param list urns: uniform resource names, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :param str words: Word(s) to search for.
        Can be an SQLite fulltext query, an fts5 string search expression.
    :param int window: number of tokens on either side to show in the collocations, between 1-25.
    :param int limit: max. number of concordances per document. Maximum value is 1000.
    :return: a table of counts
    """
    if words is None:
        return {}  # exit condition
    else:
        params = {
            'urns': urns,
            'query': words,
            'window': window,
            'limit': limit
        }
        r = requests.post(BASE_URL + "/conccount", json=params)
    return pd.DataFrame(r.json())


@_is_documented_by(concordance)
def konkordans(urns: list = None, words: str = None, window: int = 25, limit: int = 100):
    """Wrapper for :func:`concordance`."""
    return concordance(**locals())


def collocation(
        corpusquery: str = 'norge', word: str = 'arbeid', before: int = 5, after: int = 0
) -> pd.DataFrame:
    """Make a collocation from a corpus query.

    :param str corpusquery: Query string.
    :param str word: target word for the collocations.
    :param int before: number of words prior to ``word``.
    :param int after: number of words following ``word``.
    :return: a table with the resulting collocations
    """
    params = {
        'metadata_query': corpusquery,
        'word': word,
        'before': before,
        'after': after
    }
    r = requests.post(BASE_URL + "/urncolldist", json=params)
    return pd.read_json(r.text)
