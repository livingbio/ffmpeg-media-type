from dataclasses import fields, is_dataclass
from typing import Any, TypeVar, get_args, get_origin

T = TypeVar("T")


def from_dict(data_class: type[T], data: dict[str, Any]) -> T:
    """
    Convert a dictionary to a dataclass object.

    Args:
        data_class: The dataclass type.
        data: The dictionary to convert.

    Returns:
        The dataclass object.
    """

    if isinstance(data, dict):
        assert is_dataclass(data_class)
        fieldtypes = {f.name: f.type for f in fields(data_class)}
        return data_class(**{f: from_dict(fieldtypes[f], data[f]) for f in data if f in fieldtypes})  # type: ignore[return-value]
    elif get_origin(data_class) == tuple:
        # Handling tuple types by converting each element in the tuple
        # assuming all elements are of the type specified in the first argument of the tuple type
        element_type = get_args(data_class)[0]
        return tuple(from_dict(element_type, item) for item in data)
    else:
        return data
