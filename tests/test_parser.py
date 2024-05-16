from yabibf import BibTeX


def test_duplicates():
    bib = BibTeX(["tests/example.bib", "tests/example_duplicate.bib"])
    assert len(bib.entries) == 5
    assert len(bib.library.failed_blocks) == 1
    # assert bib.library.failed_blocks[0].ignore_error_block == "foo"
