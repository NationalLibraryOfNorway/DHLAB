import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dhlab",
    version="2.0.3",
    author="The National Library of Norway",
    author_email="dh-lab@nb.no",
    description="Library for text and image analysis by the Digital Humanities lab (DH-lab)",
    long_description=long_description,
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
    python_requires='>=3.2',
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
	'wordcloud'
    ]
)
