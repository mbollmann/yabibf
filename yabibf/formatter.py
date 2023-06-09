import citeproc.formatter
from citeproc import (
    Citation,
    CitationItem,
    CitationStylesStyle,
    CitationStylesBibliography,
)
from citeproc_styles import get_style_filepath


class CiteprocFormatter:
    def __init__(self, style, bibliography):
        """
        A class for formatting bibliographies with citeproc-py.

        Parameters:
            style: The name of a CSL Style.  Corresponds to the name of a .csl file in the
                   citation-style-language/styles repository:
                   <https://github.com/citation-style-language/styles>
            bibliography: A citeproc-py BibliographySource object, e.g. a BibTeX instance.
        """
        self.style_path = get_style_filepath(style)
        self.style = CitationStylesStyle(self.style_path, validate=False)
        self.bib = bibliography
        self.cs_bib = CitationStylesBibliography(
            self.style, bibliography, citeproc.formatter.html
        )

    def render(self, item):
        if isinstance(item, str):
            return self.render_key(item)
        elif isinstance(item, CitationItem):
            return self.render_item(item)
        else:
            return self.render_entry(item)

    def render_entry(self, entry):
        return self.render_key(entry.key)

    def render_key(self, key):
        item = CitationItem(key)
        return self.render_item(item)

    def render_item(self, item):
        self.cs_bib.register(Citation([item]))
        mixed_string = self.cs_bib.style.render_bibliography([item])[0]
        return str(mixed_string)
