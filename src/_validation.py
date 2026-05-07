"""Shared input validation helpers."""

from __future__ import annotations

from numbers import Integral


def validate_positive_integer(value: int, name: str) -> None:
    """Raise ValueError when value is not a positive integer."""
    if isinstance(value, bool) or not isinstance(value, Integral) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
