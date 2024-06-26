from bibtexparser.model import Entry
import citeproc.formatter
import citeproc.source
from citeproc import (
    Citation,
    CitationItem,
    CitationStylesStyle,
    CitationStylesBibliography,
)
from pathlib import Path
from unicodedata import normalize
import sys

from .decorator import BaseDecorator


if sys.version_info >= (3, 12):
    # citeproc-py-styles not supported
    def get_style_filepath(*args):
        raise RuntimeError("citeproc-py-styles not supported in Python 3.12")

else:
    from citeproc_styles import get_style_filepath


class CiteprocFormatter:
    def __init__(
        self, style: str, bibliography: citeproc.source.BibliographySource
    ) -> None:
        """
        A class for formatting bibliographies with citeproc-py.

        Parameters:
            style: The name of a CSL style, or path to a .csl file defining the style.
                   If given as a name, must correspond to the name of a .csl file in the
                   citation-style-language/styles repository:
                   <https://github.com/citation-style-language/styles>
            bibliography: A citeproc-py BibliographySource object, e.g. a BibTeX instance.
        """
        if style.endswith(".csl") and Path(style).exists():
            self.style_path = style
        else:
            self.style_path = get_style_filepath(style)
        self.style = CitationStylesStyle(self.style_path, validate=False)
        self.bib = bibliography
        self.cs_bib = CitationStylesBibliography(
            # The formatter could be changed/made configurable
            self.style,
            bibliography,
            citeproc.formatter.html,
        )
        self.decorators: list[BaseDecorator] = []

    def add_decorator(self, decorator: BaseDecorator) -> None:
        self.decorators.append(decorator)

    def render(self, item: CitationItem | Entry | str) -> str:
        if isinstance(item, str):
            item = CitationItem(item)
            return self.render_item(item)
        elif isinstance(item, CitationItem):
            return self.render_item(item)
        elif isinstance(item, Entry):
            item = CitationItem(item.key)
            return self.render_item(item)
        else:
            raise ValueError(f"Can't render {type(item)}")

    def render_item(self, item: CitationItem) -> str:
        # We register a new Citation for the paper (otherwise it won't show up
        # in the bibliography), then render a bibliography consisting only of
        # that cited paper, then take its first (and only) entry.
        self.cs_bib.register(Citation([item]))
        strings = self.cs_bib.style.render_bibliography([item])[0]
        text = normalize("NFKC", str(strings))
        return self._decorate(item, text)

    def _decorate(self, item: CitationItem, text: str) -> str:
        entry = self.bib.get_as_entry(item.key)
        for decorator in self.decorators:
            text = decorator(entry, text)
        return text
