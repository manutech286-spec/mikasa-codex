"""Desktop application entrypoint."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.bootstrap.container import build_container
from app.ui.main_window import MainWindow
from app.ui.presenters.chat_presenter import ChatPresenter
from app.ui.theme import DARK_STYLESHEET


def main() -> int:
    """Run the desktop application."""
    container = build_container()
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLESHEET)
    chat_presenter = ChatPresenter(container.engine)
    window = MainWindow(chat_presenter)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
