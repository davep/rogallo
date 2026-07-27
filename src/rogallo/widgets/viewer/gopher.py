"""Provides code to turn Gophermap into Gemtext."""

##############################################################################
# Python imports.
from collections.abc import Iterator

##############################################################################
# Gophermap imports.
from gophermap import GopherMap, ItemType

##############################################################################
# Port79 imports.
from port70 import GopherURI


##############################################################################
def to_gemtext(gophermap: str) -> Iterator[str]:
    """Convert a Gophermap into Gemtext.

    Args:
        gophermap: The Gophermap to convert.

    Yields:
        The Gemtext representation of the Gophermap.
    """
    for item in GopherMap(gophermap).items:
        match item.type:
            case ItemType.HTML:
                yield f"=> {item.selector.removeprefix('URL:')} {item.display_text}"
            case ItemType.ERROR:
                yield f"# {item.display_text}"
            case ItemType.INFO:
                yield item.display_text
            case _:
                yield (
                    f"=> {GopherURI.with_default_scheme(f'{item.host}:{item.port}/{item.type}{item.selector}')} "
                    f"{item.display_text}"
                )


### gopher.py ends here
