#!/usr/bin/env python3

import bibtexparser
from bibtexparser import middlewares as mw
from bibtexparser.model import Entry
import citeproc.source
from citeproc.source.bibtex import BibTeX as CiteprocBibTeX
import logging
from typing import Optional


log = logging.getLogger("bibtex")


class BibTeX(CiteprocBibTeX):
    """
    This class represents a BibTeX bibliography.  It parses .bib files using
    bibtexparser, but inherits from citeproc-py's BibTeX class to provide
    functionality for converting entries to CSL fields.
    """

    def __init__(
        self,
        bibfiles: Optional[list[str]] = None,
        drop_fields: Optional[list[str]] = None,
    ) -> None:
        # We're not calling super().__init__() because that automatically loads
        # and parses a BibTeX file with citeproc-py's functions, which is
        # precisely what we're trying to avoid
        self.bibliography = None
        self.drop_fields = [
            "ENTRYTYPE",
            "ID",
            "eprint",
            "archivePrefix",
            "primaryClass",
            "URN",
        ]
        if drop_fields is not None:
            self.drop_fields += drop_fields
        self.library = None
        self.preamble_macros = {}
        self.fields.update(
            {
                "url": "URL",
                "institution": "publisher",
                "school": "publisher",
                "type": "note",
            }
        )
        if bibfiles is not None:
            self.parse_bibfiles(bibfiles)

    @property
    def entries(self) -> list[Entry]:
        return self.library.entries

    def get_as_entry(self, key: str) -> Entry:
        return self.library.entries_dict.get(key)

    def parse_bibfiles(self, bibfiles: list[str]) -> None:
        bibdata = []
        for filename in bibfiles:
            with open(filename, "r") as f:
                bibdata.append(f.read())
        self.library = bibtexparser.parse_string(
            "\n".join(bibdata),
            append_middleware=[
                # transforms {\"o} -> ö, removes curly braces, etc.
                mw.LatexDecodingMiddleware(),
                # transforms dec -> 12
                mw.MonthIntMiddleware(True),
                # separates & splits author names into {first, von, last, jr}
                mw.SeparateCoAuthors(),
                mw.SplitNameParts(),
            ],
        )
        for entry in self.library.entries:
            self.add(self.create_reference(entry))

    def create_reference(self, entry: Entry) -> citeproc.source.Reference:
        csl_type = self.types[entry.entry_type]
        csl_fields = self._bibtex_to_csl(entry)
        csl_date = self._bibtex_to_csl_date(entry)
        if csl_date:
            csl_fields["issued"] = csl_date
        return citeproc.source.Reference(entry.key, csl_type, **csl_fields)

    def _bibtex_to_csl(self, entry):
        csl_dict = {}
        for field, value in entry.items():
            if field in self.drop_fields:
                continue
            try:
                csl_field = self.fields[field]
            except KeyError:
                if field not in ("year", "month", "filename"):
                    log.warning("Unsupported BibTeX field '{}'".format(field))
                continue
            if field == "pages":
                value = self._bibtex_to_csl_pages(value)
            elif field in ("author", "editor"):
                value = self._parse_author(value)
            else:
                value = str(value)
            csl_dict[csl_field] = value
        return csl_dict

    def _bibtex_to_csl_date(self, entry):
        if "month" in entry.fields_dict and "month" not in self.drop_fields:
            # already int's via mw.MonthIntMiddleware()
            begin_dict, end_dict = {"month": entry["month"]}, {"month": entry["month"]}
        else:
            begin_dict, end_dict = {}, {}
        if "year" in entry.fields_dict:
            begin_dict["year"], end_dict["year"] = self._parse_year(entry["year"])
        if not begin_dict:
            return None
        if begin_dict == end_dict:
            return citeproc.source.Date(**begin_dict)
        else:
            return citeproc.source.DateRange(
                begin=citeproc.source.Date(**begin_dict),
                end=citeproc.source.Date(**end_dict),
            )

    def _parse_year(self, year):
        year_str = str(year)
        if "–" in year_str:
            begin_year, end_year = year_str.split("–")
            begin_len, end_len = len(begin_year), len(end_year)
            if end_len < begin_len:
                end_year = begin_year[: begin_len - end_len] + end_year
        else:
            begin_year = end_year = int(year_str)
        return begin_year, end_year

    def _parse_author(self, authors):
        csl_authors = []
        for author in authors:
            csl_parts = {}
            for part, csl_label in (
                ("first", "given"),
                ("von", "non-dropping-particle"),
                ("last", "family"),
                ("jr", "suffix"),
            ):
                value = " ".join(getattr(author, part))
                if value.strip():
                    csl_parts[csl_label] = value
            name = citeproc.source.Name(**csl_parts)
            csl_authors.append(name)
        return csl_authors
