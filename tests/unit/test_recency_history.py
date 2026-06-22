"""Unit tests for the recency history class."""

##############################################################################
# Local imports.
from rogallo.history import RecencyHistory


##############################################################################
def test_empty_history() -> None:
    """Test that an empty history has no current item."""
    assert len(RecencyHistory[None]()) == 0


##############################################################################
def test_initialise_with_list() -> None:
    """Test that a history initialised with a list has the last item as current."""
    history = RecencyHistory[int]([1, 2, 3])
    assert len(history) == 3
    assert list(history) == [1, 2, 3]


##############################################################################
def test_initialise_with_tuple() -> None:
    """Test that a history initialised with a tuple has the last item as current."""
    history = RecencyHistory[int]((1, 2, 3))
    assert len(history) == 3
    assert list(history) == [1, 2, 3]


##############################################################################
def test_truncates_on_max_length() -> None:
    """Test that a history truncates when the max length is exceeded."""
    history = RecencyHistory[int]([1, 2, 3, 4, 5], max_length=5)
    history.add(6)
    assert len(history) == 5
    assert list(history) == [2, 3, 4, 5, 6]


##############################################################################
def test_truncates_on_init() -> None:
    """Test that a history truncates when initialised with a list longer than max length."""
    history = RecencyHistory[int]([1, 2, 3, 4, 5, 6], max_length=5)
    assert len(history) == 5
    assert list(history) == [2, 3, 4, 5, 6]


##############################################################################
def test_add_to_empty() -> None:
    """Test that adding an item to an empty history sets it as the current item."""
    history = RecencyHistory[int]()
    history.add(1)
    assert len(history) == 1
    assert list(history) == [1]


##############################################################################
def test_add_to_non_empty() -> None:
    """Test that adding an item to a non-empty history adds it to the end."""
    history = RecencyHistory[int]([1, 2, 3])
    history.add(4)
    assert len(history) == 4
    assert list(history) == [1, 2, 3, 4]


##############################################################################
def test_add_duplicate_item() -> None:
    """Test that adding a duplicate item moves it to the end of the history."""
    history = RecencyHistory[int]([1, 2, 3])
    history.add(2)
    assert len(history) == 3
    assert list(history) == [1, 3, 2]


### test_recency_history.py ends here
