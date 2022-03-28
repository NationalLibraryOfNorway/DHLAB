from typing import Union
from IPython.display import HTML
from PIL import Image

from dhlab.api.nb_search_api import iiif_manifest, super_search, total_search, load_picture


def pages(urn, scale=800):
    a = iiif_manifest(urn)
    return [page['images'][0]['resource']['@id'].replace(f"full/full/", "full/0,{s}/") for page in
            a['sequences'][0]['canvases']]


def get_url(urn, page=1, part=200):
    # urn as digit
    urn = "URN:NBN:no-nb_digibok_" + urn + '_{0:04d}'.format(page)
    print(urn)
    url = f"https://www.nb.no/services/image/resolver/{urn}/full/0,{part}/native.jpg"
    return url


def page_urn(urn, page=1):
    # urn as digit
    return "URN:NBN:no-nb_digibok_" + urn + '_{0:04d}'.format(page)


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
    except:
        urls = []
    return urls


def find_urls2(term, number=50, page=0):
    """generates urls from super_search for pictures"""
    x = super_search(term, number, page)
    try:
        urls = [
            f['_links']['thumbnail_custom']['href']
            for f in x['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items']
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
               and 'thumbnail_custom' in f['_links']
        ]
    except:
        urls = [' ... hmm ...']
    return urls


def get_picture_from_urn(urn: Union[int, str], width: int = 0, height: int = 300):
    """Fetch the Image object with its URN identifier.

    :meta private:

    :param urn: The uniform resource name number
    :param width: Resolution width of the image.
    :param height: Resolution height of the image.
    :return: An :py:class:`~PIL.Image.Image` object.
    """
    meta = iiif_manifest(urn)
    if 'error' not in meta:
        if width == 0 and height == 0:
            url = f"https://www.nb.no/services/image/resolver/{urn}/full/full/0/native.jpg"
        else:
            url = f"https://www.nb.no/services/image/resolver/{urn}/full/{width},{height}/0/native.jpg"
        # print(url)
    return Image.open(load_picture(url))


def get_picture_from_url(url, width=0, height=300):
    return Image.open(
        load_picture(
            url.format(width=width, height=height)
        )
    )


def get_metadata_from_url(url):
    import re
    urn = re.findall("(URN.*?)(?:/)", url)[0]
    triple = iiif_manifest(urn)
    # print(urn, triple)
    r = dict()
    if not 'error' in triple:
        r = {x['label']: x['value'] for x in triple['metadata'] if 'label' in x}
    else:
        r = triple['error']
    return r


def find_urns(term):
    """From result of super_search, to be fed into iiif_manifest"""

    ss = super_search(term)
    urns = [
        f['metadata']['identifiers']['urn']
        for f in ss['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items']
        if 'urn' in f['metadata']['identifiers']
    ]
    return urns


def total_urls(number=50, page=0):
    """find urls sequentially """
    x = total_search(number, page)
    try:
        urls = [
            f['_links']['thumbnail_custom']['href']
            for f in x['_embedded']['items']
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
               and 'thumbnail_custom' in f['_links']
        ]
    except:
        urls = []
    return urls


def json2html(meta):
    items = ["<dt>{key}</dt><dd>{val}</dd>".format(key=key, val=meta[key]) for key in meta]
    result = "<dl>{items}</dl>".format(items=' '.join(items))
    return result


def display_finds(r):
    """A list of urls in r is displayed as HTML"""
    rows = ["<tr><td><img src='{row}'</td><td>{meta}</td></tr>".format(row=row, meta=json2html(
        get_metadata_from_url(row))).format(width=0, height=200) for row in r]
    return HTML("""<html><head></head>
     <body>
     <table>
     {rows}
     </table>
     </body>
     </html>
     """.format(rows=' '.join(rows)))
