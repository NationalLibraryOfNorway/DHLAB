import requests
from IPython.display import HTML
from urllib.parse import urlparse, urljoin

def update(module=""):
    """Fetch modules from Github and write them to folder"""
    nba = requests.get("https://raw.githubusercontent.com/Yoonsen/Modules/master/{module}.py".format(module=module))
    
    if nba.status_code == 200:
        nba = nba.text
        with open('{m}.py'.format(m=module),'w', encoding='UTF-8') as pyfile:
            pyfile.write(nba)
        print("Updated file {module}.py".format(module=module))
    else:
        print("An error occured ", module, nba.status_code)
    return

def css(url = "https://raw.githubusercontent.com/Yoonsen/Modules/master/css_style_sheets/nb_notebook.css"):
    """Associate a css stylesheet with the notebook, just specify a file or web reference, default is a custom css"""
    
    uri = urlparse(url)
    css_file = ""
    
    if uri.scheme.startswith('http'):
        query = requests.get(url)
        if query.status_code == 200:
            css_file  = query.text
    
    elif uri.scheme == "file": 
        # assume on form "file:/// on windows there is drive letter on unix not"
        file_path = url[7:]
        if file_path[2] == ':': # then windows drive reference
            file_path = file_path[1:]
        with open(file_path, encoding='utf-8') as file:
            css_file = file.read()
    else: 
        # assume string is a file locator
        with open(url, encoding='utf-8') as file:
            css_file = file.read()
    
    return HTML("<style>{css_code}</style>".format(css_code = css_file))

update("nbtext")
