"""Sphinx configuration of the documentation of goldpan (https://villano-lab.github.io/goldpan/).

Build it from the repository folder::

    python -m pip install -r docs/requirements.txt
    python -m pip install -e ".[archive,parquet,root,midas]"
    python -m sphinx -b html -W --keep-going docs docs/_build/html

`-W` makes a warning (a broken reference, a docstring Sphinx cannot read) an error, as the pull-request check does.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))              # the package, even when it is not installed

project = "goldpan"
author = "goldpan authors"
copyright = "the goldpan authors"
language = "en"

extensions = [
    "myst_parser",             # the pages are Markdown
    "sphinx.ext.autodoc",      # the reference is read from the docstrings
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",     # accepts NumPy / Google style sections if a docstring uses them
    "sphinx.ext.intersphinx",  # links into numpy, awkward, pyarrow, Python
    "sphinx.ext.viewcode",
    "sphinx_copybutton",       # a copy button on every code block
]

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
exclude_patterns = ["_build", "requirements.txt"]
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3
myst_all_links_external = True                           # the pages link to other sites, not to Sphinx documents

# The docstrings put names in single backticks: show them as code, not as emphasis.
default_role = "code"

autosummary_generate = True
autodoc_default_options = {"members": True, "undoc-members": False, "show-inheritance": True}
autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_use_param = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "awkward": ("https://awkward-array.org/doc/stable/", None),
    "pyarrow": ("https://arrow.apache.org/docs/", None),
}
intersphinx_timeout = 10

html_theme = "furo"
html_title = "goldpan"
html_static_path = []
html_theme_options = {
    "source_repository": "https://github.com/villano-lab/goldpan/",
    "source_branch": "develop",
    "source_directory": "docs/",
}
html_copy_source = False
html_show_sourcelink = False


def _status_note(app, what, name, obj, options, lines):
    """Show the development status of a function (`goldpan.status`) at the top of its entry when it is not settled."""
    if getattr(obj, "status", None) == "under_development":
        note = getattr(obj, "status_note", None)
        lines[0:0] = [".. warning::", "", "   **Under development**" + (f": {note}" if note else "."), ""]


def setup(app):
    app.connect("autodoc-process-docstring", _status_note)
