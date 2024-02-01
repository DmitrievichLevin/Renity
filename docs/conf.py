"""Sphinx configuration."""

project = "Burgos"
author = "Jalin Howard"
copyright = "2024, Jalin Howard"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
