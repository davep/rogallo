"""Provides utility code for stripping emojis from text."""

##############################################################################
# Python imports.
from functools import cache
from unicodedata import category


##############################################################################
@cache
def _is_likely_emoji(character: str) -> bool:
    """Determine if a character is likely to be an emoji.

    Args:
        character: The character to check.

    Returns:
        True if the character is likely to be an emoji, False otherwise.
    """
    codepoint = ord(character)
    # Exclude Braille and CJK blocks
    if 0x2800 <= codepoint <= 0x28FF or 0x2E80 <= codepoint <= 0x9FFF:
        return False
    # Check if the character falls within known emoji ranges
    return (
        codepoint in (0x231A, 0x231B)  # Watch, Hourglass
        or 0x23E9 <= codepoint <= 0x23FA  # Media controls & Clocks
        or codepoint >= 0x2600  # Symbols, Dingbats, Modern emojis
    ) and category(character) in ("So", "Sk")


##############################################################################
def strip_emoji(text: str) -> str:
    """Strip emoji from a string.

    Args:
        text: The string to strip emoji from.

    Returns:
        The string with emoji stripped.

    Note:
        Any space that immediately follows an emoji will also be
        stripped, to avoid leaving a space that was intended to separate
        the emoji from the what follows it.
    """
    retained: list[str] = []
    retain = retained.append
    skip = False
    for character in text:
        if _is_likely_emoji(character):
            skip = True
            continue
        if skip:
            if category(character) in ("Mn", "Cf", "Me"):
                continue
            skip = False
            if character == " ":
                continue
        retain(character)
    return "".join(retained)


### strip_emoji.py ends here
