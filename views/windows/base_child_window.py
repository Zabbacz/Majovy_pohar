from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from config import Config


class BaseChildWindow(QWidget):
    closed = pyqtSignal(str)


    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        self._key = key
        self.config = config

    def closeEvent(self, event):
        self.closed.emit(self._key)
        super().closeEvent(event)
