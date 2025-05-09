# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime
import importlib
import pathlib
import sys

root_dir = pathlib.Path(__file__).parent.parent.parent.resolve().as_posix()
sys.path.insert(0, root_dir)
print(root_dir)

project = "dhlab"
author = "The National Library of Norway"
email = "dh-lab@nb.no"
copyright = f"{datetime.datetime.now().year}, {author}"
version = importlib.metadata.version("dhlab")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

root_doc = "index"

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
    {
        "path": "../../dhlab/",
        "module": "dhlab",
        "exclude_files": [
            "ngram/ngram.py",
            "graph_networkx_louvain.py",
            "module_update.py",
            "nbpictures.py",
            "nbtext.py",
            "nbtokenizer.py",
            "text/nbtokenizer.py",
            "token_map.py",
        ],
        "exclude_dirs": [
            "legacy",
            "future",
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

html_static_path = ["_static"]

html_theme = "furo"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "source_repository": "https://github.com/NationalLibraryOfNorway/DHLAB",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#0044ba",
        "color-brand-content": "#0044ba",
        "color-admonition-background": "#70a6ff",
        "font-stack": "'DM Sans', sans-serif",
        "font-stack--monospace": "Courier, monospace",
        "font-stack--headings": "'DM Mono', monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "#70a6ff",
        "color-brand-content": "#70a6ff",
        "color-admonition-background": "#0044ba",
    },
    # For components/edit-this-page.html
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/NationalLibraryOfNorway/DHLAB",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}


html_css_files = [
    "dhlab/css_style_sheets/grade3.css",
    "dhlab/css_style_sheets/monokai.css",
    "dhlab/css_style_sheets/nb_notebook_2.css",
    "dhlab/css_style_sheets/nb_notebook_blue.css",
    "dhlab/css_style_sheets/nb_notebook.css",
]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "dhlab"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "dhlab"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_images/favicon.svg"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_images/favicon.svg"  # dark blue #0044ba

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%Y-%m-%d"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True
