from PyQt6.QtWidgets import QMessageBox

def show_confirm(self, title: str, detail_text: str, text: str) -> bool:
    msg = QMessageBox(self)
    msg.setIcon(QMessageBox.Icon.Question)
    msg.setWindowTitle(title)

    msg.setText("Opravdu pokračovat?")
    msg.setInformativeText(text)
    msg.setDetailedText(detail_text)

    msg.setStandardButtons(
        QMessageBox.StandardButton.Ok |
        QMessageBox.StandardButton.Cancel
    )
    msg.setDefaultButton(QMessageBox.StandardButton.Cancel)

    result = msg.exec()

    return result == QMessageBox.StandardButton.Ok

def show_info(self, message: str, title: str = "Informace") -> bool:
    msg = QMessageBox(self)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)

    result = msg.exec()
    return result == QMessageBox.StandardButton.Ok
