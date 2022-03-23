import setuptools

import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="dhlab",
    version=get_version("dhlab/__init__.py"),
    author="The National Library of Norway",
    author_email="dh-lab@nb.no",
    description="Library for text and image analysis by the Digital Humanities lab (DH-lab)",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://dhlab.readthedocs.io",
    project_urls={
        "GitHub": "https://github.com/NationalLibraryOfNorway/DHLAB",
        "Bug Tracker": "https://github.com/NationalLibraryOfNorway/DHLAB/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'ipython',
        'ipywidgets',
        'matplotlib',
        'networkx',
        'numpy',
        'pandas',
        'Pillow',
        'python_louvain',
        'requests',
        'seaborn',
        'setuptools',
    ]
)
