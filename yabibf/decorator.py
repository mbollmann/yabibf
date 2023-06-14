from bibtexparser.model import Entry
from urllib.parse import urlparse
import logging
from typing import Optional
from unicodedata import normalize


log = logging.getLogger("bibtex")


class BaseDecorator:
    def __call__(self, entry: Entry, text: str) -> str:
        """
        A decorator modifies a bibliography entry.

        Parameters:
            entry: The BibTeX entry as parsed by bibtexparser.
            text: The generated bibliography entry as produced by citeproc-py.

        Returns:
            The same bibliography entry, optionally changed with whatever
            text decoration is desired.
        """
        return text


class LinkTitleDecorator(BaseDecorator):
    """Wraps the paper title in a link to the paper."""

    def __init__(self, css_class: str = "bibitem-title") -> None:
        self._css = css_class

    def infer_url(self, entry: Entry) -> Optional[str]:
        """Determines which URL to link to."""
        fields = entry.fields_dict
        if "url" in fields:
            return entry["url"]
        if "doi" in fields:
            return f"https://dx.doi.org/{entry['doi']}"
        if "eprint" in fields:
            url = urlparse(entry["eprint"])
            if url.scheme in ("http", "https"):
                return entry["eprint"]
            if url.scheme.lower() == "arxiv" or (
                "archivePrefix" in fields and entry["archivePrefix"].lower() == "arxiv"
            ):
                return f"https://arxiv.org/abs/{url.path}"
        return None

    def __call__(self, entry, text):
        url = self.infer_url(entry)
        title = entry["title"]
        if title not in text:
            log.warning(f"Couldn't find title string in entry '{entry.key}'")
            return text
        if url is not None:
            decorated = f'<a class="{self._css}" href="{url}">{title}</a>'
        else:
            decorated = f'<span class="{self._css}">{title}</span>'
        return text.replace(title, decorated)


class NameDecorator(BaseDecorator):
    """Wraps a given list of names in a span, for later CSS highlighting."""

    def __init__(
        self, names: list[str], css_class: str = "bibitem-highlight-name"
    ) -> None:
        self.names = [normalize("NFKC", n) for n in names]
        self._css = css_class

    def __call__(self, entry, text):
        for name in self.names:
            if name in text:
                span = f'<span class="{self._css}">{name}</span>'
                text = text.replace(name, span)
        return text
