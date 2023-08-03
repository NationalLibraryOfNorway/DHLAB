[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NationalLibraryOfNorway/digital_tekstanalyse/HEAD)
# DHLAB

<!-- start dhlab-intro -->

 [`dhlab`](https://pypi.org/project/dhlab/) is a python library for doing qualitative and quantitative analyses of the digital texts from [*nettbiblioteket*](https://www.nb.no/search) (eng: "the online library") at the [National Library of Norway](https://www.nb.no/) (NLN). *Nettbiblioteket* is the NLN's digital collection of media publications.

<!-- end dhlab-intro -->

Check out our [documentation](https://dhlab.readthedocs.io/en/latest/) for more info.

## Installation with pip

Install the latest version of [`dhlab`](https://pypi.org/project/dhlab/) in your (Unix) terminal with pip:

```shell
pip install -U dhlab
```

## Install dhlab from github repo

Open you terminal in the file location you will work with [DHLAB](https://github.com/NationalLibraryOfNorway/DHLAB).

``` shell
git clone https://github.com/NationalLibraryOfNorway/DHLAB.git
cd DHLAB
pip install -U -e .
```

## For developers
We use poetry to manage dependencies and the python package distribution.

- [Install poetry](https://python-poetry.org/docs/#installation)
- Activate a virtual environment:

    ```shell
    poetry shell
    ```

- Install the project dependencies, including the extra development dependencies:

    ```shell
    poetry install --with dev
    ```

- Update dependency versions (see [poetry docs](https://python-poetry.org/docs/managing-dependencies/#dependency-groups) for more on dependency management):

    ```shell
    poetry update
    ```

NB! Please commit the `poetry.lock` and `pyproject.toml` files if any dependencies got updated.

## Contact
<!-- start contact-info -->
The code here is developed and maintained by [The Digital Humanities lab group](https://www.nb.no/dh-lab/).

If you have any questions, or run into any problems with the code, please log them in our [issue
tracker](https://github.com/NationalLibraryOfNorway/DHLAB/issues).
<!-- end contact-info -->
