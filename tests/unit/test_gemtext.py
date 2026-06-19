"""Unit tests for the Gemtext module."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from rogallo.gemtext import (
    Gemtext,
    Heading,
    Link,
    ListItem,
    Paragraph,
    PreFormatted,
    Quote,
)


##############################################################################
def test_parse_empty_text() -> None:
    """Test parsing an empty Gemtext string."""
    assert Gemtext("").content == ()


##############################################################################
def test_str_gemtext() -> None:
    """Test the string representation of a Gemtext object."""
    text = "This is a paragraph.\n# Header 1\n* List item\n> Quote\n=> https://example.com Link\n"
    assert str(Gemtext(text)) == text


##############################################################################
@mark.parametrize(
    "gemtext, expected_text",
    [
        ("This is a paragraph.", "This is a paragraph."),
        ("This is a paragraph.\nSecond line.", "This is a paragraph."),
        ("\nSecond line.", ""),
        (" \nSecond line.", " "),
        (" > Not a quote", " > Not a quote"),
        (">Not a quote", ">Not a quote"),
        (">> Not a quote", ">> Not a quote"),
        (" # Not a header", " # Not a header"),
        ("#Not a header", "#Not a header"),
        ("##Not a header", "##Not a header"),
        ("###Not a header", "###Not a header"),
        ("#### Header 4", "#### Header 4"),
        ("*Not a list item", "*Not a list item"),
        ("** Not a list item", "** Not a list item"),
        (" * Not a list item", " * Not a list item"),
        ("=>https://example.com Not a link", "=>https://example.com Not a link"),
        ("`", "`"),
        ("``", "``"),
    ],
)
def test_parse_paragraph(gemtext: str, expected_text: str) -> None:
    """Test parsing a paragraph."""
    paragraph = Gemtext(gemtext).content[0]
    assert isinstance(paragraph, Paragraph)
    assert str(paragraph) == expected_text


##############################################################################
@mark.parametrize(
    "gemtext, expected_level, expected_content",
    [
        ("# Header 1", 1, "Header 1"),
        ("## Header 2", 2, "Header 2"),
        ("### Header 3", 3, "Header 3"),
        ("#  Header 1", 1, "Header 1"),
        ("##  Header 2", 2, "Header 2"),
        ("###  Header 3", 3, "Header 3"),
        ("# # Header 1", 1, "# Header 1"),
        ("## ## Header 2", 2, "## Header 2"),
        ("### ### Header 3", 3, "### Header 3"),
    ],
)
def test_parse_header(gemtext: str, expected_level: int, expected_content: str) -> None:
    """Test parsing headers."""
    header = Gemtext(gemtext).content[0]
    assert isinstance(header, Heading)
    assert header.level == expected_level
    assert str(header) == expected_content


##############################################################################
@mark.parametrize(
    "gemtext, expected_quote",
    [
        ("> This is a quote.", "This is a quote."),
        (">  This is a quote.", "This is a quote."),
        ("> > This is a quote.", "> This is a quote."),
        ("> This is a quote.\n> Second line.", "This is a quote."),
        ("> \nSecond line.", ""),
        (">  This is a quote", "This is a quote"),
    ],
)
def test_parse_quote(gemtext: str, expected_quote: str) -> None:
    """Test parsing a quote."""
    quote = Gemtext(gemtext).content[0]
    assert isinstance(quote, Quote)
    assert str(quote) == expected_quote


##############################################################################
@mark.parametrize(
    "gemtext, expected_item",
    [
        ("* This is a list item.", "This is a list item."),
        ("*  This is a list item.", "This is a list item."),
        ("* * This is a list item.", "* This is a list item."),
        ("* This is a list item.\n* Second item.", "This is a list item."),
        ("* \nSecond item.", ""),
        ("*  This is a list item", "This is a list item"),
    ],
)
def test_parse_list_item(gemtext: str, expected_item: str) -> None:
    """Test parsing a list item."""
    list_item = Gemtext(gemtext).content[0]
    assert isinstance(list_item, ListItem)
    assert str(list_item) == expected_item


##############################################################################
@mark.parametrize(
    "gemtext, expected_uri, expected_description",
    [
        ("=> https://example.com Example", "https://example.com", "Example"),
        ("=> https://example.com  Example", "https://example.com", "Example"),
        ("=> https://example.com  Example ", "https://example.com", "Example"),
        ("=> https://example.com  Example link", "https://example.com", "Example link"),
        (
            "=> https://example.com  Example  link",
            "https://example.com",
            "Example  link",
        ),
        ("=> https://example.com", "https://example.com", "https://example.com"),
        ("=>  https://example.com Example", "https://example.com", "Example"),
        ("=>  https://example.com  Example", "https://example.com", "Example"),
        ("=> https://example.com\tExample", "https://example.com", "Example"),
    ],
)
def test_parse_link(gemtext: str, expected_uri: str, expected_description: str) -> None:
    """Test parsing a link."""
    link = Gemtext(gemtext).content[0]
    assert isinstance(link, Link)
    assert link.uri == expected_uri
    assert str(link) == expected_description


##############################################################################
@mark.parametrize(
    "start_marker, end_marker",
    [
        ("```", "```"),
        ("``` ", "```"),
        ("````", "````"),
        ("```", "````"),
        ("```text", "```"),
    ],
)
@mark.parametrize(
    "pre_text, expected_text",
    [
        ("Paragraph", "Paragraph"),
        ("# Heading", "# Heading"),
        ("## Heading", "## Heading"),
        ("### Heading", "### Heading"),
        ("* List item", "* List item"),
        ("> Quote", "> Quote"),
        ("=> https://example.com Link", "=> https://example.com Link"),
        ("", ""),
        (" ", " "),
        (" ```", " ```"),
    ],
)
def test_parse_preformatted(
    start_marker: str, end_marker: str, pre_text: str, expected_text: str
) -> None:
    """Test parsing preformatted text."""
    preformatted = Gemtext(f"{start_marker}\n{pre_text}\n{end_marker}").content[0]
    assert isinstance(preformatted, PreFormatted)
    assert str(preformatted) == expected_text


### test_gemtext.py ends here
