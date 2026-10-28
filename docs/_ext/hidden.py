"""A ``hidden`` directive whose content is kept in the source but left out of the site.

Used for the reproduction sections at the end of the chapter pages until the
replication package is public. The content is not parsed, so cross references
inside it do not need their targets to be built.

Usage in a page::

    ::::{hidden}
    ## Reproducing the figures
    ...
    ::::
"""
from docutils.parsers.rst import Directive


class Hidden(Directive):
    """Swallow the directive body and emit nothing."""
    has_content = True

    def run(self):
        return []


def setup(app):
    app.add_directive("hidden", Hidden)
    return {"version": "1", "parallel_read_safe": True, "parallel_write_safe": True}
