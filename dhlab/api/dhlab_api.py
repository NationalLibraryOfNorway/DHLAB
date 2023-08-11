"""Python wrappers for the dhlab full text API."""
from typing import Optional, Dict, List, Tuple, Union

import pandas as pd
import requests

from pandas import DataFrame, Series

from dhlab.constants import BASE_URL

pd.options.display.max_rows = 100


def wildcard_search(
    word: str, factor: int = 2, freq_limit: int = 10, limit: int = 50
) -> DataFrame:
    """Search for words containing a wildcard."""

    res = requests.get(
        f"{BASE_URL}/wildcard_word_search",
        params={"word": word, "factor": factor, "freq_lim": freq_limit, "limit": limit},
    )
    # columns = ["key", "name", "alternatename", "latitude", "longitude", "feature class", "feature code"]
    return pd.DataFrame.from_dict(res.json(), orient="index", columns=["freq"])


def images(text: Optional[str] = None, part: bool = True):
    """Retrive images from bokhylla.

    Args:
        text: Fulltext query expression for sqlite.
        part: If False, the full page is shown.

    Returns:
        A list of image URLs for the scanned object.
    """

    params = locals()
    r = requests.get(f"{BASE_URL}/images", params=params)
    js = r.json()
    return js


def ner_from_urn(
    urn: Optional[str] = None,
    model: Optional[str] = None,
    start_page: int = 0,
    to_page: int = 0,
) -> DataFrame:
    """Get NER annotations for a text using a SpaCy NLP pipeline.

    Args:
        urn: Uniform resource name, for example: URN:NBN:no-nb_digibok_2011051112001
        model: Name of a spacy model. Check which models are available with `show_spacy_models()`
        start_page: First page to include in the analysis
        to_page: Last page to include in the analysis
    Returns:
        Name annotations and their frequencies
    """
    params = locals()
    r = requests.get(f"{BASE_URL}/ner_urn", params=params)
    df = pd.read_json(r.json())
    return df


def pos_from_urn(
    urn: Optional[str] = None,
    model: Optional[str] = None,
    start_page: int = 0,
    to_page: int = 0,
) -> DataFrame:
    """Get part of speech tags and dependency parse annotations for a text using a SpaCy NLP pipeline.

    Args:
        urn: Uniform resource name, for example: URN:NBN:no-nb_digibok_2011051112001
        model: Name of a spacy model. Check which models are available with `show_spacy_models`
        start_page: First page to include in the analysis
        to_page: Last page to include in the analysis
    Returns:
        POS tag annotations and their frequencies
    """
    params = locals()
    r = requests.get(f"{BASE_URL}/pos_urn", params=params)
    df = pd.read_json(r.json())
    return df


def show_spacy_models() -> List:
    """Show available SpaCy model names.

    Examples:
        >>> show_spacy_models()
        ['nb_core_news_lg', 'da_core_news_lg', 'nb_core_news_sm', 'en_core_web_lg', 'en_core_web_md', 'da_core_news_trf']
    """
    try:
        r = requests.get(f"{BASE_URL}/ner_models")
        # r.raise_for_status()
        res = r.json()
    except:  # (HTTPError, JSONDecodeError, ConnectionError) as error:
        # print(error.__doc__, error)
        print("Server-request gikk ikke gjennom. Kan ikke vise SpaCy-modellnavn.")
        res = []
    return res


def get_places(urn: str) -> DataFrame:
    """Look up placenames in a specific URN.

    Wrapper for the API endpoint [`/places`](https://api.nb.no/dhlab/#/default/post_places)

    Args:
        urn: Uniform resource name, for example: URN:NBN:no-nb_digibok_2011051112001

    Returns:
        A pandas.Dataframe with placenames occurring in the document

    Warning:
        The input parameter is **not** optional.
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/places", json=params)
    # print(r.status_code)
    return pd.DataFrame(r.json())


def geo_lookup(
    places: List,
    feature_class: Optional[str] = None,
    feature_code: Optional[str] = None,
    field: str = "alternatename",
) -> DataFrame:
    """From a list of places, return their geolocations.

    Args:
        places: a list of place names - max 1000
        feature_class: which GeoNames feature class to return. Example: `P`
        feature_code: which GeoNames feature code to return. Example: `PPL`
        field: which name field to match.

    Returns:
        Placenames and their corresponding geolocations.
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
    urn: Optional[str] = None,
    words: Optional[List] = None,
    window: int = 300,
    pr: int = 100,
) -> Series:
    """Count occurrences of words in the given URN object.

    Wrapper for the API endpoint [`/dispersion`](https://api.nb.no/dhlab/#/default/post_dispersion).

    Args:
        urn: Uniform resource name, for example: `URN:NBN:no-nb_digibok_2011051112001`
        words: Words to count occurrences of. Defaults to a list of punctuation marks.
        window: The number of tokens to search through per row.
        pr: The number of rows to search through per request.

    Returns:
        Frequency counts of the words in the `urn` text object.
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/dispersion", json=params)
    return pd.Series(r.json())


def get_metadata(urns: Optional[List[str]] = None) -> DataFrame:
    """Get metadata for a list of URNs.

    Wrapper for the API endpoint [`/get_metadata`](https://api.nb.no/dhlab/#/default/post_get_metadata).

    Examples:
        >>> urns = ["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2008040200106"]
        >>> meta = get_metadata(urns)
        >>> meta.title
        0    Historiske skildringer fra Baahuslen (Viken) :...
        1    Ibsen-ordbok : ordforrådet i Henrik Ibsens sam...
        Name: title, dtype: object

    Args:
        urns: Uniform resource name strings.

    Returns:
        Metadata for the given URNs.

    Warning:
        The input parameter is **not** optional.
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json=params)
    return DataFrame(r.json())


def get_identifiers(identifiers: Optional[list] = None) -> list:
    """Convert a list of resource identifiers to dhlabids.

    Examples:
        >>> urns = ['URN:NBN:no-nb_digibok_2008051404065', 'URN:NBN:no-nb_digibok_2008040200106']
        >>> ids = get_identifiers(urns)
        >>> ids
        [100445059, 100480157, 100615433]

    Args:
        identifiers: collection of oaiid, sesamid, urn or isbn10 identifiers

    Returns:
        list of dhlabids corresponding to the input identifiers.

    Warning:
        The input parameter is **not** optional.
    """
    res = requests.post(
        f"{BASE_URL}/identifiers",
        json={"identifiers": [i for i in identifiers if i != ""]},
    )
    return res.json()


def get_chunks(urn: Optional[str] = None, chunk_size: int = 300) -> Union[Dict, List]:
    """Fetch word frequencies for chunks of a given number of tokens per chunk in a text document.

    Wrapper for the API endpoint [`/chunks`](https://api.nb.no/dhlab/#/default/get_chunks).

    Examples:
        >>> chunks = get_chunks("URN:NBN:no-nb_digibok_2006082900066", chunk_size=100)
        >>> len(chunks)
        154              # Number of chunks that were found

    Args:
        urn: Uniform resource name
        chunk_size: Number of tokens to include in each chunk.

    Returns:
        list of dicts with the resulting chunk frequencies, or an empty
        dict
    """

    if urn is None:
        return {}
    r = requests.get(f"{BASE_URL}/chunks", params=locals())
    if r.status_code == 200:
        result = r.json()
    else:
        result = {}
    return result


def get_chunks_para(urn: Optional[str] = None) -> Union[Dict, List]:
    """Fetch chunks and their word frequencies from paragraphs in a text document.

    Wrapper for the API endpoint [`/chunks_para`](https://api.nb.no/dhlab/#/default/get_chunks_para).

    Args:
        urn: Uniform resource name, example: `URN:NBN:no-nb_digibok_2011051112001`

    Returns:
        A list of paragraph dictionaries with word frequencies.
        If the input parameter is missing, an empty dict is returned.
    """

    if urn is None:
        return {}
    r = requests.get(f"{BASE_URL}/chunks_para", params=locals())
    if r.status_code == 200:
        result = r.json()
    else:
        result = {}
    return result


def evaluate_documents(
    wordbags: Optional[Dict] = None, urns: Optional[List[str]] = None
) -> DataFrame:
    """Count and aggregate occurrences of topic words in a collection of text documents.

    Examples:
        >>> wordbags = {"natur": ["planter", "skog", "fjell", "fjord"], "dyr": ["hund", "katt", "fugl"]}
        >>> urns = ["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]
        >>> df = evaluate_documents(wordbags, urns)
        >>> df.dyr
        100014739     NaN
        100445059    40.0
        100630502     NaN
        Name: dyr, dtype: float64
        >>> df.natur
        100014739    19.0
        100445059    38.0
        100630502    20.0
        Name: natur, dtype: float64

    Args:
        wordbags: mapping between topics and lists of associated words or keywords.
        urns: uniform resource names of the documents to evaluate.

    Returns:
        Aggregated frequencies of the keywords in each topic per text document.
        The index is the dhlabid of the document.
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
    """Fetch a reference for the most frequent words from a given corpus in a given period.

    Wrapper for the API endpoint [`/reference_corpus`](https://api.nb.no/dhlab/#/default/get_reference_corpus).

    Examples:
        >>> df = r = get_reference(limit=10)
        >>> df.freq.head(10)
        word
        .      179730338
        ,      105895990
        i       63385398
        og      58712477
        til     30987239
        det     30559690
        er      30390595
        som     27248209
        av      26264497
        for     10385602
        Name: freq, dtype: int64

    Args:
        corpus: Document type to include in the corpus, can be either `'digibok'` or `'digavis'`.
        from_year: Starting point for time period of the corpus.
        to_year: Last year of the time period of the corpus.
        lang: Language of the corpus. Valid values are `'nob','nno','sme','sma','smj','fkv'`.
        limit: Maximum number of most frequent words.

    Returns:
        A multilevel dataframe with word frequencies, where the words are the index.
    """
    params = locals()
    r = requests.get(BASE_URL + "/reference_corpus", params=params)
    if r.status_code == 200:
        result = r.json()
    else:
        result = []
    return pd.DataFrame(result, columns=["word", "freq"]).set_index("word")


def find_urns(
    dhlabids: Optional[Union[Dict, DataFrame]] = None, mode: str = "json"
) -> DataFrame:
    """Return a list of URNs from a collection of docids.

    Args:
        dhlabids: dictionary of document IDs (`{docid: URN}`) or a `pandas.DataFrame`.
        mode: format of the input data.

    Returns:
        the URNs that were found, in a ``pandas.DataFrame``.
    """
    params = locals()
    r = requests.post(BASE_URL + "/find_urn", json=params)
    if r.status_code == 200:
        res = pd.DataFrame.from_dict(r.json(), orient="index", columns=["urn"])
    else:
        res = pd.DataFrame()
    return res


def reference_words(
    words: Optional[List] = None,
    doctype: str = "digibok",
    from_year: Union[str, int] = 1800,
    to_year: Union[str, int] = 2000,
) -> DataFrame:
    """Collect reference data for a list of words over a time period.

    Reference data are the absolute and relative frequencies of the `words`
    across all documents of the given `doctype` in the given time period
    (`from_year` - `to_year`).

    Args:
        words: list of word strings.
        doctype: type of reference document. Can be `"digibok"` or `"digavis"`.
            > **Note:** If any other string is given as the `doctype`,
               the resulting data is equivalent to what you get with `doctype="digavis"`.
        from_year: first year of publication to include
        to_year: last year of publication to include

    Returns:
        A dataframe with frequencies per year for each input word.
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/reference_words", json=params)
    print(r.status_code, BASE_URL)
    if r.status_code == 200:
        res = pd.DataFrame(r.json(), columns=["word", "freq", "relative"])
    else:
        res = pd.DataFrame()
    return res


def _ngram_doc(
    doctype: Optional[str] = None,
    word: Union[List, str] = ["."],
    title: Optional[str] = None,
    period: Optional[Tuple[int, int]] = None,
    publisher: Optional[str] = None,
    lang: Optional[str] = None,
    city: Optional[str] = None,
    ddk: Optional[str] = None,
    topic: Optional[str] = None,
) -> DataFrame:
    """Count occurrences of one or more words over a time period.

    The type of document to search through is decided by the `doctype`.
    Filter the selection of documents with metadata.
    Use % as wildcard where appropriate - no wildcards in `word` or `lang`.

    Args:
        doctype: API endpoint for the document type to get ngrams for.
            Can be `'book', 'periodicals', or 'newspapers'`.
        word: Word(s) to search for. Can be several words in a single string separated by comma,
            for example `"ord,ordene,orda"`.
        title: Title of a specific document to search through.
        period: Start and end years or dates of a time period,
            given as `(YYYY, YYYY)` or `(YYYYMMDD, YYYYMMDD)`.
        publisher: Name of a publisher.
        lang: Language as a 3-letter ISO code, for example `"nob"` or `"nno"`
        city: City of publication.
        ddk: Dewey Decimal Classification identifier.
        topic: Topic of the documents.

    Returns:
        Frequency counts of the word(s), spread across years. One year per row.
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
    title: Optional[str] = None,
    period: Optional[Tuple[int, int]] = None,
    publisher: Optional[str] = None,
    lang: Optional[str] = None,
    city: Optional[str] = None,
    ddk: Optional[str] = None,
    topic: Optional[str] = None,
) -> DataFrame:
    """Count occurrences of one or more words in books over a given time period.

    Wrapper for the API endpoint [`/ngram_book`](https://api.nb.no/dhlab/#/default/post_ngram_book)

    Filter the selection of books with metadata.
    Use % as wildcard where appropriate - no wildcards in ``word`` or ``lang``.

    Args:
        word: Word(s) to search for. Can be several words in a single string separated by comma,
            for example `"ord,ordene,orda"`.
        title: Title of a specific document to search through.
        period: Start and end years or dates of a time period,
            given as `(YYYY, YYYY)` or `(YYYYMMDD, YYYYMMDD)`.
        publisher: Name of a publisher.
        lang: Language as a 3-letter ISO code, for example `"nob"` or `"nno"`
        city: City of publication.
        ddk: Dewey Decimal Classification identifier.
        topic: Topic of the documents.

    Returns:
        Frequency counts of the word(s), spread across years. One year per row.
    """
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_book", json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    # df.index = df.index.map(pd.Timestamp)
    return df


# @_docstring_parameters_from(_ngram_doc, drop="doctype")
def ngram_periodicals(
    word: Union[List, str] = ["."],
    title: Optional[str] = None,
    period: Optional[Tuple[int, int]] = None,
    publisher: Optional[str] = None,
    lang: Optional[str] = None,
    city: Optional[str] = None,
    ddk: Optional[str] = None,
    topic: Optional[str] = None,
    **kwargs,
) -> DataFrame:
    """Get a time series of frequency counts for `word` in periodicals.

    Wrapper for the API endpoint [`/ngram_periodicals`](https://api.nb.no/dhlab/#/default/post_ngram_periodicals).

    Args:
        word: Word(s) to search for. Can be several words in a single string separated by comma,
            for example `"ord,ordene,orda"`.
        title: Title of a specific document to search through.
        period: Start and end years or dates of a time period,
            given as `(YYYY, YYYY)` or `(YYYYMMDD, YYYYMMDD)`.
        publisher: Name of a publisher.
        lang: Language as a 3-letter ISO code, for example `"nob"` or `"nno"`
        city: City of publication.
        ddk: Dewey Decimal Classification identifier.
        topic: Topic of the documents.

    Returns:
        Frequency counts of the word(s), spread across years. One year per row.
    """
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_periodicals", json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    # df.index = df.index.map(pd.Timestamp)
    return df


def ngram_news(
    word: Union[List, str] = ["."],
    title: Optional[str] = None,
    period: Optional[Tuple[int, int]] = None,
) -> DataFrame:
    """Get a time series of frequency counts for a given word in newspapers.

    Wrapper for the API endpoint [`ngram_newspapers`](https://api.nb.no/dhlab/#/default/post_ngram_newspapers).

    Args:
        word: Word(s) to search for. Can be several words in a single string separated by comma,
            for example `"ord,ordene,orda"`.
        title: Title of a specific newspaper to search through.
        period: Start and end years or dates of a time period,
            given as `(YYYY, YYYY)` or `(YYYYMMDD, YYYYMMDD)`.

    Returns:
        Frequency counts of the word(s), spread across the dates given in the time period.
        Either one year or one day per row.
    """
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(",")]
    params["word"] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_newspapers", json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient="index")
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    # df.index = df.index.map(pd.Timestamp)
    return df


def get_document_frequencies(
    urns: Optional[List[str]] = None, cutoff: int = 0, words: Optional[List[str]] = None
) -> DataFrame:
    """Fetch frequency counts of `words` in text documents.

    Wrapper for the API endpoint [`/frequencies`](https://api.nb.no/dhlab/#/default/post_frequencies).

    Args:
        urns: list of uniform resource name strings, for example:
            `["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]`
        cutoff: minimum frequency of a word to be counted
        words: a list of words to be counted.
            If a value is provided, both word counts and their relative frequency is returned.
            If not, all words from the whole document are returned.
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
        df.columns = ["urn", "word", "freq", "urncount"]
        df["relfreq"] = df["freq"] / df.urncount
        df = pd.pivot_table(
            df, values=["freq", "relfreq"], index="word", columns="urn"
        ).fillna(0)
    return df


def get_word_frequencies(
    urns: Optional[List[str]] = None, cutoff: int = 0, words: Optional[List[str]] = None
) -> DataFrame:
    """Fetch frequencies for `words` in text documents.

    Wrapper for the API endpoint [`/frequencies`](https://api.nb.no/dhlab/#/default/post_frequencies).

    Args:
        urns: Uniform resource name strings, for example:
            `["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]`
        cutoff: minimum frequency of a word to include in the output.
        words: a list of words to be counted - should not be left None.
    """
    return get_document_frequencies(urns, cutoff, words)


def get_urn_frequencies(
    urns: Optional[List[str]] = None, dhlabid: Optional[List] = None
) -> DataFrame:
    """Fetch frequency counts of documents as URNs or dhlabids.

    Wrapper for the API endpoint [`/frequencies`](https://api.nb.no/dhlab/#/default/post_frequencies).

    Args:
        urns: Uniform resource name strings, for example:
            `["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]`
        dhlabid: list of dhlabids, e.g. `[1000001,2000003]`
    """
    if dhlabid == None:
        params = {"urns": urns}
    else:
        params = {"dhlabid": dhlabid}
    r = requests.post(f"{BASE_URL}/urn_frequencies", json=params)
    result = r.json()
    # check if words are passed - return differs a bit
    df = pd.DataFrame(result)
    df.columns = ["urn", "freq"]
    return df


def get_document_corpus(**kwargs):
    """Wrapper for `document_corpus()`."""
    return document_corpus(**kwargs)


def document_corpus(
    doctype: Optional[str] = None,
    author: Optional[str] = None,
    freetext: Optional[str] = None,
    fulltext: Optional[str] = None,
    from_year: Optional[int] = None,
    to_year: Optional[int] = None,
    from_timestamp: Optional[int] = None,
    to_timestamp: Optional[int] = None,
    title: Optional[str] = None,
    ddk: Optional[str] = None,
    subject: Optional[str] = None,
    lang: Optional[str] = None,
    limit: Optional[int] = None,
    order_by: Optional[str] = None,
) -> DataFrame:
    """Fetch a corpus based on metadata.

    Wrapper for the API endpoint [`/build_corpus`](https://api.nb.no/dhlab/#/default/post_build_corpus).

    Args:
        doctype: `"digibok"`, `"digavis"`, `"digitidsskrift"` or `"digistorting"`.
        author: Name of an author.
        freetext: SQL query syntax for any of the metadata parameter values, for example: `"digibok AND Ibsen"`.
        fulltext: words within the publication.
        from_year: Start year for time period of interest.
        to_year: End year for time period of interest.
        from_timestamp: Start date for time period of interest.
            Format: `YYYYMMDD`, books have `YYYY0101`
        to_timestamp: End date for time period of interest.
            Format: `YYYYMMDD`, books have `YYYY0101`
        title: Name or title of a document.
        ddk: Dewey Decimal Classification identifier.
        subject: subject or topic keywords of the publication.
        lang: Language of the publication, as a 3-letter ISO code.
            Example: `"nob"` or `"nno"`
        limit: number of items to sample.
        order_by: order of elements in the corpus object.
            Typically used in combination with a limit.
            Example:
                `"random"` (random order, the slowest),
                `"rank"` (ordered by relevance, faster)
                or `"first"` (breadth-first, using the order in the database table, the fastest method)

    Returns:
        Corpus metadata in a DataFrame.
    """
    parms = locals()
    params = {x: parms[x] for x in parms if not parms[x] is None}

    r = requests.post(BASE_URL + "/build_corpus", json=params)

    return pd.DataFrame(r.json())


def urn_collocation(
    urns: Optional[List] = None,
    word: str = "arbeid",
    before: int = 5,
    after: int = 0,
    samplesize: int = 200000,
) -> DataFrame:
    """Create a collocation from a list of URNs.

    Wrapper for the API endpoint `/urncolldist_urn`.

    Args:
        urns: list of uniform resource name strings, for example:
            `["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]`
        word: word to construct collocation with.
        before: number of words preceding the given `word`.
        after: number of words following the given `word`.
        samplesize: total number of `urns` to search through.

    Returns:
        A dataframe with distances (the sum of distances and
        bayesian distance) and frequencies for words collocated with `word`.
    """

    params = {
        "urn": urns,
        "word": word,
        "before": before,
        "after": after,
        "samplesize": samplesize,
    }
    r = requests.post(BASE_URL + "/urncolldist_urn", json=params)
    return pd.read_json(r.json())


def totals(top_words: int = 50000) -> DataFrame:
    """Get aggregated raw frequencies of all words in the National Library's database.

    Wrapper for the API endpoint [`/totals/{top_words}`](https://api.nb.no/dhlab/#/default/get_totals__top_words).

    Examples:
        >>> # get the 5 most frequent words
        >>> t = totals(5)
        >>> t.freq
        .     7655423257
        ,     5052171514
        i     2531262027
        og    2520268056
        -     1314451583
        Name: freq, dtype: int64

    Args:
        top_words: The number of words to get total frequencies for.

    Returns:
        The most frequent words in the complete digital text collection.
    """
    r = requests.get(BASE_URL + f"/totals/{top_words}")
    return pd.DataFrame.from_dict(dict(r.json()), orient="index", columns=["freq"])


def concordance(
    urns: Optional[list] = None,
    words: Optional[str] = None,
    window: int = 25,
    limit: int = 100,
) -> DataFrame:
    """Get concordances for given words from a collection of text documents.

    Wrapper for the API endpoint [`/conc`](https://api.nb.no/dhlab/#/default/post_conc).

    Args:
        urns: uniform resource names, for example:
            `["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]`
        words: Word(s) to search for. Can be an SQLite fulltext
            query, an fts5 string search expression.
        window: number of tokens on either side to show in the
            collocations, between 1-25.
        limit: max. number of concordances per document. Maximum value is 1000.

    Returns:
        a table of concordances
    """
    if words is None:
        return {}  # exit condition
    else:
        params = {"urns": urns, "query": words, "window": window, "limit": limit}
        r = requests.post(BASE_URL + "/conc", json=params)
    return pd.DataFrame(r.json())


def concordance_counts(
    urns: Optional[list] = None,
    words: Optional[str] = None,
    window: int = 25,
    limit: int = 100,
) -> DataFrame:
    """Count concordances (keyword in context) for a corpus query (used for collocation analysis).

    Wrapper for the API endpoint [`/conccount`](https://api.nb.no/dhlab/#/default/post_conccount).

    Args:
        urns: uniform resource names, for example:
            `["URN:NBN:no-nb_digibok_2008051404065", "URN:NBN:no-nb_digibok_2010092120011"]`
        words: Word(s) to search for. Can be an SQLite fulltext
            query, an fts5 string search expression.
        window: number of tokens on either side to show in the
            collocations, between 1-25.
        limit: Maximum number of concordances to include per document. Maximum
            value is 1000.

    Returns:
        A frequency table for the concordances
    """
    if words is None:
        return {}  # exit condition
    else:
        params = {"urns": urns, "query": words, "window": window, "limit": limit}
        r = requests.post(BASE_URL + "/conccount", json=params)
    return pd.DataFrame(r.json())


def konkordans(
    urns: Optional[list] = None,
    words: Optional[str] = None,
    window: int = 25,
    limit: int = 100,
):
    """Wrapper for `concordance()`."""
    return concordance(**locals())


def word_concordance(
    urns: Optional[list] = None,
    dhlabid: Optional[list] = None,
    words: Optional[list] = None,
    before: int = 12,
    after: int = 12,
    limit: int = 100,
    samplesize: int = 50000,
) -> DataFrame:
    """Get a list of concordances from the National Library's database.

    Wrapper for the API endpoint [`/conc_word_urn`](https://api.nb.no/dhlab/#/default/conc_word_urn).

    Args:
        urns: dhlab serial ids.
            > Note: The server can take both urns and dhlabid, so we may rewrite this)
        words: Word(s) to search for. Must be a list.
        before: Between 0-24.
        after: Between 0-24 (before + sum <= 24)
        limit: max. number of concordances per server process.
        samplesize: samples from urns.

    Returns:
        a table of concordances
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
    elif urns is not None:
        params = {
            "urn": urns,
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

    r = requests.post(BASE_URL + "/conc_word_urn", json=params)

    return pd.DataFrame(
        [x for y in r.json() for x in y],
        columns=["dhlabid", "before", "target", "after"],
    )


def collocation(
    corpusquery: str = "norge", word: str = "arbeid", before: int = 5, after: int = 0
) -> DataFrame:
    """Make a collocation from a corpus query.

    Args:
        corpusquery: query string
        word: target word for the collocations.
        before: number of words prior to `word`
        after: number of words following `word`

    Returns:
        a dataframe with the resulting collocations
    """
    params = {
        "metadata_query": corpusquery,
        "word": word,
        "before": before,
        "after": after,
    }
    r = requests.post(BASE_URL + "/urncolldist", json=params)
    return pd.read_json(r.json())


# Norwegian word bank


def word_variant(word: str, form: str, lang: str = "nob") -> list:
    """Find an alternative wordform for a given word.

    Examples:
        >>> word_variant('spiste', 'pres-part')

    Args:
        word: any word string
        form: a morphological feature tag from the Norwegian wordbank
            [Orbanken](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-5/).
        lang: either "nob" or "nno"
    """
    r = requests.get(
        f"{BASE_URL}/variant_form", params={"word": word, "form": form, "lang": lang}
    )
    return r.json()


def word_paradigm(word: str, lang: str = "nob") -> list:
    """Find paradigms for a given ``word`` form.

    Examples:
        >>> word_paradigm('spiste')
        [['adj', ['spisende', 'spist', 'spiste']],
        ['verb', ['spis', 'spise', 'spiser', 'spises', 'spist', 'spiste']]]

    Args:
        word: any word string
        lang: either "nob" or "nno"
    """
    r = requests.get(f"{BASE_URL}/paradigm", params={"word": word, "lang": lang})
    return r.json()


def word_paradigm_many(wordlist: list, lang: str = "nob") -> list:
    """Find alternative forms for a list of words."""
    r = requests.post(f"{BASE_URL}/paradigms", json={"words": wordlist, "lang": lang})
    return r.json()


def word_form(word: str, lang: str = "nob") -> list:
    """Look up the morphological feature specification of a word form."""
    r = requests.get(f"{BASE_URL}/word_form", params={"word": word, "lang": lang})
    return r.json()


def word_form_many(wordlist: list, lang: str = "nob") -> list:
    """Look up the morphological feature specifications for word forms in a wordlist."""
    r = requests.post(f"{BASE_URL}/word_forms", json={"words": wordlist, "lang": lang})
    return r.json()


def word_lemma(word: str, lang: str = "nob") -> list:
    """Find the list of possible lemmas for a given word form."""
    r = requests.get(f"{BASE_URL}/word_lemma", params={"word": word, "lang": lang})
    return r.json()


def word_lemma_many(wordlist, lang="nob"):
    """Find lemmas for a list of given word forms."""
    r = requests.post(f"{BASE_URL}/word_lemmas", json={"words": wordlist, "lang": lang})
    return r.json()
