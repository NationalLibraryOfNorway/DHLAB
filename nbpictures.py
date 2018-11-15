from PIL import Image
import requests
import json
from IPython.display import HTML

def iiif_manifest(urn):
    r = requests.get("https://api.nb.no/catalog/v1/iiif/{urn}/manifest".format(urn=urn))
    return r.json()

def mods(urn):
    r = requests.get("https://api.nb.no:443/catalog/v1/metadata/{id}/mods".format(urn=urn))
    return r.json()


def super_search(term, number=50, page=0, mediatype='bilder'):
    """Søk etter term og få ut json"""
    number = min(number, 50)
    if term == '':
        r = requests.get(
            "https://api.nb.no:443/catalog/v1/items", 
             params = { 
                 'filter':'mediatype:{mediatype}'.format(mediatype=mediatype), 
                 'page':page, 
                 'size':number
             }
        )
    else:        
        r = requests.get(
            "https://api.nb.no:443/catalog/v1/items", 
             params = {
                 'q':term, 
                 'filter':'mediatype:{mediatype}'.format(mediatype=mediatype), 
                 'page':page, 
                 'size':number
             }
        )
    return r.json()

def find_urls(term, number=50, page=0, mediatype='bilder'):
    """generates urls from super_search for pictures"""
    x = super_search(term, number, page, mediatype=mediatype)
    try:
        urls =[
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



def get_picture_from_urn(urn, width=0, height=300):
    meta = iiif_manifest(urn)
    if 'error' not in meta:
        if width == 0 and height == 0:
            url = "https://www.nb.no/services/image/resolver/{urn}/full/full/0/native.jpg".format(urn=urn)
        else:
            url = "https://www.nb.no/services/image/resolver/{urn}/full/{width},{height}/0/native.jpg".format(urn=urn, width=width, height=height)
        #print(url)
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
    #print(urn, triple)
    r = dict()
    if not 'error' in triple:
        r = {x['label']:x['value'] for x in triple['metadata']  if 'label' in x }
    else:
        r = triple['error']
    return r

def find_urns(term):
    """From result of super_search, to be fed into iiif_manifest"""
    
    ss = super_search(term)
    urns = [
        f['metadata']['identifiers']['urn'] 
        for f in  ss['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items'] 
        if 'urn' in f['metadata']['identifiers']
    ]
    return urns

def total_search(size=50, page=0):
    """Finn de første antallet = 'size' fra side 'page' og få ut json"""
    size = min(size, 50)
    r = requests.get(
        "https://api.nb.no:443/catalog/v1/items", 
         params = {
             'filter':'mediatype:bilder', 
             'page':page, 
             'size':size
         }
    )
    return r.json()

def total_urls(number=50, page=0):
    """find urls sequentially """
    x = total_search(number, page)
    try:
        urls =[
            f['_links']['thumbnail_custom']['href']
            for f in x['_embedded']['items'] 
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
            and 'thumbnail_custom' in f['_links']
        ]
    except:
        urls = []
    return urls


def load_picture(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content=True
    #print(r.status_code)
    return r.raw

def json2html(meta):
    items = ["<dt>{key}</dt><dd>{val}</dd>".format(key=key, val= meta[key]) for key in meta]
    result = "<dl>{items}</dl>".format(items=' '.join(items))
    return result
        

def display_finds(r):
    """A list of urls in r is displayed as HTML"""
    rows = ["<tr><td><img src='{row}'</td><td>{meta}</td></tr>".format(row=row, meta=json2html(get_metadata_from_url(row))).format(width=0, height=200) for row in r]
    return HTML("""<html><head></head>
     <body>
     <table>
     {rows}
     </table>
     </body>
     </html>
     """.format(rows=' '.join(rows)))
