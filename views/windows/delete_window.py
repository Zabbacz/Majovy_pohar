from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from config import Config
from views.windows.base_child_window import BaseChildWindow
from services.delete_service import DeleteService


class DeleteWindow(BaseChildWindow):

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.service = DeleteService()

        self.setWindowTitle("Vyprázdnění současných tabulek")
        self.resize(600, 220)

        self._init_ui()

    # -------------------------------------------------

    def _init_ui(self):
        layout = QVBoxLayout(self)

        btn_delete = QPushButton("Vyprázdnit")
        btn_delete.clicked.connect(self._delete)

        btn_cancel = QPushButton("Zrušit")
        btn_cancel.clicked.connect(self.close)

        btns = QHBoxLayout()
        btns.addWidget(btn_delete)
        btns.addWidget(btn_cancel)

        layout.addLayout(btns)

    # -------------------------------------------------
    # ACTIONS
    # -------------------------------------------------

    def _delete(self):
        try:
            deleted = self.service.truncate_tables()

            lines = [
                f"{table}: {count} záznamů"
                for table, count in deleted.items()
            ]

            QMessageBox.information(
                self,
                "Hotovo",
                "Vymazány tabulky:\n\n" + "\n".join(lines)
            )
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Chyba", str(e))
