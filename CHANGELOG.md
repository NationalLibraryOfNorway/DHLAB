# Changelog 

## v2.9.1 (2022-09-12)

## v2.9.0 (2022-09-05)

### Feat

- added reference for words

## v2.8.2 (2022-09-01)

## v2.8.1 (2022-08-30)

### Fix

- delete whitespace

## v2.8.0 (2022-08-30)

### Feat

- added spacy pos parse (pos, lemma, dependency)

### Refactor

- **corpus**: ignore index in corpus.add (#84)

## v2.7.0 (2022-08-24)

## v2.6.3 (2022-08-23)

### Feat

- add Empty Corpus to dhlab.__init__

### Fix

- dewey search in corpus builder

## v2.6.2 (2022-08-17)

### Feat

- add corpus default limit
- add docstring to concordance

### Fix

- revert gitignore
- revert Collocation

## v2.6.1 (2022-08-15)

## v2.6.0 (2022-08-08)

### Feat

- code for word evaluations

## v2.5.0 (2022-08-05)

### Feat

-  geolocation

## v2.4.0 (2022-07-12)

### Feat

- ner with spaCy

## v2.3.6 (2022-07-12)

### Fix

- nb_ngram to point to new endpoint


## v2.3.0 (2022-06-02)

### Feat

- added access to Norsk Ordbank, wordbank

## v2.2.0 (2022-05-13)

### Feat

- ngram, geodata


## v2.1.0 (2022-05-13)

### Feat

- geodata

## v2.0.25 (2022-04-27)

### Fix

- **setup.cfg**: make package dhlab importable

## v2.0.24 (2022-04-19)

### Refactor

- expose dhlab v1 modules

## v2.0.22 (2022-03-22)

### Fix

- import all legacy modules in `__init__.py`

### Refactor
- move dhlab_v1 code into its own subpackage
- **docs/package_summary.rst**: add reference table for legacy code 

## v2.0.21 (2022-03-21)
### Refactor 
- **constants**: add global variables for URLs in constants.py 
- Reformat code with pep8 tools
- turn relative imports into absolute imports
- simplify and reduce expressions
- rename classes with CamelCase

### Docs 
- **README**: add "Example use"
- add docstrings in subpackages
- add docs/CHANGELOG.md
- **docs**: add `*.rst` documentation files 
- add autosummary of whole dhlab package
- **logo**: update logo image
- add jupyter integration and toggle feature
- add copybutton to code blocks
- add docstrings and make functions private

## v2.0.20geo (2022-03-02)

### Feat
- **dhlab.api.dhlab_api**: add function `get_places`
- **text.geo_data**: add class `GeoData`

### Fix
- **text.dispersion**: pass **kwargs to `plot()` 

## v.2.0.18dispersion (2022-02-21)

### Feat
- **text.dispersion**: add class Dispersion
- **api.dhlab_api**: add get_dispersion

### Fix
- **requirements**: remove wordcloud  

## v2.0.17params (2022-02-08)
### Refactor
- **text.corpus**: add parameter fulltext
- **api.dhlab_api.document_corpus**: add parameter fulltext
- **text.conc_coll.Concordance**: add parameters window and limit 
- **text.conc_coll.Collocations**: add parameter samplesize

### Fix 
- **text.corpus.urnlist**: fix urnlist assignment

## v2.0.12.chunk (2022-01-29)
### Refactor 
- **text.chunking**: add attribute self.chunks

## v2.0.10chunks (2022-01-29)

### Feat
- **text.conc_coll**: add class Counts 
- **text.corpus**: add class Corpus_from_identifiers
- **text.chunking**: add class Chunks
- **text.chunking**: add functions get_chunks, get_chunks_para

### Fix 
- imports
- **dhlab_api.get_chunks**: return dict not dataframe
- apply autopep8

## v2.0.5 (2022-01-19)

### Refactor

- **nbtokenizer**: edit tokens for mail and web addresses

### Feat 
- add Tokens class

### Fix 
- imports


## v2.0.2a (2022-01-18)

### Fix 

- typecheck of corpus objects

## v2.0.1.alpha6 (2022-01-18)

- changed wordcloud import
- fixed corpus transfer in conc_coll


## v2.0.0.beta (2022-01-18)

### Feat
- add get_file_from_github, download_from_github in utils

### Refactor

- New package structure

### Docs

- include installation instructions in README


## v1.0.0 (2022-01-06)

- Set up Github Actions to run automatic linting and testing
- Set up documentation pages
- Include documentation of the code in docstrings


### Fix

- address linting issues from flake8
- reformat code

### Feat

- add documentation summaries for all modules
- add documentation for the repo
- add docstrings from README.md to nbtext.py
- add pylint config file

### Refactor

- reduce code duplication
- update workflow file reference
- change str.format to f-strings
- optimize imports
- rename workflow that packages and publishes dhlab to pypi
- use default publish workflow
- reduce compatible python versions
- update publishing workflow
- type out scope for linting explicitly
- move pylint.yml

## v0.75 (2019-09-09)

- Inital release to pypi
