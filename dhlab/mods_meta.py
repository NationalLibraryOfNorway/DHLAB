import requests
from bs4 import BeautifulSoup


def konk(urns=None, word=None, before=5, after=5, only_urn=True):
    """ Simple urnkonk, only urn + concordance """
    params = locals()
    #print(params)
    r = requests.post("https://api.nb.no/ngram/urnkonk", json = params)
    return r.json()

def meta_natbib(children = False, yearfrom = "", yearto = "", lang = None, author = None, title = None, subtitle = None, publisher = None, subject = None, topic = None, marctuples = None, limit=20):
    """ New metadata - search the national bibliography using marc21 tuples """
    params = locals()
    #print(params)
    r = requests.post("https://api.nb.no/ngram/get_urns", json = params)
    return r.json()

def metadata(urns=None, marctuples = [(100,1,' ', 'a'),(260, ' ',' ', 'c'), (245,1,3,'a'),(245,1,0,'a'),(245,1,3,'b'),(245,1,0,'b'), (650,7,' ','a'), (653,' ',' ','a')]):
    """ Fetch metadata from national bibliography """
    params = locals()
    #print(params)
    r = requests.post("https://api.nb.no/ngram/metadata", json=params)
    return r.json()


def mods_meta(urn):
    if not str(urn).startswith('URN'):
        urn = "URN:NBN:no-nb_digibok_" + str(urn)
    r = requests.get("https://api.nb.no:443/catalog/v1/metadata/{id}/mods".format(id = urn))
    return r.text

def marc_meta(urn):
    
    if not str(urn).startswith('URN'):
        urn = "URN:NBN:no-nb_digibok_" + str(urn)
    r = requests.get("https://api.nb.no:443/catalog/v1/metadata/{id}/marcxml".format(id = urn))
    return r.text

def book_info(urn):
    
    def fetch(soup, tag, props={}):
        try:
            x = soup.find(tag, props).string
        except:
            x = ""
        return x

    def fetch_all(soup, tag, props={}):
        x = []
        for z in soup.find_all(tag, props):
            try:
                x.append(z.string)
            except:
                True
        return x
    
    soup = BeautifulSoup(mods_meta(urn), features='lxml')

    authors = []
    translators = []
    coworkers = []
    for x in soup.find_all('name'):
        namestr = x.namepart.string
        try:
            identifier = x.nameidentifier.string
        except:
            identifier = ""
        role = x.find('role')
        #print('role', role)
        lf = x.find('namepart',{'type':'date'})
        if lf != None:
            lf = lf.string
        if role != None:
            if role.roleterm.string == 'trl':
                translators.append((namestr, lf, identifier))
            if role.roleterm.string == 'medarb.':
                coworkers.append((namestr, lf, identifier))
        else:
            authors.append((namestr, lf, identifier))
     
    topics = fetch_all(soup,'topic')
    urn = fetch(soup,"identifier", {'type':'urn'})
    dewey = fetch(soup, 'classification',{'authority':"ddc"})
    lang = fetch(soup, "languageterm")
    sesamid = fetch(soup, "identifier", {'type':'sesamid'})
    publisher = fetch(soup,'publisher')
    translate = soup.find('language', {'objectpart':'translation'})
    #print(translate)
    trans = fetch(translate, 'languageterm')
    title = fetch(soup, 'title')
    subtitle = fetch(soup, 'subtitle')
    date = fetch(soup, 'dateissued')
    gender = fetch(soup, 'gender')
    return (authors, coworkers, translators, title, subtitle, date, lang, publisher, topics, dewey, sesamid, trans, gender)
