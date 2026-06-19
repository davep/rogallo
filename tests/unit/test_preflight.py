"""Unit tests for the Preflight module."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from rogallo.app.preflight import is_likely_capsule


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
