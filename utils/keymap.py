from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtCore import Qt


class EnterTableWidget(QTableWidget):

    def keyPressEvent(self, event):

        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.focusNextPrevChild(True)
            return

        super().keyPressEvent(event)
