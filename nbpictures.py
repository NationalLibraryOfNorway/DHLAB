from PIL import Image
import requests
import json
import os
from IPython.display import HTML
import json
import re

small_scale = 0.59
large_scale = 1.58


def nb_search(
    term = '', creator = '', 
    number = 50, 
    page = 0, 
    mediatype = 'bøker', 
    lang = "nob",
    period = (18000101, 20401231)
):
    """Søk etter term og få ut json"""
    
    number = min(number, 50)
    
    filters = []
    aq = []
    

    params = {
        'page':page, 
        'size':number
    }
    
    if lang != '':
        aq.append('languages:{lang}'.format(lang = lang ))
    
    if creator != '':
        filters.append('creator:{c}'.format(c=creator))
    
    if mediatype != '':
        filters.append('mediatype:{mediatype}'.format(mediatype=mediatype))
    
    if period != ():
        filters.append('date:[{date_from} TO {date_to}]'.format(date_from = period[0], date_to = period[1]))
    
    if filters != []:
        params['filter'] = filters
    
    if aq != []:
        params['aq'] = aq
        
    if term != '':
        params['q'] = term
    
    r = requests.get("https://api.nb.no:443/catalog/v1/items", params = params)
    return r.json()


# In[32]:




def iiif_manifest(urn):
    if not 'URN' in str(urn) and not 'digibok' in str(urn):
        urn = "URN:NBN:no-nb_digibok_" + str(urn)
    elif not 'URN' in str(urn):
        urn = "URN:NBN:no-nb_" + str(urn)
    r = requests.get("https://api.nb.no/catalog/v1/iiif/{urn}/manifest".format(urn=urn))
    return r.json()

def urns_from_super(
    term = '', 
    creator = '', 
    number = 50, 
    page = 0, 
    mediatype = 'bøker', 
    lang = "nob",
    period = (18000101, 20401231)
):
    
    res = nb_search(term, mediatype = mediatype, creator = creator, number=number, page = page, lang = lang, period = period)
    ids = [x['metadata']['identifiers']  for x in res['_embedded']['items'] ]
    return [x['urn'] for x in ids if 'urn' in x]

def get_illustration_data_from_book(urn):

    if 'digibok' in str(urn):
        urn = re.findall("[0-9]{13}", str(urn))[0] 
    r = requests.get('https://api.nb.no/ngram/illustrations', json={'urn': urn})
    return r.json() 

def get_urls_from_illustration_data(illus, part = True, scale = None, cuts = True):
    """part sets size of output of page, if part is True it returns the cut out of image
    illus is a dictionary of with entries and values like this: 
    {'height': 270, 'hpos': 251, 'page': 'digibok_2017081626006_0018', 'resolution': 400, 'vpos': 791, 'width': 373} 
    the variable cuts, if true allows cropping of image - restricted images must not go over 1024 x 1024 pixels"""
    
    if scale == None:
        if illus['resolution'] >= 300 or illus['resolution'] < 100:
            scale = large_scale
        else:
            scale = small_scale
            
    height = illus['height']
    width = illus['width']

    if cuts != False:
        if width * scale > 1024:
            width = int(1024/scale)
        if height * scale > 1024:
            height = int(1024/scale)
            
    urn = "URN:NBN:no-nb_" + illus['page']
    if part == True:
        # return cut out
        url = "https://www.nb.no/services/image/resolver/{urn}/{hpos},{vpos},{width},{height}/full/0/native.jpg".format(
            urn = urn, 
            width = int(width * scale), 
            height = int(height * scale), 
            vpos = int(int(illus['vpos']) * scale), 
            hpos = int(int(illus['hpos']) * scale)
        )
    else:
        # return whole page
        url = "https://www.nb.no/services/image/resolver/{urn}/full/0,{part}/0/native.jpg".format( part=part,
                urn = urn, width=illus['width'], height= illus['height'], vpos=illus['vpos'], hpos=illus['hpos'])
    
    return url

def display_finds(r):
    """A list of urls in r is displayed as HTML"""
    rows = ["<tr><td><img src='{row}'</td><td><a href = {meta} target='_'>{meta}</a></td></tr>".format(row=row, meta=row) for row in r]
    return HTML("""<html><head></head>
     <body>
     <table>
     {rows}
     </table>
     </body>
     </html>
     """.format(rows=' '.join(rows)))


def url2urn(url):
    return re.findall("URN:.*[0-9]{13}", url)[0]


def mods(urn):
    r = requests.get("https://api.nb.no:443/catalog/v1/metadata/{id}/mods".format(urn=urn))
    return r.json()

def pages(urn, scale=800):
    a = iiif_manifest(urn)
    return [page['images'][0]['resource']['@id'].replace("full/full/", "full/0,{s}/".format(s=scale)) for page in a['sequences'][0]['canvases']]

def load_picture(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content=True
    return r.raw

def get_url(urn, page=1, part=200):
    """From a representaion of URN (serial number or any string with serial number) - mapped to digibok"""
    import re
    
    urnserial = re.findall('[0-9]+', str(urn))
    if urnserial != []:
        urnserial = urnserial[0]
    else:
        return ""
    urn = "URN:NBN:no-nb_digibok_" + urnserial + '_{0:04d}'.format(page)
    print(urn)
    url = "https://www.nb.no/services/image/resolver/{urn}/full/0,{part}/0/native.jpg".format(urn = urn, part=part)
    return url


def page_urn(urn, page=1):
    # urn as digit
    return "URN:NBN:no-nb_digibok_" + urn + '_{0:04d}'.format(page)

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



def find_urns_sesam(term = '', creator = '', number=50, page=0, mediatype='bilder'):
    """generates urls from super_search for pictures"""
    x = nb_search(term = term, creator = creator, number = number, page = page, mediatype=mediatype)
    try:
        sesamid =[
            f['id']
            for f in x['_embedded']['items'] 
            if f['accessInfo']['accessAllowedFrom'] == 'EVERYWHERE'
            and 'thumbnail_custom' in f['_links']
        ]
    except:
        sesamid = []
    return sesamid

def save_pictures(pages, urn, root = '.'):
    """Save picture references in pages on the form: 
    pages = {
        urn1 : [page1, page2, ..., pageN], 
        urn2: [page1, ..., pageM]},
        ...
        urnK: [page1, ..., pageL]
    }
    Parameter urn is one of the keys in pages, where each page reference is a URL.
    """
    
    # In case urn is an actual URN, works also if urn is passed as sesamid

    folder_name = urn.split(':')[-1]
    folder_ref = os.path.join(root, folder_name)
    try:
        os.mkdir(folder_ref)

    except FileExistsError:
        True

    for p in pages[urn]:
        # pell ut entydig referanse til bildet fra URL-en i bildelisten som filnavn

        filename = p.split('/')[6].split(':')[-1] + '.jpg'
        
        path = os.path.join(folder_ref, filename)
        get_picture_from_url(p).save(path)
    
    return True

def save_all_pages(pages, root='.'):
    """Save picture references in pages on the form: 
    pages = {
        urn1 : [page1, page2, ..., pageN], 
        urn2: [page1, ..., pageM]},
        ...
        urnK: [page1, ..., pageL]
    }
    Each page reference is a URL.
    """
    
    # In case urn is an actual URN, works also if urn is passed as sesamid
    for urn in pages:
        folder_name = urn.split(':')[-1]
        folder_ref = os.path.join(root, folder_name)
        try:
            os.mkdir(folder_ref)

        except FileExistsError:
            True

        for p in pages[urn]:
            # pell ut entydig referanse til bildet fra URL-en i bildelisten som filnavn

            filename = p.split('/')[6].split(':')[-1] + '.jpg'

            path = os.path.join(folder_ref, filename)
            get_picture_from_url(p).save(path)

    return True

def load_picture(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content=True
    #print(r.status_code)
    return r.raw

def json2html(meta):
    items = ["<dt>{key}</dt><dd>{val}</dd>".format(key=key, val= meta[key]) for key in meta]
    result = "<dl>{items}</dl>".format(items=' '.join(items))
    return result
        

