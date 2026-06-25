"""Provides the widget that displays the document content."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.containers import EnhancedVerticalScroll


##############################################################################
class DocumentView(EnhancedVerticalScroll):
    """The scrolling container for the document."""

    HELP = """
    ## Viewer

    As well as using the common set of cursor and page keys, the following
    keys are available for movement within the document:
    """


### document_view.py ends here
