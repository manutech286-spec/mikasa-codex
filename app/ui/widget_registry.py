"""Runtime widget registry for module injection."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from PySide6.QtWidgets import QWidget


WidgetFactory = Callable[[], QWidget]


class WidgetRegistry:
    """Stores widget factories by zone name."""

    def __init__(self) -> None:
        self._factories: dict[str, list[WidgetFactory]] = defaultdict(list)

    def register(self, zone: str, factory: WidgetFactory) -> None:
        """Register a widget factory for a UI zone."""
        self._factories[zone].append(factory)

    def build_for_zone(self, zone: str) -> list[QWidget]:
        """Instantiate widgets for given zone."""
        return [factory() for factory in self._factories.get(zone, [])]
