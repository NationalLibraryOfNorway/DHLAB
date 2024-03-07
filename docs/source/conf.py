# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from datetime import datetime
import html
from importlib import metadata
import pathlib
import sys

root_dir = pathlib.Path(__file__).parent.parent.parent.resolve().as_posix()
sys.path.insert(0, root_dir)
print(root_dir)

project = "dhlab"
author = "The National Library of Norway"
email = "dh-lab@nb.no"
copyright = f"{datetime.now().year}, {author}"
version = metadata.version("dhlab")


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

root_doc = "index_home"

today_fmt = "%d %B %Y"

extensions = [
    "myst_parser",  # Markdownparser
    "autodoc2",
    "sphinx_togglebutton",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
]


templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "dhlab/trigram_lang_model",
    "dhlab/css_style_sheets",
]


# -- Extension configurations -----------------
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

autodoc2_packages = [
    "../../dhlab/api",
    "../../dhlab/future",
    "../../dhlab/images",
    "../../dhlab/ngram",
    "../../dhlab/metadata",
    "../../dhlab/text",
    "../../dhlab/visualize",
    "../../dhlab/wordbank",
    {
        "path": "../../dhlab",
        "exclude_files": [
            "ngram/ngram.py",
            "graph_networkx_louvain.py",
            "module_update.py",
            "nbpictures.py",
            "constants.py",
            "nbtext.py",
            "nbtokenizer.py",
            "token_map.py",
            "__init__.py",
            "legacy",
            "css_style_sheets",
        ],
        "auto_mode": True,
    },
]

autodoc2_replace_annotations = [
    (
        "package.MyClass",
        "package.module.MyClass",
    )
]
autodoc2_replace_bases = [
    ("package.MyClass", "package.module.MyClass"),
]
autodoc2_render_plugin = "myst"

pygments_style = "sphinx"
pygments_dark_style = "monokai"

togglebutton_hint = "Show"
togglebutton_hint_hide = "Hide"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "furo"
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

html_theme = "furo"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    # "announcement": "Welcome to the dhlab documentation!",
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "source_repository": "https://github.com/NationalLibraryOfNorway/DHLAB",
    "source_branch": "main",
    "source_directory": "docs/",
    # "light_logo": "",
    # "light_css_variables": {
    #     "color-brand-primary": "#cf2e2e",
    #     "color-brand-content": "#0693e3",
    #     "color-admonition-background": "#edeae5",
    # },
    # "dark_logo": "",
    # "dark_css_variables": {
    #     "color-brand-primary": "#cf2e2e",
    #     "color-brand-content": "#0693e3",
    #     "color-admonition-background": "#7b715e",
    # },
    # "top_of_page_button": "edit",
    # For components/edit-this-page.html
}


html_css_files = [
    "dhlab/css_style_sheets/grade3.css",
    "dhlab/css_style_sheets/monokai.css",
    "dhlab/css_style_sheets/nb_notebook_2.css",
    "dhlab/css_style_sheets/nb_notebook_blue.css",
    "dhlab/css_style_sheets/nb_notebook.css",
]

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "dhlab"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "dhlab"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_images/NB_logo_small.png"
# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_images/nb_symbol_farge_z5B_icon.ico"

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%Y-%m-%d"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True
