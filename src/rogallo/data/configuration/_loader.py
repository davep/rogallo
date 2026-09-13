"""Provides a utility function for loading configuration data."""

##############################################################################
# PyYAML imports.
from yaml import YAMLError, safe_dump, safe_load

##############################################################################
# Local imports.
from ..locations import config_dir


##############################################################################
def load_configuration[T](name: str, default: T) -> T:
    """Load the configuration data from the given file.

    Args:
        name: The name of the configuration file.
        default: The default configuration data.

    Returns:
        The loaded configuration data.
    """
    if not (
        config_file := (config_dir() / name).with_suffix(".yaml")
    ).exists() and bool(default):
        config_file.write_text(safe_dump(default), encoding="utf-8")
    try:
        return safe_load(config_file.read_text(encoding="utf-8")) or default
    except (OSError, YAMLError):
        return default


### _loader.py ends here
