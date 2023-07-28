import os
import re

import requests
from IPython.display import display, HTML, Markdown
from PIL import Image

small_scale = 0.59
large_scale = 1.58


def nb_search(
        term='', creator='',
        number=50,
        page=0,
        mediatype='bøker',
        lang="nob",
        period=(18000101, 20401231),
        extra_filters=None,
        extra_conditions=None
):
    """Søk etter term og få ut json"""
    number = min(number, 50)

    filters = []
    aq = []

    if extra_filters is not None:
        filters += extra_filters
    params = {
        'page': page,
        'size': number
    }
    if extra_conditions is not None:
        for x in extra_conditions:
            params[x] = extra_conditions[x]

    if lang != '':
        aq.append(f'languages:{lang}')

    if creator != '':
        filters.append(f'creator:{creator}')

    if mediatype != '':
        filters.append(f'mediatype:{mediatype}')

    if period != ():
        filters.append(f'date:[{period[0]} TO {period[1]}]')

    if filters:
        params['filter'] = filters

    if aq:
        params['aq'] = aq

    if term != '':
        params['q'] = term

    r = requests.get("https://api.nb.no:443/catalog/v1/items", params=params)
    return r.json()


def div_wrapper(div_content):
    return f"""<div>{div_content}</div>"""


def display_books(books, width=100):
    """A dictionary of urns - urls is displayed """

    def html_wrapper(body):
        return f"""<style>
    img {{
        width:{width}px;
        height:auto;
        max-width:100%}}
    </style>
    <body>{body}</body>"""

    book_divs = ""
    for u in books:
        mf = iiif_manifest(u)
        thumbnail = f"<img src = '{mf['thumbnail']['@id']}'></img>"
        metainfo = '\n'.join(
            [f"<b>{x['label']}</b>{x['value']}" for x in mf['metadata']])
        imgs = '\n'.join(
            [f"<img src='{pic_url}'></img>" for pic_url in books[u]])
        book_divs += div_wrapper(thumbnail + metainfo + imgs)
    return html_wrapper(book_divs)


def markdown_books(books, width=100):
    """A dictionary of urns - urls is displayed """

    book_divs = ""
    for u in books:
        mf = iiif_manifest(u)
        thumbnail = f"<h3>Forside</h3> <img src='{mf['thumbnail']['@id']}'></img>\n\n"
        metainfo = '\n'.join([
            f"<h3>Metadata</h3> <b>{x['label']}</b> {x['value']}"
            for x in mf['metadata']
        ])
        imgs = '\n'.join([
            f"<img style='float:right' src='{pic_url}' width = {width}></img>"
            for pic_url in books[u]
        ])
        book_divs += div_wrapper(thumbnail + metainfo + imgs)
    return book_divs


def iiif_manifest(urn):
    if 'URN' not in str(urn) and 'digibok' not in str(urn):
        urn = "URN:NBN:no-nb_digibok_" + str(urn)
    elif 'URN' not in str(urn):
        urn = "URN:NBN:no-nb_" + str(urn)
    r = requests.get(f"https://api.nb.no/catalog/v1/iiif/{urn}/manifest")
    return r.json()


def urns_from_super(
        term='',
        creator='',
        number=50,
        page=0,
        mediatype='bøker',
        lang="nob",
        period=(18000101, 20401231),
        filters=None,
        conditions=None
):
    res = nb_search(term, mediatype=mediatype, creator=creator, number=number,
                    page=page, lang=lang, period=period, extra_filters=filters,
                    extra_conditions=conditions)
    ids = [x['metadata']['identifiers'] for x in res['_embedded']['items']]
    return [x['urn'] for x in ids if 'urn' in x]


def get_illustration_data_from_book(urn):
    if 'digibok' in str(urn):
        urn = re.findall("[0-9]{13}", str(urn))[0]
    r = requests.get(
        'https://api.nb.no/ngram/illustrations',
        json={
            'urn': urn})
    return r.json()


def get_urls_from_illustration_data(
        illus, part=True, scale=None, cuts=True, delta=0):
    """
    Restricted images must not go over 1024 x 1024 pixels.

    :param illus: dictionary of this format:

        ``{'height': 270, 'hpos': 251, 'page': 'digibok_2017081626006_0018',
        'resolution': 400, 'vpos': 791, 'width': 373}``

    :param part: If True, return a cut out of the image
    :param scale: To be filled in
    :param cuts: If true, allow cropping of image
    :param delta: To be filled in
    :return: URL of the image
    """
    if scale is None:
        if illus['resolution'] >= 300 or illus['resolution'] < 100:
            scale = large_scale
        else:
            scale = small_scale

    height = int(illus['height']) + 2 * delta
    width = int(illus['width']) + 2 * delta
    vpos = int(illus['vpos']) - delta
    hpos = int(illus['hpos']) - delta

    if cuts:
        if width * scale > 1024:
            width = int(1024 / scale)
        if height * scale > 1024:
            height = int(1024 / scale)

    urn = "URN:NBN:no-nb_" + illus['page']
    url_prefix = "https://www.nb.no/services/image/resolver"
    if part:
        # return cut out
        url = (
            f"{url_prefix}/"
            f"{urn}/"
            f"{int(hpos * scale)},"
            f"{int(vpos * scale)},"
            f"{int(width * scale)},"
            f"{int(height * scale)}"
            f"/full/0/native.jpg"
        )
    else:
        # return whole page
        url = (
            f"{url_prefix}/"
            f"{urn}/"
            f"full/"
            f"0,{part}/"
            f"0/native.jpg"
        )

    return url


def show_illustrations_urn(urn, tilgjengelig='fritt'):
    display(
        Markdown(
            '\n'.join([
                '**' + x['label'] + '**: ' + x['value']
                for x in iiif_manifest(urn)['metadata']
            ])
        )
    )

    if tilgjengelig.lower().startswith('fri'):
        c = False
    else:
        c = True
    return display_finds(
        [
            get_urls_from_illustration_data(u, cuts=c) for u in
            get_illustration_data_from_book(urn)
        ]
    )


def display_finds_meta(r):
    """A list of urls in r is displayed as HTML"""
    rows = [(f"<tr><td><img src='{row}'</td><td><a href = {row} target='_'>"
             f"{row}</a></td></tr>") for row in r]
    return HTML(f"""<html><head></head>
     <body>
     <table>
     {' '.join(rows)}
     </table>
     </body>
     </html>
     """)


def display_finds(r):
    """A list of urls in r is displayed as HTML"""
    rows = [f"<tr><td><img src='{row}'</td></tr>" for row in r]
    return HTML(f"""<html><head></head>
     <body>
     <table>
     {' '.join(rows)}
     </table>
     </body>
     </html>
     """)


def url2urn(url):
    return re.findall("URN:.*[0-9]{13}", url)[0]


def mods(urn):
    r = requests.get(f"https://api.nb.no:443/catalog/v1/metadata/{urn}/mods")
    return r.json()


def pages(urn, scale=800):
    a = iiif_manifest(urn)
    return [page['images'][0]['resource']['@id'].replace(
        "full/full/", f"full/0,{scale}/"
    ) for page in a['sequences'][0]['canvases']]


def load_picture(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    return r.raw


def get_url(urn, page=1, part=200):
    """From a representaion of URN mapped to digibok.

     A URN is a serial number or any string with serial number.
     """
    urnserial = re.findall('[0-9]+', str(urn))
    if urnserial:
        urnserial = urnserial[0]
    else:
        return ""
    urn = f"URN:NBN:no-nb_digibok_{urnserial}_{page:04d}"
    print(urn)
    url_prefix = "https://www.nb.no/services/image/resolver"
    url = f"{url_prefix}/{urn}/full/0,{part}/0/native.jpg"
    return url


def page_urn(urn, page=1):
    # urn as digit
    return f"URN:NBN:no-nb_digibok_{urn}_{page:04d}"


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


def find_urls(term, number=50, page=0, mediatype='bilder'):
    """generates urls from super_search for pictures"""
    x = super_search(term, number, page, mediatype=mediatype)
    try:
        urls = [
            f['_links']['thumbnail_custom']['href']
            for f in x['_embedded']['items']
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
            and 'thumbnail_custom' in f['_links']
        ]
    except BaseException:  # PEP8: E722 do not use bare 'except', too broad exception clause
        urls = []
    return urls


def find_urls2(term, number=50, page=0):
    """generates urls from super_search for pictures"""
    x = super_search(term, number, page)
    try:
        urls = [
            f['_links']['thumbnail_custom']['href']
            for f in
            x['_embedded']['mediaTypeResults'][0]['result']['_embedded'][
                'items']
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
            and 'thumbnail_custom' in f['_links']
        ]
    except BaseException:  # PEP8: E722 do not use bare 'except', too broad exception clause
        urls = [' ... hmm ...']
    return urls


def get_picture_from_urn(urn, width=0, height=300):
    meta = iiif_manifest(urn)
    url_prefix = "https://www.nb.no/services/image/resolver"
    if 'error' not in meta:
        if width == 0 and height == 0:
            url = f"{url_prefix}/{urn}/full/full/0/native.jpg"
        else:
            url = f"{url_prefix}/{urn}/full/{width},{height}/0/native.jpg"
        # print(url)
    return Image.open(load_picture(url))


def get_picture_from_url(url, width=0, height=300):
    return Image.open(
        load_picture(
            url.format(width=width, height=height)
        )
    )


def get_metadata_from_url(url):
    urn = re.findall("(URN.*?)(?:/)", url)[0]
    triple = iiif_manifest(urn)
    # print(urn, triple)
    r = {}  # Local variable 'r' value is not used
    if 'error' not in triple:
        r = {x['label']: x['value']
             for x in triple['metadata'] if 'label' in x}
    else:
        r = triple['error']
    return r


def find_urns(term):
    """From result of super_search, to be fed into iiif_manifest."""

    ss = super_search(term)
    urns = [
        f['metadata']['identifiers']['urn']
        for f in
        ss['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items']
        if 'urn' in f['metadata']['identifiers']
    ]
    return urns


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


def total_urls(number=50, page=0):
    """find urls sequentially"""
    x = total_search(number, page)
    try:
        urls = [
            f['_links']['thumbnail_custom']['href']
            for f in x['_embedded']['items']
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
            and 'thumbnail_custom' in f['_links']
        ]
    except BaseException:  # PEP8: E722 do not use bare 'except', too broad exception clause
        urls = []
    return urls


def find_urns_sesam(term='', creator='', number=50,
                    page=0, mediatype='bilder'):
    """generates urls from super_search for pictures"""
    x = nb_search(term=term, creator=creator, number=number, page=page,
                  mediatype=mediatype)
    try:
        sesamid = [
            f['id']
            for f in x['_embedded']['items']
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
            and 'thumbnail_custom' in f['_links']
        ]
    except BaseException:
        sesamid = []
    return sesamid


def save_pictures(pages_, urn, root='.'):
    """Save picture references in pages on the form::

        pages = {
            urn1: [page1, page2, ..., pageN],
            urn2: [page1, ..., pageM],
            ...
            urnK: [page1, ..., pageL]}

    Parameter urn is one of the keys in pages,
    where each page reference is a URL.
    """

    # In case urn is an actual URN, works also if urn is passed as sesamid

    folder_name = urn.split(':')[-1]
    folder_ref = os.path.join(root, folder_name)
    try:
        os.mkdir(folder_ref)

    except FileExistsError:
        pass

    for p in pages_[urn]:
        # pell ut entydig referanse til bildet fra URL-en i bildelisten som
        # filnavn

        filename = p.split('/')[6].split(':')[-1] + '.jpg'

        path = os.path.join(folder_ref, filename)
        get_picture_from_url(p).save(path)

    return True


def save_all_pages(pages_, root='.'):
    """Save picture references in pages on the form::

        pages = {
            urn1 : [page1, page2, ..., pageN],
            urn2: [page1, ..., pageM],
            ...
            urnK: [page1, ..., pageL]
        }

    Each page reference is a URL.
    """

    # In case urn is an actual URN, works also if urn is passed as sesamid
    for urn in pages_:
        folder_name = urn.split(':')[-1]
        folder_ref = os.path.join(root, folder_name)
        try:
            os.mkdir(folder_ref)

        except FileExistsError:
            pass

        for p in pages_[urn]:
            # pell ut entydig referanse til bildet fra URL-en i bildelisten som
            # filnavn

            filename = p.split('/')[6].split(':')[-1] + '.jpg'

            path = os.path.join(folder_ref, filename)
            get_picture_from_url(p).save(path)

    return True


def json2html(meta):
    items = [f"<dt>{key}</dt><dd>{value}</dd>" for key, value in meta.items()]
    result = f"<dl>{' '.join(items)}</dl>"
    return result
