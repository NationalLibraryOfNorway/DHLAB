from typing import Union, List, Tuple

import pandas as pd
from pandas import DataFrame, Series
import requests

from dhlab.constants import BASE_URL

# from dhlab.utils import _docstring_parameters_from, _is_documented_by

pd.options.display.max_rows = 100

# fetch metadata


def ner_from_urn(urn: str = None, model: str = None) -> DataFrame:
    """Get NER annotations for a text (``urn``) using a spacy ``model``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param str model: name of a spacy model.
        Check which models are available with :func:`show_spacy_models`
    :return: Dataframe with annotations and their frequencies
    """

    params = locals()
    r = requests.get(f"{BASE_URL}/ner_urn", params=params)
    df = pd.read_json(r.json())
    return df


# @_docstring_parameters_from(ner_from_urn)
def pos_from_urn(urn: str = None, model: str = None) -> DataFrame:
    """Get part of speech tags and dependency parse annotations for a text (``urn``) with a SpaCy ``model``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param str model: name of a spacy model.
        Check which models are available with :func:`show_spacy_models`
    :return: Dataframe with annotations and their frequencies
    """
    params = locals()
    r = requests.get(f"{BASE_URL}/pos_urn", params=params)
    df = pd.read_json(r.json())
    return df


def show_spacy_models():
    """Show available SpaCy model names."""
    r = requests.get(f"{BASE_URL}/ner_models")
    return r.json()


def get_places(urn: str, **kwargs) -> DataFrame:
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
    # print(r.status_code)
    return pd.DataFrame(r.json())


def geo_lookup(
    places,
    feature_class: str = None,
    feature_code: str = None,
    field: str = "alternatename",
) -> DataFrame:
    """From a list of places, return their geolocations

    :param list places: a list of place names - max 1000
    :param str feature_class: which class to return
    :param str feature_code: which code to return
    :param str field: which name field to match - default alternatename
    """
    res = requests.post(
        f"{BASE_URL}/geo_data",
        json={
            "words": places,
            "feature_class": feature_class,
            "feature_code": feature_code,
            "field": field,
        },
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
    urn: str = None, words: list = None, window: int = None, pr: int = None
) -> Series:
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


def get_metadata(urns: List[str] = None) -> DataFrame:
    """Get metadata for a list of URNs.

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/get_metadata <https://api.nb.no/dhlab/#/default/post_get_metadata>`_.

    :param list urns: list of uniform resource name strings, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json=params)
    return DataFrame(r.json())


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
    """Fetch chunks from document, one for each paragraph.

    Calls the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    ``/chunks_para``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    """

    if urn is None:
        return {}
    r = requests.get(f"{BASE_URL}/chunks_para", params=locals())
    if r.status_code == 200:
        result = r.json()
    else:
        result = {}
    return result


def evaluate_documents(wordbags: dict = None, urns: list[str] = None) -> DataFrame:
    """Count and aggregate occurrences of topic ``wordbags`` for each document in a list of ``urns``.

    :param dict wordbags: a dictionary of topic keywords and lists of associated words.
        Example: ``{"natur": ["planter", "skog", "fjell", "fjord"], ... }``
    :param list urns: uniform resource names, for example:
        ``["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]``
    :return: a pandas DataFrame where columns are the topics, and the index are the dhlabids of the documents
    """
    res = requests.post(
        f"{BASE_URL}/evaluate", json={"wordbags": wordbags, "urns": urns}
    )
    df = pd.DataFrame(res.json()).transpose()
    return df


def get_reference(
    corpus: str = "digavis",
    from_year: int = 1950,
    to_year: int = 1955,
    lang: str = "nob",
    limit: int = 100000,
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
    params = locals()
    r = requests.get(BASE_URL + "/reference_corpus", params=params)
    if r.status_code == 200:
        result = r.json()
    else:
        result = []
    return pd.DataFrame(result, columns=["word", "freq"]).set_index("word")


def find_urns(docids: Union[dict, DataFrame] = None, mode: str = "json") -> DataFrame:
    """Return a list of URNs from a collection of docids.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/find_urn`.

    :param docids: dictionary of document IDs (``{docid: URN}``) or a ``pandas.DataFrame``.
    :param str mode: Default 'json'.
    :return: the URNs that were found, in a ``pandas.DataFrame``.
    """
    params = locals()
    r = requests.post(BASE_URL + "/find_urn", json=params)
    if r.status_code == 200:
        res = pd.DataFrame.from_dict(r.json(), orient="index", columns=["urn"])
    else:
        res = pd.DataFrame()
    return res


def _ngram_doc(
    doctype: str = None,
    word: Union[List, str] = ["."],
    title: str = None,
    period: Tuple[int, int] = None,
    publisher: str = None,
    lang: str = None,
    city: str = None,
    ddk: str = None,
    topic: str = None,
) -> DataFrame:
    """Count occurrences of one or more words over a time period.

    The type of document to search through is decided by the ``doctype``.
    Filter the selection of documents with metadata.
    Use % as wildcard where appropriate - no wildcards in ``word`` or ``lang``.

    :param str doctype: API endpoint for the document type to get ngrams for.
        Can be ``'book'``, ``'periodicals'``, or ``'newspapers'``.
    :param word: Word(s) to search for.
        Can be several words in a single string, separated by comma, e.g. ``"ord,ordene,orda"``.
    :type word: str or list of str
    :param title: Title of a specific document to search through.
    :param tuple[int,int] period: Start and end years of a time period,
        given as ``(YYYY, YYYY)`` or ``(YYYYMMDD, YYYYMMDD)``.
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
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_" + doctype, json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    # df.index = df.index.map(pd.Timestamp)
    return df


# @_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_book(
    word: Union[List, str] = ["."],
    title: str = None,
    period: Tuple[int, int] = None,
    publisher: str = None,
    lang: str = None,
    city: str = None,
    ddk: str = None,
    topic: str = None,
) -> DataFrame:
    """Count occurrences of one or more words in books over a given time period.

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
        topic=topic,
    )


# @_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_periodicals(
    word: Union[List, str] = ["."],
    **kwargs,
) -> DataFrame:
    """Get a time series of frequency counts for ``word`` in periodicals.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_periodicals`.
    """
    return _ngram_doc(word=word, doctype="periodicals", **kwargs)


# @_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_news(
    word: Union[List, str] = ["."],
    title: str = None,
    period: Tuple[int, int] = None,
    **kwargs,
) -> DataFrame:
    """Get a time series of frequency counts for ``word`` in newspapers.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/ngram_newspapers`.
    """
    return _ngram_doc(
        word=word, doctype="newspapers", title=title, period=period, **kwargs
    )


def get_document_frequencies(
    urns: List[str] = None, cutoff: int = 0, words: List[str] = None
) -> DataFrame:
    """Fetch frequency counts of ``words`` in documents (``urns``).

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/frequencies`.

    :param urns: list of urn strings
    :param cutoff: minimum frequency of a word to be counted
    :param words: a list of words to be counted - if left None, whole document is returned
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/frequencies", json=params)
    result = r.json()
    # check if words are passed - return differs a bit
    if words is None:
        structure = dict()
        for u in result:
            try:
                structure[u[0][0]] = dict([(x[1], x[2]) for x in u])
            except IndexError:
                pass
        df = pd.DataFrame(structure)
        df = df.sort_values(by=df.columns[0], ascending=False).fillna(0)
    else:
        df = pd.DataFrame(result)
        df.columns = ["urn", "word", "count", "urncount"]
        df = pd.pivot_table(df, values="count", index="word", columns="urn").fillna(0)
    return df


# @_docstring_parameters_from(get_document_frequencies, drop="words")
def get_word_frequencies(
    urns: List[str] = None, cutoff: int = 0, words: List[str] = None
) -> DataFrame:
    """Fetch frequency numbers for ``words`` in documents (``urns``).

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/frequencies`.

    :param words: a list of words to be counted - should not be left None
    """
    return get_document_frequencies(urns, cutoff, words)


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
    limit: int = None,
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
    :param str lang: Language of the publication, as a 3-letter ISO code.
        Example: ``"nob"`` or ``"nno"``
    :param int limit: number of items to sample.
    :return: a `pandas.DataFrame` with the corpus information.
    """
    parms = locals()
    params = {x: parms[x] for x in parms if not parms[x] is None}

    r = requests.post(BASE_URL + "/build_corpus", json=params)

    return pd.DataFrame(r.json())


def urn_collocation(
    urns: List = None,
    word: str = "arbeid",
    before: int = 5,
    after: int = 0,
    samplesize: int = 200000,
) -> DataFrame:
    """Create a collocation from a list of URNs.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/urncolldist_urn`.

    :return: distance (sum of distances and bayesian distance) and frequency.
    """

    params = {
        "urn": urns,
        "word": word,
        "before": before,
        "after": after,
        "samplesize": samplesize,
    }
    r = requests.post(BASE_URL + "/urncolldist_urn", json=params)
    return pd.read_json(r.text)


def totals(top_words: int = 50000) -> DataFrame:
    """Get total frequencies of words in database.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/totals/{top_words} <https://api.nb.no/dhlab/#/default/get_totals__top_words_>`_.

    :param int top_words: The number of words to get total frequencies for.
    """
    r = requests.get(BASE_URL + f"/totals/{top_words}")
    return pd.DataFrame.from_dict(dict(r.json()), orient="index", columns=["freq"])


def concordance(
    urns: list = None, words: str = None, window: int = 25, limit: int = 100
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
    if words is None:
        return {}  # exit condition
    else:
        params = {"urns": urns, "query": words, "window": window, "limit": limit}
        r = requests.post(BASE_URL + "/conc", json=params)
    return pd.DataFrame(r.json())


def concordance_counts(
    urns: list = None, words: str = None, window: int = 25, limit: int = 100
) -> DataFrame:
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
        params = {"urns": urns, "query": words, "window": window, "limit": limit}
        r = requests.post(BASE_URL + "/conccount", json=params)
    return pd.DataFrame(r.json())


# @_is_documented_by(concordance)
def konkordans(
    urns: list = None, words: str = None, window: int = 25, limit: int = 100
):
    """Wrapper for :func:`concordance`."""
    return concordance(**locals())


def collocation(
    corpusquery: str = "norge", word: str = "arbeid", before: int = 5, after: int = 0
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
    r = requests.post(BASE_URL + "/urncolldist", json=params)
    return pd.read_json(r.text)


# Norwegian word bank


def word_variant(word: str, form: str, lang: str = "nob") -> list:
    """Find alternative ``form`` for a given ``word`` form.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint ``/variant_form``

    Example: ``word_variant('spiste', 'pres-part')``

    :param str word: any word string
    :param str form: a morphological feature tag from the Norwegian wordbank
        `"Orbanken" <https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-5/>`_.
    :param str lang: either "nob" or "nno"
    """
    r = requests.get(
        f"{BASE_URL}/variant_form", params={"word": word, "form": form, "lang": lang}
    )
    return r.json()


def word_paradigm(word: str, lang: str = "nob") -> list:
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
    r = requests.get(f"{BASE_URL}/paradigm", params={"word": word, "lang": lang})
    return r.json()


def word_paradigm_many(wordlist: list, lang: str = "nob") -> list:
    """Find alternative forms for a list of words."""
    r = requests.post(f"{BASE_URL}/paradigms", json={"words": wordlist, "lang": lang})
    return r.json()


def word_form(word: str, lang: str = "nob") -> list:
    """Look up the morphological feature specification of a ``word`` form."""
    r = requests.get(f"{BASE_URL}/word_form", params={"word": word, "lang": lang})
    return r.json()


def word_form_many(wordlist: list, lang: str = "nob") -> list:
    """Look up the morphological feature specifications for word forms in a ``wordlist``."""
    r = requests.post(f"{BASE_URL}/word_forms", json={"words": wordlist, "lang": lang})
    return r.json()


def word_lemma(word: str, lang: str = "nob") -> list:
    """Find the list of possible lemmas for a given ``word`` form."""
    r = requests.get(f"{BASE_URL}/word_lemma", params={"word": word, "lang": lang})
    return r.json()


def word_lemma_many(wordlist, lang="nob"):
    """Find lemmas for a list of given word forms."""
    r = requests.post(f"{BASE_URL}/word_lemmas", json={"words": wordlist, "lang": lang})
    return r.json()
