from yabibf import BibTeX, CiteprocFormatter


# Setup
bib = BibTeX(["tests/example.bib"], drop_fields=["month"])
style = "association-for-computational-linguistics"
cf = CiteprocFormatter(style, bib)


def test_all_entries_parsed():
    assert len(bib.entries) == 5


def test_format_article_one_author():
    output = cf.render("sahin-2022-augment")
    assert (
        output
        == "Gözde Gül Şahin. 2022. To Augment or Not to Augment? A Comparative Study on Text Augmentation Techniques for Low-Resource NLP. <i>Computational Linguistics</i>, 48(1):5–42."
    )


def test_format_inproceedings_two_authors():
    output = cf.render("bollmann-sogaard-2021-error")
    assert (
        output
        == "Marcel Bollmann and Anders Søgaard. 2021. Error Analysis and the Role of Morphology. In <i>Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume</i>, pages 1887–1900, Online. Association for Computational Linguistics."
    )
