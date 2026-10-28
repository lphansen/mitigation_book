"""Author year citations with round brackets, as the paper prints them.

sphinxcontrib.bibtex's ``author_year`` style uses square brackets, so
``{cite:t}`MiaoWang:2007``` would read "Miao and Wang [2007]". This extension
registers ``author_year_round``, the same style with round brackets and a
plain "et al." for three or more authors, giving "Miao and Wang (2007)" and
"Anderson et al. (2003)". Select it with ``bibtex_reference_style``.
"""

import dataclasses

from docutils import nodes
from sphinxcontrib.bibtex.plugin import register_plugin
from sphinxcontrib.bibtex.style.referencing import BracketStyle, PersonStyle
from sphinxcontrib.bibtex.style.referencing.author_year import AuthorYearReferenceStyle
from sphinxcontrib.bibtex.style.referencing.basic_author_year import (
    BasicAuthorYearTextualReferenceStyle)
from sphinxcontrib.bibtex.style.template import join, reference, year


def previous_sibling(self):
    """Return the node before this one in its parent, or None for a first child.

    docutils 0.18 computes ``parent[index - 1]``, which for a first child is
    ``parent[-1]``, the last sibling. For a bibliography that is a citation, so
    the HTML writer skips the opening ``<div class="citation-list">`` but still
    writes its closing tag, and the stray ``</div>`` pushes the page footer out
    of the article column. This is the behavior of later docutils releases.
    """
    parent = self.parent
    if parent is None:
        return None
    index = parent.index(self)
    return parent[index - 1] if index > 0 else None


nodes.Node.previous_sibling = previous_sibling


def round_brackets():
    """Return a bracket style that wraps citations in parentheses."""
    return BracketStyle(left="(", right=")")


def paper_persons():
    """Return a person style that abbreviates three or more authors as "et al."."""
    return PersonStyle(other=" et al.")


@dataclasses.dataclass
class LinkedTextualReferenceStyle(BasicAuthorYearTextualReferenceStyle):
    """Textual author year reference whose link covers the authors and the year.

    The base style links only the year, so "Anderson et al. (2003)" would be
    clickable on "2003" alone.
    """

    def inner(self, role_name):
        """Return the template of one textual reference, all of it inside the link."""
        return reference[
            join(sep=self.text_reference_sep)[
                self.person.author_or_editor_or_title(full="s" in role_name),
                join[self.bracket.left, year, self.bracket.right],
            ]
        ]


@dataclasses.dataclass
class RoundAuthorYearReferenceStyle(AuthorYearReferenceStyle):
    """Author year referencing style with round brackets."""

    bracket_parenthetical: BracketStyle = dataclasses.field(default_factory=round_brackets)
    bracket_textual: BracketStyle = dataclasses.field(default_factory=round_brackets)
    bracket_author: BracketStyle = dataclasses.field(default_factory=round_brackets)
    bracket_label: BracketStyle = dataclasses.field(default_factory=round_brackets)
    bracket_year: BracketStyle = dataclasses.field(default_factory=round_brackets)
    person: PersonStyle = dataclasses.field(default_factory=paper_persons)

    def __post_init__(self):
        """Build the sub styles, then swap in the fully linked textual style."""
        super().__post_init__()
        self.styles = [
            LinkedTextualReferenceStyle(bracket=s.bracket, person=s.person,
                                        text_reference_sep=s.text_reference_sep)
            if type(s) is BasicAuthorYearTextualReferenceStyle else s
            for s in self.styles
        ]
        self.role_style.update(
            (role_name, style) for style in self.styles for role_name in style.role_names())


def setup(app):
    """Register the style with pybtex when Sphinx loads the extension.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        The Sphinx application.

    Returns
    -------
    dict
        Extension metadata.
    """
    register_plugin("sphinxcontrib.bibtex.style.referencing", "author_year_round",
                    RoundAuthorYearReferenceStyle)
    return {"parallel_read_safe": True}
