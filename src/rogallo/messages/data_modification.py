"""Provides messages related data modification."""

##############################################################################
# Textual imports.
from textual.message import Message


##############################################################################
class BookmarksModified(Message):
    """A message indicating that the bookmarks have been modified."""


##############################################################################
class ClientCertificatesModified(Message):
    """Notify that the client certificates have changed."""


##############################################################################
class HistoryModified(Message):
    """A message sent when the history is modified."""


### data_modification.py ends here
