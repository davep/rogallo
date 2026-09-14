"""Provides a utility function for loading configuration data."""

##############################################################################
# Python imports.
from dataclasses import Field, asdict, fields, is_dataclass
from typing import Any, ClassVar, Protocol

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


##############################################################################
class ConfigurationClass(Protocol):
    """Protocol that helps declare a type as being a dataclass."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


##############################################################################
def load_configuration_into[T: ConfigurationClass](
    configuration_class: type[T], name: str
) -> T:
    """Load the configuration data from the given file into a dataclass.

    Args:
        configuration_class: The class to load the configuration info.
        name: The name of the configuration file.

    Returns:
        An instance of the class populated with the loaded configuration data.
    """
    assert is_dataclass(configuration_class)
    wanted = {field.name for field in fields(configuration_class) if field.init}
    return configuration_class(
        **{
            key: value
            for key, value in load_configuration(
                name, asdict(configuration_class())
            ).items()
            if key in wanted
        }
    )


### _loader.py ends here
