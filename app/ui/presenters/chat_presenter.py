"""Presenter for chat interactions."""

from __future__ import annotations

from PySide6.QtCore import QObject, QThread, Signal

from app.engine.engine import MikasaEngine


class _ChatWorker(QObject):
    """Background worker for non-blocking chat calls."""

    finished = Signal(str)

    def __init__(self, engine: MikasaEngine, message: str) -> None:
        super().__init__()
        self._engine = engine
        self._message = message

    def run(self) -> None:
        """Run engine call off the UI thread."""
        reply = self._engine.handle_chat(self._message)
        self.finished.emit(reply)


class ChatPresenter(QObject):
    """UI-facing presenter for chat workflow."""

    reply_ready = Signal(str)

    def __init__(self, engine: MikasaEngine) -> None:
        super().__init__()
        self._engine = engine
        self._threads: list[QThread] = []

    def send_message(self, message: str) -> None:
        """Submit a message to engine using worker thread."""
        thread = QThread()
        worker = _ChatWorker(self._engine, message)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self.reply_ready.emit)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(lambda: self._threads.remove(thread))
        self._threads.append(thread)
        thread.start()
