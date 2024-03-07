
# [![DH-LAB logo](_images/DHlab_logo_web_en_black.png)](https://www.nb.no/dh-lab/)

<!-- 
::: dhlab
-->

```{include} ../../README.md
:start-after: <!-- start dhlab-intro -->
:end-before: <!-- end dhlab-intro -->
:relative-docs: 
:relative-images:
``` 

Head to our [official homepage](https://www.nb.no/dh-lab/) for tutorials, how-to-guides, interactive web apps, and more information about the DH-lab group.


## Installation

Ensure that you already have  [Python](https://www.python.org/downloads/) >=3.9 installed.

Install the latest version of the [`dhlab`](https://pypi.org/project/dhlab/) python package in your (Unix) terminal with pip:

```shell
pip install -U dhlab
```

```{include} ./docs_functionality.md
:heading-offset: 1
relative-docs: docs/source/
```

Try some of our [examples](./docs_example_use.md) to get started.

```{toctree}
:name: contents
:hidden:
:glob:
:maxdepth: 1

docs_example_use
reference
apidocs/index
term_definitions
```