"""Provides a class for holding all supported clients."""

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
# Port70 imports.
from port70 import Client as GopherClient

##############################################################################
# Port79 imports.
from port79 import Client as FingerClient

##############################################################################
# Port1900 imports.
from port1900 import Client as NexClient

##############################################################################
# Sybaritic imports.
from sybaritic import Client as SpartanClient

##############################################################################
# Wasat imports.
from wasat import Client as GeminiClient


##############################################################################
class Clients(NamedTuple):
    """A class for holding all supported clients."""

    finger: FingerClient
    """The finger client."""

    gemini: GeminiClient
    """The gemini client."""

    gopher: GopherClient
    """The gopher client."""

    nex: NexClient
    """The Nex client."""

    spartan: SpartanClient
    """The spartan client."""


### clients.py ends here
