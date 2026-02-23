"""Theme helpers."""

from __future__ import annotations

DARK_STYLESHEET = """
QWidget { background: #0f172a; color: #dbeafe; font-size: 13px; }
QFrame#Panel { border: 1px solid #334155; border-radius: 6px; }
QProgressBar { border: 1px solid #334155; border-radius: 4px; text-align: center; }
QProgressBar::chunk { background-color: #38bdf8; }
QLineEdit, QTextEdit, QListWidget { background: #111827; border: 1px solid #334155; }
QPushButton { background: #1d4ed8; border-radius: 4px; padding: 5px 8px; }
"""
