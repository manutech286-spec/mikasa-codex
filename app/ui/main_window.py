"""Game-style HUD main window."""

from __future__ import annotations

from PySide6.QtCore import QEasingCurve, Property, QPropertyAnimation
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.ui.presenters.chat_presenter import ChatPresenter


class MainWindow(QMainWindow):
    """HUD window shell with non-blocking chat interactions."""

    def __init__(self, chat_presenter: ChatPresenter) -> None:
        super().__init__()
        self._chat_presenter = chat_presenter
        self.setWindowTitle("MIKASA CODEX Lab")
        self.resize(1200, 760)
        self._pulse = 0.0
        self._build_ui()
        self._chat_presenter.reply_ready.connect(self._on_reply)

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)

        bars = QHBoxLayout()
        self.energy = self._make_bar("Energy", 80)
        self.focus = self._make_bar("Focus", 90)
        self.sync = self._make_bar("Sync", 65)
        bars.addWidget(self.energy)
        bars.addWidget(self.focus)
        bars.addWidget(self.sync)
        layout.addLayout(bars)

        body = QHBoxLayout()
        body.addWidget(self._left_panel())
        body.addWidget(self._center_panel(), 2)
        body.addWidget(self._right_panel())
        layout.addLayout(body)

        layout.addWidget(QLabel("XP 1240/2000 | Level 7 | Evolution: Sentinel"))
        self.setCentralWidget(root)

    def _left_panel(self) -> QWidget:
        panel = QFrame(objectName="Panel")
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("Avatar: [placeholder anim]"))
        self.mood_label = QLabel("Mood: Calm")
        layout.addWidget(self.mood_label)
        return panel

    def _center_panel(self) -> QWidget:
        panel = QFrame(objectName="Panel")
        layout = QVBoxLayout(panel)
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type command...")
        send = QPushButton("Send")
        send.clicked.connect(self._send_chat)
        layout.addWidget(QLabel("Chat Console"))
        layout.addWidget(self.chat_log)
        layout.addWidget(self.chat_input)
        layout.addWidget(send)
        return panel

    def _right_panel(self) -> QWidget:
        panel = QFrame(objectName="Panel")
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("Quests"))
        quests = QListWidget()
        quests.addItems(["Review daily notes", "Create search shortcut"])
        layout.addWidget(quests)
        return panel

    def _send_chat(self) -> None:
        message = self.chat_input.text().strip()
        if not message:
            return
        self.chat_log.append(f"You: {message}")
        self.chat_input.clear()
        self._chat_presenter.send_message(message)

    def _on_reply(self, text: str) -> None:
        self.chat_log.append(text)
        self._animate_mood()

    def _animate_mood(self) -> None:
        anim = QPropertyAnimation(self, b"pulse")
        anim.setDuration(350)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.valueChanged.connect(lambda _: self.mood_label.setText("Mood: Focused"))
        anim.start()
        self._anim_ref = anim

    def _make_bar(self, label: str, value: int) -> QWidget:
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.addWidget(QLabel(label))
        bar = QProgressBar()
        bar.setValue(value)
        layout.addWidget(bar)
        return wrapper

    def get_pulse(self) -> float:
        """Expose animation property for Qt."""
        return self._pulse

    def set_pulse(self, value: float) -> None:
        """Update animation property for Qt."""
        self._pulse = value

    pulse = Property(float, get_pulse, set_pulse)
