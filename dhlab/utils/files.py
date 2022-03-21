import contextlib
import os
from pathlib import Path

import requests
from IPython.display import Markdown, display


def printmd(S):
    """Use ``IPython.display`` to render markdown text."""
    display(Markdown(S))
    return


def download_from_github(filename=None, user=None, repository=None, branch='master',
                         overwrite=False,
                         silent=False):
    """Fetch a file from Github and write it to working directory.

    :param filename:     Filename, including file extension (e.g. `.py` or `.txt`)
    :param user:         Github username of the repo owner.
    :param repository:   Github repository name.
    :param branch:       Name of the repo branch. Defaults to 'master'.
    :param overwrite:    Whether to overwrite existing files in working directory. Defaults to not
                         overwrite.
    :param silent:       Whether to output logging messages to stdout. Default is not silent.
    """

    nba = requests.get(
        f"https://raw.githubusercontent.com/{user}/{repository}/{branch}/{filename}",
        headers={'Cache-Control': 'no-cache'}
    )
    if nba.status_code == 200:
        file_exists = os.path.exists(filename)
        if file_exists and not overwrite:
            if not silent:
                printmd(
                    f"File {os.path.abspath(filename)} exists - call `download_from_github('{filename}', overwrite "
                    f"= True)` in order to download module `{filename}` anyway")
        else:
            with open(filename, 'w+', encoding='utf-8') as pyfile:
                pyfile.write(nba.text)
                pyfile.flush()
                pyfile.close()
            if not silent:
                printmd(f"Downloaded file `{os.path.abspath(filename)}`")
    else:
        printmd(f"Failed to download {filename} with http code {nba.status_code}")


def get_file_from_github(url, overwrite=False, silent=False):
    """Fetch a file on github.

    it is enough with reference
    it will look in raw user content for the file.
    
    :param overwrite: defaults to no overwrite
    :param silent: default is not silent"""

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
        if file_exists and not overwrite:
            if not silent:
                printmd(
                    f"File {os.path.abspath(filename)} exists -"
                    f" call `download('{filename}', overwrite = True)` in order to "
                    f"download `{filename}` anyway")
        else:
            nba = nba.text
            with open(filename, 'w', encoding='UTF-8') as pyfile:
                pyfile.write(nba)
                pyfile.flush()
                pyfile.close()
            if not silent:
                printmd(f"Downloaded file `{os.path.abspath(filename)}`")
    else:
        printmd(f"Failed to download {fileref} with http response code {nba.status_code}")

    return


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit.

    Source: https://stackoverflow.com/a/42441759

    :meta private:
    """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
