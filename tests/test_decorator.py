from yabibf import BibTeX, NameDecorator, LinkTitleDecorator


# Setup
bib = BibTeX(["tests/example.bib"], drop_fields=["month"])


def test_name_decorator1():
    decorator = NameDecorator(["Mike Tyson", "Anders Søgaard", "Leonard Bernstein"])
    # entry = bib.get_as_entry("bollmann-sogaard-2021-error")
    text = "Marcel Bollmann and Anders Søgaard. 2021. Error Analysis and the Role of Morphology. In <i>Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume</i>, pages 1887–1900, Online. Association for Computational Linguistics."
    decorated = decorator(None, text)
    assert (
        decorated
        == 'Marcel Bollmann and <span class="bibitem-highlight-name">Anders Søgaard</span>. 2021. Error Analysis and the Role of Morphology. In <i>Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume</i>, pages 1887–1900, Online. Association for Computational Linguistics.'
    )


def test_name_decorator2():
    decorator = NameDecorator(["Tianyu Gao", "Danqi Chen"])
    # entry = bib.get_as_entry("li-etal-2022-ditch")
    text = "Huihan Li, Tianyu Gao, Manan Goenka, and Danqi Chen. 2022. Ditch the Gold Standard: Re-evaluating Conversational Question Answering. In <i>Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</i>, pages 8074–8085, Dublin, Ireland. Association for Computational Linguistics."
    decorated = decorator(None, text)
    assert (
        decorated
        == 'Huihan Li, <span class="bibitem-highlight-name">Tianyu Gao</span>, Manan Goenka, and <span class="bibitem-highlight-name">Danqi Chen</span>. 2022. Ditch the Gold Standard: Re-evaluating Conversational Question Answering. In <i>Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)</i>, pages 8074–8085, Dublin, Ireland. Association for Computational Linguistics.'
    )


def test_linktitle_decorator_with_url():
    decorator = LinkTitleDecorator()
    entry = bib.get_as_entry("bollmann-sogaard-2021-error")
    text = "Marcel Bollmann and Anders Søgaard. 2021. Error Analysis and the Role of Morphology. In <i>Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume</i>, pages 1887–1900, Online. Association for Computational Linguistics."
    decorated = decorator(entry, text)
    assert (
        decorated
        == 'Marcel Bollmann and Anders Søgaard. 2021. <a class="bibitem-title" href="https://aclanthology.org/2021.eacl-main.162">Error Analysis and the Role of Morphology</a>. In <i>Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume</i>, pages 1887–1900, Online. Association for Computational Linguistics.'
    )


def test_linktitle_decorator_with_doi():
    decorator = LinkTitleDecorator()
    entry = bib.get_as_entry("sahin-2022-augment")
    text = "Gözde Gül Şahin. 2022. To Augment or Not to Augment? A Comparative Study on Text Augmentation Techniques for Low-Resource NLP. <i>Computational Linguistics</i>, 48(1):5–42."
    decorated = decorator(entry, text)
    assert (
        decorated
        == 'Gözde Gül Şahin. 2022. <a class="bibitem-title" href="https://dx.doi.org/10.1162/coli_a_00425">To Augment or Not to Augment? A Comparative Study on Text Augmentation Techniques for Low-Resource NLP</a>. <i>Computational Linguistics</i>, 48(1):5–42.'
    )


def test_linktitle_decorator_with_arxiv():
    decorator = LinkTitleDecorator()
    entry = bib.get_as_entry("rust2023language")
    text = "Phillip Rust, Jonas F. Lotz, Emanuele Bugliarello, Elizabeth Salesky, Miryam de Lhoneux, and Desmond Elliott. 2023. Language Modelling with Pixels."
    decorated = decorator(entry, text)
    assert (
        decorated
        == 'Phillip Rust, Jonas F. Lotz, Emanuele Bugliarello, Elizabeth Salesky, Miryam de Lhoneux, and Desmond Elliott. 2023. <a class="bibitem-title" href="https://arxiv.org/abs/2207.06991">Language Modelling with Pixels</a>.'
    )
