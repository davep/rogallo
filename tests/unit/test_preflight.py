"""Unit tests for the Preflight module."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from rogallo.preflight import is_likely_capsule, is_likely_page_relative


##############################################################################
@mark.parametrize(
    "uri, result",
    [
        ("/", True),
        ("relative/path", True),
        ("http://example.com", False),
        ("gemini://example.com", False),
        ("ftp://example.com", False),
        ("", True),
        ("   ", True),
    ],
)
def test_is_likely_page_relative(uri: str, result: bool) -> None:
    """Test the is_likely_page_relative function."""
    assert is_likely_page_relative(uri) is result


##############################################################################
@mark.parametrize(
    "uri, result",
    [
        ("gemini://example.com", True),
        ("gemini://example.com/path", True),
        ("http://example.com", False),
        ("/", True),
        ("relative/path", True),
        ("ftp://example.com", False),
        ("not a uri", True),
        ("", True),
        ("   ", True),
    ],
)
def test_is_likely_capsule(uri: str, result: bool) -> None:
    """Test the is_likely_capsule function."""
    assert is_likely_capsule(uri) is result


### test_preflight.py ends here
