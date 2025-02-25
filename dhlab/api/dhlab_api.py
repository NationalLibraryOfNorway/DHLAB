from io import StringIO
from typing import Dict, List, Tuple, Union

import pandas as pd

# from requests import HTTPError, JSONDecodeError, ConnectionError
from pandas import DataFrame, Series

from dhlab.constants import BASE_URL
from dhlab.api.utils import api_get, api_post, DHLabApiError
from scipy.sparse import dok_matrix
import requests

pd.options.display.max_rows = 100

# wildcard search for words


def wildcard_search(
    word: str,
    factor: int | None = 2,
    freq_limit: int | None = 10,
    limit: int | None = 50,
    session: requests.Session | None = None
) -> DataFrame:
    """Get words, with frequencies, using '*' as a wildcard.

    For example, searching "ord*en*" might return:
        ```
                      freq
        ordbogen       874
        ordboken     10604
        ...
        ordningen   368131
        ordnmgen       722
        ...
        ```

    :param word: Word to search, allowing (potentially multiple) '*' as a wildcard
    :param factor: Max length of matched words, as a factor of `word`
    :param freq_limit: Lower frequency limit of returned matched words
    :param limit: Max number of returned results, prioritized by frequency
    """
    resp = api_get(
        f"{BASE_URL}/wildcard_word_search",
        params={"word": word, "factor": factor, "freq_lim": freq_limit, "limit": limit},
        session=session
    )

    return pd.DataFrame.from_dict(resp.json(), orient="index", columns=["freq"])


# fetch metadata


def images(
    text: str | None = None,
    part: int | None = True,
    hits: int | None = 500,
    delta: int | None = 0,
    session: requests.Session | None = None
) -> list[str]:
    """Retrive images from bokhylla

    :param text: Fulltext query expression for sqlite.
    :param part: If a number, the whole page is shown. If True, get auto-scaled image.
    :param delta: If part==True, show `delta` additional pixels on each side of image
    :param hits: Number of images
    :return: List of image URLs
    """

    resp = api_get(
        f"{BASE_URL}/images",
        params = {"text": text, "part": part, "hits": hits, "delta": delta},
        session=session
    )

    return resp.json()


def ner_from_urn(
    urn: str | None = None,
    model: str | None = None,
    start_page: int = 0,
    to_page: int = 0,
    session: requests.Session | None = None
) -> DataFrame:
    """Get NER annotations for a text (``urn``) using a spacy ``model``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param str model: name of a spacy model.
        Check which models are available with :func:`show_spacy_models`
    :return: Dataframe with annotations and their frequencies
    """
    resp = api_get(
        f"{BASE_URL}/ner_urn",
        params={"urn": urn, "model": model, "start_page": start_page, "to_page": to_page},
        session=session
    )

    return pd.read_json(resp.json())


def pos_from_urn(
    urn: str | None = None,
    model: str | None = None,
    start_page: int = 0,
    to_page: int = 0,
    session: requests.Session | None = None
) -> DataFrame:
    """Get part of speech tags and dependency parse annotations for a text (``urn``) with a SpaCy ``model``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param str model: name of a spacy model.
        Check which models are available with :func:`show_spacy_models`
    :param int start_page:
    :param int to_page:
    :return: Dataframe with annotations and their frequencies
    """
    resp = api_get(
        f"{BASE_URL}/pos_urn",
        params={"urn": urn, "model": model, "start_page": start_page, "to_page": to_page},
        session=session
    )

    return pd.read_json(resp.json())


def show_spacy_models(session: requests.Session | None = None ) -> List:
    """Show available SpaCy model names."""
    resp = api_get(f"{BASE_URL}/ner_models", session=session)

    return resp.json()


def get_places(urn: str, session: requests.Session | None = None) -> DataFrame:
    """Look up placenames in a specific URN.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/places <https://api.nb.no/dhlab/#/default/post_places>`_.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    """
    r = api_post(f"{BASE_URL}/places", json={"urn": urn}, session=session)
    return pd.DataFrame(r.json())


def geo_lookup(
    places: List,
    feature_class: str | None = None,
    feature_code: str | None = None,
    field: str = "alternatename",
    session: requests.Session | None = None
) -> DataFrame:
    """From a list of places, return their geolocations

    :param list places: a list of place names - max 1000
    :param str feature_class: which GeoNames feature class to return. Example: ``P``
    :param str feature_code: which GeoNames feature code to return. Example: ``PPL``
    :param str field: which name field to match - default "alternatename".
    """
    res = api_post(
        f"{BASE_URL}/geo_data",
        json={
            "words": places,
            "feature_class": feature_class,
            "feature_code": feature_code,
            "field": field,
        },
        session=session
    )
    columns = [
        "geonameid",
        "name",
        "alternatename",
        "latitude",
        "longitude",
        "feature_class",
        "feature_code",
    ]
    return pd.DataFrame(res.json(), columns=columns)


def get_dispersion(
    urn: str | None = None,
    words: List | None = None,
    window: int = 300,
    pr: int = 100,
    session: requests.Session | None = None) -> Series:
    """Count occurrences of words in the given URN object.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint ``/dispersion``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param list words: list of words. Defaults to a list of punctuation marks.
    :param int window: The number of tokens to search through per row. Defaults to 300.
    :param int pr: defaults to 100.
    :return: a ``pandas.Series`` with frequency counts of the words in the URN object.
    """
    params = {"pr": pr, "urn": urn, "window": window, "words": words}
    r = api_post(f"{BASE_URL}/dispersion", json=params, session=session)
    return pd.Series(r.json())


def get_metadata(urns: List[str] | None = None, session: requests.Session | None = None) -> DataFrame:
    """Get metadata for a list of URNs.

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/get_metadata <https://api.nb.no/dhlab/#/default/post_get_metadata>`_.

    :param list urns: list of uniform resource name strings, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    """
    r = api_post(f"{BASE_URL}/get_metadata", json={"urns": urns}, session=session)
    return DataFrame(r.json())


def get_identifiers(identifiers: list | None = None, session: requests.Session | None = None) -> list:
    """Convert a list of identifiers, oaiid, sesamid, urns or isbn10 to dhlabids"""

    if identifiers is None:
        identifiers = []

    res = api_post(
        f"{BASE_URL}/identifiers",
        json={"identifiers": [i for i in identifiers if i != ""]},
        session=session
    )
    return res.json()


def get_chunks(
    urn: str | None = None,
    chunk_size: int = 300,
    session: requests.Session | None = None
) -> Union[Dict, List]:
    """Get the text in the document ``urn`` as frequencies of chunks
     of the given ``chunk_size``.

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    ``/chunks``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param int chunk_size: Number of tokens to include in each chunk.
    :return: list of dicts with the resulting chunk frequencies, or an empty dict
    """
    resp = api_get(
        f"{BASE_URL}/chunks",
        params={"urn": urn, "chunk_size": chunk_size},
        session=session
    )

    return resp.json()


def get_chunks_para(urn: str | None = None, session: requests.Session | None = None) -> Union[Dict, List]:
    """Fetch chunks and their frequencies from paragraphs in a document (``urn``).

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    ``/chunks_para``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :return: list of dicts with the resulting chunk frequencies, or an empty dict
    """
    resp = api_get(
        f"{BASE_URL}/chunks_para",
        params={"urn": urn},
        session=session
    )

    return resp.json()


def evaluate_documents(
    wordbags: Dict | None = None,
    urns: List[str] | None = None,
    session: requests.Session | None = None
) -> DataFrame:
    """Count and aggregate occurrences of topic ``wordbags`` for each document in a list of ``urns``.

    :param dict wordbags: a dictionary of topic keywords and lists of associated words.
        Example: ``{"natur": ["planter", "skog", "fjell", "fjord"], ... }``
    :param list urns: uniform resource names, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :return: a ``pandas.DataFrame`` with the topics as columns, indexed by the dhlabids of the
        documents.
    """
    res = api_post(
        f"{BASE_URL}/evaluate", json={"wordbags": wordbags, "urns": urns},
        session=session
    )
    df = pd.DataFrame(res.json()).transpose()
    return df


def get_reference(
    corpus: str = "digavis",
    from_year: int = 1950,
    to_year: int = 1955,
    lang: str = "nob",
    limit: int = 100000,
    session: requests.Session | None = None
) -> DataFrame:
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
    resp = api_get(
        BASE_URL + "/reference_corpus",
        params={"corpus": corpus, "from_year": from_year, "to_year": to_year, "lang": lang, "limit": limit},
        session=session
    )

    return pd.DataFrame(resp.json(), columns=["word", "freq"]).set_index("word")


def find_urns(
    docids: Union[Dict, DataFrame] | None = None,
    mode: str = "json",
    session: requests.Session | None = None
) -> DataFrame:
    """Return a list of URNs from a collection of docids.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/find_urn`.

    :param docids: dictionary of document IDs (``{docid: URN}``) or a ``pandas.DataFrame``.
    :param str mode: Default 'json'.
    :return: the URNs that were found, in a ``pandas.DataFrame``.
    """
    resp = api_post(
        BASE_URL + "/find_urn",
        json={"docids": docids, "mode": mode},
        session=session
    )

    return pd.DataFrame.from_dict(resp.json(), orient="index", columns=["urn"])


def _ngram_doc(
    doctype: str = "",
    word: List | str | None = None,
    title: str | None = None,
    period: Tuple[int, int] | None = None,
    publisher: str | None = None,
    lang: str | None = None,
    city: str | None = None,
    ddk: str | None = None,
    topic: str | None = None,
    session: requests.Session | None = None
) -> DataFrame:
    """Count occurrences of one or more words over a time period.

    The type of document to search through is decided by the `doctype`.
    Filter the selection of documents with metadata.
    Use % as wildcard where appropriate - no wildcards in `word` or `lang`.

    Args:
        doctype: API endpoint for the document type to get ngrams for.
            Can be `'book'`, `'periodicals'`, or `'newspapers'`.
        word: Word(s) to search for.
            Can be several words in a single string, separated by comma, e.g. `"ord,ordene,orda"`.
        title: Title of a specific document to search through.
        period: Start and end years or dates of a time period,
            given as `(YYYY, YYYY)`` or `(YYYYMMDD, YYYYMMDD)`.
        publisher: Name of a publisher.
        lang: Language as a 3-letter ISO code (e.g. `"nob"` or `"nno"`)
        city: City of publication.
        ddk: [Dewey Decimal Classification](https://no.wikipedia.org/wiki/Deweys_desimalklassifikasjon) identifier.
        topic: Topic of the documents.

    Returns:
        a `pandas.DataFrame` with the resulting frequency counts of the word(s),
            spread across years. One year per row.
    """
    if word is None:
        word = ["."]

    params = {"doctype": doctype, "word": word, "title": title, "period": period,
              "publisher": publisher, "lang": lang, "city": city, "ddk": ddk, "topic": topic}
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if params[x] is not None}
    r = api_post(BASE_URL + "/ngram_" + doctype, json=params, session=session)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    if not isinstance(df.index, pd.MultiIndex):
        raise DHLabApiError(f"{isinstance(df.index, pd.MultiIndex)=}")
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    return df


def reference_words(
    words: List | None = None,
    doctype: str = "digibok",
    from_year: Union[str, int] = 1800,
    to_year: Union[str, int] = 2000,
    session: requests.Session | None = None
) -> DataFrame:
    """Collect reference data for a list of words over a time period.

    Reference data are the absolute and relative frequencies of the ``words``
    across all documents of the given ``doctype`` in the given time period
    (``from_year`` - ``to_year``).

    :param list words: list of word strings.
    :param str doctype: type of reference document. Can be ``"digibok"`` or ``"digavis"``.
        Defaults to ``"digibok"``.

        .. note::
           If any other string is given as the ``doctype``,
           the resulting data is equivalent to what you get with
           ``doctype="digavis"``.

    :param int from_year: first year of publication
    :param int to_year: last year of publication
    :return: a DataFrame with the words' frequency data
    """
    resp = api_post(
        f"{BASE_URL}/reference_words",
        json={"words": words, "doctype": doctype, "from_year": from_year, "to_year": to_year},
        session=session
    )

    return pd.DataFrame(resp.json(), columns=["word", "freq", "relative"])


# @_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_book(
    word: Union[List, str] = ["."],
    title: str | None = None,
    period: Tuple[int, int] | None = None,
    publisher: str | None = None,
    lang: str | None = None,
    city: str | None = None,
    ddk: str | None = None,
    topic: str | None = None,
    session: requests.Session | None = None
) -> DataFrame:
    """Count occurrences of one or more words in books over a given time period.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_book`.

    Filter the selection of books with metadata.
    Use % as wildcard where appropriate - no wildcards in ``word`` or ``lang``.

    :param word: Word(s) to search for.
        Can be several words in a single string, separated by comma, e.g. ``"ord,ordene,orda"``.
    :type word: str or list of str
    :param str title: Title of a specific document to search through.
    :param period: Start and end years or dates of a time period,
        given as ``(YYYY, YYYY)`` or ``(YYYYMMDD, YYYYMMDD)``.
    :type period: tuple of ints
    :param str publisher: Name of a publisher.
    :param str lang: Language as a 3-letter ISO code (e.g. ``"nob"`` or ``"nno"``)
    :param str city: City of publication.
    :param str ddk: `Dewey Decimal Classification
        <https://no.wikipedia.org/wiki/Deweys_desimalklassifikasjon>`_ identifier.
    :param str topic: Topic of the documents.
    :return: a ``pandas.DataFrame`` with the resulting frequency counts of the word(s),
        spread across years. One year per row.
    """
    params = {"word": word, "title": title, "period": period, "publisher": publisher,
              "lang": lang, "city": city, "ddk": ddk, "topic": topic}
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if params[x] is not None}
    r = api_post(BASE_URL + "/ngram_book", json=params, session=session)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    if not isinstance(df.index, pd.MultiIndex):
        raise DHLabApiError(f"{isinstance(df.index, pd.MultiIndex)=}")
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    return df


# @_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_periodicals(
    word: Union[List, str] = ["."],
    title: str | None = None,
    period: Tuple[int, int] | None = None,
    publisher: str | None = None,
    lang: str | None = None,
    city: str | None = None,
    ddk: str | None = None,
    topic: str | None = None,
    session: requests.Session | None = None,
    **kwargs,
) -> DataFrame:
    """Get a time series of frequency counts for ``word`` in periodicals.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_periodicals`.

    :param word: Word(s) to search for.
        Can be several words in a single string, separated by comma, e.g. ``"ord,ordene,orda"``.
    :type word: str or list of str
    :param str title: Title of a specific document to search through.
    :param period: Start and end years or dates of a time period,
        given as ``(YYYY, YYYY)`` or ``(YYYYMMDD, YYYYMMDD)``.
    :type period: tuple of ints
    :param str publisher: Name of a publisher.
    :param str lang: Language as a 3-letter ISO code (e.g. ``"nob"`` or ``"nno"``)
    :param str city: City of publication.
    :param str ddk: `Dewey Decimal Classification
        <https://no.wikipedia.org/wiki/Deweys_desimalklassifikasjon>`_ identifier.
    :param str topic: Topic of the documents.
    :return: a ``pandas.DataFrame`` with the resulting frequency counts of the word(s),
        spread across years. One year per row.
    """
    params = {"word": word, "title": title, "period": period, "publisher": publisher,
              "lang": lang, "city": city, "ddk": ddk, "topic": topic}
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if params[x] is not None}
    r = api_post(BASE_URL + "/ngram_periodicals", json=params, session=session)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    if not isinstance(df.index, pd.MultiIndex):
        raise DHLabApiError(f"{isinstance(df.index, pd.MultiIndex)=}")
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    return df


def ngram_news(
    word: Union[List, str] = ["."],
    title: str | None = None,
    period: Tuple[int, int] | None = None,
    session: requests.Session | None = None
) -> DataFrame:
    """Get a time series of frequency counts for ``word`` in newspapers.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_newspapers`.

    :param word: Word(s) to search for.
        Can be several words in a single string, separated by comma, e.g. ``"ord,ordene,orda"``.
    :type word: str or list of str
    :param str title: Title of a specific newspaper to search through.
    :param period: Start and end years or dates of a time period,
        given as ``(YYYY, YYYY)`` or ``(YYYYMMDD, YYYYMMDD)``.
    :type period: tuple of ints
    :return: a ``pandas.DataFrame`` with the resulting frequency counts of the word(s),
        spread across the dates given in the time period. Either one year or one day per row.
    """
    params = {"word": word, "title": title, "period": period}
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if params[x] is not None}
    r = api_post(BASE_URL + "/ngram_newspapers", json=params, session=session)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    if not isinstance(df.index, pd.MultiIndex):
        raise DHLabApiError(f"{isinstance(df.index, pd.MultiIndex)=}")
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    return df

def get_document_frequencies(
    urns: List[str] | None = None,
    cutoff: int = 0,
    words: List[str] | None = None,
    sparse: bool = False,
    session: requests.Session | None = None
) -> DataFrame:
    """Fetch frequency counts of ``words`` in documents (``urns``).

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/frequencies`.

    :param list urns: list of uniform resource name strings, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :param int cutoff: minimum frequency of a word to be counted
    :param list words: a list of words to be counted - if left None, whole document is returned. If not None both the counts and their relative frequency is returned.
    :param bool sparse: create a sparse matrix for memory efficiency
    """
    def _create_sparse_matrix(structure):
        """Create a sparse matrix from an API counts object"""

        # fetch all words
        words = list(set(word for dct in structure.values() for word in dct))
        # fetch all dhlabids
        dhlabids = list(structure.keys())
        # create an int/dhlabid mapping
        dhlabid_to_col = {dhlabid: idx for idx, dhlabid in enumerate(dhlabids)}
        # create an int/word mapping
        word_to_row = {word: idx for idx, word in enumerate(words)}

        # construct the matrix with each word as a row and each dhlabid as a column (DTM)
        num_cols = len(dhlabids)
        num_rows = len(words)
        sparse_matrix = dok_matrix((num_rows, num_cols), dtype=int)

        # incrementally fill the sparse matrix from dictionary
        for col_idx, dhlabid in enumerate(dhlabids):
            dct = structure[dhlabid]
            for word, value in dct.items():
                row_idx = word_to_row[word]
                sparse_matrix[row_idx, col_idx] = value

        df_sparse = pd.DataFrame.sparse.from_spmatrix(sparse_matrix, index=words, columns=dhlabids)
        return df_sparse

    params = {"urns": urns, "cutoff": cutoff, "words": words}
    r = api_post(f"{BASE_URL}/frequencies", json=params, session=session)
    result = r.json()
    # check if words are passed - return differs a bit
    if words is None:
        structure = dict()
        for u in result:
            try:
                structure[u[0][0]] = dict([(x[1], x[2]) for x in u])
            except IndexError:
                pass

        if sparse == True:
            df = _create_sparse_matrix(structure)
        else:
            df = pd.DataFrame(structure)
        
        df = df.sort_values(by=df.columns[0], ascending=False).fillna(0)
    else:
        df = pd.DataFrame(result)
        df.columns = ["urn", "word", "freq", "urncount"]
        df["relfreq"] = df["freq"] / df.urncount
        df = pd.pivot_table(
            df, values=["freq", "relfreq"], index="word", columns="urn"
        ).fillna(0)
    return df


def get_word_frequencies(
    urns: List[str] | None = None,
    cutoff: int = 0,
    words: List[str] | None = None,
    session: requests.Session | None = None
) -> DataFrame:
    """Fetch frequency numbers for ``words`` in documents (``urns``).

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/frequencies`.

    :param list urns: list of uniform resource name strings, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :param int cutoff: minimum frequency of a word to be counted
    :param list words: a list of words to be counted - should not be left None.
    """
    return get_document_frequencies(urns, cutoff, words, session=session)


def get_urn_frequencies(
    urns: List[str] | None = None,
    dhlabid: List[int] | None = None,
    session: requests.Session | None = None
) -> DataFrame:
    """Fetch frequency counts of documents as URNs or DH-lab ids.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/frequencies`.

    :param list urns: list of uniform resource name strings, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :param list dhlabid: list of numbers for dhlabid:
        ``[1000001, 2000003]``
    """
    if dhlabid is None:
        params = {"urns": urns}
    else:
        params = {"dhlabid": dhlabid}
    r = api_post(f"{BASE_URL}/urn_frequencies", json=params, session=session)
    result = r.json()
    # check if words are passed - return differs a bit
    df = pd.DataFrame(result)
    df.columns = ["urn", "freq"]
    return df


def document_corpus(
    doctype: str | None = None,
    author: str | None = None,
    freetext: str | None = None,
    fulltext: str | None = None,
    from_year: int | None = None,
    to_year: int | None = None,
    from_timestamp: int | None = None,
    to_timestamp: int | None = None,
    title: str | None = None,
    ddk: str | None = None,
    subject: str | None = None,
    publisher: str | None = None,
    literaryform: str | None = None,
    genres: str | None = None,
    city: str | None = None,
    lang: str | None = None,
    limit: int | None = None,
    order_by: str | None = None,
    session: requests.Session | None = None
) -> DataFrame:
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
    :param str publisher: Name of publisher.
    :param str literaryform: literary form of the publication (books)
    :param str genres: genre of the publication.
    :param str city: place of publication
    :param str lang: Language of the publication, as a 3-letter ISO code.
        Example: ``"nob"`` or ``"nno"``
    :param int limit: number of items to sample.
    :param str order_by: order of elements in the corpus object. Typically used in combination with a limit. Example ``"random"`` (random order, the slowest), ``"rank"`` (ordered by relevance, faster) or ``"first"`` (breadth-first, using the order in the database table, the fastest method)
    :return: a ``pandas.DataFrame`` with the corpus information.
    """
    parms = {"doctype": doctype, "author": author, "freetext": freetext,
             "fulltext": fulltext, "from_year": from_year, "to_year": to_year,
             "from_timestamp": from_timestamp, "to_timestamp": to_timestamp,
             "title": title, "ddk": ddk, "subject": subject, "publisher": publisher,
             "literaryform": literaryform, "genres": genres, "city": city,
             "lang": lang, "limit": limit, "order_by": order_by}

    params = {x: parms[x] for x in parms if parms[x] is not None}

    r = api_post(BASE_URL + "/build_corpus", json=params, session=session)

    return pd.DataFrame(r.json())


get_document_corpus = document_corpus # Function alias


def urn_collocation(
    urns: List[str] | None = None,
    word: str = "arbeid",
    before: int = 5,
    after: int = 0,
    samplesize: int = 200000,
    session: requests.Session | None = None
) -> DataFrame:
    """Create a collocation from a list of URNs.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/urncolldist_urn`.

    :param list urns: list of uniform resource name strings, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :param str word: word to construct collocation with.
    :param int before: number of words preceding the given ``word``.
    :param int after: number of words following the given ``word``.
    :param int samplesize: total number of ``urns`` to search through.
    :return: a ``pandas.DataFrame`` with distance (sum of distances and bayesian distance) and
        frequency for words collocated with ``word``.
    """

    params = {
        "urn": urns,
        "word": word,
        "before": before,
        "after": after,
        "samplesize": samplesize,
    }
    r = api_post(BASE_URL + "/urncolldist_urn", json=params, session=session)
    return pd.read_json(StringIO(r.json()))


def totals(top_words: int = 50000, session: requests.Session | None = None) -> DataFrame:
    """Get aggregated raw frequencies of all words in the National Library's database.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/totals/{top_words} <https://api.nb.no/dhlab/#/default/get_totals__top_words_>`_.

    :param int top_words: The number of words to get total frequencies for.
    :return: a ``pandas.DataFrame`` with the most frequent words.
    """
    resp = api_get(BASE_URL + f"/totals/{top_words}", session=session)

    return pd.DataFrame.from_dict(dict(resp.json()), orient="index", columns=["freq"])


def concordance(
    urns: list,
    words: str,
    window: int = 25,
    limit: int = 100,
    session: requests.Session | None = None
) -> DataFrame:
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
    params = {"urns": urns, "query": words, "window": window, "limit": limit}
    r = api_post(BASE_URL + "/conc", json=params, session=session)
    return pd.DataFrame(r.json())


konkordans = concordance # Function alias


def concordance_counts(
    urns: list,
    words: str,
    window: int = 25,
    limit: int = 100,
    session: requests.Session | None = None
) -> DataFrame:
    """Count concordances (keyword in context) for a corpus query (used for collocation analysis).

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
    params = {"urns": urns, "query": words, "window": window, "limit": limit}
    r = api_post(BASE_URL + "/conccount", json=params, session=session)

    return pd.DataFrame(r.json())


def word_concordance(
    urn: list | None = None,
    dhlabid: list | None = None,
    words: list | None = None,
    before: int = 12,
    after: int = 12,
    limit: int = 100,
    samplesize: int = 50000,
    session: requests.Session | None = None
) -> DataFrame:
    """Get a list of concordances from the National Library's database.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/conc <https://api.nb.no/dhlab/#/default/conc_word_urn>`_.

    :param list urns: dhlab serial ids. (server can take both urns and dhlabid but so we may rewrite this to)
    :param str words: Word(s) to search for -- must be a list
    :param int before: between 0-24.
    :param int after: between 0-24 (before + sum <= 24)
    :param int limit: max. number of concordances per server process.
    :param int samplesize: samples from urns.
    :return: a table of concordances
    """

    # server checks if either dhlabid or urns are present in the parameters, so only one of them
    # is passed. The return is dhlabid anyhow.

    if dhlabid is not None:
        params = {
            "dhlabid": dhlabid,
            "words": words,
            "before": before,
            "after": after,
            "limit": limit,
            "samplesize": samplesize,
        }
    elif urn is not None:
        params = {
            "urn": urn,
            "words": words,
            "before": before,
            "after": after,
            "limit": limit,
            "samplesize": samplesize,
        }
    else:
        params = {
            "words": words,
            "before": before,
            "after": after,
            "limit": limit,
            "samplesize": samplesize,
        }

    r = api_post(BASE_URL + "/conc_word_urn", json=params, session=session)

    return pd.DataFrame(
        [x for y in r.json() for x in y],
        columns=["dhlabid", "before", "target", "after"],
    )


def collocation(
    corpusquery: str = "norge",
    word: str = "arbeid",
    before: int = 5,
    after: int = 0,
    session: requests.Session | None = None
) -> DataFrame:
    """Make a collocation from a corpus query.

    :param str corpusquery: query string
    :param str word: target word for the collocations.
    :param int before: number of words prior to ``word``
    :param int after: number of words following ``word``
    :return: a dataframe with the resulting collocations
    """
    params = {
        "metadata_query": corpusquery,
        "word": word,
        "before": before,
        "after": after,
    }
    r = api_post(BASE_URL + "/urncolldist", json=params, session=session)
    return pd.read_json(r.json())


# Norwegian word bank


def word_variant(
    word: str,
    form: str,
    lang: str = "nob",
    session: requests.Session | None = None
) -> list:
    """Find alternative ``form`` for a given ``word`` form.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint ``/variant_form``

    Example: ``word_variant('spiste', 'pres-part')``

    :param str word: any word string
    :param str form: a morphological feature tag from the Norwegian wordbank
        `"Orbanken" <https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-5/>`_.
    :param str lang: either "nob" or "nno"
    """
    resp = api_get(
        f"{BASE_URL}/variant_form",
        params={"word": word, "form": form, "lang": lang},
        session=session
    )

    return resp.json()


def word_paradigm(word: str, lang: str = "nob", session: requests.Session | None = None) -> list:
    """Find paradigms for a given ``word`` form.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint ``/paradigm``

    Example:

    .. code-block:: python

        word_paradigm('spiste')
        # [['adj', ['spisende', 'spist', 'spiste']],
        # ['verb', ['spis', 'spise', 'spiser', 'spises', 'spist', 'spiste']]]

    :param str word: any word string
    :param str lang: either "nob" or "nno"
    """
    resp = api_get(
        f"{BASE_URL}/paradigm",
        params={"word": word, "lang": lang},
        session=session
    )

    return resp.json()


def word_paradigm_many(wordlist: list, lang: str = "nob", session: requests.Session | None = None) -> list:
    """Find alternative forms for a list of words.
    :param wordlist: `List` of words
    :param lang: Language
    """
    r = api_post(f"{BASE_URL}/paradigms", json={"words": wordlist, "lang": lang}, session=session)
    return r.json()


def word_form(word: str, lang: str = "nob", session: requests.Session | None = None) -> list:
    """Look up the morphological feature specification of a ``word`` form.
    :param word: Word
    :param lang: Language
    """
    resp = api_get(
        f"{BASE_URL}/word_form",
        params={"word": word, "lang": lang},
        session=session
    )

    return resp.json()


def word_form_many(wordlist: list, lang: str = "nob", session: requests.Session | None = None) -> list:
    """Look up the morphological feature specifications for word forms in a ``wordlist``.
    :param wordlist: `List` of words
    :param lang: Language
    """
    r = api_post(f"{BASE_URL}/word_forms", json={"words": wordlist, "lang": lang}, session=session)
    return r.json()


def word_lemma(word: str, lang: str = "nob", session: requests.Session | None = None) -> list:
    """Find the list of possible lemmas for a given ``word`` form.
    :param word: Word to find lemmas for
    :param lang: Language
    """
    r = api_get(
        f"{BASE_URL}/word_lemma",
        params={"word": word, "lang": lang},
        session=session
    )

    return r.json()


def word_lemma_many(wordlist, lang="nob"):
    """Find lemmas for a list of given word forms."""


def query_imagination_corpus(
    category=None,
    author=None,
    title=None,
    year=None,
    publisher=None,
    place=None,
    oversatt=None,
    session: requests.Session | None = None
):
    """Fetch data from imagination corpus"""
    params = {"category": category, "author": author, "title": title, "year": year,
              "publisher": publisher, "place": place, "oversatt": oversatt}
    params = {key: params[key] for key in params if params[key] is not None}

    resp = api_get(f"{BASE_URL}/imagination", params=params, session=session)
    return resp.json()
