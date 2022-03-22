# Changelog

## Release 2.0.22 update docs (2022-03-22)

* import all legacy modules in __init__.py
* move dhlab_v1 code into its own subpackage
* (docs): add reference table for legacy code 

## Release 2.0.20 geo_data (2022-02-21)
* add function `dhlab.api.dhlab_api.get_places`
* add class text.geo_data.GeoData

## Release 2.0.18 dispersion (2022-02-21)
* add class text.dispersion.Dispersion

## Release 2.0.10 chunking (2022-01-29)
* add classes in text subpackage:
  * corpus.Corpus_from_identifiers
  * conc_coll.Counts
  * chunking.Chunks


## Release v2.0.5 nbtokenizer (2022-01-19)

* edit tokens for mail and web addresses
* add Tokens class

## Release v2.0.1.beta (2022-01-18)

* changed wordcloud import
* fixed corpus transfer in conc_coll


## Pre-release v2.0.0 (2022-01-18)
#### Features
* add get_file_from_github, download_from_github in utils

#### Refactors

* New package structure

#### Fixes

* remove static path, remove fail on warning

#### Docs

* update link to notebook repo
* include installation instructions in README


## Release v1.0.0 (2022-01-06)

* Set up Github Actions to run automatic linting and testing
* Set up documentation pages
* Include documentation of the code in docstrings


## Release 0.75

Inital release to pypi
