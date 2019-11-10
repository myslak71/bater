"""validators for bater.App attributes."""
import attr


def is_percentage(instance: attr.s, attribute: attr.Attribute, value) -> None:
    """TODO"""
    if not 0 <= value <= 100:
        raise ValueError(f"{attribute.name} must be a value between 0 and 100")


def is_positive(instance: attr.s, attribute: attr.Attribute, value) -> None:
    """TODO"""
    if value <= 0:
        raise ValueError(f"{attribute.name} must be a positive number")
