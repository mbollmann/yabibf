# yabibf: Yet Another BIBliography Formatter

This package was born out of a need to convert BibTeX bibliographies into
formatted HTML entries.  It combines bibtexparser and citeproc-py with some
simple and potentially error-prone string replacement.  In other words, it's a
duct-taped monstrosity.  I probably would've been better off doing this in
another programming language with better libraries, yet here we are.

Use at your own risk.


## Installation

For now, just do:

```
pip install git+https://github.com/mbollmann/yabibf.git
```

## Sample Usage

Let's say we have a file named `test.bib` with this single entry:

```bibtex
@inproceedings{bollmann-sogaard-2021-error,
    title = "Error Analysis and the Role of Morphology",
    author = "Bollmann, Marcel  and
      S{\o}gaard, Anders",
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume",
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.eacl-main.162",
    doi = "10.18653/v1/2021.eacl-main.162",
    pages = "1887--1900"
}
```

Then we could do:

```python
from yabibf import BibTeX, CiteprocFormatter, NameDecorator, LinkTitleDecorator

bib = BibTeX(["test.bib"])
style = "association-for-computational-linguistics"
cf = CiteprocFormatter(style, bib)
cf.decorators = [
    NameDecorator(["Marcel Bollmann", "John Doe", "Jane Doe"]),
    LinkTitleDecorator(),
]
print(cf.render("bollmann-sogaard-2021-error"))
```

This should give us:

```html
<span class="bibitem-highlight-name">Marcel Bollmann</span> and Anders Søgaard. 2021. <a class="bibitem-title" href="https://aclanthology.org/2021.eacl-main.162">Error Analysis and the Role of Morphology</a>. In <i>Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume</i>, pages 1887–1900, Online. Association for Computational Linguistics.
```
