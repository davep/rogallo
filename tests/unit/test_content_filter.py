"""Unit tests for the content filter."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
#
# Without screens being imported I have a circular import. I need to fix
# this generally.
from rogallo import screens  # noqa: F401
from rogallo.widgets.viewer.gemtext.content_filter import GemtextContent


##############################################################################
@mark.parametrize(
    "source, result",
    [
        ("", ""),
        (" ", " "),
        ("💩 ", ""),
        ("💩", ""),
        ("💩💩💩💩💩", ""),
        ("💩 💩 💩 💩 💩 ", ""),
        ("Hello, world! 🌍", "Hello, world! "),
        ("No emoji here.", "No emoji here."),
        ("Multiple emojis 😄😎👍", "Multiple emojis "),
        ("Emoji with space 😄 ", "Emoji with space "),
        ("😄 Hello", "Hello"),
        ("✏️ Hello", "Hello"),
        ("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Hello", "Hello"),
        ("🧑🏻‍🤝‍🧑🏿 Hello", "Hello"),
    ],
)
def test_strip_emoji(source: str, result: str) -> None:
    """Test the _strip_emoji method of GemtextContent."""
    assert GemtextContent._strip_emoji(source) == result


### test_content_filter.py ends here
