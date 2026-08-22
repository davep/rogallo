"""Provides a function for decoding text from a response."""

##############################################################################
# Sybaritic imports.
from sybaritic import Response as SpartanResponse
from sybaritic import ResponseError as SpartanResponseError

##############################################################################
# Wasat imports.
from wasat import ProtocolError as GeminiProtocolError
from wasat import Response as GeminiResponse


##############################################################################
async def decode_text(response: GeminiResponse | SpartanResponse) -> str:
    """Decode the text from a response.

    Args:
        response: The response to decode.

    Returns:
        The decoded text.
    """
    try:
        # Give the library a chance to decode the text using the charset
        # specified in the response headers.
        return await response.text()
    except (GeminiProtocolError, SpartanResponseError):
        # If the library fails to decode the text, fall back to latin-1.
        return await response.text(encoding="latin-1")


### text_decoder.py ends here
