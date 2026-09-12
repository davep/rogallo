"""Provides a function to initially load some data.

Most configuration data is cached, so any part of the application can call
on the load function without needing to worry about keeping its own cache.
However, it's useful for the user that, after first run, any defaults that
should be written to file get written right away, rather than on first-need.

This module provides a function to do that initial load/create.
"""

##############################################################################
# Local imports.
from .aliases import load_aliases
from .toolbar import load_toolbar


##############################################################################
def initial_load() -> None:
    """Perform an initial load of some application data."""
    load_aliases()
    load_toolbar()


### initial_load.py ends here
