import requests
import os
from IPython.display import HTML, Markdown, display

def printmd(S):
    display(Markdown(S))
    return

def download_from_github(file = None, user = None, repository = None, branch = 'master', overwrite = False, silent = False):
    """Fetch a file from Github and write it to working directory, 
    supply user and repository, 
    branch defaults to master
    overwrite: defaults to no overwrite
    silent: default is not silent"""
    
    nba = requests.get(
        f"https://raw.githubusercontent.com/{user}/{repository}/{branch}/{file}",
        headers={'Cache-Control': 'no-cache'}
        )
    if nba.status_code == 200:
        filename = f'{file}'
        file_exists = os.path.exists(filename)
        if file_exists and not(overwrite):
            if not silent:
                printmd(f"File {os.path.abspath(filename)} exists - call `download('{file}', overwrite = True)` in order to download module `{file}` anyway")
        else:
            nba = nba.text
            with open(filename,'w', encoding='UTF-8') as pyfile:
                pyfile.write(nba)
                pyfile.flush()
                pyfile.close()
            if not silent:
                printmd(f"Downloaded file `{os.path.abspath(file)}`")
    else:
        printmd(f"""Failed to download {file} with http code {nba.status_code}""")
        
    return

def get_file_from_github(url, overwrite = False, silent = False):
    """fetch a file on github, 
    it is enough with reference 
    it will look in raw user content for the file
    
    overwrite: defaults to no overwrite
    silent: default is not silent"""
    
    if url.startswith("https://github.com/") or url.startswith("github.com"):
        trail = url.split("github.com")[-1].replace('blob/', '')
        fileref = f"""https://raw.githubusercontent.com{trail}"""
    elif url.startswith("raw.githubusercontent"):
        fileref = f"""https://{url}"""
    elif url.startswith("https://raw.githubusercontent"):
        fileref = url
    else:
        return "is this is a file on github?"
        
    nba = requests.get(
        f"{fileref}",
        headers={'Cache-Control': 'no-cache'}
        )
    if nba.status_code == 200:
        filename = os.path.basename(fileref)
        file_exists = os.path.exists(filename)
        if file_exists and not(overwrite):
            if not silent:
                printmd(f"File {os.path.abspath(filename)} exists - call `download('{filename}', overwrite = True)` in order to download `{filename}` anyway")
        else:
            nba = nba.text
            with open(filename,'w', encoding='UTF-8') as pyfile:
                pyfile.write(nba)
                pyfile.flush()
                pyfile.close()
            if not silent:
                printmd(f"Downloaded file `{os.path.abspath(filename)}`")
    else:
        printmd(f"""Failed to download {fileref} with http response code {nba.status_code}""")
        
    return