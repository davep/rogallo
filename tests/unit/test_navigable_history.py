"""Unit tests for the navigable history class."""

##############################################################################
# Local imports.
from rogallo.history import NavigableHistory


##############################################################################
def test_empty_history() -> None:
    """Test that an empty history has no current item."""
    history = NavigableHistory[None]()
    assert history.current_item is None
    assert history.current_location is None
    assert history.can_go_backward is False


##############################################################################
def test_initialise_with_list() -> None:
    """Test that a history initialised with a list has the last item as current."""
    items = [1, 2, 3]
    history = NavigableHistory[int](items)
    assert history.current_item == 3
    assert history.current_location == 2
    assert history.can_go_backward is True


##############################################################################
def test_initialise_with_tuple() -> None:
    """Test that a history initialised with a tuple has the last item as current."""
    items = (1, 2, 3)
    history = NavigableHistory[int](items)
    assert history.current_item == 3
    assert history.current_location == 2
    assert history.can_go_backward is True


##############################################################################
def test_truncates_on_max_length() -> None:
    """Test that a history truncates when the max length is exceeded."""
    items = [1, 2, 3, 4, 5]
    history = NavigableHistory[int](items, max_length=5)
    history.add(6)
    assert len(history) == 5
    assert list(history) == [2, 3, 4, 5, 6]
    assert history.current_item == 6


##############################################################################
def test_truncates_on_init() -> None:
    """Test that a history truncates when initialised with a list longer than max length."""
    items = [1, 2, 3, 4, 5, 6]
    history = NavigableHistory[int](items, max_length=5)
    assert len(history) == 5
    assert list(history) == [2, 3, 4, 5, 6]
    assert history.current_item == 6


##############################################################################
def test_add_to_empty() -> None:
    """Test that adding an item to an empty history sets it as the current item."""
    history = NavigableHistory[int]()
    assert history.current_item is None
    assert history.current_location is None
    assert history.can_go_backward is False
    assert history.can_go_forward is False
    history.add(1)
    assert history.current_item == 1
    assert history.current_location == 0
    assert history.can_go_backward is False
    assert history.can_go_forward is False


##############################################################################
def test_add_to_non_empty() -> None:
    """Test that adding an item to a non-empty history sets it as the current item."""
    history = NavigableHistory[int]([1, 2, 3])
    assert history.current_item == 3
    assert history.current_location == 2
    assert history.can_go_backward is True
    assert history.can_go_forward is False
    history.add(4)
    assert history.current_item == 4
    assert history.current_location == 3
    assert history.can_go_backward is True
    assert history.can_go_forward is False


##############################################################################
def test_add_removes_forward_history() -> None:
    """Test that adding an item removes forward history."""
    history = NavigableHistory[int]([1, 2, 3])
    assert history.backward() is True
    history.add(4)
    assert history.current_item == 4
    assert history.current_location == 2
    assert history.can_go_backward is True
    assert history.can_go_forward is False
    assert list(history) == [1, 2, 4]


##############################################################################
def test_backward() -> None:
    """Test that going backward works."""
    history = NavigableHistory[int]([1, 2, 3])
    assert history.backward() is True
    assert history.current_item == 2
    assert history.current_location == 1
    assert history.can_go_backward is True
    assert history.can_go_forward is True
    assert history.backward() is True
    assert history.current_item == 1
    assert history.current_location == 0
    assert history.can_go_backward is False
    assert history.can_go_forward is True
    assert history.backward() is False


##############################################################################
def test_forward() -> None:
    """Test that going forward works."""
    history = NavigableHistory[int]([1, 2, 3])
    history.goto(0)
    assert history.forward() is True
    assert history.current_item == 2
    assert history.current_location == 1
    assert history.can_go_backward is True
    assert history.can_go_forward is True
    assert history.forward() is True
    assert history.current_item == 3
    assert history.current_location == 2
    assert history.can_go_backward is True
    assert history.can_go_forward is False
    assert history.forward() is False


### test_navigable_history.py ends here
