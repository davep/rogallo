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

    async def close(self) -> None:
        """Close all clients."""
        await self.gemini.close()

    @classmethod
    def create(cls) -> Self:
        """Create a new instance of the clients class.

        Returns:
            A new instance of the clients class.
        """
        config = load_configuration()
        return cls(
            finger=FingerClient(timeout=config.connection_timeout),
            gemini=GeminiClient(
                client_cert_store_path=client_certificates_directory(),
                connect_timeout=config.connection_timeout,
                max_redirects=config.maximum_redirects,
                read_timeout=config.read_timeout,
                trust_store_path=trust_file(),
                verify_mode=config.capsule_certificate_verify_mode,
            ),
            gopher=GopherClient(timeout=config.connection_timeout),
            nex=NexClient(timeout=config.connection_timeout),
            spartan=SpartanClient(timeout=config.connection_timeout),
        )


### clients.py ends here
