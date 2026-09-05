"""Provides code that resolves a request to open a string URI."""

##############################################################################
# Port70 imports.
from port70 import GopherURI
from port70 import URIError as GopherURIError

##############################################################################
# Port79 imports.
from port79 import FingerURI
from port79 import URIError as FingerURIError

##############################################################################
# Port1900 imports.
from port1900 import NexURI
from port1900 import URIError as NexURIError

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI
from sybaritic import URIError as SpartanURIError

##############################################################################
# Wasat imports
from wasat import GeminiURI, TitanURI
from wasat import URIError as GeminiURIError

##############################################################################
# Local imports.
from ...messages import OpenFromFileSystem, OpenLocation, OpenURI
from ...preflight import (
    is_likely_schemeless_capsule,
    is_local_directory,
    is_local_text_file,
    local_index_from_uri,
    path_from_uri,
)
from .local_messages import OpenUnsupportedURI


##############################################################################
def uri_resolver(
    request: OpenURI,
) -> OpenFromFileSystem | OpenLocation | OpenUnsupportedURI:
    """Turn a URI request into a location.

    Args:
        uri: The URI request to turn into a location.

    Returns:
        A message for opening the location.
    """

    # Work through the supported URI types.
    for uri_type, uri_error in (
        (GeminiURI, GeminiURIError),
        (TitanURI, GeminiURIError),
        (FingerURI, FingerURIError),
        (GopherURI, GopherURIError),
        (SpartanURI, SpartanURIError),
        (NexURI, NexURIError),
    ):
        try:
            return OpenLocation(
                uri_type(request.uri), allow_cached=request.allow_cached
            )
        except uri_error:
            pass

    # Perhaps it's a local text file?
    if is_local_text_file(request.uri):
        return OpenLocation(path_from_uri(request.uri))

    # Before we give up on the filesystem, let's see if it's a
    # directory.
    if is_local_directory(request.uri):
        return (
            # Open as a file...
            OpenLocation(candidate)
            # ...if we could find a a candidate index file in the directory...
            if (candidate := local_index_from_uri(request.uri)).is_file()
            # ...otherwise kick off the file picker to let the user choose a file.
            else OpenFromFileSystem(candidate)
        )

    # It's not an obvious supported-protocol URI, and it's not a file in the
    # local filesystem. Before we pass it off to the system browser, let's
    # see it could look like a Gemini URI if we add the scheme. Note that
    # this means that we give priority to `gemini://` over any other
    # protocol when it comes to the user entering `example.com` alone.
    if is_likely_schemeless_capsule(request.uri):
        return OpenLocation(
            GeminiURI.with_default_scheme(request.uri),
            allow_cached=request.allow_cached,
        )

    # Otherwise, try to open it in the system browser.
    return OpenUnsupportedURI(request.uri)


### uri_resolver.py ends here
