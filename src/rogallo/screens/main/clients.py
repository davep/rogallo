"""Provides a class for holding all supported clients."""

##############################################################################
# Python imports.
from typing import NamedTuple, Self

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
# Local imports.
from ...data import client_certificates_directory, load_configuration, trust_file


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

    @classmethod
    def create(cls) -> Self:
        """Create a new instance of the clients class.

        Returns:
            A new instance of the clients class.
        """
        return cls(
            gemini=GeminiClient(
                verify_mode=load_configuration().capsule_certificate_verify_mode,
                trust_store_path=trust_file(),
                client_cert_store_path=client_certificates_directory(),
                connect_timeout=load_configuration().connection_timeout,
                read_timeout=load_configuration().read_timeout,
                max_redirects=load_configuration().maximum_redirects,
            ),
            finger=FingerClient(
                timeout=load_configuration().connection_timeout,
            ),
            gopher=GopherClient(
                timeout=load_configuration().connection_timeout,
            ),
            spartan=SpartanClient(
                timeout=load_configuration().connection_timeout,
            ),
            nex=NexClient(
                timeout=load_configuration().connection_timeout,
            ),
        )


### clients.py ends here
