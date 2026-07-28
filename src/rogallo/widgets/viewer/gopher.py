"""Provides code to turn Gophermap into Gemtext."""

##############################################################################
# Python imports.
from collections.abc import Iterator

##############################################################################
# Gophermap imports.
from gophermap import GopherMap, ItemType

##############################################################################
# Port79 imports.
from port70 import GopherURI, URIError

##############################################################################
# Local imports.
from ...data import load_configuration


##############################################################################
def to_gemtext(gophermap: str) -> Iterator[str]:
    """Convert a Gophermap into Gemtext.

    Args:
        gophermap: The Gophermap to convert.

    Yields:
        The Gemtext representation of the Gophermap.
    """
    badges = (
        load_configuration().gopher_type_badges
        if load_configuration().gopher_show_type_badges
        else {}
    )
    for item in GopherMap(gophermap).items:
        if badge := badges.get(item.type, ""):
            badge += " "
        match item.type:
            case ItemType.HTML:
                yield f"=> {item.selector.removeprefix('URL:')} {badge}{item.display_text}"
            case ItemType.ERROR:
                yield f"# {item.display_text}"
            case ItemType.INFO:
                yield item.display_text
            case _:
                try:
                    yield (
                        f"=> {GopherURI.with_default_scheme(f'{item.host}:{item.port}/{item.type}{item.selector}')}"
                        f" {badge}{item.display_text}"
                    )
                except URIError:
                    yield f"```\n{item.raw}\n```"


### gopher.py ends here
