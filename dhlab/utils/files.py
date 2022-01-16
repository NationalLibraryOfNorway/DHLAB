import requests
import os
from IPython.display import HTML, Markdown, display

def printmd(S):
    display(Markdown(S))
    return

def download(module="", user = "Yoonsen", overwrite=True, silent=False):
    """Fetch modules from Github using username and default path and write them to folder"""
    nba = requests.get(
        "https://raw.githubusercontent.com/{user}/Modules/master/{module}.py".format(module=module),
        headers={'Cache-Control': 'no-cache'}
        )
    if nba.status_code == 200:
        filename = f'{module}.py'
        file_exists = os.path.exists(filename)
        if file_exists and not(overwrite):
            if not silent:
                printmd(f"File {os.path.abspath(filename)} exists - call `download('{module}', overwrite = True)` in order to download module `{module}` anyway")
        else:
            nba = nba.text
            with open(filename,'w', encoding='UTF-8') as pyfile:
                pyfile.write(nba)
                pyfile.flush()
                pyfile.close()
            if not silent:
                printmd(f"Updated file `{os.path.abspath(module)}.py`")
    else:
        printmd( 
            """{intro} for {module} with error {code}""".format(
                intro = "An error occured during download", 
                module = module, 
                code= nba.status_code
            )
        )
    return

def get_url(url, filename = None):
    """Fetch url and write content to folder"""
    return "oops"