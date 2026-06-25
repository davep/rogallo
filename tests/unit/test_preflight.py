"""Unit tests for the Preflight module."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Pytest imports.
from pytest import mark, raises

##############################################################################
# Local imports.
from rogallo.preflight import is_likely_capsule, is_likely_page_relative, path_from_uri


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


##############################################################################
@mark.parametrize(
    "uri, result",
    [
        ("file:///tmp/test.gmi", Path("/tmp/test.gmi").resolve()),
        ("/tmp/test.gmi", Path("/tmp/test.gmi").resolve()),
    ],
)
def test_path_from_uri_file(uri: str, result: Path) -> None:
    """Test the path_from_uri function with a file URI."""
    assert path_from_uri(uri) == result


##############################################################################
@mark.parametrize(
    "uri",
    [
        ("http://example.com"),
        ("gemini://example.com"),
        ("ftp://example.com"),
        ("//example.com"),
    ],
)
def test_path_from_uri_invalid(uri: str) -> None:
    """Test the path_from_uri function with an invalid URI."""
    with raises(ValueError):
        _ = path_from_uri(uri)


### test_preflight.py ends here
