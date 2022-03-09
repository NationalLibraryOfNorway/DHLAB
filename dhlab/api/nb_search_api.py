import pandas as pd
import requests


def load_picture(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    # print(r.status_code)
    return r.raw


def iiif_manifest(urn):
    r = requests.get(f"https://api.nb.no/catalog/v1/iiif/{urn}/manifest")
    return r.json()


def mods(urn):
    r = requests.get(f"https://api.nb.no:443/catalog/v1/metadata/{urn}/mods")
    return r.json()


def super_search(term, number=50, page=0, mediatype='bilder'):
    """Søk etter term og få ut json"""
    number = min(number, 50)
    if term == '':
        r = requests.get(
            "https://api.nb.no:443/catalog/v1/items",
            params={
                'filter': f'mediatype:{mediatype}',
                'page': page,
                'size': number
            }
        )
    else:
        r = requests.get(
            "https://api.nb.no:443/catalog/v1/items",
            params={
                'q': term,
                'filter': f'mediatype:{mediatype}',
                'page': page,
                'size': number
            }
        )
    return r.json()


def total_search(size=50, page=0):
    """Finn de første antallet = 'size' fra side 'page' og få ut json"""
    size = min(size, 50)
    r = requests.get(
        "https://api.nb.no:443/catalog/v1/items",
        params={
            'filter': 'mediatype:bilder',
            'page': page,
            'size': size
        }
    )
    return r.json()


def get_df(frases, title='aftenposten'):
    """get document phrases"""
    querystring = " + ".join(['"' + frase + '"' for frase in frases])
    query = {
        'q': querystring,
        'size': 1,
        'aggs': 'year',
        # 'filter':'mediatype:{mt}'.format(mt=media),
        'filter': f'title:{title}'
    }
    r = requests.get("https://api.nb.no/catalog/v1/items", params=query)
    aggs = r.json()['_embedded']['aggregations'][0]['buckets']
    return {x['key']: x['count'] for x in aggs}


def get_json(frases, mediatype='aviser'):

    querystring = " + ".join(['"' + frase + '"' for frase in frases])
    query = {
        'q': querystring,
        'size': 1,
        'snippets': mediatype,
        'aggs': 'year',

        #        'filter':'mediatype:{mt}'.format(mt=mediatype),
        'searchType': 'FULL_TEXT_SEARCH'
        # 'filter':'title:{title}'.format(title=title)
    }
    r = requests.get("https://api.nb.no/catalog/v1/items", params=query)
    aggs = r.json()
    return aggs


def get_data(frase, media='avis', title='jazznytt'):

    query = {
        'q': '"' + frase + '""',
        'size': 1,
        'aggs': 'year',
        'filter': 'mediatype:{mt}'.format(mt=media),
        'filter': 'title:{title}'.format(title=title)
    }
    r = requests.get("https://api.nb.no/catalog/v1/items", params=query)
    return r.json()


def get_data_and(frases, title='aftenposten', media='avis'):

    querystring = " + ".join(['"' + frase + '"' for frase in frases])
    print(querystring)
    query = {
        'q': querystring,
        'size': 1,
        'aggs': 'year',
        # 'filter':'mediatype:{mt}'.format(mt=media),
        'filter': 'title:{title}'.format(title=title)
    }
    r = requests.get("https://api.nb.no/catalog/v1/items", params=query)
    return r.json()


def get_df_pd(frase, media='bøker'):
    return pd.DataFrame.from_dict(
        get_df(frase, media=media), orient='index').sort_index()


def get_konks(urn, phrase, window=1000, n=1000):

    querystring = '"' + phrase + '"'
    query = {
        'q': querystring,
        'fragments': n,
        'fragSize': window

    }
    r = requests.get(
        "https://api.nb.no/catalog/v1/items/{urn}/contentfragments".format(urn=urn), params=query)
    res = r.json()
    results = []
    try:
        for x in res['contentFragments']:
            urn = x['pageid']
            hit = x['text']
            splits = hit.split('<em>')
            s2 = splits[1].split('</em>')
            before = splits[0]
            word = s2[0]
            after = s2[1]
            results.append({'urn': urn, 'before': before,
                           'word': word, 'after': after})
    except BaseException:
        results = []
    return results


def get_phrase_info(urn, phrase, window=1000, n=1000):

    querystring = '"' + phrase + '"'
    query = {
        'q': querystring,

    }
    r = requests.get(
        f"https://api.nb.no/catalog/v1/items/{urn}/contentfragments",
        params=query)
    res = r.json()
    return res
