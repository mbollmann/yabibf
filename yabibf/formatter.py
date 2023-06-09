from citeproc_styles import get_style_filepath


class CiteprocFormatter():

    def __init__(self, style):
        """
        A class for formatting bibliographies with citeproc-py.

        Parameters:
            style: The name of a CSL Style.  Corresponds to the name of a .csl file in the
                   citation-style-language/styles repository:
                   <https://github.com/citation-style-language/styles>
        """
        self.style_path = get_style_filepath(style)
